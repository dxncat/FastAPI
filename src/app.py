from fastapi import FastAPI
from models.Item import Item
from models.User import User

app = FastAPI()

@app.get("/")
async def read_root():
    return {"ping": "pong"}

productos = [
    Item(id = 1, nombre = "Pantalón jean", descripción = "Pantalón tipo jean oversize con diseño pintado a mano de flores con pinturas para tela en tonalidades fuertes.", precio = 122000, descuento = 70, imagen = "https://i.pinimg.com/736x/ad/95/7a/ad957a8fabe079a049b6237b3417ca5f.jpg", tag = "nuevo"),
    Item(id = 2, nombre = "Hoodie Lava", descripción = "Hoodie con diseño de lava en tonalidades rojas y naranjas, con capucha y bolsillos.", precio = 70000, imagen = "https://i.pinimg.com/564x/73/e6/3f/73e63f855002499b8aedcba978cab43b.jpg", tag = "oferta"),
    Item(id = 3, nombre = "Pantalón jean", descripción = "Pantalón tipo jean oversize con diseño pintado a mano de calaveras con pinturas para tela en tonalidades fuertes.", precio = 120000, descuento = 70,imagen = "https://i.pinimg.com/564x/0d/fc/43/0dfc43b450bab778c838db45d7b87636.jpg", tag = "nuevo"),
    Item(id = 4, nombre = "Hoodie Skeleton", descripción = "Hoodie con diseño de esqueleto en tonalidades grises y negras, con capucha y bolsillos.", precio = 130000, imagen = "https://i.pinimg.com/736x/10/41/4e/10414e2a7e1e61bd714d932402b9ca15.jpg", tag = "oferta"),
    Item(id = 5, nombre = "Conjunto Invierno 2024", descripción = "Conjunto de invierno con diseño de paisaje invernal en tonalidades azules y blancas, con gorro y guantes.", precio = 380000, descuento = 30, imagen = "https://i.pinimg.com/564x/eb/7c/54/eb7c54adc4d0eef108a55311d3187a07.jpg" , tag = "nuevo"),
    Item(id = 6, nombre = "Hoodie Limited Edition", descripción = "Hoodie edición limitada con diseño de galaxia en tonalidades moradas y azules, con capucha y bolsillos.", precio = 250000, imagen = "https://i.pinimg.com/736x/00/de/22/00de22019b1ad09d0038c3362f047e22.jpg", tag = "oferta")
]

lista_usuarios = [
    User(id = 1, nickname = "Jorge", correo = "jorge@gmail.com", contraseña = "1234", direccion = "Calle 123", numero = 1234567890, es_tienda = False)
]

#region Items

@app.get("/items")
async def items():
    return productos

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = filter(lambda x: x.id == item_id, productos)
    try:
        return list(item)[0]
    except:
        return {"error": "Producto no encontrado"}
    
@app.get("/items/tags/{item_tag}")
async def read_item(item_tag: str):
    item = filter(lambda x: x.tag == item_tag, productos)
    try:
        return list(item)
    except:
        return {"error": "Productos con tag no encontrados"}
#endregion

#region Usuarios
@app.get("/usuarios")
async def usuarios():
    return lista_usuarios

@app.get("/usuarios/{usuario_id}")
async def read_usuario(usuario_id: int):
    usuario = filter(lambda x: x.id == usuario_id, lista_usuarios)
    try:
        return list(usuario)[0]
    except:
        return {"error": "Usuario no encontrado"}
    
@app.get("/usuarios/")
async def read_usuario(id: int):
    usuario = filter(lambda x: x.id == id, lista_usuarios)
    try:
        return list(usuario)[0]
    except:
        return {"error": "Usuario no encontrado"}