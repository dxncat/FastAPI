def user_schema(user) -> dict:
    return {
        "id": user["_id"],
        "nickname": user["nickname"],
        "correo": user["correo"],
        "contraseña": user["contraseña"],
        "direccion": user["direccion"],
        "numero": user["numero"],
        "es_tienda": user["es_tienda"]
    }