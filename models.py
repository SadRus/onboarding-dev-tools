from datetime import datetime
from pydantic import BaseModel, Field, validator


# Написать вложенную схему валидации данных
class Order(BaseModel):
    order_id: int
    count: int = Field(default=1)
    country_code: str
    expires_at: datetime = Field(alias='expires_at')

    @validator('order_id')
    def id_is_positive(cls, value):
        if value <= 0:
            raise ValueError('ERROR: "order_id" must be a positive')
        return value
