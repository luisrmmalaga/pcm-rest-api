import datetime

from bson import ObjectId
from fastapi import APIRouter, Response, status
from pymongo import DESCENDING
from starlette.status import HTTP_204_NO_CONTENT

from config.db import connection
from models.logUsuario import LogUsuario
from schemas.logUsuario import logUserEntity, logUsersEntity
from tools.geolocation import (get_area_of_circle, get_geoJSON_coordinates,
                               get_radians)

logUser = APIRouter()

@logUser.get('/logUsers', response_model=list[LogUsuario], tags=["Log Usuarios"])
def get_all_log_users():
    return logUsersEntity(connection.PCM.LogUsuario.find())

@logUser.get('/logUsers/{timestamp}', response_model=list[LogUsuario], tags=["Log Usuarios"])
def get_filtered_log_users(timestamp: float):
    
    
    fecha_actual = datetime.datetime.now()
    timestamp_actual = datetime.datetime.timestamp(fecha_actual)* 1000
    timestamp_limite = timestamp_actual - (timestamp * 1000)

    filtro = {
        "timestamp": {
            "$gte": timestamp_limite,
            "$lt": timestamp_actual
        }
    }
    
    result = logUsersEntity(connection.PCM.LogUsuario.find(filtro))
    return result

@logUser.get('/logsIn/{latitud}/{longitud}', response_model=dict, tags=["Log Usuarios"])
def get_logs_in_selected_location_radius(latitud: float, longitud:float):
    center = [longitud,latitud]
    users = connection.PCM.LogUsuario.distinct("idUsuario")
    radio = 100
    fecha_actual = datetime.datetime.now()
    timestamp_actual = datetime.datetime.timestamp(fecha_actual)* 1000
    timestamp_limite = timestamp_actual - (86400 * 1000)

    logs = []

    for user in users:
        query = {
            "idUsuario": user,
            "coordenadas": {
                            "$geoWithin":
                              {"$centerSphere": [center, get_radians(radio)]}
            },
            "timestamp": {
                "$gte": timestamp_limite,
                "$lt": timestamp_actual
            }
        }
        log =  connection.PCM.LogUsuario.find(query).sort("timestamp", DESCENDING).limit(1)
        logs.extend(log)
    
    userLogs = len(logs)
    density = round(userLogs/get_area_of_circle(radio* 0.001),2)

    result = {"densidad":density,"usuarios":userLogs,"data":logUsersEntity(logs)}

    return result

@logUser.get('/logsInFavourite/{latitud}/{longitud}/{radio}', response_model=dict, tags=["Log Usuarios"])
def get_logs_in_favourite_radius(latitud: float, longitud:float, radio:int):
    center = [longitud,latitud]
    users = connection.PCM.LogUsuario.distinct("idUsuario")
    fecha_actual = datetime.datetime.now()
    timestamp_actual = datetime.datetime.timestamp(fecha_actual)* 1000
    timestamp_limite = timestamp_actual - (86400 * 1000)

    logs = []

    for user in users:
        query = {
            "idUsuario": user,
            "coordenadas": {
                            "$geoWithin":
                              {"$centerSphere": [center, get_radians(radio)]}
            },
            "timestamp": {
                "$gte": timestamp_limite,
                "$lt": timestamp_actual
            }
        }
        log =  connection.PCM.LogUsuario.find(query).sort("timestamp", DESCENDING).limit(1)
        logs.extend(log)

    userLogs = len(logs)
    density = round(userLogs/get_area_of_circle(radio* 0.001),2)

    result = {"densidad":density,"usuarios":userLogs, "data":logUsersEntity(logs)}

    return result

@logUser.post('/logUser', response_model=LogUsuario, tags=["Log Usuarios"])
def create_log_user(logUser: LogUsuario):
    new_log_user = dict(logUser)
    coordenadas = dict(logUser.coordenadas)
    new_log_user['coordenadas'] = get_geoJSON_coordinates(coordenadas)

    id =  connection.PCM.LogUsuario.insert_one(new_log_user).inserted_id
    logUser = connection.PCM.LogUsuario.find_one({"_id":id})

    return logUserEntity(logUser)

@logUser.get('/logUser/{id}', response_model=LogUsuario, tags=["Log Usuarios"])
def get_logs_user(id: str):
    return logUserEntity(connection.PCM.LogUsuario.find_one({"_id":ObjectId(id)}))

@logUser.put('/logUser/{id}', response_model=LogUsuario, tags=["Log Usuarios"])
def update_log_user(id: str, logUser: LogUsuario):
    update_log_user = dict(logUser)
    coordenadas = dict(logUser.coordenadas)
    update_log_user['coordenadas'] = get_geoJSON_coordinates(coordenadas)
    
    connection.PCM.LogUsuario.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(update_log_user)})
    return logUserEntity(connection.PCM.LogUsuario.find_one({"_id":ObjectId(id)}))

@logUser.delete('/logUser/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Log Usuarios"])
def delete_log_user(id: str):
    logUserEntity(connection.PCM.LogUsuario.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

@logUser.delete('/all/logUsers', status_code=status.HTTP_204_NO_CONTENT, tags=["Log Usuarios"])
def delete_all_logs():
    connection.PCM.LogUsuario.delete_many({})
    return Response(status_code=HTTP_204_NO_CONTENT)