from utils.db import execute, fetch, get_insert_query, get_fetch_query, get_update_query, get_delete_query, get_array_update_query, get_array_fetch_query, get_array_delete_query, get_fetch_by_pattern_query
from enums.roles import RoleEnum
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from utils.const import UNAUTHORIZED, configure_404_message
import asyncio


async def is_admin(username: str):
    values = {"username": username}
    query = get_fetch_query("users", "role", values)
    results = await fetch(query, False, values)

    if results is not None:
        if results["role"] == RoleEnum.ADMIN:
            return True
        else:
            return False
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=configure_404_message("user"))


async def get_entity(table, fields, values):
    """
    Returns an entity from the database if exists, otherwise returns False.

    :param table: specifies the table you wish to query : str
    :param fields: specifies the fields you wish to return from the query : str || List[str]
    :param values: specifies both the query parameters and values needed for databases module configuration : Dict
    :return: results from query || False
    """
    query = get_fetch_query(table, fields, values)
    results = await fetch(query, False, values)

    if results is None:
        return False

    return results


async def get_entities(table, fields, values=None):
    query = get_fetch_query(table, fields, values)
    results = await fetch(query, True, values)

    if results is None:
        return False

    return results


async def get_entities_by_pattern(table, fields, values):
    query = get_fetch_by_pattern_query(table, fields, values)
    results = await fetch(query, True, values)

    if results is None:
        return False

    return results


async def get_whisky_price_by_date_and_name(table, fields, name, date):
    if isinstance(fields, list):
        fields = ", ".join(fields)

    values = {"index_name": name, "month": f"%{date}%"}

    query = f"SELECT {fields} FROM {table} WHERE index_name = :index_name AND month LIKE :month"
    print(query)
    results = await fetch(query, True, values)

    if results is None:
        return False

    return results


async def check_element_in_array(table, fields, array):
    fields_array = []
    for key in fields:
        fields_array.append({key: fields[key]})

    query = get_array_fetch_query(table, fields_array, array)

    results = await fetch(query, False, fields)

    if results:
        return True

    return False


async def get_portfolio_entities(table, field, user_id):
    values = {
        "user_id": user_id
    }

    query = f"SELECT * FROM {table} WHERE id = ANY((SELECT {field} FROM portfolio WHERE user_id = :user_id)::INT[])"
    results = await fetch(query, True, values)

    if results is None:
        return False

    return results


async def insert_entity(table, entity):
    """
    Inserts a new entity into the database

    :param table: specifies the table you wish to insert into : str
    :param entity: specifies the fields and values you wish to insert : Dict
    :return: none
    """
    values = dict(entity)
    query = get_insert_query(table, values)

    return await execute(query, False, values)


async def insert_whisky_entities(table, entities):
    query_values = entities[0]
    query = get_insert_query(table, query_values)
    return await execute(query, True, entities)


async def insert_dummy_entities(table, entities):
    query_values = entities[0]['owner']

    values = []
    for user in entities:
        values.append(user['owner'])

    query = get_insert_query(table, query_values)

    return await execute(query, True, values)


async def update_entity(table, fields, values):
    query = get_update_query(table, fields, values)
    values = {**fields, **values}
    await execute(query, False, values)


async def update_entity_array(table, fields, query_params, array):
    query = get_array_update_query(table, fields, query_params, array)
    fields = {**fields, **query_params}
    await execute(query, False, fields)


async def delete_entity(table, values):
    query = get_delete_query(table, values)
    await execute(query, False, values)


async def delete_entity_array(table, fields, query_params, array):
    query = get_array_delete_query(table, fields, query_params, array)
    fields = {**fields, **query_params}
    await execute(query, False, fields)

