from models.user import User
from enums.roles import RoleEnum

user1 = {
    "role": RoleEnum.ADMIN,
    "username": "frankdev95",
    "email_address": "frankdev95@protonmail.com",
    "password": "8v7w_c.'vZ;et8c-"
}
user2 = {
    "username": "johnbass25",
    "email_address": "johnny123@gmail.com",
    "password": "wkAdr6Z.DA&Y^eRJ"
}
user3 = {
    "username": "whiskylover87",
    "email_address": "rosielockett95@hotmail.co.uk",
    "password": "Q=T(P26DCrr#g6Ab"
}
user4 = {
    "username": "bourbondrinker20",
    "email_address": "jennysmith32@gmail.co.uk",
    "password": "4sHKy*dYRmL[$L6X"
}
user5 = {
    "username": "daveeast95",
    "email_address": "daveeaston95@hotmail.com",
    "password": "4acgxyrTF*3H[s}p"
}

users = [User(**user1), User(**user2), User(**user3), User(**user4), User(**user5)]
