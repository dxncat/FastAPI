from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    nickname: str
    correo: str
    direccion: str | None
    numero: int | None
    es_tienda: bool = False
    desactivado: bool = False