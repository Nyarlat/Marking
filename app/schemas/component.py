from pydantic import BaseModel, Field


class Component(BaseModel):
    article: str = Field(alias="ДетальАртикул")
    number: float = Field(alias="ПорядковыйНомер")
    name: str = Field(alias="ДетальНаименование")
    order_number: str = Field(alias="ЗаказНомер")
    station: str = Field(alias="СтанцияБлок")

    class Config:
        populate_by_name = True
