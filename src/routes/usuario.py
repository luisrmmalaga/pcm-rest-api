from fastapi import APIRouter, Response, status
from config.db import connection
from models.usuario import Usuario
from schemas.usuario import userEntity, usersEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[Usuario], tags=["Usuarios"])
def get_all_users():
    return usersEntity(connection.PCM.Usuario.find())

@user.post('/user', response_model=Usuario, tags=["Usuarios"])
def create_user(user: Usuario):
    new_user = dict(user)
    new_user['_id']= ObjectId(user._id)
    new_user['coordenadas'] = dict(user.coordenadas)

    id =  connection.PCM.Usuario.insert_one(new_user).inserted_id
    user = connection.PCM.Usuario.find_one({"_id":id})

    return userEntity(user)

@user.get('/user/{id}', response_model=Usuario, tags=["Usuarios"])
def get__user(id: str):
    return userEntity(connection.PCM.Usuario.find_one({"_id":ObjectId(id)}))

@user.put('/user/{id}', response_model=Usuario, tags=["Usuarios"])
def update_user(id: str, user: Usuario):
    update_user = dict(user)
    update_user['coordenadas'] = dict(user.coordenadas)
    connection.PCM.Usuario.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(update_user)})
    return userEntity(connection.PCM.Usuario.find_one({"_id":ObjectId(id)}))

@user.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def delete_user(id: str):
    userEntity(connection.PCM.Usuario.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)