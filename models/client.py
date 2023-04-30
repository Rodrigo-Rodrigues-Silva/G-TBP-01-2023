from pydantic import BaseModel, Field
from models.pydanticObjectId import PydanticObjectId


class Client(BaseModel):
    id: PydanticObjectId | None = Field(alias='_id')
    name: str
    last_name: str
    cpf: str
    phone: str
    e_mail: str
    credit: float

    class Config:
        schema_extra = {
            "example": {
                "_id": "6449d20ce7475e6200d028fc",
                "name": "Arnold",
                "last_name": "Schwarzenegger Silva",
                "cpf": "062.040.533-01",
                "phone": "(84) 88217 6852",
                "e_mail": "test@gamil.com",
                "credit": 100.00,
            }
        }


class ClientCreate(BaseModel):
    name: str
    last_name: str
    cpf: str
    phone: str
    e_mail: str
    credit: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Arnold",
                "last_name": "Schwarzenegger Silva",
                "cpf": "062.040.533-01",
                "phone": "(84) 88217 6852",
                "e_mail": "test@gamil.com",
                "credit": 100.00,
            }
        }


class ClientUpdateCredit(BaseModel):
    credit: float

    class Config:
        schema_extra = {
            "example": {
                "credit": 100.00,
            }
        }
