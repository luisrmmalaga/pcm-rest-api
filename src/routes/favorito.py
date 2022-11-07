from bson import ObjectId
from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT

from config.db import connection
from models.favorito import Favorito
from schemas.favorito import favoritoEntity, favoritosEntity

favorito = APIRouter()

@favorito.get('/favourites', response_model=list[Favorito], tags=["Favoritos"])
def get_all_favourites():
    return favoritosEntity(connection.PCM.Favorito.find())

@favorito.post('/favourite', response_model=Favorito, tags=["Favoritos"])
def create_favourite(favorito: Favorito):
    new_favorito = dict(favorito)
    new_favorito['coordenadas'] = dict(favorito.coordenadas)

    id =  connection.PCM.Favorito.insert_one(new_favorito).inserted_id
    favorito = connection.PCM.Favorito.find_one({"_id":id})

    return favoritoEntity(favorito)

@favorito.get('/favourites/{id}', response_model=Favorito, tags=["Favoritos"])
def get_favourites_by_user_id(id: str):
    return favoritoEntity(connection.PCM.Favorito.find({"idUsuario":id}))

@favorito.put('/favourite/{id}', response_model=Favorito, tags=["Favoritos"])
def update_favourite(id: str, favorito: Favorito):
    update_favorito = dict(favorito)
    update_favorito['coordenadas'] = dict(favorito.coordenadas)
    connection.PCM.Favorito.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(update_favorito)})
    return favoritoEntity(connection.PCM.Favorito.find_one({"_id":ObjectId(id)}))

@favorito.delete('/favourite/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Favoritos"])
def delete_favourite(id: str):
    favoritoEntity(connection.PCM.Favorito.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)