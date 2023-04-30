import datetime
import pytest
from fastapi import HTTPException
from validations import booking
from models.booking import BookingCreate, BookingUpdateDate


def test_check_booking_error_404():
    data = datetime.datetime.today()
    new_booking = BookingCreate(
        id_client="64495a7f91bc67b0fcc39675",
        id_room="",
        check_in=None,
        check_out=None,
        start_date=data,
        final_date=data,
        note=False,
        confirm=False)
    with pytest.raises(HTTPException) as error:
        booking.check_booking(new_booking)
    assert error.value.status_code == 422


def test_check_booking_error_422_full():
    data = datetime.datetime.today()
    new_booking = BookingCreate(
        id_client="",
        id_room="",
        check_in=None,
        check_out=None,
        start_date=data,
        final_date=data,
        note=False,
        confirm=False)
    with pytest.raises(HTTPException) as error:
        booking.check_booking(new_booking)
    assert error.value.status_code == 422


def test_check_dates_error_422_full():
    data = datetime.datetime.today()
    new_booking_dates = BookingUpdateDate(start_date=data, final_date=data)
    with pytest.raises(HTTPException) as error:
        booking.check_dates(new_booking_dates)
    assert error.value.status_code == 404


def test_check_id_error_422():
    with pytest.raises(HTTPException) as error:
        booking.check_id("", "test")
    assert error.value.status_code == 404
    assert error.value.detail == {"loc": ['test'],
                                  "msg": ["test is not valid"],
                                  "type": "value_error"}


def test_check_if_exists_error_422():
    with pytest.raises(HTTPException) as error:
        booking.check_if_exists("64495a7f91bc67b0fcc39675")
    assert error.value.status_code == 404
    assert error.value.detail == "Not found"


def test_validate_object_id_ok():
    assert booking.validate_object_id("64495a3477d59781a12e0f96")


def test_validate_object_id_fail():
    assert booking.validate_object_id("") is False
