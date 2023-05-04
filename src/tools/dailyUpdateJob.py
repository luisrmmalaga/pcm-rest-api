import datetime

from models.coordenadas import Coordenadas
from models.favorito import Favorito
from routes.checkpoint import create_checkpoint
from routes.favorito import get_all_favourites, upsert_favourite
from routes.logUsuario import get_logs_in_favourite_radius


def job():
   favourites = get_all_favourites()

   for favourite in favourites:
      print("**** Updating "+ favourite['_id'] +" ****")
      favouriteData = get_logs_in_favourite_radius(favourite['coordenadas']['latitud'],favourite['coordenadas']['longitud'],favourite['radio'])

      usuarios = favouriteData['usuarios']
      densidad = favouriteData['densidad']
      timestamp = datetime.datetime.timestamp(datetime.datetime.now()) * 1000

      checkpoint = {
            "idUsuario": favourite['idUsuario'],
            "idFavorito":  favourite['_id'],
            "timestamp": timestamp,
            "densidad": densidad,
            "usuarios": usuarios,
        }
      
      coordenadas = Coordenadas(latitud=favourite['coordenadas']['latitud'], longitud=favourite['coordenadas']['longitud'])
      favorito = Favorito(idUsuario=favourite['idUsuario'], nombre=favourite['nombre'],coordenadas=coordenadas,
                           timestampCreacion=favourite['timestampCreacion'], timestampUltimaMuestra=timestamp,densidad=densidad, radio= favourite['radio'])

      create_checkpoint(checkpoint)
      upsert_favourite(favourite['idUsuario'],favourite['coordenadas']['latitud'],favourite['coordenadas']['longitud'],favourite['timestampCreacion'],favorito)
      print("**** Location updated "+ favourite['_id'] +" ****")

   print("------ Daily update done ------")