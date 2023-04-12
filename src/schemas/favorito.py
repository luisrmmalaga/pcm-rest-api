def favoritoEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "idUsuario":item["idUsuario"],
        "nombre":item["nombre"],
        "coordenadas":{
            "longitud":item["coordenadas"]["coordinates"][0],
            "latitud":item["coordenadas"]["coordinates"][1],
        },
        "timestampCreacion":item["timestampCreacion"],
        "timestampUltimaMuestra": item["timestampUltimaMuestra"],
        "densidad":item["densidad"],
        "radio":item["radio"]
    }

def favoritosEntity(entity) -> list:
   return [favoritoEntity(item) for item in entity]