#Этот файл занимается считыванием возможных комнат, сохранением игры, загрузкой
import json
from random import randint as rnd

from game_objects import *

def read(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def read_level_objects_data(filename):
    '''
    i_spider, i_skelet, i_wall отвечают за кол-во спавнящихся Entity min = 0 max = 4 or 3
    Функция считывает файл формата json, ищет в нём пауков,
    скелетов и стены, засовывает их в общий список объектов
    '''

    spider_amount = rnd(0, 4)
    skelet_amount = rnd(0, 3)
    wall_amount = rnd(0, 3)

    i_spider = 0
    i_skelet = 0
    i_wall = 0
    
    level = read(filename)
    level_object = Level()
    for obj in level:
        if obj == 'spiders':
            while i_spider < spider_amount:
                spider = Spider()
                read_spider_data(level[obj], spider, i_spider)
                level_object.obj_list.append(spider)
                i_spider += 1
        if obj == 'skelets':
            while i_skelet < skelet_amount:
                skelet = Skelet()
                read_skelet_data(level[obj], skelet, i_skelet)
                level_object.obj_list.append(skelet)
                i_skelet += 1
        if obj == 'walls':
            while i_wall < wall_amount:
                wall = Wall()
                wall_number = 4 - i_wall
                read_wall_data(level[obj], wall, i_wall)
                level_object.obj_list.append(wall)
                i_wall += 1

    return level_object





def read_spider_data(line, spider,spider_number):
    '''
    Пример:
    Spider 10 10
    Spider <x> <y>
    s - кол-во пауков в файле
    '''
    spider.x = line[spider_number][0]
    spider.y = line[spider_number][1]
    
    pass


def read_skelet_data(line, skelet, skelet_number):
    '''
    Skelet <x> <y>
    s - кол-во скелетов в файле
    '''
    skelet.x = line[skelet_number][0]
    skelet.y = line[skelet_number][1]
    pass

def read_wall_data(line,wall,wall_number):
    '''
    Wall <x> <y>
    s - кол-во стен в файле
    '''
    wall.x = line[wall_number][0]
    wall.y = line[wall_number][1]
    pass


def save_data(levels, character, filename):
    #saves/[name].json
    #Level 1: object_list = [spider, wall, bomb]
    #Level 2: list = ...
    #...
    #Character: [health, gold, weapon]
    data = [i.toJSON() for i in levels]
    data += [character.toJSON()]
    write(data, filename)


def load_data(filename):
    #распакуй мне [name].json в переменную list_of_objects_and_character
    #list_of_objects_and_character[последний индекс] = character
    #return list...
    data = read(filename)
    levels = [data[i] for i in range(len(data)) if i < len(data) - 1]
    character = data[len(data) - 1]
    return levels, character




#в мейне:
#information = load_data(save.json)
# =

    
