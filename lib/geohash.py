#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
geohash
"""

from math import pi
import math

from geoprint import EARTH_RADIUS, encode, neighbors
from geoprint import decodemap


# 经纬度变化一度，距离变化 distance_delta
DISTANCE_DELTA = 2 * pi * EARTH_RADIUS / 360


def geo_int(latitude, longitude):
    geo_code = encode(float(latitude), float(longitude), 16)
    # 第一位是东西部，
    value_string = "".join(str(decodemap[c]) for c in geo_code[1:])
    value = int(value_string, 4)
    if geo_code[0] == 'w':
        value = -value
    return value, geo_code


def nearby_geocode(latitude, longitude, radius):
    """
    根据经纬度坐标和半径，算出附近的点所在的方格 geocode
    :param longitude:
    :param latitude:
    :param radius:
    :return: 返回以 (longitude, latitude) 为圆心 radius 为半径的圆所在方格 geocode 列表
    """
    if radius <= 0:
        return []
    try:
        latitude = float(latitude)
    except:
        latitude = 0
    try:
        longitude = float(longitude)
    except:
        longitude = 0
    angel_delta = radius / DISTANCE_DELTA

    precision = 0
    angel_area = 90.  # 180 / 2

    # 计算需要多少位(bit)
    while angel_delta <= angel_area:
        precision += 1
        angel_area /= 2

    precision += 1  # 第一位 w/e，占据一位
    geo_code = encode(latitude, longitude, precision)
    nearby = neighbors(geo_code)
    nearby_dict = dict(nearby)

    # 合并 4 个方格为一个，9个方格还剩 6 个(1大5小)
    combine_list = []
    if geo_code[:-1] == nearby_dict["S"][:-1]:
        combine_list.append("S")
    elif geo_code[:-1] == nearby_dict["N"][:-1]:
        combine_list.append("N")

    if geo_code[:-1] == nearby_dict["E"][:-1]:
        combine_list.append("E")
    elif geo_code[:-1] == nearby_dict["W"][:-1]:
        combine_list.append("W")

    if len(combine_list) == 2:
        corner = "".join(combine_list)
        # 如果 4 个方格的前 length - 1 个字节是一样的，它们可以合并为一个大方格
        if geo_code[:-1] == nearby_dict[corner][:-1]:
            nearby_dict.pop(combine_list[0])
            nearby_dict.pop(combine_list[1])
            nearby_dict.pop(corner)

            geo_code = geo_code[:-1]

    return [geo_code] + nearby_dict.values()


def compute_distance(lat1, lon1, lat2, lon2):
    """
    算两个经纬度间距离（米）
    """
    pi = math.pi
    try:
        lat1 = float(lat1) * pi / 180
    except:
        lat1 = 0
    try:
        lon1 = float(lon1) * pi / 180
    except:
        lon1 = 0
    try:
        lat2 = float(lat2) * pi / 180
    except:
        lat2 = 0
    try:
        lon2 = float(lon2) * pi / 180
    except:
        lon2 = 0

    # 地球半径(km)
    radius = 6371
    return int(math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) *
                         math.cos(lat2) * math.cos(lon1 - lon2)) * radius * 1000)


if __name__ == "__main__":
    t = nearby_geocode(126.333, 39.888, DISTANCE_DELTA * 40)
    print t
    t = nearby_geocode(126.333, 39.888, DISTANCE_DELTA * 20)
    print t
    t = nearby_geocode(126.333, 39.888, DISTANCE_DELTA * 10)
    print t
    t = nearby_geocode(126.333, 39.888, DISTANCE_DELTA * 5)
    print t
    t = nearby_geocode(126.333, 39.888, DISTANCE_DELTA)
    print t

    t = nearby_geocode(126.333, 39.888, 500)
    print t

    t = nearby_geocode(126.333, 39.888, 400)
    print t