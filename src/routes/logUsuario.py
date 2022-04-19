from fastapi import APIRouter, Response, status
from config.db import connection
from models.logUsuario import LogUsuario
from schemas.logUsuario import logUserEntity, logUsersEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

logUser = APIRouter()

@logUser.get('/logUsers', response_model=list[LogUsuario], tags=["Log Usuarios"])
def get_all_users():
    return logUsersEntity(connection.PCM.LogUsuario.find())

@logUser.post('/logUser', response_model=LogUsuario, tags=["Log Usuarios"])
def create_user(logUser: LogUsuario):
    new_log_user = dict(logUser)
    new_log_user['coordenadas'] = dict(logUser.coordenadas)

    id =  connection.PCM.LogUsuario.insert_one(new_log_user).inserted_id
    logUser = connection.PCM.LogUsuario.find_one({"_id":id})

    return logUserEntity(logUser)

@logUser.get('/logUser/{id}', response_model=LogUsuario, tags=["Log Usuarios"])
def get__user(id: str):
    return logUserEntity(connection.PCM.LogUsuario.find_one({"_id":ObjectId(id)}))

@logUser.put('/logUser/{id}', response_model=LogUsuario, tags=["Log Usuarios"])
def update_user(id: str, logUser: LogUsuario):
    update_log_user = dict(logUser)
    update_log_user = ObjectId(logUser.idUsuario)
    update_log_user['coordenadas'] = dict(logUser.coordenadas)
    connection.PCM.LogUsuario.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(update_log_user)})
    return logUserEntity(connection.PCM.LogUsuario.find_one({"_id":ObjectId(id)}))

@logUser.delete('/logUser/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Log Usuarios"])
def delete_user(id: str):
    logUserEntity(connection.PCM.LogUsuario.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)