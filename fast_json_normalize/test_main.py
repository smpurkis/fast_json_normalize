import datetime
from time import time

import pandas as pd

from fast_json_normalize import fast_json_normalize

# example json data
data = {"hello": ["thisisatest", 999898, datetime.date.today()],
        "nest1": {"nest2": {"nest3": "nest3_value", "nest3_int": 3445}},
        "nest1_list": {"nest2": ["blah", 32423, 546456.876, 92030234]},
        "hello2": "string"}
hundred_rows = [data for i in range(100)]
ten_thousand_rows = [data for i in range(10000)]
hundred_thousand_rows = [data for i in range(100000)]
million_rows = [data for i in range(1000000)]


def test_pandas_dict_equality():
    pandas_json_normalize_df = pd.json_normalize(data)
    fast_json_normalize_df = fast_json_normalize(data, to_pandas=True, cythonized=False)
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())
    fast_json_normalize_df = fast_json_normalize(data, to_pandas=True)
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_pandas_dict_equality_ordered():
    pandas_json_normalize_df = pd.json_normalize(data)
    fast_json_normalize_df = fast_json_normalize(data, to_pandas=True, order_to_pandas=True, cythonized=False)
    assert all(pandas_json_normalize_df.columns == fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())
    fast_json_normalize_df = fast_json_normalize(data, to_pandas=True, order_to_pandas=True)
    assert all(pandas_json_normalize_df.columns == fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_pandas_list_equality():
    pandas_json_normalize_df = pd.json_normalize(hundred_rows)
    fast_json_normalize_df = fast_json_normalize(hundred_rows, to_pandas=True, cythonized=False)
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())
    fast_json_normalize_df = fast_json_normalize(hundred_rows, to_pandas=True)
    assert set(pandas_json_normalize_df.columns) == set(fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_pandas_list_equality_ordered():
    pandas_json_normalize_df = pd.json_normalize(hundred_rows)
    fast_json_normalize_df = fast_json_normalize(hundred_rows, to_pandas=True, order_to_pandas=True, cythonized=False)
    assert all(pandas_json_normalize_df.columns == fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())
    fast_json_normalize_df = fast_json_normalize(hundred_rows, to_pandas=True, order_to_pandas=True)
    assert all(pandas_json_normalize_df.columns == fast_json_normalize_df.columns)
    assert all(pandas_json_normalize_df.to_records() == fast_json_normalize_df.to_records())


def test_speed_hundred_rows_ordered():
    s = time()
    pd.json_normalize(hundred_rows)
    pandas_json_normalize_time_taken = time() - s
    print(f"\npandas time taken for a 100 rows: {pandas_json_normalize_time_taken}")
    s = time()
    fast_json_normalize(hundred_rows, to_pandas=True, order_to_pandas=True, cythonized=False)
    fast_json_normalize_time_taken = time() - s
    print(f"fast implementation time taken for a 100 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_ten_thousand_rows_ordered():
    s = time()
    pd.json_normalize(ten_thousand_rows)
    pandas_json_normalize_time_taken = time() - s
    print(f"\npandas time taken for a 10,000 rows: {pandas_json_normalize_time_taken}")
    s = time()
    fast_json_normalize(ten_thousand_rows, to_pandas=True, order_to_pandas=True, cythonized=False)
    fast_json_normalize_time_taken = time() - s
    print(f"fast implementation time taken for a 10,000 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_hundred_thousand_rows_ordered():
    s = time()
    pd.json_normalize(hundred_thousand_rows)
    pandas_json_normalize_time_taken = time() - s
    print(f"\npandas time taken for a 100,0000 rows: {pandas_json_normalize_time_taken}")
    s = time()
    fast_json_normalize(hundred_thousand_rows, to_pandas=True, order_to_pandas=True, cythonized=False)
    fast_json_normalize_time_taken = time() - s
    print(
        f"fast implementation (maintaining pandas order) time taken for a 100,000 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken


def test_speed_hundred_thousand_rows_ordered_cythonized():
    s = time()
    pd.json_normalize(hundred_thousand_rows)
    pandas_json_normalize_time_taken = time() - s
    print(f"\npandas time taken for a 100,0000 rows: {pandas_json_normalize_time_taken}")
    s = time()
    fast_json_normalize(hundred_thousand_rows, to_pandas=True, order_to_pandas=True, cythonized=True)
    fast_json_normalize_time_taken = time() - s
    print(
        f"fast implementation (maintaining pandas order) time taken for a 100,000 rows: {fast_json_normalize_time_taken}")
    assert fast_json_normalize_time_taken < pandas_json_normalize_time_taken