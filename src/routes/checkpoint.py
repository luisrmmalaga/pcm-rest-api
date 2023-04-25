import datetime

from bson import ObjectId
from fastapi import APIRouter, Response, status
from pymongo import ASCENDING
from starlette.status import HTTP_204_NO_CONTENT

from config.db import connection
from models.checkpoint import Checkpoint
from routes.favorito import get_favourites_by_user_id_and_fav_name
from schemas.checkpoint import checkpointEntity, checkpointsEntity

checkpoint = APIRouter()


@checkpoint.post('/checkpoint', response_model=Checkpoint, tags=["Chekpoints"])
def create_checkpoint(checkpoint: Checkpoint):
    new_checkpoint = dict(checkpoint)
    
    id =  connection.PCM.Checkpoint.insert_one(new_checkpoint).inserted_id
    checkpoint = connection.PCM.Checkpoint.find_one({"_id":id})

    return checkpointEntity(checkpoint)

@checkpoint.get('/checkpoints', response_model=list[Checkpoint], tags=["Checkpoints"])
def get_all_checkpoints():
    return checkpointsEntity(connection.PCM.Checkpoint.find())

@checkpoint.get('/checkpoints/{idUsuario}', response_model=list[dict], tags=["Checkpoints"])
def get_checkpoints_by_userId(idUsuario:str):

    fecha_actual = datetime.datetime.now()
    fecha_7_dias_atras = fecha_actual - datetime.timedelta(days=7)
    timestamp_actual = datetime.datetime.timestamp(fecha_actual)* 1000
    timestamp_7_dias_atras = datetime.datetime.timestamp(fecha_7_dias_atras)* 1000

    filtro = {
        "idUsuario": idUsuario,
        "timestamp": {
            "$gte": timestamp_7_dias_atras,
            "$lt": timestamp_actual
        }
    }

    checkpoints = checkpointsEntity(connection.PCM.Checkpoint.find(filtro).sort("timestamp", ASCENDING))

    temp_dict = {}

    for obj in checkpoints:
        favorito = connection.PCM.Favorito.find_one({"_id":ObjectId(obj['idFavorito'])})['nombre']
        datos = {
            'timestamp': obj['timestamp'],
            'densidad': obj['densidad']
        }
        if favorito not in temp_dict:
            temp_dict[favorito] = {
                'favorito': favorito,
                'datos': []
            }
        temp_dict[favorito]['datos'].append(datos)

    return list(temp_dict.values())

@checkpoint.get('/checkpoints/{idUsuario}/from/{favName}', response_model=list[Checkpoint], tags=["Checkpoints"])
def get_checkpoints_by_userId_and_fav_name(idUsuario:str, favName:str):
    favId = get_favourites_by_user_id_and_fav_name(idUsuario, favName)[0]['_id']
    
    return checkpointsEntity(connection.PCM.Checkpoint.find({"idUsuario":idUsuario, "idFavorito":favId}))

@checkpoint.get('/trend/{favName}/{idUsuario}', response_model=float, tags=["Checkpoints"])
def calculate_trending(favName: str, idUsuario:str):

    favId = get_favourites_by_user_id_and_fav_name(idUsuario, favName)[0]['_id']
    values = checkpointsEntity(connection.PCM.Checkpoint.find({"idFavorito":favId}).sort("timestamp", -1).limit(2))

    if len(values) == 0:
        res = 0
    elif len(values) == 1:
        res = values[0]['densidad'] 
    else:
        res = values[0]['densidad'] - values[1]['densidad'] 

    return res

@checkpoint.delete('/checkpoints', status_code=status.HTTP_204_NO_CONTENT, tags=["Chekpoints"])
def delete_all_checkpoint():
    connection.PCM.Checkpoint.delete_many({})
    return Response(status_code=HTTP_204_NO_CONTENT)