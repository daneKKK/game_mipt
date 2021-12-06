import pygame as pg
import numpy as np
import os, random

from game_objects import *
from game_input import *
from game_vis import *

#Переменные для отсчёта времени
FPS = 30
clock = pg.time.Clock()
timer = 0

#Данные по игре
levels = []
player = []
current_level_index = 0
isOpened = False
attackedAlready = False

#Жива ли программа
alive = True


def load_save(filename):
    #Загрузка сейва
    global levels
    global player
    global current_level_index
    try:
        levels, player, current_level_index = load_data(filename)
    except FileNotFoundError:
        print('Файл не найден!')

def checkPlayerOnLevel():
    '''Проверка местонахождения игрока на уровне
    '''
    global player
    global current_level_index
    global levels
    if player.x >= 9.5 and player.x <= 10.5 and player.y >= 19:
        current_level_index += 1
        player.y = 1.01
    if player.x >= 9.5 and player.x <= 10.5 and player.y <= 1:
        if current_level_index > 0:
            current_level_index -= 1
            player.y = 18.99
    if current_level_index + 1 > len(levels):
        createNewLevel()
    if player.x >= 20 - player.r:
        player.x = 20 - player.r
    if player.x <= player.r:
        player.x = player.r
    if player.y >= 20 - player.r:
        player.y = 20 - player.r
    if player.y <= player.r:
        player.y = player.r

    

def createNewLevel():
    '''
    Создание нового уровня из библиотеки уровней
    '''
    global levels
    new_level_name = random.choice(os.listdir("levels\\"))
    new_level = read_level_objects_data(os.path.join("levels", new_level_name))
    levels += [new_level]

def setPlayer():
    '''
    Создание нового игрока
    '''
    global player

    player = Player(10, 1)

def entity_ai():
    '''
    Обработка действий мобов
    '''
    global timer
    global player
    global levels
    global current_level_index
    #if timer % 30 != 0:
    #    return
    for i in levels[current_level_index].obj_list:
        if i.living:
            if i.health <= 0:
                levels[current_level_index].obj_list.remove(i)
                continue
            if levels[current_level_index].line_of_sight((i.x, i.y),
                                                         (player.x, player.y)):
                angle = math.atan2((player.y - i.y), (player.x - i.x))
                i.move(angle)
                i.look_at(angle)
                if (((player.x - i.x) ** 2 + (player.y - i.y) ** 2 <= 1
                     or i.type == "skelet")
                    and timer % 30 == 0):
                    new_list, player = i.attack((player.x, player.y),
                                                levels[current_level_index].obj_list,
                                                player)
                    levels[current_level_index].obj_list = new_list
        if i.type == "arrow":
            new_list, player = i.move(levels[current_level_index], player)
            levels[current_level_index].obj_list = new_list
            #i.move(levels[current_level_index])
def main():
    global levels
    global player
    global current_level_index
    global timer

    pg.init()

    setPlayer()

    width = 800
    height = 800
    screen = pg.display.set_mode((width, height))
    drawer = Drawer(screen)

    alive = True

    while alive:
        anyEnemyLeft = False
        
        drawLevel(isOpened)


        checkPlayerOnLevel()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                alive = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    alive = False
                    pg.quit()
                elif event.key == pg.K_f:
                    print(levels[current_level_index])
            elif event.type == pg.MOUSEBUTTONDOWN and not attackedAlready:
                print(event.pos)
                print(((event.pos[0] - 20) / 760 * 20, (event.pos[1] - 20)/760 * 20))
                new_obj = player.attack(((event.pos[0] - 20) / 760 * 20,
                                         (event.pos[1] - 20)/760 * 20),
                                        levels[current_level_index].obj_list)
                levels[current_level_index].obj_list = new_obj
                    
        if pg.key.get_pressed()[pg.K_s]:
            player.move(math.pi/2)
        if pg.key.get_pressed()[pg.K_w]:
            player.move(-math.pi/2)
        if pg.key.get_pressed()[pg.K_d]:
            player.move(0)
        if pg.key.get_pressed()[pg.K_a]:
            player.move(math.pi)

        for i in levels[current_level_index].obj_list:
            if i.living:
                anyEnemyLeft = True

        entity_ai()
        
        if alive:
            drawer.update(levels[current_level_index], player)



        timer += 1
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()

