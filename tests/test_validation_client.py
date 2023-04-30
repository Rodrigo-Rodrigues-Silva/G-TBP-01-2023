import pytest
from fastapi import HTTPException
from validations import client


def test_check_name_error_422():
    with pytest.raises(HTTPException) as error:
        client.check_name("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['name'],
                                  "msg": ["name cannot be empty and must have 3 or more letters"],
                                  "type": "value_error"}


def test_check_last_name_error_422():
    with pytest.raises(HTTPException) as error:
        client.check_last_name("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['last_name'],
                                  "msg": ["last_name cannot be empty and must have 3 or more letters"],
                                  "type": "value_error"}


def test_check_cpf_error_422():
    with pytest.raises(HTTPException) as error:
        client.check_cpf("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['cpf'],
                                  "msg": ["cpf must to be on format 000.000.000-00"],
                                  "type": "value_error"}


def test_check_phone_error_422():
    with pytest.raises(HTTPException) as error:
        client.check_phone("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['phone'],
                                  "msg": ["phone must to be on format (00) 00000 0000"],
                                  "type": "value_error"}


def test_check_email_error_422():
    with pytest.raises(HTTPException) as error:
        client.check_e_mail("")
    assert error.value.status_code == 422
    assert error.value.detail == {"loc": ['e_mail'],
                                  "msg": ["e_mail must to be on format aaaa@bbbb.ccc"],
                                  "type": "value_error"}


def test_validate_name_ok():
    assert client.validate_name("Jose")


def test_validate_name_less_than_3():
    assert client.validate_name("Be") is False


def test_validate_name_white_space():
    assert client.validate_name("  ") is False


def test_validate_cpf_ok():
    assert client.validate_cpf("000.000.000-00")


def test_validate_cpf_fail():
    assert client.validate_cpf('00000000000') is False


def test_validate_phone_ok_1():
    assert client.validate_phone("(84) 12345 1234")


def test_validate_phone_ok_2():
    assert client.validate_phone("84 12345 1234")


def test_validate_phone_ok_3():
    assert client.validate_phone("84-12345-1234")


def test_validate_phone_fail():
    assert client.validate_phone('9999') is False


def test_validate_email_ok():
    assert client.validate_email("teste@gmail.com")


def test_validate_email_fail():
    assert client.validate_email('testegmail.com') is False
