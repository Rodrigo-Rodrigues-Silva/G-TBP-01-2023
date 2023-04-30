import pytest
import requests

url_base = 'http://127.0.0.1:8000/rooms'


def test_room_post():
    new_room = {
        "number": "Quarto Teste 33",
        "cost": 120.00
    }
    x = requests.post(url_base, json=new_room)
    requests.delete(url_base + '/' + x.json()["_id"])
    assert x.status_code == 200


def test_room_post_error_409():
    room = requests.post(url_base, json={
        "number": "Quarto Teste 34",
        "cost": 120.00
    })
    x = requests.post(url_base, json={
        "number": "Quarto Teste 34",
        "cost": 120.00
    })
    requests.delete(url_base + '/' + room.json()["_id"])
    assert x.status_code == 409


def test_room_get():
    x = requests.get(url_base)
    assert x.status_code == 200


def test_room_put():
    new_room = {
        "number": "Quarto Teste 35",
        "cost": 120.00
    }
    x = requests.put(url_base, json=new_room)
    assert x.status_code == 404
