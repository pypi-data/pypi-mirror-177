import json
import zlib

import cloudpickle


def pickle_dumps(obj: object) -> bytes:
    """It returns the compressed (zlib) pickled object. The Pickle DEFAULT_PROTOCOL is used
    for maximum compatibility.

    Args:
        obj (object): Object to serialize.

    Returns:
        bytes: Compressed serialized object.
    """
    return zlib.compress(cloudpickle.dumps(obj, protocol=cloudpickle.DEFAULT_PROTOCOL))


def pickle_loads(data: bytes) -> object:
    """It returns the loaded object, afer uncompressing and unpickling it.

    Args:
        data (bytes): Serialized object.

    Returns:
        object: Unserialized object.
    """
    return cloudpickle.loads(zlib.decompress(data))


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
