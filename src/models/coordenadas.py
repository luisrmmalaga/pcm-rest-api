from pydantic import BaseModel


class Coordenadas(BaseModel):
    latitud: float
    longitud: float