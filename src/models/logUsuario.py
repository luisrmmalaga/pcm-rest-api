from pydantic import BaseModel
from bson import ObjectId
from models.coordenadas import Coordenadas

class LogUsuario(BaseModel):
    _id: ObjectId
    idUsuario: str
    coordenadas: Coordenadas
    timestamp: float