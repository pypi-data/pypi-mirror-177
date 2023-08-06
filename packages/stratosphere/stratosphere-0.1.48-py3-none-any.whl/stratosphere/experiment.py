import logging
import random
from pickle import PickleError
from typing import Callable, List, Union

import joblib
import pandas as pd
from sqlalchemy.orm import load_only
from stratosphere import config
from stratosphere.job import Job
from stratosphere.run import Run
from stratosphere.store import serialization
from stratosphere.store.db import schema
from stratosphere.store.db.database import Database, explode_json_column, next_ulid, pandas_query, sanitize_table_name
from stratosphere.utils import log, time
from stratosphere.utils.enums import IfExists, enforce_enum
from stratosphere.utils.environment import get_environment


class ExperimentAlreadyExists(Exception):
    """Exception to handle the attempt to add one more experiment with the same name."""

    def __init__(self, name):
        self.message = f"Experiment '{name}' already existing, use if_exists=\"replace\" to overwrite it."
        super().__init__(self.message)


class ExperimentNotFoundException(Exception):
    """Exception raised if the experiment is not found."""

    def __init__(self, name):
        self.message = f"Experiment '{name}' not found. List with .ls() the available experiments."
        super().__init__(self.message)


class ExperimentReadOnlyException(Exception):
    """Exception raised upon attempting the persistance of an experiment loaded in read-only SQL mode."""

    def __init__(self, name):
        self.message = f"Experiment '{name}' is loaded in SQL read-only mode."
        super().__init__(self.message)


class RunNotFoundException(Exception):
    """Exception raised if the run is not found."""

    def __init__(self, run_id):
        self.message = f"Run '{run_id}' not found. List with .df() the available runs."
        super().__init__(self.message)


