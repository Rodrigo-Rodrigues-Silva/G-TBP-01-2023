import datetime
from pydantic import BaseModel, Field
from models.pydanticObjectId import PydanticObjectId

from pydantic import BaseModel


class Booking(BaseModel):
    id: PydanticObjectId | None = Field(alias='_id')
    id_client: str
    check_in: datetime.datetime | None
    check_out: datetime.datetime | None
    id_room: str
    start_date: datetime.datetime
    final_date: datetime.datetime
    note: bool
    confirm: bool

    class Config:
        schema_extra = {
            "example": {
                "_id": "6449af1fc1869be6429dd8e7",
                "id_client": "6449d20ce7475e6200d028fc",
                "check_in": "2023-04-26T23:24:45.480+00:00",
                "check_out": "2023-04-30T23:24:45.480+00:00",
                "id_room": "64495a3477d59781a12e0f96",
                "start_date": "2023-04-26T23:24:45.480+00:00",
                "final_date": "2023-04-30T23:24:45.480+00:00",
                "note": True,
                "confirm": True
            }
        }


class BookingCreate(BaseModel):
    id_client: str
    id_room: str
    start_date: datetime.datetime
    final_date: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "id_client": "6449d20ce7475e6200d028fc",
                "id_room": "64495a3477d59781a12e0f96",
                "start_date": "2023-04-26T23:24:45.480+00:00",
                "final_date": "2023-04-30T23:24:45.480+00:00"
            }
        }


class BookingUpdateDate(BaseModel):
    start_date: datetime.datetime
    final_date: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "start_date": "2023-04-26T23:24:45.480+00:00",
                "final_date": "2023-04-30T23:24:45.480+00:00",
            }
        }
