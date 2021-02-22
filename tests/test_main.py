import datetime
from time import time

import pandas as pd

from fast_json_normalize import fast_json_normalize

# example json data
data = {"hello": ["thisisatest", 999898, datetime.date.today()],
        "nest1": {"nest2": {"nest3": "nest3_value", "nest3_int": 3445}},
        "nested_list": ["blah", 32423, 546456.876, 92030234],
        "hello2": "string"}
hundred_rows = [data for i in range(100)]
ten_thousand_rows = [data for i in range(10000)]
hundred_thousand_rows = [data for i in range(100000)]
million_rows = [data for i in range(1000000)]


def timeit(func, arguments):
    start = time()
    func(arguments)
    return time() - start


def test_pandas_dict_equality():
    pandas_json_normalize_df = pd.json_normalize(data)
    fast_json_normalize_df = fast_json_normalize.fast_json_normalize(data, to_pandas=True)
    p = pandas_json_normalize_df.to_records()
    f = fast_json_normalize_df.to_records()
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_pandas_list_equality():
    pandas_json_normalize_df = pd.json_normalize(hundred_rows)
    fast_json_normalize_df = fast_json_normalize.fast_json_normalize(hundred_rows, to_pandas=True)
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_speed_hundred_rows():
    pandas_json_normalize_time_taken = timeit(pd.json_normalize, hundred_rows)
    print(f"\npandas time taken for a 100 rows: {pandas_json_normalize_time_taken}")
    fast_json_normalize_time_taken = timeit(fast_json_normalize.fast_json_normalize, hundred_rows)
    print(f"fast implementation time taken for a 100 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_ten_thousand_rows():
    pandas_json_normalize_time_taken = timeit(pd.json_normalize, ten_thousand_rows)
    print(f"\npandas time taken for 10,000 rows: {pandas_json_normalize_time_taken}")
    fast_json_normalize_time_taken = timeit(fast_json_normalize.fast_json_normalize, ten_thousand_rows)
    print(f"fast implementation time taken for 10,000 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_hundred_thousand_rows():
    pandas_json_normalize_time_taken = timeit(pd.json_normalize, hundred_thousand_rows)
    print(f"\npandas time taken for 100 for a 100,000 rows: {pandas_json_normalize_time_taken}")
    fast_json_normalize_time_taken = timeit(fast_json_normalize.fast_json_normalize, hundred_thousand_rows)
    print(f"fast implementation time taken for a 100,000 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_million_rows():
    pandas_json_normalize_time_taken = timeit(pd.json_normalize, million_rows)
    print(f"\npandas time taken for 100 for a million rows: {pandas_json_normalize_time_taken}")
    fast_json_normalize_time_taken = timeit(fast_json_normalize.fast_json_normalize, million_rows)
    print(f"fast implementation time taken for a million rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken
