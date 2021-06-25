from datetime import date
from typing import Optional
from fastapi import Query, Body
from pydantic import BaseModel
from enums.roles import RoleEnum


class User(BaseModel):
    role: RoleEnum = RoleEnum.PERSONNEL
    username: str
    first_name: Optional[str] = Body(None)
    last_name: Optional[str] = Body(None)
    dob: date = date(2001, 1, 1)
    email_address: str = Query(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$")
    password: str
    country: Optional[str] = Body(None)

