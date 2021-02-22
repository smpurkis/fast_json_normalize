import pandas as pd
import pytest

from fast_json_normalize import fast_json_normalize


def test_empty_list():
    assert fast_json_normalize([]) == []


def test_empty_dict():
    assert fast_json_normalize({}) == {}


def test_empty_string():
    with pytest.raises(TypeError):
        fast_json_normalize("")
        fast_json_normalize("test")


def test_number():
    with pytest.raises(TypeError):
        fast_json_normalize(3)
        fast_json_normalize(17.2)


def test_empty_dataframe():
    with pytest.raises(TypeError):
        fast_json_normalize(pd.DataFrame)
