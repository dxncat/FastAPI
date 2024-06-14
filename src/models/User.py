from pydantic import BaseModel

class User(BaseModel):
    id: int
    nickname: str
    correo: str
    contraseña: str
    direccion: str
    numero: int
    es_tienda: bool