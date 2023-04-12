def logUserEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "idUsuario":item["idUsuario"],
        "coordenadas":{
            "longitud":item["coordenadas"]["coordinates"][0],
            "latitud":item["coordenadas"]["coordinates"][1],
        },
        "timestamp": item["timestamp"],
    }

def logUsersEntity(entity) -> list:
   return [logUserEntity(item) for item in entity]