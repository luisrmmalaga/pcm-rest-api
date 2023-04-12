def userEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "timestampCreacion": item["timestampCreacion"],
        "timestampFin": item["timestampFin"],
        "timestampUltimoRegistro": item["timestampUltimoRegistro"],
        "coordenadas":{
            "longitud":item["coordenadas"]["coordinates"][0],
            "latitud":item["coordenadas"]["coordinates"][1],
        },
    }

def usersEntity(entity) -> list:
   return [userEntity(item) for item in entity]