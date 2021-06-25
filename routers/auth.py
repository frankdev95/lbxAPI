from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.basic_user import BasicUser
from models.user import User
from utils.security import authenticate_user, create_jwt_token, get_hashed_password as get_password
from utils.db_functions import get_entity, insert_entity
from utils.const import UNAUTHORIZED, JWT_EXPIRATION_TIME_SECONDS, configure_404_message
import utils.redis as re
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from starlette.exceptions import HTTPException
import pickle

router = APIRouter(
    tags=["authentication"]
)


@router.post("/token", summary="Authenticate user and create JWT", response_description="The created JWT")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Create a **JWT** if user is authenticated

    Authenticate the user using the received form data, and if successful create and return the JWT.
    """
    redis_key = f"{form_data.username},{form_data.password}"
    user = await re.redis.get(redis_key)

    if not user:
        basic_user = BasicUser(**{
            "username": form_data.username,
            "password": form_data.password
        })

        user = await authenticate_user(basic_user)

        if user:
            re.redis.set(redis_key, pickle.dumps(user), expire=1800)
    else:
        user = pickle.loads(user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@router.post("/signin", status_code=HTTP_200_OK)
async def login_user(credentials: BasicUser):
    redis_key = f"signin {credentials.username},{credentials.password}"
    user = await re.redis.get(redis_key)

    if user:
        user = pickle.loads(user)
    if not user:
        user = await get_entity("users", "*", {"username": credentials.username})
        if user:
            auth_user = await authenticate_user(credentials)
            if auth_user is None:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect password")

            re.redis.set(redis_key, pickle.dumps(user), expire=1800)
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user"))

    return {
        "token": create_jwt_token(credentials),
        "expires_in": JWT_EXPIRATION_TIME_SECONDS,
        "user": user
    }


@router.post("/signup", status_code=HTTP_201_CREATED)
async def register_new_user(user: User):
    if await get_entity("users", "*", {"username": user.username}):
        raise HTTPException(status_code=HTTP_409_CONFLICT)

    hashed_password = get_password(user.password)
    user.password = hashed_password

    user_id = await insert_entity("users", user)
    await insert_entity("portfolio", {"user_id": user_id})

    return {
        "detail": "Successfully created user"
    }


@router.get("/hash/{password}")
async def get_hashed_password(password: str):
    return get_password(password)

