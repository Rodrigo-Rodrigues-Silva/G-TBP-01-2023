import datetime
from fastapi import APIRouter, HTTPException, File, UploadFile
from config.database import booking_collection, client_collection, room_collection
from models.booking import Booking, BookingCreate, BookingUpdateDate
from models.client import Client
from models.room import Room
from utils.util import error_detail, format_currency
from validations.booking import check_booking, check_id, check_if_exists, check_dates
from bson.objectid import ObjectId
from pathlib import Path
from fpdf import FPDF
from fastapi.responses import FileResponse

router = APIRouter(prefix='/bookings', tags=['bookings'])


@router.get('/', response_model=list[Booking])
async def booking_list():
    return list(booking_collection.find())


@router.get('/id_client/{id_client}', response_model=list[Booking])
async def get_bookings_for_clients(id_client: str):
    check_id(id_client, "id_client")
    return list(booking_collection.find({"id_client": id_client}))


@router.get('/id_room/{id_room}', response_model=list[Booking])
async def get_bookings_for_room(id_room: str):
    check_id(id_room, "id_room")
    return list(booking_collection.find({"id_room": id_room}))


@router.post('/', response_model=Booking,
             responses={404: {"description": "Not found"}, 409: {"description": "already exists"}})
async def new_booking(booking: BookingCreate):
    check_booking(booking)
    client_exists(booking.id_client)
    room_exists(booking.id_room)
    check_conflit_date(booking.dict())
    new = dict(booking) | {"check_in": None, "check_out": None, "note": False, "confirm": False}
    result = booking_collection.insert_one(new)
    return booking_collection.find_one({"_id": result.inserted_id})


@router.put('/{id_booking}/dates', response_model=Booking, responses={404: {"description": "Not found"}})
async def update_dates(id_booking: str, booking: BookingUpdateDate):
    check_id(id_booking, "id_booking")
    reserve = check_if_exists(id_booking)
    if reserve["note"]:
        raise HTTPException(status_code=422, detail=error_detail(["note"], ["note has already been sent"]))
    check_dates(booking)
    reserve["start_date"] = booking.start_date
    reserve["final_date"] = booking.final_date
    check_conflit_date(reserve)
    booking_collection.find_one_and_update({"_id": ObjectId(id_booking)},
                                           {"$set": dict(booking)})
    return booking_collection.find_one({"_id": ObjectId(id_booking)})


@router.post("/upload/{id}", response_model=Booking,
             responses={500: {"description": "There was an error uploading the file"}})
def upload(id_booking: str, file: UploadFile = File(...)):
    check_id(id_booking, "id_booking")
    reserve = booking_collection.find_one({"_id": ObjectId(id_booking)})
    check_if_exists(id_booking)
    try:
        ext = Path(file.filename).suffix
        contents = file.file.read()
        with open(f'files\\{reserve["_id"]}{ext}', 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="There was an error uploading the file")
    finally:
        file.file.close()
    booking_collection.find_one_and_update({"_id": ObjectId(id_booking)},
                                           {"$set": {"note": True}})
    return booking_collection.find_one({"_id": ObjectId(id_booking)})


@router.put("/confirm/{id}", response_model=Booking)
async def confirm(id_booking: str):
    check_id(id_booking, "id_booking")
    reserve = check_if_exists(id_booking)
    if not reserve["note"]:
        raise HTTPException(status_code=422,
                            detail={"loc": ["note"], "msg": "note was not sent", "type": "value_error"})
    client = client_collection.find_one({"_id": ObjectId(reserve["id_client"])})
    room = room_collection.find_one({"_id": ObjectId(reserve["id_room"])})
    create_pdf(reserve, client, room)
    booking_collection.find_one_and_update({"_id": ObjectId(id_booking)},
                                           {"$set": {"confirm": True}})
    return booking_collection.find_one({"_id": ObjectId(id_booking)})


@router.get("/download/{id}")
async def download(id_booking: str):
    check_id(id_booking, "id_booking")
    reserve = check_if_exists(id_booking)
    if not reserve["confirm"]:
        raise HTTPException(status_code=422, detail="no pdf created")
    file_path = f"pdfs\\{reserve['_id']}.pdf"
    file_name = f"{reserve['_id']}.pdf"

    return FileResponse(path=file_path, filename=file_name, media_type='application/pdf')


