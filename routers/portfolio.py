from fastapi import Depends, APIRouter
from utils.const import configure_404_message
from utils.security import check_jwt_token
from utils.db_functions import get_entity, get_entities, insert_entity, delete_entity, update_entity, \
    check_element_in_array, update_entity_array, get_portfolio_entities, delete_entity_array
from utils.redis import is_redis_test_mode
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_200_OK

router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)],
    prefix="/portfolio"
)


# PORTFOLIO

@router.get("", status_code=HTTP_200_OK)
async def get_portfolio_by_user_id(user_id: int):
    portfolio = await get_entity("portfolio", "*", {"user_id": user_id})

    if portfolio:
        return portfolio

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("portfolio"))


@router.get("/field")
async def get_portfolio_field(user_id: int, field: str):
    portfolio = await get_entity("portfolio", field, {"user_id": user_id})

    if portfolio:
        return portfolio

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message(field))


@router.post("/{user_id}", status_code=HTTP_201_CREATED)
async def create_portfolio(user_id: int):
    await insert_entity("portfolio", {"user_id": user_id})

    return {
        "detail": "portfolio successfully created"
    }


@router.get('/items')
async def get_portfolio_items(table: str, field: str, user_id: int):
    results = await get_portfolio_entities(table, field, user_id)

    if results:
        return results

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message(field))


async def add_portfolio_item(bottle_id: int, user_id: int, list: str):
    if await check_element_in_array("portfolio", {"user_id": user_id, "bottle_id": bottle_id}, list):
        raise HTTPException(status_code=HTTP_409_CONFLICT,
                            detail=f"The bottle with this id already belongs to this {list}")

    if await get_entity("user_bottles", "*", {"bottle_id": bottle_id}):
        await update_entity("user_bottles", {list: True}, {"bottle_id": bottle_id})
    else:
        await insert_entity("user_bottles", {"user_id": user_id, "bottle_id": bottle_id, list: True})

    await update_entity_array("portfolio", {"bottle_id": bottle_id}, {"user_id": user_id}, list)


# COLLECTION


@router.get('/collection/id')
async def get_collection_ids():
    collection = await get_entities("portfolio", "collection")

    if collection:
        return collection

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("collection"))


@router.post("/collection/", status_code=HTTP_201_CREATED)
async def add_to_collection(bottle_id: int, user_id: int,):
    await add_portfolio_item(bottle_id, user_id, 'collection')

    return {
        "detail": "whisky successfully added to collection"
    }


@router.delete("/collection/")
async def delete_collection_item(bottle_id: int, user_id: int):
    await delete_entity_array("portfolio", {"bottle_id": bottle_id}, {"user_id": user_id}, "collection")
    await update_entity("user_bottles", {"collection": False}, {"bottle_id": bottle_id})

    return {
        "detail": "collection item successfully deleted"
    }


# WISHLIST


@router.get("/wishlist")
async def get_wishlist():
    wishlist = await get_entities("portfolio", "wishlist")

    if wishlist:
        return wishlist

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("wishlist"))


@router.post("/wishlist/")
async def add_to_wishlist(bottle_id: int, user_id: int):
    await add_portfolio_item(bottle_id, user_id, 'wishlist')

    return {
        "detail": "whisky successfully added to wishlist"
    }


@router.delete("/wishlist/")
async def delete_wishlist_item(bottle_id: int, user_id: int):
    await delete_entity_array("portfolio", {"bottle_id": bottle_id}, {"user_id": user_id}, "wishlist")
    await update_entity("user_bottles", {"wishlist": False}, {"bottle_id": bottle_id})

    return {
        "detail": "collection item successfully deleted"
    }

# REVIEWS


@router.get("/review/score")


# USER BOTTLES


@router.get("/bottles")
async def get_user_bottles(bottle_id: int, user_id: int,):
    results = await get_entity("user_bottles", "*", {"user_id": user_id, "bottle_id": bottle_id})

    if results:
        return results

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user bottles"))