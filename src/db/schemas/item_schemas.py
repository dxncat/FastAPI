def item_schema(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nombre": item["nombre"],
        "descripción": item["descripción"],
        "precio": item["precio"],
        "descuento": item["descuento"],
        "imagen": item["imagen"],
        "tag": item["tag"],
        "autor": item["autor"]
    }

def items_schema(items) -> list:
    return [item_schema(item) for item in items]