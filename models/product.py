from pydantic import BaseModel


class Product(BaseModel):
    bottle_id: int
    vendor_id: int
    region_id: int