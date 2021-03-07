import pandas as pd
from fast_json_normalize.cythonized import fast_json_normalize_cythonized


def fast_json_normalize(json_object: list or dict, separator: str = ".", to_pandas: bool = True,
                        order_to_pandas: bool = True, cythonized: bool = True):
    if cythonized:
        normalised_json_object = fast_json_normalize_cythonized(
            json_object=json_object,
            separator=separator,
            to_pandas=to_pandas,
            order_to_pandas=order_to_pandas
        )
    else:

        # main recursive function, maintains object types, not ordering
        def _normalise_json(object_: object, key_string_: str = "", new_dict_: dict = None, separator_: str = "."):
            if isinstance(object_, dict):
                for key, value in object_.items():
                    new_key = key_string_ + separator_ + key
                    _normalise_json(object_=value,
                                    key_string_=new_key if new_key[len(separator_) - 1] != separator_ else new_key[len(
                                        separator_):],  # to avoid adding the separator to the start of every key
                                    new_dict_=new_dict_,
                                    separator_=separator_)
            else:
                new_dict_[key_string_] = object_
            return new_dict_

        # depth aware recursive function, maintains object types and pandas column ordering
        def _normalise_json_ordered(object_: dict, separator_: str = "."):
            top_dict_ = {k: v for k, v in object_.items() if not isinstance(v, dict)}
            nested_dict_ = _normalise_json({k: v for k, v in object_.items() if isinstance(v, dict)},
                                           separator_=separator_,
                                           new_dict_={})
            return {**top_dict_, **nested_dict_}

        # expect a dictionary, as most jsons are. However, lists are perfectly valid
        if isinstance(json_object, dict):
            if not order_to_pandas:
                normalised_json_object = _normalise_json(object_=json_object,
                                                         separator_=separator,
                                                         new_dict_={})
            else:
                normalised_json_object = _normalise_json_ordered(object_=json_object,
                                                                 separator_=separator)
        elif isinstance(json_object, list):
            if not order_to_pandas:
                normalised_json_object = [_normalise_json(row,
                                                          separator_=separator,
                                                          new_dict_={}) for row in json_object]
            else:
                normalised_json_object = [fast_json_normalize(row,
                                                              separator=separator,
                                                              order_to_pandas=order_to_pandas,
                                                              to_pandas=False,
                                                              cythonized=cythonized) for row in json_object]
        else:
            raise TypeError(
                "Json object type {} not valid. Please pass a list or a dictionary as a valid json object".format(
                    type(json_object)))

    if to_pandas:
        if isinstance(json_object, dict):
            df = pd.DataFrame(data=[normalised_json_object.values()],
                              columns=list(normalised_json_object.keys()))
            return df
        else:
            return pd.DataFrame(normalised_json_object)
    # to mimic the pandas function, add option to convert to pandas as parameter
    return normalised_json_object
