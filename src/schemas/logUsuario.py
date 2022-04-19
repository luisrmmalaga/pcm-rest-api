def logUserEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "idUsuario":item["idUsuario"],
        "coordenadas":{
            "latitud":item["coordenadas"]["latitud"],
            "longitud":item["coordenadas"]["longitud"],
        },
        "timestamp": item["timestamp"],
    }

def logUsersEntity(entity) -> list:
   return [logUserEntity(item) for item in entity]