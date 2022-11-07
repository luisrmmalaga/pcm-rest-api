def favoritoEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "idUsuario":item["idUsuario"],
        "coordenadas":{
            "latitud":item["coordenadas"]["latitud"],
            "longitud":item["coordenadas"]["longitud"],
        },
        "timestampUltimaMuestra": item["timestampUltimaMuestra"],
        "densidad":item["densidad"]
    }

def favoritosEntity(entity) -> list:
   return [favoritoEntity(item) for item in entity]