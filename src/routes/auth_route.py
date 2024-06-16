from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models.User as user_entity
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

router = APIRouter(tags=["auth"],
                   responses={404: {"message": "No encontrado"}})

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = config("SECRET_KEY")

crypt_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    ) 
                   
oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

users_db = {
    "dxncat": {
        "id": 1,
        "nickname": "dxncat",
        "correo": "dxncat@gmail.com",
        "contraseña": "$2a$12$G4B6ibt5In4B2QhGe5wgR.qW0DuIAJ5aTSp1qOAyF8NfYYedsboXm",
        "direccion": "Calle 123",
        "numero": 1234567890,
        "es_tienda": False
    },
    "dxncat_store": {
        "id": 2,
        "nickname": "dxncat_store",
        "correo": "dxncat@store.com",
        "contraseña": "$2a$12$csEo.TdVIvwUSUZ06pab0exKpc6KU/gyQCF9fGWdWbrNuw5LFEpX6",
        "direccion": "Calle 321",
        "numero": 987654321,
        "es_tienda": True,
        "desactivado": True
        }
}

async def auth_user(token: str = Depends(oauth_schema)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if user is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    return user_entity.search_user(user, users_db)

async def current_user(current: user_entity.User = Depends(auth_user)):
    if current.desactivado:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    print(user_db)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")
    user = user_entity.search_user_db(form.username)
    if not crypt_context.verify(form.password, user.contraseña):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    access_token = jwt.encode(
        {
            "sub": user.nickname,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(user: user_entity.User = Depends(current_user)):
    return user