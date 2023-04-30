import pytest
import requests

url_base = 'http://127.0.0.1:8000/clients'


def test_client_post():
    new_client = {
        "name": "teste",
        "last_name": "python",
        "cpf": "999.999.999-99",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    x = requests.post(url_base, json=new_client)
    requests.delete(url_base + '/' + x.json()["_id"])
    assert x.status_code == 200


def test_client_post_error_409():
    client = requests.post(url_base, json={
        "name": "teste",
        "last_name": "java",
        "cpf": "999.999.999-88",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    })
    x = requests.post(url_base, json={
        "name": "teste",
        "last_name": "java",
        "cpf": "999.999.999-88",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    })
    requests.delete(url_base + '/' + client.json()["_id"])
    assert x.status_code == 409


def test_client_get():
    x = requests.get(url_base)
    assert x.status_code == 200


def test_client_put_404():
    new_client = {
        "name": "teste245",
        "last_name": "ruby",
        "cpf": "123.999.999-99",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    x = requests.put(url_base, json=new_client)
    assert x.status_code == 404


def test_client_put_from_cpf_422():
    new_client = {
        "name": "teste",
        "last_name": "ruby",
        "cpf": "111.111.222-66",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    x = requests.put(url_base + f'/cpf/aaa', json=new_client)
    assert x.status_code == 422


def test_client_put_from_cpf_404():
    new_client = {
        "name": "teste",
        "last_name": "ruby",
        "cpf": "111.111.222-66",
        "phone": "00 99999 8888",
        "e_mail": "aaaa@aaaa.aaaa",
        "credit": 100
    }
    x = requests.put(url_base + f'/cpf/111.111.222-66', json=new_client)
    assert x.status_code == 404


def test_client_get_from_cpf_404():
    x = requests.get(url_base + f'/cpf/111.111.222-66')
    assert x.status_code == 404


def test_client_get_from_cpf_422():
    x = requests.get(url_base + f'/cpf/aa')
    assert x.status_code == 422


def test_add_credit_404():
    new_client = {
        "credit": 100
    }
    x = requests.put(url_base + f'/cpf/111.111.222-66', json=new_client)
    assert x.status_code == 404
