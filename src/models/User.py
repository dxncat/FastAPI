from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    nickname: str
    contraseña: str = None
    correo: str
    direccion: str | None
    numero: int | None
    es_tienda: bool = False
    desactivado: bool = False

    def search_user(field: str, key, db_client, user_schema):
        return User(**user_schema(db_client.users.find_one({field: key})))