def userEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "timestampCreacion": item["timestampCreacion"],
        "timestampFin": item["timestampFin"],
        "timestampUltimoRegistro": item["timestampUltimoRegistro"],
        "coordenadas":{
            "latitud":item["coordenadas"]["latitud"],
            "longitud":item["coordenadas"]["longitud"],
        },
    }

def usersEntity(entity) -> list:
   return [userEntity(item) for item in entity]