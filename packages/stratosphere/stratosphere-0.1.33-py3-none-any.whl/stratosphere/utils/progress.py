import warnings
import sys

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

if "pyodide" in sys.modules:
    tqdm.monitor_interval = 0


def progress(*args, **kwargs):
    return tqdm(*args, **kwargs)
