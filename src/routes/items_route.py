from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from auth.auth_user import current_user
from models.Item import Item
from db.client import db_client
import models.User as user_entity
from db.schemas.item_schemas import items_schema

router = APIRouter(prefix="/items",
                   tags=["items"],
                   responses={404: {"message": "No encontrado"}})


@router.get("/", response_model=list[Item])
async def items():
    return items_schema(db_client.items.find())

@router.get("/{item_id}")
async def read_item(item_id: str):
    return Item.search_item("_id", ObjectId(item_id))
    
@router.get("/tags/{item_tag}")
async def read_item(item_tag: str):
    try:
        items = db_client.items.find({"tag": item_tag})
        return items_schema(items)
    except:
        raise HTTPException(status_code=404, detail="Item no encontrado")

@router.get("/autor/{autor}")
async def read_item(autor: str):
    try:
        items = db_client.items.find({"autor": autor})
        return items_schema(items)
    except:
        raise HTTPException(status_code=404, detail="Item no encontrado")

@router.post("/", response_model = Item, status_code=201)
async def create_item(item: Item, user: user_entity.User = Depends(current_user)):
    item_dict = dict(item)
    del item_dict["id"]
    item_dict["autor"] = user.nickname
    id = db_client.items.insert_one(item_dict).inserted_id
    new_item = db_client.items.find_one({"_id": id})
    return Item(**new_item)