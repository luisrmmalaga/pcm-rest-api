from pydantic import BaseModel
from bson import ObjectId
from models.coordenadas import Coordenadas

class Usuario(BaseModel):
    _id: ObjectId
    timestampCreacion: float
    timestampFin: float
    timestampUltimoRegistro: float
    coordenadas: Coordenadas