import pygame as pg
import math

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
        for obj in level.obj_list:
            if obj.living:
                self.drawHPbar(obj)
        self.draw(player)
        
        pg.display.update()



    def draw(self, obj):
        if obj.living:
            self.draw_entity(obj)
        elif obj.type == "wall":
            self.draw_wall(obj)
        elif obj.type == "arrow":
            self.draw_arrow(obj)

    def rot_center(self, image, angle):

        """rotate an image while keeping its center and size"""

        angle = 270 - angle * 180 / math.pi
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw_entity(self, obj):
        texture_surface = pg.image.load(obj.texturepath).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (int(3 * scale_size(obj.r)), int(3 * scale_size(obj.r))))
        texture_surface = self.rot_center(texture_surface, obj.facing_angle)
        self.screen.blit(texture_surface, (scale_x(obj.x - obj.r), scale_y(obj.y - obj.r)))

    def draw_wall(self, obj):
        texture_surface = pg.image.load(obj.texturepath).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (int(scale_size(obj.size)), int(scale_size(obj.size))))
        self.screen.blit(texture_surface, (scale_x(obj.x), scale_y(obj.y)))

    def draw_arrow(self, obj):
        texture_surface = pg.image.load(obj.texturepath).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (int(2 * scale_size(obj.r)), int(2 * scale_size(obj.r))))
        texture_surface = self.rot_center(texture_surface, obj.angle)
        self.screen.blit(texture_surface, (scale_x(obj.x - obj.r), scale_y(obj.y - obj.r)))
        
    def drawHPbar(self, obj):
        hp_rect_width = obj.health / obj.max_health * 3 * scale_size(obj.r)
        hp_rect_coords = (scale_x(obj.x) - hp_rect_width / 2,
                          scale_y(obj.y - obj.r) - 4,
                          hp_rect_width, 4)
        pg.draw.rect(self.screen, (0, 255, 0), hp_rect_coords)
