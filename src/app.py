from fastapi import FastAPI

from routes.favorito import favorito
from routes.logUsuario import logUser
from routes.usuario import user

app = FastAPI(title="PCM REST API with FastAPI and MongoDB", version= "0.0.1")

app.include_router(user)
app.include_router(logUser)
app.include_router(favorito)


