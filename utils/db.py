from databases import Database
from utils.const import DB, testing
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

db = Database(DB)


async def execute(query, multiple, values=None):
    if testing:
        await db.connect()

    try:
        if multiple:
            return await db.execute_many(query=query, values=values)
        else:
            return await db.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        if testing:
            await db.disconnect()


async def fetch(query, fetch_all, values=None):
    if testing:
        await db.connect()

    output = None

    try:
        if fetch_all:
            result = await db.fetch_all(query=query, values=values)
            if result is not None:
                output = []
                for row in result:
                    output.append(dict(row))
        else:
            result = await db.fetch_one(query=query, values=values)
            if result is not None:
                output = dict(result)

    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        if testing:
            await db.disconnect()

    return output


def parse_fields(fields):
    return {
        "columns": "(" + "".join([f"{key}," for key in fields])[:-1] + ")",
        "values": "(" + "".join([f":{key}," for key in fields])[:-1] + ")"
    }


def parse_assignment_operators(query_params):
    return "".join([f"{key} = :{key} AND " for key in query_params])[:-5]


def parse_array_assignment_operators(query_params):
    return "".join([f"{next(iter(value))} = :{next(iter(value))} AND " for index, value in enumerate(query_params) if
                    index < len(query_params) - 1])


def parse_pattern_assignment_operators(query_params):
    return "".join([f"{key} LIKE :{key} AND " for key in query_params])[:-5]


def get_insert_query(table, fields):
    return f"INSERT INTO {table}{parse_fields(fields)['columns']} VALUES {parse_fields(fields)['values']} RETURNING id"


def get_fetch_query(table, fields, query_params=None):
    if isinstance(fields, list):
        fields = ", ".join(fields)

    qualification = ""

    if query_params is not None:
        qualification = "WHERE " + parse_assignment_operators(query_params)

    return f"SELECT {fields} FROM {table} {qualification}"


def get_fetch_by_pattern_query(table, fields, query_params):
    if isinstance(fields, list):
        fields = ", ".join(fields)

    return f"SELECT {fields} FROM {table} WHERE {parse_pattern_assignment_operators(query_params)}"


def get_update_query(table, fields, query_params):
    values = ", ".join([f"{key} = :{key}" for key in fields])
    return f"UPDATE {table} SET {values} WHERE {parse_assignment_operators(query_params)}"


def get_delete_query(table, query_params):
    return f"DELETE FROM {table} WHERE {parse_assignment_operators(query_params)}"


# ARRAY QUERIES


def get_array_fetch_query(table, fields, array):
    key = next(iter(fields))
    return f"SELECT * FROM {table} WHERE {parse_array_assignment_operators(fields)}:{next(iter(fields[len(fields) - 1]))} = ANY ({array})"


def get_array_update_query(table, fields, query_params, array):
    key = next(iter(fields))
    return f"UPDATE {table} SET {array} = array_append({array}, :{key}) WHERE {parse_assignment_operators(query_params)}"


def get_array_delete_query(table, fields, query_params, array):
    key = next(iter(fields))
    return f"UPDATE {table} SET {array} = array_remove({array}, :{key}) WHERE {parse_assignment_operators(query_params)}"

