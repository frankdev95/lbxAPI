from typing import Optional
from fastapi import Body
from pydantic import BaseModel
from enums.roles import RoleEnum


class BasicUser(BaseModel):
    username: str
    password: Optional[str] = Body(None)
    disabled: bool = False
    role: RoleEnum = RoleEnum.PERSONNEL
