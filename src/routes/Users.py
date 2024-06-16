from fastapi import APIRouter, HTTPException
from models.User import User
from db.client import db_client
from db.schemas.user import user_schema

router = APIRouter(prefix="/usuarios",
                   tags=["usuarios"],
                   responses={404: {"message": "No encontrado"}})

# lista_usuarios = [
#     User(id = 1, nickname = "Jorge", correo = "jorge@gmail.com", contraseña = "1234", direccion = "Calle 123", numero = 1234567890, es_tienda = False),
#     User(id = 2, nickname = "Maria", correo = "maria@gmail.com", contraseña = "1234", direccion = "Calle 123", numero = 1234567890, es_tienda = False),
#     User(id = 3, nickname = "Tienda1", correo = "tienda1@gmail.com", contraseña = "1234", direccion = "Calle 123", numero = 1234567890, es_tienda = True)
# ]

@router.get("/")
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
    
@router.post("/", response_model=User, status_code=201)
async def create_usuario(usuario: User):

    # if usuario.nickname in map(lambda x: x.nickname, lista_usuarios):
    #     raise HTTPException(status_code=400, detail="Usuario ya existe")
    user_dict = dict(usuario)
    print(user_dict)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    print(id)
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    print(new_user)
    return User(**new_user)

@router.put("/{usuario_id}")
async def update_usuario(usuario_id: int, usuario: User):
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