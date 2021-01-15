from geopy.geocoders import Photon
from geopy.distance import geodesic
import json
from urllib.request import urlopen


def get_ipgeodata():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    return data['city']


def get_geodata(location):
    geolocator = Photon(user_agent='measurements')
    geodata = geolocator.geocode(location)
    return geodata


def get_distance(pointA, pointB):
    distance = geodesic(pointA, pointB).km
    return round(distance, 2)


def update_map_location(pointA, pointB):
    return [(pointA[0] + pointB[0]) / 2, (pointA[1] + pointB[1]) / 2]


def get_zoom_value(distance):
    if distance <= 200:
        return 8
    elif distance >200 and distance <=5000:
        return 4
    else:
        return 2
