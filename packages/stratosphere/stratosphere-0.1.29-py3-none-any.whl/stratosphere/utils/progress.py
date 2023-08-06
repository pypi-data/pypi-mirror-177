import warnings

# Detect if we're running the notebook in a colab.
# If this is the case, we can avoid using tqdm.auto, which doesn't seem to work properly.
try:
    import google.colab

    IN_COLAB = True
except ModuleNotFoundError:
    IN_COLAB = False


with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    if IN_COLAB:
        from tqdm import tqdm
    else:
        from tqdm.auto import tqdm

import sys


def progress(*args, **kwargs):
    t = tqdm(*args, **kwargs)
    if "pyodide" in sys.modules:
        # running in Pyodide
        t.monitor_interval = 0
    return t
