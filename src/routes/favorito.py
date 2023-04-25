import datetime

from bson import ObjectId
from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT

from config.db import connection
from models.favorito import Favorito
from routes.logUsuario import get_logs_in_favourite_radius
from schemas.favorito import favoritoEntity, favoritosEntity
from tools.geolocation import get_geoJSON_coordinates

favorito = APIRouter()

@favorito.get('/favourites', response_model=list[Favorito], tags=["Favoritos"])
def get_all_favourites():
    return favoritosEntity(connection.PCM.Favorito.find())

@favorito.post('/favourite', response_model=Favorito, tags=["Favoritos"])
def create_favourite(favorito: Favorito):
    new_favorito = dict(favorito)
    new_favorito['coordenadas'] = get_geoJSON_coordinates(dict(favorito.coordenadas))

    id =  connection.PCM.Favorito.insert_one(new_favorito).inserted_id
    favorito = connection.PCM.Favorito.find_one({"_id":id})

    return favoritoEntity(favorito)

@favorito.put('/{userId}/favourite/{latitude}/{longitude}/{timestampCreacion}', response_model=Favorito, tags=["Favoritos"])
def upsert_favourite(userId:str, latitude: float, longitude:float, timestampCreacion:float, favorito: Favorito):
    filter = { 
        'idUsuario': userId,
        "coordenadas": get_geoJSON_coordinates({
            "latitud": latitude,
            "longitud": longitude
        }),
        "timestampCreacion" : timestampCreacion
    }

    densityFromLocation = get_logs_in_favourite_radius(favorito.coordenadas.latitud, favorito.coordenadas.longitud, favorito.radio)['densidad']
    
    upsert_favorito = dict(favorito)
    upsert_favorito['coordenadas'] = get_geoJSON_coordinates(dict(favorito.coordenadas))
    upsert_favorito['densidad'] = densityFromLocation

    new_values = { "$set": dict(upsert_favorito) }

    connection.PCM.Favorito.update_one(filter, new_values, upsert=True)

    filter = { 
        'idUsuario': upsert_favorito['idUsuario'],
        "coordenadas": upsert_favorito['coordenadas'],
        "timestampCreacion" : upsert_favorito['timestampCreacion'] 
    }

    return favoritoEntity(connection.PCM.Favorito.find_one(filter))

@favorito.get('/favourites/{id}', response_model=list[Favorito], tags=["Favoritos"])
def get_favourites_by_user_id(id: str):
    return favoritosEntity(connection.PCM.Favorito.find({"idUsuario":id}))

@favorito.get('/favourites/{id}/from/{favName}', response_model=list[Favorito], tags=["Favoritos"])
def get_favourites_by_user_id_and_fav_name(id: str, favName: str):
    return favoritosEntity(connection.PCM.Favorito.find({"idUsuario":id, "nombre": favName}))

@favorito.put('/favourite/{id}', response_model=Favorito, tags=["Favoritos"])
def update_favourite(id: str, favorito: Favorito):
    update_favorito = dict(favorito)
    update_favorito['coordenadas'] = get_geoJSON_coordinates(favorito.coordenadas)
    connection.PCM.Favorito.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(update_favorito)})
    return favoritoEntity(connection.PCM.Favorito.find_one({"_id":ObjectId(id)}))

@favorito.delete('/favourite/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Favoritos"])
def delete_favourite(id: str):
    favoritoEntity(connection.PCM.Favorito.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

@favorito.delete('/{idUsuario}/{timestampCreacion}/coordinates/{latitud}/{longitud}', status_code=status.HTTP_204_NO_CONTENT, tags=["Favoritos"])
def delete_favourite_by_userid_timestamp_and_coordinates(idUsuario: str,timestampCreacion:float, latitud: float,longitud:float):
    coords = get_geoJSON_coordinates(dict({"latitud":latitud,"longitud":longitud}))
    favoritoEntity(connection.PCM.Favorito.find_one_and_delete({"idUsuario":idUsuario,"timestampCreacion":timestampCreacion,"coordenadas":coords}))
    return Response(status_code=HTTP_204_NO_CONTENT)

@favorito.delete('/all/favourites', status_code=status.HTTP_204_NO_CONTENT, tags=["Favoritos"])
def delete_all_favourites():
    connection.PCM.Favorito.delete_many({})
    return Response(status_code=HTTP_204_NO_CONTENT)