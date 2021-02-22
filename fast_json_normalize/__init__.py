import pandas as pd


def fast_json_normalize(json_object: list or dict, separator: str = ".", to_pandas: bool = True,
                        order_to_pandas: bool = True):
    # main recursive function, maintains object types, not ordering
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

    # depth aware recursive function, maintains object types and pandas column ordering
    def _normalise_json_ordered(object_: list or dict, key_string_: str = "", nested_dict_: dict = None,
                                top_dict_: dict = None,
                                separator_: str = ".", depth: int = 0):
        if isinstance(object_, dict):
            for key, value in object_.items():
                new_key = f"{key_string_}{separator_}{key}"
                _normalise_json_ordered(object_=value,
                                        key_string_=new_key if new_key[len(separator_) - 1] != separator_
                                        else new_key[len(separator_):],
                                        # to avoid adding the separator to the start of every key
                                        nested_dict_=nested_dict_,
                                        top_dict_=top_dict_,
                                        separator_=separator_,
                                        depth=depth + 1)
        elif isinstance(object_, list):
            if depth == 1:
                top_dict_[key_string_] = object_
            else:
                nested_dict_[key_string_] = object_
        elif isinstance(object_, str) or isinstance(object_, int) or isinstance(object_, float):
            if depth == 1:
                top_dict_[key_string_] = object_
            else:
                nested_dict_[key_string_] = object_
        else:
            if depth == 1:
                top_dict_[key_string_] = object_
            else:
                nested_dict_[key_string_] = object_
        return top_dict_, nested_dict_

    # expect a dictionary, as most jsons are. However, lists are perfectly valid
    if isinstance(json_object, dict):
        if not order_to_pandas:
            normalised_json_object = _normalise_json(object_=json_object,
                                                     separator_=separator,
                                                     new_dict_={})
        else:
            top_dict, nested_dict = _normalise_json_ordered(object_=json_object,
                                                            separator_=separator,
                                                            nested_dict_={},
                                                            top_dict_={},
                                                            depth=0)
            normalised_json_object = {**top_dict, **nested_dict}
        if to_pandas:
            df = pd.DataFrame(data=[normalised_json_object.values()],
                              columns=list(normalised_json_object.keys()))
            return df
    elif isinstance(json_object, list):
        if not order_to_pandas:
            normalised_json_object = [_normalise_json(row,
                                                      separator_=separator,
                                                      new_dict_={}) for row in json_object]
        else:
            normalised_json_object = [fast_json_normalize(row,
                                                          separator=separator,
                                                          order_to_pandas=order_to_pandas,
                                                          to_pandas=False) for row in json_object]
        if to_pandas:
            return pd.DataFrame(normalised_json_object)
    else:
        raise TypeError(
            f"Json object type {type(json_object)} not valid. Please pass a list or a dictionary as a valid json object")

    # to mimic the pandas function, add option to convert to pandas as parameter
    return normalised_json_object
