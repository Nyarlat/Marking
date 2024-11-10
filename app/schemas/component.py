from pydantic import BaseModel, Field


class Component(BaseModel):
    article: str = Field(default=None, alias="ДетальАртикул")
    number: float = Field(default=None, alias="ПорядковыйНомер")
    name: str = Field(default=None, alias="ДетальНаименование")
    order_number: str = Field(default=None, alias="ЗаказНомер")
    station: str = Field(default=None, alias="СтанцияБлок")

    class Config:
        populate_by_name = True
