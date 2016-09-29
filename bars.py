# -*- coding: utf-8 -*-
import json
import sys
import math
import os
reload(sys)
import locale
sys.setdefaultencoding(locale.getpreferredencoding())

def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)

def get_biggest_bar(data):
    biggest_bar = data[0]
    for bar in data:
        if bar["Cells"]["SeatsCount"] > biggest_bar["Cells"]["SeatsCount"]:
            biggest_bar = bar

    return biggest_bar


def get_smallest_bar(data):
    smallest_bar = data[0]
    for bar in data:
        if bar["Cells"]["SeatsCount"] < smallest_bar["Cells"]["SeatsCount"]:
            smallest_bar = bar
    return smallest_bar


def get_ort_distance(latitude_1, longitude_1, latitude_2, longitude_2):  # Расчет ортодромии
    latitude_1 = math.radians(latitude_1)
    latitude_2 = math.radians(latitude_2)
    longitude_1 = math.radians(longitude_1)
    longitude_2 = math.radians(longitude_2)
    earth_radius = 6371
    latitude_delta = abs(latitude_2 - latitude_1)
    longitude_delta = abs(longitude_2 - longitude_1)
    central_angle = 2*math.asin(math.sqrt(math.pow(math.sin(latitude_delta/2), 2)
                                          + math.cos(latitude_1)*math.cos(latitude_2)*math.pow(math.sin(longitude_delta/2), 2)))
    return earth_radius*central_angle


def get_closest_bar(data, longitude, latitude):

    closest_bar = data[0]
    least_distance = get_ort_distance(latitude, longitude, closest_bar["Cells"]["geoData"]["coordinates"][0],
                        closest_bar["Cells"]["geoData"]["coordinates"][1])

    for bar in data:
        new_distance = get_ort_distance(latitude, longitude, bar["Cells"]["geoData"]["coordinates"][1],
                                        bar["Cells"]["geoData"]["coordinates"][0])

        if new_distance < least_distance:
            least_distance = new_distance
            closest_bar = bar
    print(least_distance)
    return closest_bar


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
                print(u'Пожалуйста, введите местоположение заного')
                continue
        break

    data = load_data('Bars.json')
    if data is None:
        print (u'Данных нет или указан неверный путь к файлу')
    else:
        biggest_bar = get_biggest_bar(data)
        smallest_bar = get_smallest_bar(data)
        closest_bar = get_closest_bar(data, longitude, latitude)
        # Вывод найденных баров
        print(u'Самый большой бар: %s, адрес: %s количество мест: %i' % (biggest_bar["Cells"]["Name"],
                                                                         biggest_bar["Cells"]["Address"],
                                                                         biggest_bar["Cells"]["SeatsCount"]))
        print(u'Caмый маленький бар: %s, адрес: %s количество мест: %i' % (smallest_bar["Cells"]["Name"],
                                                                           smallest_bar["Cells"]["Address"],
                                                                           smallest_bar["Cells"]["SeatsCount"]))
        print(u'Ближайший к вам бар: %s, адрес: %s количество мест: %i' % (closest_bar["Cells"]["Name"],
                                                                           closest_bar["Cells"]["Address"],
                                                                           closest_bar["Cells"]["SeatsCount"]))
