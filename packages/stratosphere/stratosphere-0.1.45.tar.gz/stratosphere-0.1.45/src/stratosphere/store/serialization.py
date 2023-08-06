import json
import zlib
from io import BytesIO
from typing import Union

import cloudpickle
import pandas as pd
from stratosphere import config


# Default protocol for Python 3.7, compatible with Python >= 3.7
PICKLE_DEFAULT_PROTOCOL = 3


def compress(data: bytes) -> bytes:
    if config.serialization.enable_compression:
        return zlib.compress(data)
    else:
        return data


def decompress(data: bytes) -> bytes:
    if config.serialization.enable_compression:
        return zlib.decompress(data)
    else:
        return data


def pickle_dumps(obj: object) -> bytes:
    """It returns the compressed (zlib) pickled object. The Pickle DEFAULT_PROTOCOL is used
    for maximum compatibility.

    Args:
        obj (object): Object to serialize.

    Returns:
        bytes: Compressed serialized object.
    """
    return compress(cloudpickle.dumps(obj, protocol=PICKLE_DEFAULT_PROTOCOL))


def pickle_loads(data: bytes) -> object:
    """It returns the loaded object, afer uncompressing and unpickling it.

    Args:
        data (bytes): Serialized object.

    Returns:
        object: Unserialized object.
    """
    return cloudpickle.loads(decompress(data))


def pickle_size(obj: object, unit: str = "b") -> int:
    """It returns the size of the object once serialised (including compression).

    Args:
        obj (object): Object to analyse.
        unit (str, optional): Unit of measure, b (Bytes), kb (KiloBytes), mb (MegaBytes). Defaults to "b".

    Returns:
        int: Size of the serialized object.
    """
    size_object = len(pickle_dumps(obj))
    if unit == "b":
        return int(size_object * 1e2) / 1e2
    elif unit == "kb":
        return int(size_object * 1e-3 * 1e2) / 1e2
    elif unit == "mb":
        return int(size_object * 1e-6 * 1e2) / 1e2
    else:
        return None


def json_dumps(obj: object) -> str:
    """Serialize an object to its JSON string representation.

    Args:
        obj (object): Object to serialize.

    Returns:
        str: Serialized object.
    """
    return json.dumps(obj)


def json_loads(obj: str) -> object:
    """Unserialize an object from its JSON string representation.

    Args:
        obj (str): Object to unserialize.

    Returns:
        object: Unserialized object.
    """
    return json.loads(obj)


def pd_dumps(obj: Union[pd.Series, pd.DataFrame]) -> str:
    """Dump a Pandas dataframe or a series to CSV format

    Args:
        obj (Union[pd.Series, pd.DataFrame]): Pandas series or frame to dump

    Returns:
        str: String representing the dumped object
    """
    return compress(obj.to_csv(float_format="%.4f").encode(encoding="UTF-8"))


def pd_loads(obj: str) -> Union[pd.Series, pd.DataFrame]:
    """Load Pandas series or dataframe from CSV format

    Args:
        obj (str): Serialized Pandas series or frame to load

    Returns:
        Union[pd.Series, pd.DataFrame]: Unserialized object
    """
    return pd.read_csv(BytesIO(decompress(obj)), index_col=0)
