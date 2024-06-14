from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    id: int
    nombre: str
    descripción: str
    precio: int
    descuento: Union[int, None] = None
    imagen: str
    tag: str