from fastapi import APIRouter, Depends
from utils.security import check_jwt_token
from utils.db_functions import insert_entity, get_entity, get_entities
from utils.const import configure_insert_message, configure_404_message
from models.bottle import Bottle
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import utils.redis as re
from utils.redis import is_redis_test_mode

router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)]
)


@router.get("/bottles")
async def get_bottles():
    bottles = await get_entities("bottles", "*")

    if bottles:
        return bottles

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("bottles"))


@router.get("/bottle/{id}")
async def get_bottle(id: int):
    redis_key = f"{id}"
    result = await re.redis.get(redis_key)
    storage_source = ""

    if result:
        bottle = result
        storage_source = "redis"
    else:
        bottle = await get_entity("bottles", "*", {"id": id})
        if bottle is not None:
            re.redis.set(redis_key, str(bottle), expire=1800)
            storage_source = "db"

    if bottle:
        return {"source": storage_source, "bottle": bottle}

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("bottle"))


@router.post("/bottle", status_code=HTTP_201_CREATED)
async def create_bottle(bottle: Bottle):
    await insert_entity("bottles", bottle)
    return {
        "detail": configure_insert_message("bottle"),
        "bottle": bottle
    }


