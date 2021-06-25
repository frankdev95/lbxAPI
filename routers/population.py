from fastapi import Depends, APIRouter
from utils.security import check_jwt_token
from utils.db_functions import insert_whisky_entities
import requests

router = APIRouter(
    dependencies=[Depends(check_jwt_token)],
    prefix="/populate"
)


@router.get("/token")
def get_token():
    payload = {'username': 'londonbarrelhouse', 'password': 'aLs*@#716led!'}
    r = requests.post('https://api.whiskybase.com/api/v1/auth/authorize', data=payload)
    return r.json()


@router.get("")
async def populate_database_group(index_group: str, table: str):
    params = {'index_group': index_group, 'perpage': 500}
    headers = {'Authorization':
                   'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjVkYzM4YWVjZWFiMzViY2M0YzJlZmQ5ODRjMjRlODZhMWQxZmQ4ZGQyMzJkODQ3MmJkZDI0M2EzODI1NzNlN2RjOTk1ODdkOTNlYzZlZGU3In0.eyJhdWQiOiIxIiwianRpIjoiNWRjMzhhZWNlYWIzNWJjYzRjMmVmZDk4NGMyNGU4NmExZDFmZDhkZDIzMmQ4NDcyYmRkMjQzYTM4MjU3M2U3ZGM5OTU4N2Q5M2VjNmVkZTciLCJpYXQiOjE2MjQ1MjIwNDYsIm5iZiI6MTYyNDUyMjA0NiwiZXhwIjoxNjU2MDU4MDQ2LCJzdWIiOiIxOTUxNTciLCJzY29wZXMiOltdfQ.BIE6HEemAh-8UGXEzurtFz5LHKbDyP2QW7UZ1S6pdMRgo4YxFs0RSaypfGrpf13M0SGGcAKNTgiOT1x5tASHijxTs8oA3qbrfZEyNZLYKs4BwSLJi6u9HX4ohPPnavdp5tYVn9X67vLVL7cjHbZOJIJdbAoQ35UXKaVs0O1xpBlgCE_kyNFx-BqXJKUfptaVBcKE_JgrQuIzoBuDgeDC6EiuoaZ_RqReqtHIjcF8p-tsqFyD3WHQSUcRVLMn5XxmRSszEi0MMoSAXj4MXRQ4nNXVK7WOJ0B7mArqz2c52z5KVpqXPvhUR0WYujEcrCJFRPk5Nc_FHtqmnMxBttdLl2baolc568iKNe5xo0tumra4M1u3a1iXFyS-PREEk0mjY93E9o8FIs0K9I8Klz5wMSgWtFWkHwehpT5ujFDOFNNypmlx_xe8qinSZBTyaMX6pagyzL3AVqYZS-NuppnECkSnq0XPjZ_GS6YAy1-n0jw0dldY_QwdZ-J_auQd21afC4Vb9yYY8bxMunUNgv4JzbbQPEk_36vHS9lKZ8jnp413t0deSU_wzOSPLjGvZNzh75SCjebLjInVWqyYdEOGmnABv-6xgSEAihy1lvtktesiv6r2SzB1-TqcP2GsLxusEoEqLRUs2ye8oKx85ytmmYxhx5_fAtILu5JWdYGubJQ'}
    r = requests.get("https://api.whiskybase.com/api/v2/auctions/group", params=params, headers=headers)
    r_data = r.json()['data']
    pages = r.json()['last_page']
    await insert_whisky_entities(table, r_data)

    if pages > 1:
        for i in range(2, pages + 1):
            params['page'] = i
            r = requests.get("https://api.whiskybase.com/api/v2/auctions/group", params=params, headers=headers)
            r_data = r.json()['data']
            await insert_whisky_entities(table, r_data)


@router.get("/fab50")
async def populate_database_fab50():
    pass
