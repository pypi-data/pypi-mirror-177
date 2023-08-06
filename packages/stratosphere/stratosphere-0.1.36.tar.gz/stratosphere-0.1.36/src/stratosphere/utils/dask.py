import logging
from asyncio.exceptions import CancelledError
from datetime import datetime

import pandas as pd
from IPython.display import clear_output
from dask.distributed import Client
from tabulate import tabulate

import dask
import time
from stratosphere import config
from stratosphere.run import Run
from stratosphere.utils import log
from typing import Dict, Union, Callable


def log_event(msg: Union[Dict, str]):
    """Log structured event with Dask.

    Args:
        msg (Union[Dict, str]): Event to log.
    """
    dask.distributed.get_worker().log_event("stratosphere", msg)


def dask_logger(run: Run, insert_delay: float = 0) -> Run:
    """Dask logger function that can be appended on experiments,
    to log the attributes of executed runs with Dask, enabling
    real-time experiment tracking. Tracked properties:

    Args:
        run (Run): Run to track.
        insert_delay (float, optional): Introduce a delay (seconds),
        useful to demonstrate the tracking functionality. Defaults to 0.

    Returns:
        Run: unaltered run after tracking it.
    """
    if insert_delay > 0:
        time.sleep(insert_delay)
    log_event({"run_id": run.run_id, "attributes": run.attributes})
    return run


@log.default_exception_handler
def monitor_latest_event(client_address: str = config.dask.scheduler_address):
    """Utility function to report the latest tracked Run event, useful to start
    debugging execution issues. The function returns after a keyboard interrupt
    or after the connection with the scheduler is lost, which can happen if:
    1. The connection delay is too low (see config.dask)
    2. The Dask scheduler terminated, either nicely or after a failure

    Args:
        client_address (str, optional): Dask scheduler address. Defaults to config.dask.scheduler_address.
    """
    log.init_logging(logging.INFO)

    def display_progress(df):
        clear_output(wait=True)
        print(
            f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Count events:"
            f" {len(df)}\n"
        )
        print(tabulate(df.iloc[-1].to_frame()))

    monitor_events(display_progress, client_address=client_address)


@log.default_exception_handler
def monitor_events(func: Callable, client_address: str = config.dask.scheduler_address):
    """Utility function to execute a callable, passing a Pandas dataframe as argument, representing
    all the tracked events. It can be used to implement custom tracking monitors.

    Args:
        func (Callable): Function that accepts as argument a Pandas dataframe, representing the
        tracked events.
        client_address (str, optional): _description_. Defaults to config.dask.scheduler_address.
    """
    try:
        with Client(
            address=client_address, timeout=config.dask.client_timeout
        ) as client:
            while True:
                events = client.get_events("stratosphere")
                df = pd.json_normalize([event[1] for event in events])
                func(df)
                time.sleep(1)
    except (CancelledError, OSError):
        logging.error("Connection failed or cluster terminated")
