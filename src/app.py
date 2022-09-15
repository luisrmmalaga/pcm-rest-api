from fastapi import FastAPI
from routes.usuario import user
from routes.logUsuario import logUser

app = FastAPI(title="PCM REST API with FastAPI and MongoDB", version= "0.0.1")

app.include_router(user)
app.include_router(logUser)


