import pygame as pg
import numpy as np
import os, random
import pygame_menu
from pygame.locals import *

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

def saveGame(filename):
    '''
    Сохранение уровня, игрока, индекса текущего уровня в filename.json
    '''
    global levels
    global player
    global current_player_index
    filename += '.json'
    path_name = os.path.join('saves', filename)
    save_data(levels, player, current_level_index, path_name)    


def loadGame(filename):
    '''
    Загрузка уровня, игрока, индекса текущего уровня из filename.json
    Если файла не существует, то в консоли выведится ошибка.
    '''
    global levels
    global player
    global current_player_index
    filename += '.json'
    path_name = os.path.join('saves', filename)
    try:
        levels, player, current_level_index = load_data(path_name)
    except FileNotFoundError:
        print('Файл не найден!')

def endGame():
    '''
    Меню конца игры. Может заново запустить main()
    '''
    global screen
    global current_level_index
    game_over_menu = pygame_menu.Menu('Конец игры', 800, 800,
                                      theme=pygame_menu.themes.THEME_BLUE)
    game_over_menu.add.label(('Уровень ' + str(current_level_index + 1)),
                             max_char=-1, font_size=40)
    game_over_menu.add.label('Вы умерли', max_char=-1, font_size=20)
    game_over_menu.add.button('Выйти в главное меню', main)
    game_over_menu.add.button('Выход', pg.quit)
    game_over_menu.mainloop(screen)



def checkPlayerOnLevel():
    '''Проверка местонахождения игрока в пределах уровня
    '''
    global player
    global current_level_index
    global levels

    #Переход игрока на другой уровень, если он рядом с дверьми
    if player.x >= 9.5 and player.x <= 10.5 and player.y >= 19 and not anyEnemyLeft:
        current_level_index += 1
        player.y = 1.01
    if player.x >= 9.5 and player.x <= 10.5 and player.y <= 1 and not anyEnemyLeft:
        if current_level_index > 0:
            current_level_index -= 1
            player.y = 18.99
            
    #Создание нового уровня, если индекс текущего уровня выходит за пределы массива
    #уровней
    if current_level_index + 1 > len(levels):
        createNewLevel()

    #Удержание игрока в пределах уровня    
    if player.x >= 20 - player.r:
        player.x = 20 - player.r
    if player.x <= player.r:
        player.x = player.r
    if player.y >= 20 - player.r:
        player.y = 20 - player.r
    if player.y <= player.r:
        player.y = player.r

def checkEntityInWalls(obj, level):
    '''
    Проверка, находится ли объект в obj в какой-либо из стен уровня level.
    obj - объект класса Entity,
    level - объект класса Level
    '''
    points = [(obj.x - obj.r / (2)**(1/2), obj.y - obj.r / (2)**(1/2)),
              (obj.x + obj.r / (2)**(1/2), obj.y - obj.r / (2)**(1/2)),
              (obj.x - obj.r / (2)**(1/2), obj.y + obj.r / (2)**(1/2)),
              (obj.x + obj.r / (2)**(1/2), obj.y + obj.r / (2)**(1/2)),
              (obj.x, obj.y - obj.r),
              (obj.x + obj.r, obj.y),
              (obj.x, obj.y + obj.r),
              (obj.x - obj.r, obj.y)]
               
    for i in level.obj_list:
        if i.type == "wall":
            if i.point_in_obj(points[4]):
                obj.y = i.y + i.size + obj.r
            elif i.point_in_obj(points[5]):
                obj.x = i.x - obj.r
            elif i.point_in_obj(points[6]):
                obj.y = i.y - obj.r
            elif i.point_in_obj(points[7]):
                obj.x = i.x + i.size + obj.r

