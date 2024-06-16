from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    nickname: str
    correo: str
    direccion: str | None
    numero: int | None
    es_tienda: bool = False
    desactivado: bool = False

    def search_nickname(nickname: str, db_client, user_schema):
        try:
            return User(**user_schema(db_client.local.users.find_one({"nickname": nickname})))
        except:
            return {"error": "Usuario no encontrado"}
        
    def search_email(email: str, db_client, user_schema):
        try:
            return User(**user_schema(db_client.local.users.find_one({"correo": email})))
        except:
            return {"error": "Usuario no encontrado"}

class UserDB(User):
    contraseña: str

def search_user_db(nickname: str, users_db: dict):
    if nickname in users_db:
        return UserDB(**users_db[nickname])
