from fastapi import APIRouter, Depends
from utils.security import check_jwt_token
from utils.db_functions import get_entities, get_entities_by_pattern, get_whisky_price_by_date_and_name
from utils.const import configure_404_message
from utils.helper_functions import configure_whisky_price_data
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
import utils.redis as re
import pickle

router = APIRouter(
    dependencies=[Depends(check_jwt_token)],
    prefix="/distillers"
)


@router.get("")
async def get_distillers():
    return await configure_whisky_price_data("distillers", "distillers")


@router.get("/name")
async def get_distillers_by_name(distiller: str):
    return await configure_whisky_price_data(f"distillers-{distiller}", "distillers", distiller, "index_name")


@router.get("/year")
async def get_distillers_by_month(year: str):
    redis_key = f"distillers-{year}"
    distillers = await re.redis.get(redis_key)

    if distillers:
        distillers = pickle.loads(distillers)
    else:
        distillers = await get_entities_by_pattern("distillers", "*", {"month": f"%{year}%"})

        if distillers:
            re.redis.set(redis_key, pickle.dumps(distillers), expire=1800)
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("distillers"))

    return distillers


@router.get("/{name}/{year}")
async def get_distillers_by_name_and_year(name: str, year: str):
    distillers = await get_whisky_price_by_date_and_name("distillers", "*", name, year)

    if distillers:
        return distillers

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("distillers"))