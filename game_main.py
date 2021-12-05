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
    if player.x >= 9.5 and player.x <= 10.5 and player.y <= 1:
        if current_level_index > 0:
            current_level_index -= 1
    if current_level_index + 1 > len(levels):
        createNewLevel()

    

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

    player = Player()
    player.x = 10
    player.y = 1

def entity_ai():
    '''
    Обработка действий мобов
    '''
    global timer
    global player
    global level
    global current_level_index
    pass

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
                    print(levels[current_level_index].obj_list)

        for i in levels[current_level_index].obj_list:
            if i.living:
                anyEnemyLeft = True

        entity_ai()
        
        if alive:
            drawer.update(levels[current_level_index], player)



        timer += 1
        clock.tick(FPS)
    

if __name__ == "__main__":
    main()

