from fastapi import APIRouter, HTTPException
from config.database import room_collection, booking_collection
from models.room import Room, RoomCreate
from validations.room import *
from bson.objectid import ObjectId

router = APIRouter(prefix='/rooms', tags=['rooms'])


@router.get('/', response_model=list[Room])
async def rooms_list():
    return list(room_collection.find())


@router.post('/', response_model=Room, responses={409: {"description": "already exists"}})
async def new_room(room: RoomCreate):
    check_room(room)
    result = room_collection.find_one({"number": room.number})
    if result:
        raise HTTPException(status_code=409, detail="Room already exists")
    room_collection.insert_one(dict(room))
    return room_collection.find_one({"number": room.number})


@router.put('/', response_model=Room, responses={404: {"description": "Not found"}})
async def update_one(room: RoomCreate):
    check_room(room)
    result = room_collection.find_one({"number": room.number})
    if not result:
        raise HTTPException(status_code=404, detail="Room not found")
    room_collection.find_one_and_update({"_id": result["_id"]}, {"$set": dict(room)})
    room = room_collection.find_one({"number": room.number})
    return room


@router.delete('/{id_room}')
async def delete(id_room: str):
    booking = booking_collection.find_one({"id_room": id_room})
    if booking:
        raise HTTPException(status_code=422,
                            detail="Client has a reservation, delete the reservation before deleting the client.")
    room_collection.delete_one({"_id": ObjectId(id_room)})
