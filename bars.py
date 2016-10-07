# -*- coding: utf-8 -*-
from json import load
from math import radians, asin, cos, sqrt, sin
from os.path import exists


def load_data(filepath):
    if not exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return load(file_handler)


def get_biggest_bar(data):
    return max(data, key=lambda x: get_seats_count(x))

def get_seats_count(list):
    return list["Cells"]["SeatsCount"]


def get_coordinates(list):
    return list["Cells"]["geoData"]["coordinates"]


def get_smallest_bar(data):
    return min(data, key=lambda x: get_seats_count(x))

def get_ort_distance(latitude_1, longitude_1, latitude_2, longitude_2):  # Расчет ортодромии
    latitude_1 = radians(latitude_1)
    latitude_2 = radians(latitude_2)
    longitude_1 = radians(longitude_1)
    longitude_2 = radians(longitude_2)
    earth_radius = 6371
    latitude_delta = abs(latitude_2 - latitude_1)
    longitude_delta = abs(longitude_2 - longitude_1)
    central_angle = 2*asin(sqrt((sin(latitude_delta/2))**2 + cos(latitude_1)*cos(latitude_2)
                                * (sin(longitude_delta/2))**2))
    return earth_radius*central_angle


def get_closest_bar(data, longitude, latitude):

    return min(data, key=lambda x: get_ort_distance(latitude, longitude, get_coordinates(x)[0], get_coordinates(x)[1]))

if __name__ == '__main__':

    # Ввод текущего местоположения
    while True:
        print(u'Введите координаты вашего местоположения')
        try:
            latitude = float(input(u'Введите широту: '))
        except NameError:
            latitude = None
        if latitude is None:
            print(u'Пожалуйста, введите широту заного')
            continue
        try:
            longitude = float(input(u'Введите долготу: '))
        except NameError:
            if longitude is None:
                print(u'Пожалуйста, введите ваше местоположение заново')
                continue
        break

    filepath = raw_input(u'Введите путь к файлу с данными о барах:')
    data = load_data(filepath)
    if data is None:
        print (u'Данных нет или указан неверный путь к файлу')
    else:
        biggest_bar = get_biggest_bar(data)['Cells']
        smallest_bar = get_smallest_bar(data)['Cells']
        closest_bar = get_closest_bar(data, longitude, latitude)['Cells']
        # Вывод найденных баров
        print(u'Самый большой бар: %s, адрес: %s количество мест: %i' % (biggest_bar["Name"],
                                                                         biggest_bar["Address"],
                                                                         biggest_bar["SeatsCount"]))
        print(u'Caмый маленький бар: %s, адрес: %s количество мест: %i' % (smallest_bar["Name"],
                                                                           smallest_bar["Address"],
                                                                           smallest_bar["SeatsCount"]))
        print(u'Ближайший к вам бар: %s, адрес: %s количество мест: %i' % (closest_bar["Name"],
                                                                           closest_bar["Address"],
                                                                           closest_bar["SeatsCount"]))
