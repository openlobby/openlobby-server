from datetime import datetime


def strip_value(data, *path):
    element = path[0]
    value = data.get(element)
    if len(path) == 1:
        data[element] = "__STRIPPED__"
        return value
    else:
        if isinstance(value, dict):
            return strip_value(value, *path[1:])
        elif isinstance(value, list):
            return [strip_value(item, *path[1:]) for item in value]
        else:
            raise NotImplementedError()


def dates_to_iso(data):
    for key, val in data.items():
        if isinstance(val, datetime):
            data[key] = val.isoformat()
    return data
