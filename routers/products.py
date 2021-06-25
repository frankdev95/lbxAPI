from fastapi import APIRouter, Depends
from models.product import Product
from utils.security import check_jwt_token
from utils.db_functions import get_entity, insert_entity, delete_entity
from utils.const import configure_404_message, configure_delete_message, configure_insert_message
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
import utils.redis as re
from utils.redis import is_redis_test_mode

router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)]
)


@router.get("/product/{id}", summary="Get product from id", response_description="The queried product", status_code=HTTP_200_OK)
async def get_product_by_id(id: int):
    redis_key = f"{id}"
    result = await re.redis.get(redis_key)
    storage_source = ""

    if result:
        product = result
        storage_source = "redis"
    else:
        product = await get_entity("products", "*", {"id": id})
        if product:
            re.redis.set(redis_key, str(product), expire=1800)
            storage_source = "db"

    if product:
        return {"source": storage_source, "product" : product}

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("product"))


@router.post("/product", status_code=HTTP_201_CREATED)
async def create_product(product: Product):
    await insert_entity("products", product)
    return {
        "detail": configure_insert_message("product"),
        "product": product
    }


@router.delete("/product/{id}", status_code=HTTP_200_OK)
async def delete_product(id: int):
    await delete_entity("products", {"id": id})
    raise HTTPException(status_code=HTTP_200_OK, detail=configure_delete_message("product"))