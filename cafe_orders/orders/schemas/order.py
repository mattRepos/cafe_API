from pydantic import BaseModel, Field, field_validator
from typing import List

class ItemSchema(BaseModel):
    name: str
    price: float = Field(..., gt=0)

class OrderCreateSchema(BaseModel):
    table_number: int = Field(..., gt=0)
    items: List[ItemSchema]

    @field_validator('items')
    def validate_items(cls, items):
        if not items:
            raise ValueError("Список блюд в заказе не должен быть пустым")
        return items

class StatusSchema(BaseModel):
    status: str = Field(..., pattern="^(pending|ready|paid)$")