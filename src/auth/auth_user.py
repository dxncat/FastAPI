from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from decouple import config
import jwt
import models.User as user_entity 

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = "HS256"
SECRET_KEY = config("SECRET_KEY")

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
    return user_entity.User.search_user("nickname", user)

async def current_user(current: user_entity.User = Depends(auth_user)):
    if current.desactivado:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current