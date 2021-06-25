from fastapi import FastAPI, Depends
from starlette.requests import Request
from datetime import datetime
from routers import users, auth, customers, products, bottles, portfolio, reviews, population, distilllers
from utils.db import db
from utils.const import REDIS_URL, testing
import utils.redis as re
import aioredis

tags_metadata = [
    {
        "name": "authentication",
        "description": "Manages API **authentication** procedures such as JSON Web Token creation."
    },
    {
        "name": "users",
        "description": "Operations regarding users. The **login** and **registration** logic can be found here."
    },
]

app = FastAPI(
    title="LBX RestAPI Documentation",
    description="Manages and facilitates data requests and responses from the LBX mobile app to the database.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(bottles.router)
app.include_router(portfolio.router)
app.include_router(reviews.router)
app.include_router(population.router)
app.include_router(distilllers.router)


@app.on_event("startup")
async def connect_db():
    if not testing:
        await db.connect()
        re.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")
async def disconnect_db():
    if not testing:
        await db.disconnect()
        re.redis.close()
        await re.redis.wait_close()


# Calculate the server response time in microseconds and send information back via custom header
@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
