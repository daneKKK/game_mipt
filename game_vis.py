import pygame as pg

def drawLevel(isOpened):
    if isOpened:
        pass
    else:
        pass

def scale_x(x):
    return 20 + x * 38

def scale_y(y):
    return 20 + y * 38

def scale_size(r):
    return r * 38

class Drawer:
    def __init__(self, screen):
        self.screen = screen


    def update(self, level, player):
        self.screen.fill((255, 255, 255))
        for obj in level.obj_list:
            self.draw(obj)

        self.draw(player)
        
        pg.display.update()



    def draw(self, obj):
        if obj.living:
            self.draw_entity(obj)
        elif obj.type == "wall":
            self.draw_wall(obj)
        elif obj.type == "arrow":
            self.draw_arrow(obj)

    def draw_entity(self, obj):
        pg.draw.circle(self.screen, (0, 0, 0),
                       (scale_x(obj.x), scale_y(obj.y)), scale_size(obj.r))

    def draw_wall(self, obj):
        pg.draw.rect(self.screen, (0, 0, 0),
                     (scale_x(obj.x), scale_y(obj.y),
                      scale_size(obj.size), scale_size(obj.size)))
        
        
