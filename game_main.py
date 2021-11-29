import pygame as pg
import numpy as np

from game_objects import *
from game_input import *
from game_vis import *

FPS = 30
clock = pg.time.Clock()
timer = 0

levels = []
player = []
current_level_index = 0
alive = True
isOpened


def load_save(filename):
    global levels
    global player
    global current_level_index
    try:
        levels, player, current_level_index = load_data(filename)
    except FileNotFoundError:
        print('Файл не найден!')

def checkPlayerOnLevel():
    pass

def createNewLevel():
    global levels
    new_level = []
    levels += [new_level]

def setPlayer():
    global player

    player = Player()

def entity_ai(entity, level, player):
    global timer
    pass

def main():
    global levels
    global player
    global current_level_index

    pg.init()

    setPlayer()

    width = 800
    height = 800
    screen = pg.display.set_mode((width, height))

    while alive:
        screen.fill((255, 255, 255))
        anyEnemyLeft = False
        
        drawLevel(isOpened)


        checkPlayerOnLevel()
        
        for event in pg.event.get():
            pass

        for i in levels[current_level_index].obj_list:
            if i.living:
                i, obj_list, player = entity_ai(i, obj_list, player)
                anyEnemyLeft = True
            draw(i, screen)

        draw(player, screen)



        timer += 1
        clock.tick(FPS)
    
    
