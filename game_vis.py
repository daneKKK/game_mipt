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

    def rot_center(image, angle):

        """rotate an image while keeping its center and size"""

        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw_entity(self, obj):
        texture_surface = pg.image.load(obj.texturepath)
        texture_surface = pg.transform.scale(texture_surface, (scale_size(obj.r), (scale_size(obj.r))))
        texture_surface = self.rot_center(texture_surface, obj.facing_angle)
        self.screen.blit(texture_surface, (scale_x(obj.x - obj.r), scale_y(obj.y - obj.r)))

    def draw_wall(self, obj):
        pg.draw.rect(self.screen, (0, 0, 0),
                     (scale_x(obj.x), scale_y(obj.y),
                      scale_size(obj.size), scale_size(obj.size)))

    def draw_arrow(self, obj):
        pg.draw.circle(self.screen, (100, 100, 100),
                       (scale_x(obj.x), scale_y(obj.y)), 4)
        
        
