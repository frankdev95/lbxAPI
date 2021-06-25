from pydantic import BaseModel
from typing import Optional
from fastapi import Body
from datetime import date


class Review(BaseModel):
    user_id: int
    bottle_id: int
    title: Optional[str] = Body(None)
    appearance: Optional[str] = Body(None)
    nose: Optional[str] = Body(None)
    palate: Optional[str] = Body(None)
    finish: Optional[str] = Body(None)
    conclusion: Optional[str] = Body(None)
    rating: float
    created_at: Optional[date] = date.today()
    modified_at: Optional[date]

