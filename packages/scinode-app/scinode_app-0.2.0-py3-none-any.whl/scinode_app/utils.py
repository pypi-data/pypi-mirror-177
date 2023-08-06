def serializable_object(data):
    """for data and results

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(data, dict):
        for key, value in data.items():
            value["value"] = serializable(value["value"])
    elif isinstance(data, tuple):
        for value in data:
            value["value"] = serializable(value["value"])
    return data


def serializable(data):
    """Numpy type, e.g. int64, is not JSON serializable

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    if "numpy.int64" in str(type(data)):
        print("int64")
        data = int(data)
    elif "numpy.array" in str(type(data)):
        data = data.tolist()
    return data
