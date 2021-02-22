import pandas as pd


def fast_json_normalize(json_object: list or dict, separator: str = ".", to_pandas: bool = False):
    # main recursive function, maintains object types
    def _normalise_json(object_: list or dict, key_string_: str = "", new_dict_: dict = None, separator_: str = "."):
        if isinstance(object_, dict):
            for key, value in object_.items():
                new_key = f"{key_string_}{separator_}{key}"
                _normalise_json(object_=value,
                                key_string_=new_key if new_key[len(separator_) - 1] != separator_ else new_key[len(
                                    separator_):],  # to avoid adding the separator to the start of every key
                                new_dict_=new_dict_,
                                separator_=separator_)
        elif isinstance(object_, list):
            new_dict_[key_string_] = object_
        elif isinstance(object_, str) or isinstance(object_, int) or isinstance(object_, float):
            new_dict_[key_string_] = object_
        else:
            new_dict_[key_string_] = object_
        return new_dict_

    # expect a dictionary, as most jsons are. However, lists are perfectly valid
    if isinstance(json_object, dict):
        normalised_json_object = _normalise_json(object_=json_object,
                                                 separator_=separator,
                                                 new_dict_={})
        if to_pandas:
            return pd.DataFrame(data=[normalised_json_object.values()],
                                columns=list(normalised_json_object.keys()))
    elif isinstance(json_object, list):
        normalised_json_object = [_normalise_json(row,
                                                  separator_=separator,
                                                  new_dict_={}) for row in json_object]
        if to_pandas:
            return pd.DataFrame(normalised_json_object)
    else:
        raise TypeError(
            f"Json object type {type(json_object)} not valid. Please pass a list or a dictionary as a valid json object")

    # to mimic the pandas function, add option to convert to pandas as parameter
    return normalised_json_object