class Experiment:
    """This class represents a new experiment.

    Raises:
        ExperimentNotFoundException: Raised if we try to use a non-existing experiment.
        ExperimentAlreadyExists: Raised if the experiment name is already present.

    Returns:
        Experiment: A defined experiment, ready to be executed, tracked, stored, queried.
    """

    # schema_cls is the SQLAlchemy model mapped to this class.
    schema_cls = schema.Experiment

    def __init__(
        self,
        db: Database = None,
        name: str = None,
        funcs: Union[Callable, List[Callable]] = None,
        kwargs: dict = None,
        attributes: dict = None,
        parameter_grid: List = None,
        experiment_id: str = None,
        execution_time: int = None,
        completion_time: int = None,
        runs: List[Run] = None,
        sql_only: bool = False,
    ):
        """Create a new experiment.

        Args:
            db (Database, optional): Database to link to. Defaults to None.
            name (str, optional): Name of the experiment. Defaults to None.
            funcs (Union[Callable, List[Callable]], optional): One or more functions to call. Defaults to None.
            kwargs (dict, optional): Fixed parameters passed to the functions. Defaults to None.
            attributes (dict, optional): Fixed experiment attributes to be tracked. Defaults to None.
            parameter_grid (List, optional): Grid of parameters, used to generate the run parameters.
            Defaults to None.
            experiment_id (str, optional): ID of the experiment to be used. Defaults to None.
            execution_time (int, optional): Start time of the execution. Defaults to None.
            completion_time (int, optional): Completion time of the execution. Defaults to None.
            runs (List[Run], optional): List of runs belonging to the experiment. Defaults to None.
            sql_only (bool, optional): If active, only the SQL interface is available and persistance is disabled.
        """
        self.db = db
        self.name = name

        # set table name, sanitizing it
        self.table_name = get_table_name(self.name)

        # normalise funcs to a list of functions.
        if funcs is None:
            self.funcs = []
        elif callable(funcs):
            self.funcs = [funcs]
        else:
            self.funcs = funcs

        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs

        # we set the dict here and not directly in the constructor definition to make sure that
        # we create a new dict at every object, without sharing it as a static attribute across
        # instances.
        self.attributes = {} if attributes is None else attributes
        self.parameter_grid = parameter_grid

        # make sure that there's always at least one element, ensuring that at least one run will
        # be defined.
        if self.parameter_grid == [] or self.parameter_grid is None:
            self.parameter_grid = [{}]

        # Setted here, for similar reasons of self.attributes.
        self.experiment_id = experiment_id if experiment_id is not None else next_ulid()
        self.execution_time = execution_time
        self.completion_time = completion_time
        self.runs = runs

        self.sql_only = sql_only

    def __reduce__(self):
        """
        When we pickle the experiment (this happens as soon as we try to
        store it in the database), pickle will use this constructor to build
        a clean object to be stored.

        The .db field is set to None and is populated by the Stratosphere instance.
        This lets us manage more transparently the linked database, avoiding
        unpickable objects in SQLAlchemy.

        Returns:
            Experiment: An unpickled Experiment object, ready to be linked
            to a database and used.
        """
        return self.__class__, (
            None,
            self.name,
            self.funcs,
            self.kwargs,
            self.attributes,
            self.parameter_grid,
            self.experiment_id,
            self.execution_time,
            self.completion_time,
            self.runs,
        )

    def query(self, query: str, verbose: bool = False) -> pd.DataFrame:
        """Query the experiment's table

        Args:
            query (str): SQL query. {e} is replaced with the table name of the experiment,
            {id} with the experiment ID, and {ee} with the experiments table.
            verbose (bool, optional): If true, print the resulting query. Defaults to False.

        Returns:
            pd.DataFrame: Result of the query.
        """

        return self.db.pandas(
            query.format(id=f"'{self.experiment_id}'", e=self.table_name, ee=config.db.experiments_table),
            verbose=verbose,
        )

    @classmethod
    def load(cls, db: Database, name: str):
        """Load an experiment from database.

        Args:
            db (Database): Reference to a database.
            name (str): Name of the experiment.

        Raises:
            ExperimentNotFoundException: Raised if the experiment is not found.

        Returns:
            Experiment: Loaded experiment.
        """

        # Create a new session
        with db.session() as session:
            record = session.query(cls.schema_cls).filter_by(name=name).first()

            # IF the record is not found, raise an error.
            if record is None:
                raise ExperimentNotFoundException(name)

            # Unpicke the serialized object.
            try:
                experiment = serialization.pickle_loads(record.serialized)
                # Set the db of the experiment. Pickled db instances are never re-instantiated
                # completely, this let us reuse the existing database instance. See the Database
                # class for more comments on this.
                #
                # Important: this let us use SQLite memory databases, as only one instance is
                # used on all experiments.
                experiment.db = db
                return experiment
            except PickleError:
                # Unpickling failed (it happens between Python 3.7 / Python 3.8, and in case of missing
                # dependencies, and different architectures).
                logging.warning("Unpicking failed, this experiment is loaded in SQL read-only mode.")
                experiment = Experiment(db=db, name=name, experiment_id=record.id, sql_only=True)
                return experiment

    @log.default_exception_handler
    @log.timeit
    def execute(
        self,
        funcs: Union[str, Callable, List[Callable]] = None,
        backend=joblib.parallel.DEFAULT_BACKEND,
        n_jobs=-1,
    ):
        """Execute the experiment, then retuning it.

        Args:
            funcs (Union[Callable, List[Callable]], optional): Function(s) that will override the defined ones.
            If the value is "all", the re-evaluation of all defined functions is forced. Defaults to None.
            backend (_type_, optional): Joblib baackend. Defaults to joblib.parallel.DEFAULT_BACKEND.
            n_jobs (int, optional): Parallelization degree, defined as in Joblib. Defaults to -1.

        Returns:
            Run: the same experiment, ready for chained operations.
        """

        self.execution_time = time.current_time()

        if funcs == "all":
            # If we pass 'all', we force the re execution of all funcs.
            funcs = self.funcs

        # If this is not the first execution ...
        if self.runs is not None:
            # If we want to override the functions to execute ...
            if funcs is not None:
                # ... we can reuse the runs context, and execute the functions on them.
                tasks = [Run.execute_func(run, override_funcs=funcs) for run in self.runs]

            else:
                # else: ... there is nothing to do, the runs context is already up to date.
                tasks = []
        else:
            # If this is the first execution, we build and execute the runs from scratch.
            parameters_list = self.parameter_grid.copy()
            # We shuffle the parameters, so that partial experiment statistics and expected
            # duration are more representative of all runs.
            random.shuffle(parameters_list)

            tasks = [
                Run.execute_func(
                    Run(
                        kwargs=self.kwargs,
                        parameters=parameters,
                        funcs=self.funcs,
                        experiment_name=self.name,
                    ),
                    override_funcs=funcs,
                )
                for parameters in parameters_list
            ]

        if len(tasks) > 0:
            # We update the runs context only if there are tasks to execute.
            self.runs = Job(tasks, n_jobs=n_jobs, backend=backend).execute()

        self.completion_time = time.current_time()
        return self

    def record(self) -> schema.Experiment:
        """Build an SQLAlchemy ORM object from the existing Experiment object.

        Returns:
            schema.Experiment: SQLAlchemy ORM object.
        """
        return self.schema_cls(
            id=self.experiment_id,
            name=self.name,
            environment=serialization.json_dumps(get_environment()),
            execution_time=self.execution_time,
            completion_time=self.completion_time,
            attributes=serialization.json_dumps({**self.attributes}),
            serialized=serialization.pickle_dumps(self),
        )

    def info(self):
        """Print some stats about the experiment.

        Returns:
            Experiment: self
        """
        logging.info("Experiment info")
        logging.info(f"  id...............: {self.experiment_id}")
        logging.info(f"  name.............: '{self.name}'")
        logging.info(f"  funcs............: {[func.__name__ for func in self.funcs]}")
        logging.info(f"  kwargs...........: {list(self.kwargs.keys())}")

        logging.info(f"  parameter_grid...: {list(self.parameter_grid[0].keys())} ({len(self.parameter_grid)})")

        logging.info(f"  attributes.......: {list(self.attributes.keys())}")
        logging.info(f"  size (Mb)........: {self.size('mb')} (compressed)")
        logging.info(f"  table name.......: {self.table_name}")

        return self

    @log.default_exception_handler
    def persist(self, if_exists: IfExists = IfExists["fail"]):
        """Persist the experiment.

        Args:
            if_exists (IfExists, optional): Either "replace" or "fail". Defaults to "fail".

        Raises:
            ExperimentReadOnlyException: Experiment loaded in SQL read-only mode.

        Returns:
            _type_: self.
        """

        if self.sql_only:
            raise ExperimentReadOnlyException(self.name)

        logging.info(f"Persisting experiment (table name: {self.table_name})")

        if_exists = enforce_enum(if_exists, IfExists)

        # First, we try to delete the record, honoring the if_exists preference.
        self.delete(if_exists)
        # Then, we:
        # 1. Add the experiment record to the "experiments" table.
        # 2. Add the experiment table "experiment_{name}".

        with self.db.session() as session:
            session.add(self.record())
            session.commit()
        self.db.pandas_to_sql(self.df(), self.table_name, if_exists.name)

        return self

    @log.default_exception_handler
    def lookup(self, run_id: str) -> Run:
        """Lookup a run by ID

        Args:
            run_id (str): ID of the run to lookup.

        Raises:
            RunNotFoundException: Raised if run ID not found.

        Returns:
            Run: The matching run.
        """

        if self.runs is None:
            raise RunNotFoundException(run_id)

        # A rather unperformance way to look up the run.
        # TODO: change .runs to a dict.
        for run in self.runs:
            if run.run_id == run_id:
                return run

    @log.default_exception_handler
    def delete(self, if_exists: IfExists = IfExists["fail"]) -> None:
        """Delete the expeirment.

        Args:
            if_exists (IfExists, optional): Either "replace" or "fail". In case
            the experiment exists and the value is "replace", nothing happens.
            If the experiment exists and the value is "fail", it will raise an
            exception. It is designed to work correctly together with insertions.
            Defaults to "fail".

        Raises:
            ExperimentAlreadyExists: Raised if the experiment exists.
        """

        if_exists = enforce_enum(if_exists, IfExists)

        # Create a new session
        with self.db.session() as session:
            # If we find the record ...
            if session.query(self.schema_cls).filter_by(name=self.name).count() > 0:
                # And we are fine deleting it, proceed.
                if if_exists == IfExists["replace"]:
                    session.query(Experiment.schema_cls).filter(Experiment.schema_cls.name == self.name).delete()
                else:
                    # Otherwise, raise an exception.
                    raise ExperimentAlreadyExists(self.name)
            session.commit()

        # We also need to drop the experiment table.
        self.db.drop_table(self.table_name)

    @log.default_exception_handler
    def df(self, include_experiment=True) -> pd.DataFrame:
        """Returns a Pandas dataframe representing the experiment, including
        parameters and attributes. The processing does not depend on
        database queries, but the returned dataframe matches the contents
        of the experiment table (which is generated using this method).

        In presence of overlapping column names from the fixed attributes
        of the experiment and the run attributes, the run_attributes use
        "_run" as suffix.

        Args:
            include_experiment (bool, optional): If False, do not include the
            fixed experiment attributes (it will be a constant column).
            Defaults to True.

        Raises:
            ExperimentReadOnlyException: Experiment loaded in SQL read-only mode.

        Returns:
            pd.DataFrame: Pandas dataframe representing the tracked properties.
        """

        if self.sql_only:
            raise ExperimentReadOnlyException(self.name)

        # Load the dataframe from a dict or list of dicts.
        df_runs = pd.json_normalize([{**run.attributes, **{"id_run": run.run_id}} for run in self.runs])

        if not include_experiment:
            return reorder_columns(df_runs, ["id_run"]).apply(pd.to_numeric, errors="ignore")
        else:
            df_experiment = pd.json_normalize(
                {
                    **self.attributes,
                    **{"id_experiment": self.experiment_id, "name": self.name},
                }
            )

            # In case of overlapping column names, the ones from runs use the _run suffix.
            df = df_experiment.merge(
                df_runs,
                how="cross",
                suffixes=("", "_run"),
            )

            return reorder_columns(df, ["name", "id_experiment", "id_run"]).apply(pd.to_numeric, errors="ignore")

    def size(self, unit: str = "b") -> int:
        """Return the size of the pickled version of the expeirment.

        Args:
            unit (str, optional): Unit of measure: "b" (Bytes), "kb" (KiloBytes), "mb" (MegaBytes). Defaults to "b".

        Returns:
            int: Size of the experiment once pickled.
        """
        return serialization.pickle_size(self, unit=unit)

    @classmethod
    def ls(cls, db: Database) -> pd.DataFrame:
        """List experiments in a database.

        Args:
            db (Database): Database instance.

        Returns:
            pd.DataFrame: List of experiments.
        """
        with db.session() as session:
            df_experiments = pandas_query(
                session.query(Experiment.schema_cls).options(
                    load_only(
                        Experiment.schema_cls.id,
                        Experiment.schema_cls.name,
                        Experiment.schema_cls.attributes,
                    )
                ),
                session,
            )

            df_experiments = df_experiments.rename(columns={"id": "experiment_id"})

            # Add table name
            df_experiments["table_name"] = df_experiments["name"].apply(get_table_name)

            # Explode attributes
            df_experiments = explode_json_column(df_experiments, "attributes")

            return df_experiments


def reorder_columns(df: pd.DataFrame, ordered_columns: List[str]) -> List[str]:
    """Given a dataframe, enforce a partial ordering of some columns, appending
    the remaining ones in sorted order.

    Args:
        df (pd.DataFrame): Consider the columns from thsi dataframe.
        ordered_columns (List[str]): Consider this partial ordering of the columns.

    Returns:
        List[str]: New ordering of all columns for the {df} dataframe.
    """

    remaining_columns = sorted([col_name for col_name in df.columns if col_name not in ordered_columns])
    return df[ordered_columns + remaining_columns]


def get_table_name(name_experiment: str) -> str:
    """Return the table name of the experiment

    Args:
        name_experiment (str): Name of the experiment

    Returns:
        str: Table name
    """

    return sanitize_table_name(f"{config.db.experiment_table_prefix}{name_experiment}")
