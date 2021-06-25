from fastapi import Depends
from passlib.context import CryptContext
from models.basic_user import BasicUser
from enums.roles import RoleEnum
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_SECONDS, JWT_SECRET_KEY, JWT_ALGORITHM, UNAUTHORIZED
from fastapi.security import OAuth2PasswordBearer
from utils.db_functions import get_entity, is_admin
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt

pwd_context = CryptContext(schemes=["sha256_crypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


# Hash the received password using the hashing algorithm specified
def get_hashed_password(password):
    return pwd_context.hash(password)


# Verify a users password by comparing it to the hashed password
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        return False


user_admin = BasicUser(**{
    "username": "frankadmin",
    "password": get_hashed_password("password"),
    "disabled": False,
    "role": RoleEnum.ADMIN
})

jwt_user = BasicUser(**{
    "username": "frankadmin",
    "password": "password"
})


# Authenticate user
async def authenticate_user(user: BasicUser):

    if await is_admin(user.username):
        user.role = RoleEnum.ADMIN
    else:
        user.role = RoleEnum.PERSONNEL

    password = await get_entity("users", "password", {"username": user.username})

    if password is not None:
        if verify_password(user.password, password["password"]):
            return user

    return None


# Create JWT token based on credentials given
def create_jwt_token(user: BasicUser):
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(seconds=JWT_EXPIRATION_TIME_SECONDS)
    }
    return jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Check the validity of the JWT token
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration_date = datetime.fromtimestamp(jwt_payload.get("exp"))

        if datetime.now() < expiration_date:
            if await get_entity("users", "id", {"username": username}):
                return final_authorisation(role)

    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


def final_authorisation(role):
    if role == RoleEnum.ADMIN:
        return True
    return False
