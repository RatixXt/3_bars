# -*- coding: utf-8 -*-
import json
import sys
import math

reload(sys)
import locale
sys.setdefaultencoding(locale.getpreferredencoding())

def load_data(filepath):
    json_data = open(filepath)
    data = json.load(json_data)

    return data


def get_biggest_bar(data):
    big = data[0]
    for num in data:
        if num["Cells"]["SeatsCount"] > big["Cells"]["SeatsCount"]:
            big = num

    return big


def get_smallest_bar(data):
    small = data[0]
    for num in data:
        if num["Cells"]["SeatsCount"] < small["Cells"]["SeatsCount"]:
            small = num
    return small

def ortodrom(a_1, b_1, a_2, b_2):  # Расчет ортодромии
    a_1 = math.radians(a_1)
    a_2 = math.radians(a_2)
    b_1 = math.radians(b_1)
    b_2 = math.radians(b_2)
    res = math.acos(math.sin(a_1)*math.sin(a_2)+math.cos(a_1)*math.cos(a_2)*math.cos(b_2 - b_1))
    return 111.7*res

def get_closest_bar(data, longitude, latitude):

    nearest = data[0]
    near_ort = ortodrom(latitude, longitude, nearest["Cells"]["geoData"]["coordinates"][0],
                        nearest["Cells"]["geoData"]["coordinates"][1])

    for num in data:
        new_ort = ortodrom(latitude, longitude, num["Cells"]["geoData"]["coordinates"][0],
                           num["Cells"]["geoData"]["coordinates"][1])
        if new_ort < near_ort:
            near_ort = new_ort
            nearest = num
    return nearest


if __name__ == '__main__':

    # Ввод текущего местоположения
    print(u'Введите координаты вашего местоположения')
    a = float(input(u'Введите широту: '))
    b = float(input(u'Введите долготу: '))

    data = load_data('Bars.json')
    big = get_biggest_bar(data)
    small = get_smallest_bar(data)
    nearest = get_closest_bar(data, b, a)
    # Вывод найденных баров
    print(u'Самый большой бар: ' + big["Cells"]["Name"] + u', адрес: ' + big["Cells"]["Address"]
          + u' количество мест: ' + str(big["Cells"]["SeatsCount"]))
    print(u"Caмый маленький бар: " + small["Cells"]["Name"] + u', адрес: ' + small["Cells"]["Address"]
          + u' количество мест: ' + str(small["Cells"]["SeatsCount"]))
    print(u"Ближайший к вам бар: " + nearest["Cells"]["Name"] + u', адрес: ' + nearest["Cells"]["Address"])
