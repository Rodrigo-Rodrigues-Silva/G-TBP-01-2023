import pytest
from fastapi import HTTPException
from validations.room import validate_cost, validate_number, check_cost, check_number


def test_validate_number_ok():
    assert validate_number("teste")


def test_validate_number_empty():
    assert validate_number('') is False


def test_validate_number_white_spaces():
    assert validate_number('   ') is False


def test_validate_cost_ok():
    assert validate_cost(5)


def test_validate_cost_less_than_1():
    assert validate_cost(0) is False


def test_check_cost_error_422():
    with pytest.raises(HTTPException) as error:
        check_cost(0)
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['coast'], "msg": ["cost must to be greater than 1"], "type": "value_error"}


def test_check_number_error_422():
    with pytest.raises(HTTPException) as error:
        check_number("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['number'], "msg": ["number cannot be empty"], "type": "value_error"}
