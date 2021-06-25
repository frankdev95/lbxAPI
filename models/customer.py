from pydantic import BaseModel
from models.basic_user import BasicUser


class Customer(BaseModel):
    user: BasicUser
    phone: str
    address: str