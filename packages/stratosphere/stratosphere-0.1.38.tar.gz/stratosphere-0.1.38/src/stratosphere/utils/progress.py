import warnings
import sys

try:
    import google.colab

    in_colab = True
except ModuleNotFoundError:
    in_colab = False


if "pyodide" in sys.modules:
    in_pyodide = True
else:
    in_pyodide = False

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    if in_colab:
        from tqdm import tqdm
    else:
        from tqdm.auto import tqdm

    if in_pyodide:
        tqdm.monitor_interval = 0


def progress(*args, **kwargs):
    return tqdm(*args, **kwargs)
