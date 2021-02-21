import datetime

import pandas as pd

data = {"hello": ["thisisatest", 999898, datetime.date.today()],
        "nest1": {"nest2": {"nest3": "nest3_value", "nest3_int": 3445}}, "nested_list": ["blah", 32423, 546456.876],
        "hello2": "string"}
data = [data for i in range(100)]
print(data)


def normalise_json(data, separator="."):
    def _normalise_json(data, key_string="", new_dict={}, separator="."):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_key = f"{key_string}{separator}{key}"
                    _normalise_json(value, new_key if new_key[0] != separator else new_key[1:], new_dict=new_dict, separator=separator)
            elif isinstance(data, list):
                new_dict[key_string] = data
            elif isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
                new_dict[key_string] = data
            else:
                new_dict[key_string] = str(data)
            return new_dict
    if isinstance(data, list):
        return [_normalise_json(row) for row in data]
    elif isinstance(data, dict):
        return _normalise_json(data)
    else:
        raise TypeError(f"Json object type {type(data)} not valid. Please pass a list or a dictionary")



custom = [normalise_json(d) for d in data]
custom_df = pd.DataFrame(custom)

normalized_data = pd.json_normalize(data)
c1 = set(custom_df.columns)
c2 = set(normalized_data.columns)
print(c1 == c2)
print(custom_df.to_records() == normalized_data.to_records())
# print(normalized_data)
