import json

from bson import ObjectId
from db import connection
from fastapi import APIRouter

logUser = APIRouter()

f = open('perchel.json')
f2 = open('centro malaga.json')
data = json.load(f)
data2 = json.load(f2)  
f.close()
f2.close()

formatted_data = []

for i in data:
    formatted_data.extend([{
        "_id": ObjectId(i['_id']),
        "idUsuario": i['idUsuario'],
        "coordenadas":{
            "type": "Point",
            "coordinates":[i['longitud'],i['latitud']]
        },
        "timestamp": i['timestamp']
    }])
for i in data2:
    formatted_data.extend([{
        "_id": ObjectId(i['_id']),
        "idUsuario": i['idUsuario'],
        "coordenadas":{
            "type": "Point",
            "coordinates":[i['longitud'],i['latitud']]
        },
        "timestamp": i['timestamp']
    }])

connection.PCM.LogUsuario.insert_many(formatted_data)
