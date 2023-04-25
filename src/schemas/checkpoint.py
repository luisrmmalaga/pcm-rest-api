def checkpointEntity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "idUsuario":item["idUsuario"],
        "idFavorito":item["idFavorito"],
        "timestamp":item["timestamp"],
        "densidad":item["densidad"],
        "usuarios":item["usuarios"]
    }

def checkpointsEntity(entity) -> list:
   return [checkpointEntity(item) for item in entity]