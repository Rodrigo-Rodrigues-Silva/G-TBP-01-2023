from pydantic import BaseModel, Field
from models.pydanticObjectId import PydanticObjectId


class Room(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    number: str
    cost: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "_id": "6449d20ce7475e6200d028fc",
                "number": "27A",
                "cost": 35.4,
            }
        }


class RoomCreate(BaseModel):
    number: str
    cost: float

    class Config:
        schema_extra = {
            "example": {
                "number": "27A",
                "cost": 35.4,
            }
        }
