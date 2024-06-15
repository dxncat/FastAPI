from fastapi import FastAPI
from routes import items, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#rutas
app.include_router(items.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"ping": "pong"}
