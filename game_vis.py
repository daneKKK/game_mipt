import pygame as pg
import math, os

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


def drawFirstLevel(screen):
    background = os.path.join('resources', 'Pictures', 'Background', 'B1.png')
    texture_surface = pg.image.load(background).convert()
    screen.blit(texture_surface, (0, 0))

    pg.font.init()
    myFont = pg.font.SysFont('Calibri', 30)
    textSurface = myFont.render('Передвигайтесь с помощью WASD', False,
                                (255, 255, 255))
    width = textSurface.get_width()
    height = textSurface.get_height()
    screen.blit(textSurface, (400 - width // 2, 400))

    textSurface = myFont.render('Атакуйте с помощью ЛКМ', False,
                                (255, 255, 255))
    width = textSurface.get_width()
    height2 = textSurface.get_height()
    screen.blit(textSurface, (400 - width // 2, 400 + height + 2))

    textSurface = myFont.render('Нажмите F для смены оружия', False,
                                (255, 255, 255))
    width = textSurface.get_width()
    height3 = textSurface.get_height()
    screen.blit(textSurface, (400 - width // 2, 400 + height + height2 + 4))

    textSurface = myFont.render('ESCAPE для выхода в меню', False,
                                (255, 255, 255))
    width = textSurface.get_width()
    screen.blit(textSurface, (400 - width // 2,
                              400 + height + height2 + height3 + 6))

class Drawer:

    optimized_walls = []
    wall_optimizing = False
    
    def __init__(self, screen):
        self.screen = screen


    def update(self, level, player, current_level_index):
        if any ([i.living for i in level.obj_list]):
            self.drawClosedLevel()
        else:
            self.drawOpenedLevel()

        self.current_index = current_level_index

        if len(self.optimized_walls) <= current_level_index:
            wall_counter = 0
            for i in level.obj_list:
                if i.type == "wall":
                    wall_counter += 1
            self.optimized_walls += [wall_counter >= 50]

        self.wall_optimizing = self.optimized_walls[current_level_index]
            

        if current_level_index == 0:
            drawFirstLevel(self.screen)

        for obj in level.obj_list:
            self.draw(obj)
        for obj in level.obj_list:
            if obj.living:
                self.drawHPbar(obj)
        self.draw(player)
        for obj in level.obj_list:
            if obj.living:
                self.drawHPbar(obj)
        self.drawPlayerHP(player)
        self.drawWeaponIcon(player)
        self.drawLevelNumber(current_level_index)
        
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
        self.screen.blit(texture_surface, (scale_x(obj.x - obj.r * 1.5),
                                           scale_y(obj.y - obj.r  * 1.5)))

    def drawHPbar(self, obj):
        hp_rect_width = obj.health / obj.max_health * 3 * scale_size(obj.r)
        hp_rect_coords = (scale_x(obj.x) - hp_rect_width / 2,
                          scale_y(obj.y - obj.r) - 4,
                          hp_rect_width, 4)
        pg.draw.rect(self.screen, (0, 255, 0), hp_rect_coords)

    def drawPlayerHP(self, obj):
        hp_rect_width_red = 3 * scale_size(2)
        hp_rect_width_green = obj.health / obj.max_health * 3 * scale_size(2)
        pg.draw.rect(self.screen, (255, 0, 0), (2, 2,
                                                hp_rect_width_red, 11))
        pg.draw.rect(self.screen, (0, 255, 0), (2, 2,
                                                hp_rect_width_green, 11))
    def draw_wall(self, obj):
        if self.wall_optimizing:
            self.draw_optimized_wall(obj)
            return
        texture_surface = pg.image.load(obj.texturepath).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (int(scale_size(obj.size)), int(scale_size(obj.size))))
        self.screen.blit(texture_surface, (scale_x(obj.x), scale_y(obj.y)))

    def draw_optimized_wall(self, obj):
        pg.draw.rect(self.screen, (150, 150, 150), (scale_x(obj.x),
                                                    scale_y(obj.y),
                                                    scale_size(obj.size),
                                                    scale_size(obj.size)))
        

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

    def drawWeaponIcon(self, player):
        sword_icon = os.path.join('resources', 'squid1.png')
        bow_icon = os.path.join('resources', 'squid1.png')
        if player.weapon.type == "sword":
            pg.draw.rect(self.screen, (0, 0, 0), (600, 2, 40, 40))
        else:
            pg.draw.rect(self.screen, (0, 0, 0), (640, 2, 40, 40))

        texture_surface = pg.image.load(sword_icon).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (32, 32))
        self.screen.blit(texture_surface, (604, 4))

        texture_surface = pg.image.load(bow_icon).convert_alpha()
        texture_surface = pg.transform.scale(texture_surface, (32, 32))
        self.screen.blit(texture_surface, (644, 4))

    def drawLevelNumber(self, current_level_index):
        if current_level_index > 0:
            text = "Уровень: " + str(current_level_index)
        else:
            text = "Обучение"
        myFont = pg.font.SysFont('Calibri', 30)
        text_surface = myFont.render(text, False, (255, 255, 255))
        width = text_surface.get_width()
        self.screen.blit(text_surface, (400 - width // 2, 2))

    def drawOpenedLevel(self):
        texturepath = os.path.join('resources', 'Pictures', 'Background', 'Bcl.png')
        texture_surface = pg.image.load(texturepath).convert()
        self.screen.blit(texture_surface, (0, 0))

    def drawClosedLevel(self):
        texturepath = os.path.join('resources', 'Pictures', 'Background', 'Bop.png')
        texture_surface = pg.image.load(texturepath).convert()
        self.screen.blit(texture_surface, (0, 0))
