from datetime import date
from enums.roles import RoleEnum
from utils.security import get_hashed_password

user = {
    "username": "test",
    "dob": date(2000, 1, 1),
    "email_address": "test@123.com",
    "password": get_hashed_password("test123"),
    "role": RoleEnum.ADMIN
}

post_user = {
    "username": "post_test",
    "dob": "2000-01-01",
    "email_address": "post_test@123.com",
    "password": "test123",
    "role": RoleEnum.ADMIN
}
