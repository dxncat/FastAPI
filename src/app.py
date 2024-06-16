from fastapi import FastAPI
from routes import auth_route, items_route, users_route
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#rutas
app.include_router(items_route.router)
app.include_router(users_route.router)
app.include_router(auth_route.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"ping": "pong"}
