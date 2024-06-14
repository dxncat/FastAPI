from fastapi import FastAPI
from routes import Items, Users

app = FastAPI()

#rutas
app.include_router(Items.router)
app.include_router(Users.router)

@app.get("/")
async def read_root():
    return {"ping": "pong"}
