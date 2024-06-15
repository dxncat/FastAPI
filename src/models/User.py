from pydantic import BaseModel

class User(BaseModel):
    id: int
    nickname: str
    correo: str
    direccion: str
    numero: int
    es_tienda: bool
    desactivado: bool = False