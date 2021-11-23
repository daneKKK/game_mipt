#Этот файл занимается считыванием возможных комнат, сохранением игры, загрузкой

def read_level_objects_data(filename):

    #level.object_list += [spider, wall]
    
    level = Level()
    level.object_list += [spider]
    ...

    ...

    return level


def read_spider_data(line):
    '''
    Пример:
    Spider 10 10

    Spider <x> <y>
    '''
    
    pass

def read_wall_data(line):
    '''
    
    '''
    pass


def save_data(levels, character):
    #saves/[name].json
    #Level 1: object_list = [spider, wall, bomb]
    #Level 2: list = ...
    #...
    #Character: [health, gold, weapon]

def load_data(filename):
    #распакуй мне [name].json в переменную list_of_objects_and_character
    #list_of_objects_and_character[последний индекс] = character
    #return list...

#в мейне:
#information = load_data(save.json)
# =

    