def createNewLevel():
    '''
    Создание нового уровня из библиотеки уровней
    '''
    global levels
    new_level_name = random.choice(os.listdir("levels\\"))
    new_level = read_new_level(os.path.join("levels", new_level_name))
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
    
    for i in levels[current_level_index].obj_list:
        #Обработка живых существ на уровне (кроме игрока)
        if i.living:
            #Проверка на смерть
            if i.health <= 0:
                levels[current_level_index].obj_list.remove(i)
                continue
            #Проверка на видимость игрока
            if levels[current_level_index].line_of_sight((i.x, i.y),
                                                         (player.x, player.y)):
                angle = math.atan2((player.y - i.y), (player.x - i.x))
                #Движение к игроку при определённых условиях, поворот к игроку,
                #смена анимации движения
                if (not (i.type == "skelet" and
                         ((player.x - i.x) ** 2 + (player.y - i.y) ** 2 <= 9))
                    and not ((player.x - i.x) ** 2 + (player.y - i.y) ** 2 <= 1)):
                    i.move(angle)
                    if timer % 10 == 0:
                        i.changeTexture("move")
                i.look_at(angle)
                #Атака при определённых условиях
                if (((player.x - i.x) ** 2 + (player.y - i.y) ** 2 <= 2.25
                     or i.type == "skelet")
                    and timer % 30 == 0):
                    i.changeTexture("attack")
                    new_list, player = i.attack((player.x, player.y),
                                                levels[current_level_index].obj_list,
                                                player)
                    levels[current_level_index].obj_list = new_list
            #Проверка на столкновение со стенами
            checkEntityInWalls(i, levels[current_level_index])

        #Обработка поведения стрел: попадание в сущности, стены или границы уровня
        if i.type == "arrow":
            new_list, player = i.move(levels[current_level_index], player)
            levels[current_level_index].obj_list = new_list
            if i.x >= 20 or i.x <= 0 or i.y >= 20 or i.y <= 0:
                levels[current_level_index].obj_list.remove(i)
