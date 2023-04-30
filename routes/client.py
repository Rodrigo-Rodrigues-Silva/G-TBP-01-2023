from fastapi import APIRouter, HTTPException
from config.database import client_collection, booking_collection
from models.client import Client, ClientCreate, ClientUpdateCredit
from validations.client import *
from utils.util import error_detail
from bson.objectid import ObjectId

router = APIRouter(prefix='/clients', tags=['clients'])


@router.get('/', response_model=list[Client])
async def client_list():
    return list(client_collection.find())


@router.get('/cpf/{cpf}', response_model=Client, responses={404: {"description": "Not found"}})
async def get_one(cpf: str):
    if not validate_cpf(cpf):
        raise HTTPException(status_code=422, detail=error_detail(["cpf"], ["cpf must to be on format 000.000.000-00"]))
    client = client_collection.find_one({"cpf": cpf})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post('/', response_model=Client, responses={409: {"description": "already exists"}})
async def new_client(client: ClientCreate):
    check_client(client)
    result = client_collection.find_one({"cpf": client.cpf})
    if result:
        raise HTTPException(status_code=409, detail="Client already exists")
    client_collection.insert_one(dict(client))
    return client_collection.find_one({"cpf": client.cpf})


@router.put('/', response_model=Client, responses={404: {"description": "Not found"}})
async def update_one(client: ClientCreate):
    check_client(client)
    result = client_collection.find_one({"cpf": client.cpf})
    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    client_collection.find_one_and_update({"_id": result["_id"]}, {"$set": dict(client)})
    return client_collection.find_one({"cpf": client.cpf})


@router.put('/cpf/{cpf}', response_model=Client, responses={404: {"description": "Not found"}})
async def add_credit(cpf: str, client: ClientUpdateCredit):
    if not validate_cpf(cpf):
        raise HTTPException(status_code=422, detail=error_detail(["cpf"], ["cpf must to be on format 000.000.000-00"]))
    result = client_collection.find_one({"cpf": cpf})
    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    client.credit += result["credit"]
    client_collection.find_one_and_update({"_id": result["_id"]}, {"$set": dict(client)})
    return client_collection.find_one({"cpf": cpf})


@router.delete('/{id_client}')
async def delete(id_client: str):
    booking = booking_collection.find_one({"id_client": id_client})
    if booking:
        raise HTTPException(status_code=422,
                            detail="Client has a reservation, delete the reservation before deleting the client.")
    client_collection.delete_one({"_id": ObjectId(id_client)})
