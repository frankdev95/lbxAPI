from typing import List, Dict
from fastapi import APIRouter, Depends, File, Response
from models.user import User
from models.basic_user import BasicUser
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from utils.security import check_jwt_token, get_hashed_password, authenticate_user
from utils.const import configure_404_message
from utils.db_functions import insert_entity, get_entity, get_entities, update_entity, is_admin, delete_entity
from utils.helper_functions import upload_image_to_server
from utils.redis import is_redis_test_mode
import utils.redis as re
import pickle


router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)]
)


@router.get("/user/{username}", summary="Get user from username", response_description="The queried user",
            status_code=HTTP_200_OK)
async def get_user_by_username(username: str):
    """
    Return a **user** and all relevant information

    Query a **user** by **username**, and if **user** exists return all relevant information regarding the **user**.
    """
    redis_key = f"{username}"
    user = await re.redis.get(redis_key)

    if user:
        user = pickle.loads(user)
    else:
        user = await get_entity("users", "*", {"username": username})
        if user:
            re.redis.set(redis_key, pickle.dumps(user), expire=1800)
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user"))

    return {"user": user}


@router.get("/users", response_model=List[User], response_model_exclude={"password"}, status_code=HTTP_200_OK)
async def get_users():
    users = await get_entities("users", "*")

    if users:
        return users

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user"))


@router.post("/user/validate")
async def validate_user(user: BasicUser):
    redis_key = f"{user.username},{user.password}"
    result = await re.redis.get(redis_key)

    if result:
        user = result
        detail = "redis"
    else:
        user = await authenticate_user(user)
        detail = "db"
        await re.redis.set(redis_key, str(user))

    if user is not None:
        return {"detail": detail, "user": user}

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


@router.post("/user", summary="Create new user", response_description="The created user", status_code=HTTP_201_CREATED)
async def create_user(user: User):
    """
    Create a new **user** and return created user

    Receive the new **user** credentials via the request and create **user** with the received data, if successful
    return newly created user
    """
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    user_id = await insert_entity("users", user)

    return {
        "user_id": user_id,
        "user": user,
        "detail": "successfully created user"
    }


@router.post("/user/photo")
async def upload_user_photo(response: Response, photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(photo))
    r = await upload_image_to_server(photo)
    return r


@router.patch("/user", status_code=HTTP_200_OK)
async def patch_user(values: Dict):
    query = await update_entity("users", values["fields"], values["params"])
    return {"result": "User successfully updated"}


@router.delete("/user/{username}/{id}", status_code=HTTP_200_OK)
async def delete_user(id: int, role=Depends(is_admin)):
    query = await delete_entity("users", {"id": id})
    return {"detail": "User record successfully deleted"}
