from functools import partial
from typing import Callable, Union
from typing import List

from stratosphere.store.db.database import next_ulid
from stratosphere.utils.time import current_time


class Run:
    """A run represents an instance of the experiment, obtained by
    combining the fixed and variable parameters. The Run objects
    (and the tracked attributes)  must be serializable with cloudpickle.
    """

    def __init__(
        self,
        kwargs: dict = None,
        parameters: dict = None,
        attributes: dict = None,
        blobs: dict = None,
        funcs: Union[Callable, List[Callable]] = None,
        experiment_name: str = None,
    ):
        """Create a new run.

        Args:
            kwargs (dict, optional): Fixed parameters for all runs of an experiment. Defaults to None.
            parameters (dict, optional): Variable parameters to be considered for this run. Defaults to None.
            attributes (dict, optional): Attributes to be tracked. Defaults to None.
            blobs (dict, optional): Binary attributes to be tracked. Defaults to None.
            funcs (Union[Callable, List[Callable]], optional): One or more functions to be executed. Their only parameter is an instance of
            the Run class itself.
            experiment_name (str, optional): Name of the experiment the run belongs to. Defaults to None.
        """

        self.kwargs = {} if kwargs is None else kwargs
        self.parameters = {} if parameters is None else parameters
        self.attributes = {} if attributes is None else attributes
        self.blobs = {} if blobs is None else blobs
        self.funcs = [] if funcs is None else funcs
        self.execution_time = None
        self.completion_time = None
        self.run_id = next_ulid()
        self.experiment_name = experiment_name

    @classmethod
    def execute(cls, run):
        """Execute the functions on the Run object. The functions can modify its .attributes and .blobs
        fields, that are treated as state accumulators. Other changes to the Run object might be lost
        if pickling and moving the Run, therefore they are discouraged.

        Args:
            run (Run): Run we want to execute.

        Returns:
            Run: Run object after the execution of the functions.
        """

        run.execution_time = current_time()

        # The funcs field might be one or more functions.
        if callable(run.funcs):
            run.funcs(run)
        else:
            [func(run) for func in run.funcs]

        run.completion_time = current_time()
        return run

    @classmethod
    def execute_func(
        cls,
        run,
        override_funcs: Union[Callable, List[Callable]] = None,
    ):
        """_summary_

        Args:
            run (_type_): _description_
            override_funcs (Union[Callable, List[Callable]], optional):
            Function(s) to be executed, overriding the already configured ones.
            Important, the new functions are overwriting the existing ones.


        Returns:
            Callable: function ready to be called, to execute the run.
        """
        if override_funcs:
            run.funcs = override_funcs
        return partial(cls.execute, run)
