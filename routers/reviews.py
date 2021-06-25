from fastapi import Depends, APIRouter
from utils.security import check_jwt_token
from utils.redis import is_redis_test_mode
from utils.db_functions import get_entities, insert_entity, delete_entity
from utils.const import configure_404_message, configure_insert_message, configure_delete_message
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from models.review import Review

router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)],
    prefix="/reviews"
)


@router.get("")
async def get_bottle_reviews(bottle_id: int):
    results = await get_entities("reviews", "*", {"bottle_id": bottle_id})


@router.get("/score")
async def get_average_review_score(bottle_id: int):
    results = await get_entities("reviews", "rating", {"bottle_id": bottle_id})

    if results:
        total = 0
        for rating in results:
            total += rating['rating']

        average = total / len(results)

        return average

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("reviews"))


@router.post("")
async def create_review(review: Review):
    await insert_entity("reviews", review)

    return {
        "detail": configure_insert_message("review"),
        "review": review
    }


@router.delete("/{id}")
async def delete_review(id: int):
    await delete_entity("reviews", {"id": id})

    return configure_delete_message("review")