import requests
import utils.api as api
from urllib.parse import urlencode
from geopy.distance import geodesic

# API key
key = api.amap_key
url = 'https://restapi.amap.com/v3/direction/driving?'
# 返回结果控制 base:返回基本信息；all：返回全部信息
extensions = 'base'

# Bing
bp_url = 'http://dev.virtualearth.net/REST/v1/Locations?'
br_url = 'http://dev.virtualearth.net/REST/v1/Routes?'


def get_point_by_bing(addressLine: str, maxResults: int = 1):
    """返回地点经纬度坐标及格式化地址

    Args:
        locality (str): 地区，如城市或临近地点
        maxResults (int, optional): 返回结果最大个数. Defaults to 1.

    Returns:
        coord: 经纬度坐标
        address: 格式化地址
    """
    params = {'countryRegion': 'AU', 'addressLine': addressLine,
              'maxResults': maxResults, 'key': api.bing_key}
    constructed_url = bp_url + urlencode(params)

    response = requests.get(url=constructed_url).json()
    # print(constructed_url)
    coord = response['resourceSets'][0]['resources'][0]['point']['coordinates']
    address = response['resourceSets'][0]['resources'][0]['address']['formattedAddress']
    return coord, address


def get_distance_by_bing(origin, destination):
    """获取两坐标点或地址之间的距离

    Args:
        origin (str, list[float]): 起点的地址或经纬度
        destination (str, list[float]): 终点的地址或经纬度

    Returns:
        double: 距离，单位：公里
    """
    if isinstance(origin, list):
        origin = f'{origin[0]},{origin[0]}'
    if isinstance(destination, list):
        origin = f'{destination[0]},{destination[0]}'

    params = {'wp.1': origin,
              'wp.2': destination, 'key': api.bing_key}
    constructed_url = br_url + urlencode(params)

    response = requests.get(url=constructed_url).json()

    return response['resourceSets'][0]['resources'][0]['travelDistance']


def get_geo_distance(origin: dict, destination: dict):
    origin = (origin['lat'], origin['lng'])
    destination = (destination['lat'], destination['lng'])
    distance = geodesic(origin, destination).km
    return distance


def get_distance_by_amap(origin: str, destination: str):
    """返回两坐标点间的驾车距离，单位：米

    Args:
        origin (str): 起点经纬度
        destination (str): 终点经纬度

    Returns:
        str: 驾车距离
    """

    constructed_url = f'{url}origin={origin}&destination={destination}&extensions={extensions}&key={key}'

    response = requests.get(url=constructed_url).json()

    print(response['route']['paths'][0]['distance'])
    return response['route']['paths'][0]['distance']


def get_point_by_here(address: str):
    base = 'https://geocode.search.hereapi.com/v1/geocode?'
    params = {'q': address, 'politicalView': 'AUS',
              'limit': 1, 'apiKey': api.here_key3}
    constructed_url = base + urlencode(params)

    response = requests.get(url=constructed_url).json()
    state = response['items'][0]['address']['state']
    city = response['items'][0]['address']['city']
    address = response['items'][0]['address']['label']
    coord = response['items'][0]['position']
    return coord, address, city, state
