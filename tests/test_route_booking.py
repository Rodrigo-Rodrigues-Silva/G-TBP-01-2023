from datetime import datetime, timedelta
import requests

url_base = 'http://127.0.0.1:8000/bookings'
url_client = 'http://127.0.0.1:8000/clients'
url_room = 'http://127.0.0.1:8000/rooms'


def test_booking_get():
    x = requests.get(url_base)
    assert x.status_code == 200


def test_booking_get_from_client():
    x = requests.get(url_base + '/id_client/64495a7f91bc67b0fcc39675')
    assert x.status_code == 200


def test_booking_get_from_room():
    x = requests.get(url_base + '/id_room/64495a7f91bc67b0fcc39675')
    assert x.status_code == 200


def test_booking_post():
    new_client = {
        "name": "teste",
        "last_name": "python2",
        "cpf": "199.999.999-99",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    client = requests.post(url_client, json=new_client)
    new_room = {
        "number": "Quarto Teste 36",
        "cost": 120.00
    }
    room = requests.post(url_room, json=new_room)
    date_start = (datetime.now() + timedelta(days=1)).isoformat()
    date_end = (datetime.now() + timedelta(days=3)).isoformat()
    new_booking = {
        "id_client": client.json()["_id"],
        "id_room": room.json()["_id"],
        "start_date": date_start,
        "final_date": date_end
    }
    booking = requests.post(url_base, json=new_booking)
    requests.delete(url_base + '/' + booking.json()["_id"])
    requests.delete(url_room + '/' + room.json()["_id"])
    requests.delete(url_client + '/' + client.json()["_id"])
    assert booking.status_code == 200


def test_booking_update_dates():
    new_client = {
        "name": "teste",
        "last_name": "python2",
        "cpf": "299.999.999-99",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    client = requests.post(url_client, json=new_client)
    new_room = {
        "number": "Quarto Teste 37",
        "cost": 120.00
    }
    room = requests.post(url_room, json=new_room)
    date_start = (datetime.now() + timedelta(days=1)).isoformat()
    date_end = (datetime.now() + timedelta(days=3)).isoformat()
    new_booking = {
        "id_client": client.json()["_id"],
        "id_room": room.json()["_id"],
        "start_date": date_start,
        "final_date": date_end
    }
    booking = requests.post(url_base, json=new_booking)
    date_end = (datetime.now() + timedelta(days=10)).isoformat()
    change = {
        "start_date": date_start,
        "final_date": date_end
    }
    update_dates = requests.put(url_base + '/' + booking.json()["_id"] + '/dates', json=change)
    requests.delete(url_base + '/' + booking.json()["_id"])
    requests.delete(url_room + '/' + room.json()["_id"])
    requests.delete(url_client + '/' + client.json()["_id"])
    assert update_dates.status_code == 200
