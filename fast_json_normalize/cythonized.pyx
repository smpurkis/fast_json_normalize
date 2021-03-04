cimport cython

# main recursive function, maintains object types, not ordering
cpdef dict _normalise_json_cythonized(object_: object, str key_string_: str = "", dict new_dict_: dict = None, str separator_: str = "."):

    cdef:
        str key
        object value
        str new_key

    if isinstance(object_, dict):
        for key, value in object_.items():
            new_key = key_string_ + separator_ + key
            _normalise_json_cythonized(object_=value,
                            key_string_=new_key if new_key[len(separator_) - 1] != separator_ else new_key[len(separator_):],
                            # to avoid adding the separator to the start of every key
                            new_dict_=new_dict_,
                            separator_=separator_)
    else:
        new_dict_[key_string_] = object_
    return new_dict_

# depth aware recursive function, maintains object types and pandas column ordering
cpdef dict _normalise_json_ordered_cythonized(dict object_: dict, str separator_: str = "."):

    cdef:
        str k
        object v
        dict top_dict_
        dict nested_dict_

    top_dict_ = {k: v for k, v in object_.items() if not isinstance(v, dict)}
    nested_dict_ = _normalise_json_cythonized({k: v for k, v in object_.items() if isinstance(v, dict)},
                                   separator_=separator_,
                                   new_dict_={})
    return {**top_dict_, **nested_dict_}


cpdef object fast_json_normalize_cythonized(object json_object: list or dict, str separator: str = ".", bint to_pandas: bool = True, bint order_to_pandas: bool = True):

    cdef:
        dict row

    # expect a dictionary, as most jsons are. However, lists are perfectly valid
    if isinstance(json_object, dict):
        if not order_to_pandas:
            normalised_json_object = _normalise_json_cythonized(object_=json_object,
                                                     separator_=separator,
                                                     new_dict_={})
        else:
            normalised_json_object = _normalise_json_ordered_cythonized(object_=json_object,
                                                             separator_=separator)
    elif isinstance(json_object, list):
        if not order_to_pandas:
            normalised_json_object = [_normalise_json_cythonized(row,
                                                      separator_=separator,
                                                      new_dict_={}) for row in json_object]
        else:
            normalised_json_object = [fast_json_normalize_cythonized(row,
                                                          separator=separator,
                                                          order_to_pandas=order_to_pandas,
                                                          to_pandas=False) for row in json_object]
    else:
        raise TypeError(
            f"Json object type {type(json_object)} not valid. Please pass a list or a dictionary as a valid json object")

    # to mimic the pandas function, add option to convert to pandas as parameter
    return normalised_json_object