def mainMenu():
    '''
    Функция, создающая главное меню.
    '''
    menu = pygame_menu.Menu('Главное меню', 800, 800,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть', mainloop)
    menu.add.button('Сохранить', save_menu)
    menu.add.button('Загрузить', load_menu)
    menu.add.button('Выход', pg.quit)
    return menu

def saveMenu():
    '''
    Функция, создающая подменю сохранения игры
    '''
    saveMenu = pygame_menu.Menu('Сохранение', 800, 800,
                                theme=pygame_menu.themes.THEME_BLUE)
    saveMenu.add.label('Введите название сохранения', max_char=-1,
                   font_size=40)
    saveMenu.add.text_input('', default='New save', maxchar=20, onreturn=saveGame)
    saveMenu.add.label('Нажмите ENTER, чтобы подтвердить выбор', max_char=-1,
                       font_size=40)
    saveMenu.add.button('Назад', pygame_menu.events.BACK)
    return saveMenu

def loadMenu():
    '''
    Функция, создающая подменю загрузки игры
    '''
    loadMenu = pygame_menu.Menu('Загрузка', 800, 800,
                                theme=pygame_menu.themes.THEME_BLUE)
    loadMenu.add.label('Введите название сохранения', max_char=-1,
                   font_size=40)
    loadMenu.add.text_input('', default='New save', maxchar=20, onreturn=loadGame)
    loadMenu.add.label('Нажмите ENTER, чтобы подтвердить выбор', max_char=-1,
                       font_size=40)
    loadMenu.add.button('Назад', pygame_menu.events.BACK)
    return loadMenu


def main():
    '''
    Первый запуск главного меню
    '''
    global levels
    global player
    global current_level_index
    global timer
    global screen
    global drawer
    global main_menu
    global save_menu
    global load_menu

    #Обнуление всех игровых переменных
    levels = []
    player = []
    current_level_index = 0
    timer = 0
    screen = []
    drawer = []
    main_menu = []

    #Инициализация pygame и окна
    pg.init()

    flags = DOUBLEBUF
    width = 800
    height = 800
    screen = pg.display.set_mode((width, height), flags)
    drawer = Drawer(screen)

    setPlayer()

    #Создание менюшек и запуск главного меню
    save_menu = saveMenu()
    load_menu = loadMenu()
    main_menu = mainMenu()
    main_menu.mainloop(screen)

def mainloop():
    '''
    Фунция основного цикла игры
    '''
    global levels
    global player
    global current_level_index
    global timer
    global screen
    global drawer
    global main_menu
    global save_menu
    global load_menu

    
    alive = True

    #Двигался или атаковал ли игрок недавно
    hasMoved = False
    hasAttacked = False

    #Есть ли враги на уровне
    anyEnemyLeft = True

    #Основной цикл
    while alive:
        #Проверка на нахождение игрока в пределах уровня
        checkPlayerOnLevel(anyEnemyLeft)

        #Обнуление информации о движении и атаке
        hasMoved = False
        if timer % 15 == 0:
            hasAttacked = False

        #Обработка событий игрока
        for event in pg.event.get():
            #Выход
            if event.type == pg.QUIT:
                alive = False
                pg.quit()
            #Кнопки на клавиатуре
            elif event.type == pg.KEYDOWN:
                #Выход в меню
                if event.key == pg.K_ESCAPE:
                    alive = False
                    main_menu.mainloop(screen)
                #Смена оружия
                elif event.key == pg.K_f:
                    if player.weapon.type == "sword":
                        player.weapon = Bow()
                    else:
                        player.weapon = Sword()
            #Атака, если игрок не атаковал недавно
            elif event.type == pg.MOUSEBUTTONDOWN and not attackedAlready:
                attack_position = ((event.pos[0] - 20) / 760 * 20,
                                   (event.pos[1] - 20)/760 * 20)
                if not hasAttacked:
                    attack_pos_rel = ((event.pos[0] - 20) / 760 * 20 - player.x,
                                  (event.pos[1] - 20)/760 * 20 - player.y)
                    attack_pos_rel = (min(player.weapon.reach * math.cos(player.facing_angle), attack_pos_rel[0]),
                                      min(player.weapon.reach * math.sin(player.facing_angle), attack_pos_rel[1]))
                    attack_pos = (attack_pos_rel[0] + player.x, attack_pos_rel[1] + player.y)
                    
                    new_obj = player.attack(attack_pos,
                                            levels[current_level_index].obj_list)
                    levels[current_level_index].obj_list = new_obj
                    hasAttacked = True
                    player.changeTexture("attack")
            #Направление взгляда персонажа
            elif event.type == pg.MOUSEMOTION:
                angle = math.atan2(((event.pos[1] - 20) / 760 * 20 - player.y),
                                   ((event.pos[0] - 20)/760 * 20 - player.x))
                player.look_at(angle)

        #Обработка движения персонажа
        if pg.key.get_pressed()[pg.K_s]:
            player.move(math.pi/2)
            hasMoved = True
        if pg.key.get_pressed()[pg.K_w]:
            player.move(-math.pi/2)
            hasMoved = True
        if pg.key.get_pressed()[pg.K_d]:
            player.move(0)
            hasMoved = True
        if pg.key.get_pressed()[pg.K_a]:
            player.move(math.pi)
            hasMoved = True

        #Проверка, находится ли игрок в стене
        checkEntityInWalls(player, levels[current_level_index])

        #Анимация движения
        if hasMoved and not hasAttacked and timer % 10 == 0:
            player.changeTexture("move")

        #Проверка на наличие врагов на уровне
        anyEnemyLeft = any([i.living for i in levels[current_level_index].obj_list])
            
        #Интеллект мобов
        entity_ai()

        #Проверка персонажа на смерть
        if player.health <= 0:
            endGame()

        #Рисование на экране, если программа ещё работает
        if alive:
            drawer.update(levels[current_level_index], player,
                          current_level_index)


        #Увеличение таймера (от него зависит скорость атаки всех сущностей)
        timer += 1
        
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()

