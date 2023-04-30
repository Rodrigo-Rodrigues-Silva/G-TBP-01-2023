import re
from utils.util import error_detail
from models.client import ClientCreate
from fastapi import HTTPException


def check_client(client: ClientCreate):
    check_name(client.name)
    check_last_name(client.last_name)
    check_cpf(client.cpf)
    check_phone(client.phone)
    check_e_mail(client.e_mail)


def check_name(name: str):
    if not validate_name(name):
        raise HTTPException(status_code=422,
                            detail=error_detail(["name"], ["name cannot be empty and must have 3 or more letters"]))


def check_last_name(last_name: str):
    if not validate_name(last_name):
        raise HTTPException(status_code=422,
                            detail=error_detail(["last_name"],
                                                ["last_name cannot be empty and must have 3 or more letters"]))


def check_cpf(cpf: str):
    if not validate_cpf(cpf):
        raise HTTPException(status_code=422, detail=error_detail(["cpf"], ["cpf must to be on format 000.000.000-00"]))


def check_phone(phone: str):
    if not validate_phone(phone):
        raise HTTPException(status_code=422,
                            detail=error_detail(["phone"], ["phone must to be on format (00) 00000 0000"]))


def check_e_mail(email: str):
    if not validate_email(email):
        raise HTTPException(status_code=422,
                            detail=error_detail(["e_mail"], ["e_mail must to be on format aaaa@bbbb.ccc"]))


def validate_name(name: str) -> bool:
    return len(name) > 3 and not name.isspace()


def validate_cpf(cpf: str) -> bool:
    return bool(re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf))


def validate_phone(phone: str) -> bool:
    return bool(re.search(r'\(?\d{2}\)?(\s|-)?\d{5}(\s|-)?\d{4}', phone))


def validate_email(email: str) -> bool:
    return bool(re.search(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+', email))
