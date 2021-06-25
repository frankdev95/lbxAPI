from fastapi import APIRouter, Depends
from utils.security import check_jwt_token
from models.customer import Customer
from utils.db_functions import insert_entity, get_entity
from utils.const import configure_404_message
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from utils.redis import is_redis_test_mode


router = APIRouter(
    dependencies=[Depends(check_jwt_token), Depends(is_redis_test_mode)]
)


@router.get("/customer/{id}/user", summary="Get user related to customer",
            response_description="The user from the queried customer")
async def get_user_from_customer(id: int):
    customer = await get_entity("customers", "user_id", {"id": id})

    if customer:
        user_id = customer["user_id"]
        user = await get_entity("users", "*", {"id": user_id})
        return user

    return HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("customer"))


@router.post("/customer", summary="Create new customer", response_description="The created customer",
             status_code=HTTP_201_CREATED)
async def create_customer(customer: Customer):
    user = await get_entity("users", "id", {"username": customer.user.username})

    if user:
        user_id = user["id"]

        customer_obj = {
            "user_id": user_id,
            "phone": customer.phone,
            "address": customer.address
        }

        await insert_entity("customers", customer_obj)

        return customer

    return HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user"))

