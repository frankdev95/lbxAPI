import requests
from utils.const import IMAGEBB_URL
from utils.db_functions import get_entities_by_pattern, get_entities
from utils.const import configure_404_message
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
import pickle
import utils.redis as re


async def upload_image_to_server(file):
    r = requests.post(IMAGEBB_URL, files={"image": file})
    return r.json()


async def configure_whisky_price_data(redis_key, table, field=None, column=None):
    distillers = await re.redis.get(redis_key)

    if distillers:
        distillers = pickle.loads(distillers)
    else:
        if column:
            distillers = await get_entities(table, "*", {column: field})
        else:
            distillers = await get_entities(table, "*")

        if distillers:
            re.redis.set(redis_key, pickle.dumps(distillers), expire=1800)
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("distillers"))

    return distillers
