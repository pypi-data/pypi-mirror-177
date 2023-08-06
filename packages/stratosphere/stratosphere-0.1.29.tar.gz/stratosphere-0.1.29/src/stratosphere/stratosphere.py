import copy
from typing import Callable, List, Union


from stratosphere import config
from stratosphere.experiment import Experiment
from stratosphere.utils.enums import IfExists, enforce_enum
from stratosphere.store.db.database import Database
from stratosphere.utils import log
import pandas as pd


class Stratosphere:
    """Instantiate the Stratosphere handler, it can then be sued
    to create, query, manage experiments. You can instantiate one or more,
    they do work together nicely without interfering.
    """

    def __init__(self, url: str = config.db.default_url, echo: bool = False):
        """Create a new Stratosphere handler.

        Args:
            url (str, optional): Database URL. Defaults to config.db.default_url.
            echo (bool, optional): Enable SQLAlchemy logging. Defaults to False.
        """

        log.init_logging(config.log.level)
        self.db = Database(url, echo=echo)

    @log.default_exception_handler
    def define(
        self,
        name: str = None,
        funcs: Union[Callable, List[Callable]] = None,
        kwargs: dict = None,
        attributes: dict = None,
        parameter_grid: List = None,
    ) -> Experiment:
        """Define a new experiment.

        Args:
            name (str, optional): Name of the experiment (must be unique). Defaults to None.
            funcs (Union[Callable, List[Callable]], optional): Function(s) we want to apply to the input parameters. Defaults to None.
            kwargs (dict, optional): Fixed arguments to the functions. Defaults to None.
            attributes (dict, optional): Fixed experiment properties to be tracked. Defaults to None.
            parameter_grid (List, optional): Variable parameters to pass to the functions. Defaults to None.

        Returns:
            Experiment: The newly defined experiment, reaady to be executed.
        """

        return Experiment(
            db=self.db,
            name=name,
            funcs=funcs,
            kwargs=kwargs,
            attributes=attributes,
            parameter_grid=parameter_grid,
        )

    @log.default_exception_handler
    def ls(self) -> pd.DataFrame:
        """List the tracked experiments.

        Returns:
            pd.DataFrame: Pandas dataframe.
        """
        return Experiment.ls(self.db)

    @log.default_exception_handler
    def load(self, name: str = None) -> Experiment:
        """Load an experiment from the database and return it.

        Args:
            name (str, optional): The name of the experiment. Defaults to None.

        Returns:
            Experiment: The loaded experiment.
        """
        return Experiment.load(self.db, name)

    @log.default_exception_handler
    def persist(
        self, experiment: Experiment, if_exists: IfExists = "fail"
    ) -> Experiment:
        """Persist the experiment to the database (not necessarily
        the one used to track it initially).

        Args:
            experiment (Experiment): Experiment object to be persisted.
            if_exists (IfExists, optional): Either "replace" of "fail" in case
            the experiment name is already present. Defaults to "fail".

        Returns:
            Experiment: The persisted experiment.
        """

        # Enforce if_exists value
        if_exists = enforce_enum(if_exists, IfExists)

        # We make a copy of the experiment, and change the database reference.
        # We can then use all its methods, including persist(...).
        experiment = copy.deepcopy(experiment)
        experiment.db = self.db
        experiment.persist(if_exists=if_exists)
        return experiment
