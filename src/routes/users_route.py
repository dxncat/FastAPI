from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from passlib.context import CryptContext
import models.User as user_entity
from db.client import db_client
from db.schemas.user_schema import user_schema, users_schema

router = APIRouter(prefix="/usuarios",
                   tags=["usuarios"],
                   responses={404: {"message": "No encontrado"}})

crypt_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    ) 

@router.get("/", response_model = list[user_entity.User])
async def usuarios():
    return users_schema(db_client.users.find())

@router.get("/{usuario_id}")
async def read_usuario(usuario_id: str):
    return user_entity.User.search_user("_id", ObjectId(usuario_id), db_client, user_schema)
    
@router.get("/")
async def read_usuario(id: str):
        return user_entity.User.search_user("_id", ObjectId(id), db_client, user_schema)

    
@router.post("/", response_model = user_entity.User, status_code=201)
async def create_usuario(usuario: user_entity.User):
    if db_client.users.find_one({"correo": usuario.correo}):
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    user_dict = dict(usuario)
    del user_dict["id"]
    user_dict["contraseña"] = crypt_context.hash(user_dict["contraseña"])
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return user_entity.User(**new_user)

@router.put("/", response_model = user_entity.User)
async def update_usuario(usuario: user_entity.User):
    try:
        user_dict = dict(usuario)
        del user_dict["id"]
        db_client.users.find_one_and_replace({"_id": ObjectId(usuario.id)}, user_dict)
        return user_entity.User.search_user("_id", ObjectId(usuario.id), db_client, user_schema)
    except:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.delete("/{usuario_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(usuario_id)})
    if not found:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")