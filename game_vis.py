import pygame as pg

def drawLevel(isOpened):
    if isOpened:
        pass
    else:
        pass

def scale_x(x):
    return x

def scale_y(y):
    return y

class Drawer:
    def __init__(self, screen):
        self.screen = screen


    def update(self, level, player):
        self.screen.fill((0, 0, 0))
        for obj in objects:
            obj.draw(self.screen)
        
        pg.display.update()
        
