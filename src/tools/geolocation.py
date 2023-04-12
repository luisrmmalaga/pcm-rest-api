import math

from tools.constant import EARTH_RADIUS


def get_radians(radiusInMeters: int):
    return radiusInMeters * 0.001 / EARTH_RADIUS

def get_geoJSON_coordinates(coordinates):
        return {
            'type' : "Point",
            'coordinates' : [ coordinates['longitud'], coordinates['latitud']]
        }

def get_area_of_circle(radius: int):
    area = math.pi * radius ** 2
    return area