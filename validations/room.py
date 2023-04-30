from utils.util import error_detail
from models.room import RoomCreate
from fastapi import HTTPException


def validate_number(number: str):
    return len(number.replace(' ', '')) > 0


def validate_cost(cost: float):
    return cost > 1


def check_room(room: RoomCreate):
    check_number(room.number)
    check_cost(room.cost)


def check_cost(cost: float):
    if not validate_cost(cost):
        raise HTTPException(status_code=422, detail=error_detail(["coast"], ["cost must to be greater than 1"]))


def check_number(number: str):
    if not validate_number(number):
        raise HTTPException(status_code=422, detail=error_detail(["number"], ["number cannot be empty"]))
