from bson import ObjectId
from utils.util import error_detail
from models.booking import BookingCreate, BookingUpdateDate, Booking
from fastapi import HTTPException
from config.database import booking_collection, client_collection, room_collection
import datetime


def validate_object_id(object_id: str):
    return ObjectId.is_valid(object_id)


def check_if_exists(id_booking: str) -> Booking:
    reserve = booking_collection.find_one({"_id": ObjectId(id_booking)})
    if not reserve:
        raise HTTPException(status_code=404, detail="Not found")
    return reserve


def check_id(value: str, name_field: str):
    if not validate_object_id(value):
        raise HTTPException(status_code=404, detail=error_detail([name_field], [f"{name_field} is not valid"]))


def check_dates(booking: BookingUpdateDate):
    errors = []
    msgs = []
    if booking.start_date >= booking.final_date:
        errors.append("start_date")
        msgs.append("start_date must be less than final_date")
    if booking.start_date.date() < datetime.datetime.now().date():
        errors.append("start_date")
        msgs.append("start_date must be equal or greater than today's date")
    if len(errors):
        raise HTTPException(status_code=404, detail=error_detail(errors, msgs))


def check_booking(booking: BookingCreate):
    errors = []
    msgs = []
    if not validate_object_id(booking.id_client):
        errors.append("id_client")
        msgs.append("id_client is not valid")
    if not validate_object_id(booking.id_room):
        errors.append("msg")
        msgs.append("id_room is not valid")
    if len(errors):
        raise HTTPException(status_code=422, detail=error_detail(errors, msgs))
    check_dates(booking)
