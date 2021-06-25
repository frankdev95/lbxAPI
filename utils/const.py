import os

JWT_SECRET_KEY = "67e0913bbb13dbfa654008874de8c4a7ab628ca3d033f66c4e53dfdd221d9e44c58cd10eb4b41945fd2a3e4de966d051a249e3ac36c29fa7677fb8cd801afb201a3dca7e2ff9184cf91ea795e71e0eb5"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_SECONDS = 60 * 60 * 24 * 5

testing = False
is_load_test = False
is_production = True if os.getenv("PRODUCTION") == "True" else False
# is_production = False

DB_HOST = "localhost:5432"
DB_USER = "admin"
DB_PASSWORD = "gdup5kldn"
DB_NAME = "lbx"

HOST_PRODUCTION = "10.106.0.2"

HOST_DB_HOST = "localhost:9000"
HOST_DB_USER = "test"
HOST_DB_PASSWORD = "test"
HOST_DB_NAME = "test"


if testing or is_load_test:
    DB = f"postgresql://{HOST_DB_USER}:{HOST_DB_PASSWORD}@{HOST_DB_HOST}/{HOST_DB_NAME}"
elif is_production:
    DB = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST_PRODUCTION}/{DB_NAME}"
else:
    DB = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

UNAUTHORIZED = "Whoops, you are not authorised for this request"

IMAGEBB_API_KEY = "f4023ddd3a09f371bdb3d67a5f0b1925"
IMAGEBB_URL = "https://api.imgbb.com/1/upload?key=f4023ddd3a09f371bdb3d67a5f0b1925"


if testing or is_load_test:
    REDIS_URL = "redis://localhost:8080"
elif is_production:
    REDIS_URL = f"redis://{HOST_PRODUCTION}"
else:
    REDIS_URL = "redis://localhost:6379"


def configure_404_message(entity):
    return f"The {entity} with given credentials does not exist"


def configure_insert_message(entity):
    return f"{entity} successfully inserted"


def configure_update_message(entity):
    return f"{entity} successfully updated"


def configure_delete_message(entity):
    return f"{entity} successfully deleted"

