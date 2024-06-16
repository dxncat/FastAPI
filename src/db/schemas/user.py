def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "nickname": user["nickname"],
        "correo": user["correo"],
        "direccion": user["direccion"],
        "numero": user["numero"],
        "es_tienda": user["es_tienda"]
    }