@router.put('/checkin/{id}', response_model=Booking)
async def checkin(id_booking: str):
    check_id(id_booking, "id_booking")
    reserve = check_if_exists(id_booking)
    if reserve["check_in"]:
        raise HTTPException(status_code=422,
                            detail={"loc": ["check_in"], "msg": "checkin has already been carried out",
                                    "type": "value_error"})
    room = room_collection.find_one({"_id": ObjectId(reserve["id_room"])})
    number_days = (reserve["final_date"] - reserve["start_date"]).days
    client = client_collection.find_one({"_id": ObjectId(reserve["id_client"])})
    balance = client["credit"] - room["cost"] * number_days
    booking_collection.find_one_and_update({"_id": ObjectId(id_booking)},
                                           {"$set": {"check_in": datetime.datetime.now()}})
    client_collection.find_one_and_update({"_id": ObjectId(reserve["id_client"])},
                                          {"$set": {"credit": balance}})
    return booking_collection.find_one({"_id": ObjectId(id_booking)})


@router.put('/checkout/{id}', response_model=Booking)
async def checkout(id_booking: str):
    check_id(id_booking, "id_booking")
    reserve = check_if_exists(id_booking)
    if not reserve["check_in"]:
        raise HTTPException(status_code=422,
                            detail={"loc": ["check_in"], "msg": "checkin was not done",
                                    "type": "value_error"})
    if reserve["check_out"]:
        raise HTTPException(status_code=422,
                            detail={"loc": ["check_in"], "msg": "check_out has already been carried out",
                                    "type": "value_error"})
    booking_collection.find_one_and_update({"_id": ObjectId(id_booking)},
                                           {"$set": {"check_out": datetime.datetime.now()}})
    return booking_collection.find_one({"_id": ObjectId(id_booking)})


@router.delete('/{id_booking}')
async def delete(id_booking: str):
    booking_collection.delete_one({"_id": ObjectId(id_booking)})


def client_exists(client_id: str):
    client = client_collection.find_one({"_id": ObjectId(client_id)})
    if not client:
        raise HTTPException(status_code=404, detail=error_detail(["id_client"], ["client not found"]))


def room_exists(room_id: str):
    room = room_collection.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail=error_detail(["id_room"], ["room not found"]))


def check_conflit_date(booking: Booking | BookingCreate):
    if "_id" in booking:
        another_reserve = booking_collection.find_one(
            {
                "_id": {"$ne": ObjectId(booking['_id'])},
                "id_room": booking['id_room'],
                "$or": [{"$and": [{"final_date": {"$gte": booking['start_date']}},
                                  {"start_date": {"$lte": booking['start_date']}}]},
                        {"$and": [{"final_date": {"$gte": booking['final_date']}},
                                  {"start_date": {"$lte": booking['final_date']}}]}],
            })
    else:
        another_reserve = booking_collection.find_one(
            {
                "id_room": booking['id_room'],
                "$or": [{"$and": [{"final_date": {"$gte": booking['start_date']}},
                                  {"start_date": {"$lte": booking['start_date']}}]},
                        {"$and": [{"final_date": {"$gte": booking['final_date']}},
                                  {"start_date": {"$lte": booking['final_date']}}]}],
            })
    if another_reserve:
        text = f"Date is reserved for {another_reserve['start_date']} to {another_reserve['final_date']}"
        raise HTTPException(status_code=409, detail=text)


def create_pdf(booking: Booking, client: Client, room: Room):
    pdf = FPDF()
    pdf.add_page()
    number_days = (booking["final_date"] - booking["start_date"]).days

    pdf.set_font("Helvetica", size=13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Client Information", ln=1, align="C")
    pdf.cell(0, 10, txt=f'Name: {client["name"]} {client["last_name"]}', ln=1, align="L")
    pdf.cell(0, 10, txt='Contats', ln=1, align="L")
    pdf.cell(0, 10, txt=f'Phone: {client["phone"]}', ln=1, align="L")
    if client["e_mail"] is not None:
        pdf.cell(0, 10, txt=f'E-mail: {client["e_mail"]}', ln=1, align="L")
    pdf.cell(0, 10, txt='', ln=1, align="L")
    pdf.cell(200, 10, txt="Reserve Information", ln=1, align="C")
    pdf.cell(0, 10, txt=f'Room: {room["number"]}', ln=1, align="L")
    pdf.cell(0, 10, txt=f'Date for checkin: {booking["start_date"]}', ln=1, align="L")
    pdf.cell(0, 10, txt=f'Number of Days: {number_days}', ln=1, align="L")
    pdf.cell(0, 10, txt=f'Total cost: {format_currency(number_days * room["cost"])}', ln=1, align="L")
    pdf.output(f"pdfs\\{booking['_id']}.pdf")
