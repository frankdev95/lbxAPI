from typing import Optional
from fastapi import Body
from pydantic import BaseModel, Field
from datetime import date


class Bottle(BaseModel):
    title: str
    age: int = Field(..., gt=0)
    vintage: Optional[date] = Body(None)
    bottled: Optional[date] = Body(None)
    volume: int = Field(..., gt=0)
    ml: int = Field(..., gt=0)
    latest_price: int = Field(..., gt=0)
    latest_price_date: date
    cask: Optional[int] = Body(None)
    num_bottles: Optional[int] = Body(None)
    identifier: Optional[int] = Body(None)