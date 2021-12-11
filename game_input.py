#Этот файл занимается считыванием возможных комнат, сохранением игры, загрузкой
import json
from random import randint as rnd

from game_objects import *


def read(filename):
    '''
    Читает json файл и возвращает информацию из него
    '''
    with open(filename, 'r') as file:
        return json.load(file)


def write(data, filename):
    '''
    Записывает информацию в json файл
    '''
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def read_new_level(filename):
   '''
   Берёт filename, достаёт из него информацию, прогоняет
   её через read_level_objects_data и возвращает результат
   '''
    level = read(filename)
    return read_level_objects_data(level)


def read_level_objects_data(data):
    '''
    Принимает массив уровня и возвращает уровень, как объект
    '''
    
    level = data
    level_object = Level()
    level_object.obj_list = []
    for obj in level:
        if obj == 'spiders':
            for i in range(len(level[obj])):
                spider =read_spider_data(level[obj], i)
                level_object.obj_list.append(spider)
        if obj == 'skelets':
            for i in range(len(level[obj])):
               skelet = read_skelet_data(level[obj], i)
               level_object.obj_list.append(skelet)
        if obj == 'walls':
            for i in range(len(level[obj])):
                wall = read_wall_data(level[obj], i)
                level_object.obj_list.append(wall)

    return level_object


def read_spider_data(line, spider_number):
    '''
    Пример:
    Spider 10 10
    Spider <x> <y>
    s - кол-во пауков в файле
    '''
    x = line[spider_number][0]
    y = line[spider_number][1]
    return Spider(x, y)
    

def read_skelet_data(line, skelet_number):
    '''
    Skelet <x> <y>
    s - кол-во скелетов в файле
    '''
    x = line[skelet_number][0]
    y = line[skelet_number][1]
    return Skelet(x, y)


def read_wall_data(line, wall_number):
    '''
    Wall <x> <y>
    s - кол-во стен в файле
    '''
    x = line[wall_number][0]
    y = line[wall_number][1]
    return Wall(x, y)


def save_data(levels, character, current_level_index, filename):
    '''
    Сохраняет игру в json файл
    '''
    data = [i.toJSON() for i in levels]
    data += [character.toJSON(current_level_index)]
    write(data, filename)


def load_data(filename):
    '''
    Выполняет загрузку levels и character из файла failname
    '''
    data = read(filename)
    levels = [read_level_objects_data(data[i]) for i in range(len(data)) if i < len(data) - 1]
    character = Player()
    character.health = float(data[len(data)-1]['health'])
    character.x = float(data[len(data)-1]['x'])
    character.y = float(data[len(data)-1]['y'])
    current_level_index = int(data[len(data)-1]['current_level'])
    return levels, character, current_level_index

#в мейне:
#information = load_data(save.json)
# =

    
