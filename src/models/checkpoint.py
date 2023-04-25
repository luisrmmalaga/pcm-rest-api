from bson import ObjectId
from pydantic import BaseModel


class Checkpoint(BaseModel):
    _id: ObjectId
    idUsuario: str
    idFavorito: str
    timestamp: float
    densidad: float
    usuarios: int