from pydantic import BaseModel
from db.client import db_client
from db.schemas.item_schemas import item_schema

class Item(BaseModel):
    id: str = None
    nombre: str
    descripción: str
    precio: int
    descuento: int = 0
    imagen: str
    tag: str
    autor: str = None

    def search_item(field: str, key):
        return Item(**item_schema(db_client.items.find_one({field: key})))