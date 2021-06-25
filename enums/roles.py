from enum import Enum
from pydantic import BaseModel


class RoleEnum(str, Enum):
    ADMIN = "admin"
    PERSONNEL = "personnel"
