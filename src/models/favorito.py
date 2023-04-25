from bson import ObjectId
from pydantic import BaseModel

from models.coordenadas import Coordenadas


class Favorito(BaseModel):
    
    _id: ObjectId
    idUsuario: str
    nombre: str
    coordenadas: Coordenadas
    timestampCreacion: float
    timestampUltimaMuestra: float
    densidad: float
    radio: int