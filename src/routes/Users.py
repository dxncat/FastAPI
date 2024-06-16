from fastapi import APIRouter, HTTPException
import models.User as user_entity
from db.client import db_client
from db.schemas.user import user_schema

router = APIRouter(prefix="/usuarios",
                   tags=["usuarios"],
                   responses={404: {"message": "No encontrado"}})

lista_usuarios = db_client.local.users.find({})

@router.get("/", response_model = list(user_entity.User))
async def usuarios():
    return lista_usuarios

@router.get("/{usuario_id}")
async def read_usuario(usuario_id: int):
    usuario = filter(lambda x: x.id == usuario_id, lista_usuarios)
    try:
        return list(usuario)[0]
    except:
        return {"error": "Usuario no encontrado"}
    
@router.get("/")
async def read_usuario(id: int):
    usuario = filter(lambda x: x.id == id, lista_usuarios)
    try:
        return list(usuario)[0]
    except:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.post("/", response_model = user_entity.User, status_code=201)
async def create_usuario(usuario: user_entity.User):
    if type(user_entity.User.search_user(usuario.correo, db_client, user_schema)) == user_entity.User:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    user_dict = dict(usuario)
    print(user_dict)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    return user_entity.User(**new_user)

@router.put("/{usuario_id}")
async def update_usuario(usuario_id: int, usuario: user_entity.User):
    if usuario_id in map(lambda x: x.id, lista_usuarios):
        lista_usuarios[usuario_id - 1] = usuario
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: int):
    if usuario_id in map(lambda x: x.id, lista_usuarios):
        lista_usuarios.remove(list(filter(lambda x: x.id == usuario_id, lista_usuarios))[0])
        return {"message": "Usuario eliminado"}
    else: 
        return {"error": "Usuario no encontrado"}