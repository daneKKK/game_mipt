import math, json, os, random

#Этот файл хранит информацию о всех классах

class Level:
    '''
    Класс уровень. Должен хранить информацию о всех объектах на нём.
    '''

    x_border = 20
    y_border = 20
    
    obj_list = []

    def line_of_sight(self, pos1, pos2):
        '''
        Проверка на то, видна ли точка pos1 из точки pos2
        pos1, pos2 - пары чисел (координат)
        '''
        x1, y1 = pos1
        x2, y2 = pos2
        distance = math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2)
        i = 2
        while i <= distance:
            current_point = (x1 - i * (x1 - x2) / distance,
                             y1 - i * (y1 - y2) / distance)
            for obj in self.obj_list:
                if obj.point_in_obj(current_point):
                    return False
            i += 1
        x_border = self.x_border
        y_border = self.y_border
        return not (abs(x1 - x_border // 2) > x_border or abs(y1 - x_border // 2) > y_border
                    or abs(x2 - x_border // 2) > x_border or abs(y2 - x_border // 2) > y_border)
        return True

    
    def toJSON(self):
        spiders = [[i.x, i.y] for i in self.obj_list if i.type == "spider"]
        skelets = [[i.x, i.y] for i in self.obj_list if i.type == "skelet"]
        walls = [[i.x+0.5, i.y+0.5] for i in self.obj_list if i.type == "wall"]
        level_data = {"spiders": spiders, "skelets": skelets, "walls": walls}
        return level_data

#Подход к объектам: в целях упрощения просчёта столкновений объектов сделаем их
#минимальный размер, равный 0.5

class Entity:
    '''
    Класс всех живых объектов.
    '''
    x = 0
    y = 0
    r = 0.5
    max_health = 10
    health = 10
    speed = 1 / 30
    facing_angle = 0
    attack_value = 1
    attack_speed = 30
    living = True
    texture = None
    texturepath1 = os.path.join('resources', 'face.png')
    texturepath2 = os.path.join('resources', 'face.png')
    texturepath_atk = os.path.join('resources', 'face.png')
    texturepath = os.path.join('resources', 'face.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def changeTexture(self, action):
        if action == "attack":
            self.texturepath = self.texturepath_atk
        elif action == "move":
            if self.texturepath == self.texturepath1:
                self.texturepath = self.texturepath2
            else:
                self.texturepath = self.texturepath1
            

    def attack(self, attacked_pos, obj_list, player):
        '''
        Атака по всем объектам в  данной точке.
        attacked_pos - позиция, по которой атакует наш экземпляр класса
        obj_list - список объектов на уровне
        player - игрок
        '''
        for i in obj_list:
            if self == i:
                continue
            if i.point_in_obj(attacked_pos) and i.living:
                i.get_damage(self.attack_value)
        if player.point_in_obj(attacked_pos) and not (self is player):
            player.get_damage(self.attack_value)
        return obj_list, player
            

    def point_in_obj(self, point):
        '''
        Проверяет, находится ли точка в объекте
        point - кортеж с 2 координатами
        '''
        x, y = point
        distance = (x - self.x) ** 2 + (y - self.y) ** 2
        return distance <= self.r * self.r

    def move(self, angle):
        '''
        Передвижение по направлению на угол angle
        angle - угол в радианах
        '''
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def get_damage(self, attack):
        '''
        Нанесение урона объекту
        attack - float, нанесенный урон
        '''
        self.health -= attack

    def look_at(self, angle):
        '''
        Изменение угла, на который смотрит объект
        angle - угол в радианах
        '''
        self.facing_angle = angle

    def draw(self, screen):
        pass

class Spider(Entity):
    '''
    Класс Паук. Наследует от Entity
    '''
    type = "spider"
    texturepath1 = os.path.join('resources', 'Pictures', 'Spider', 's1.png')
    texturepath2 = os.path.join('resources', 'Pictures', 'Spider', 's2.png')
    texturepath_atk = os.path.join('resources', 'Pictures', 'Spider', 's5.png')
    texturepath = os.path.join('resources', 'Pictures', 'Spider', 's1.png')
    speed = 3 / 30



class Skelet(Entity):
    '''
    Скелет-лучник. Наследует от Entity. Атакует издалека.
    '''
    type = "skelet"
    texturepath1 = os.path.join('resources', 'Pictures', 'Enemy', 'e2.png')
    texturepath2 = os.path.join('resources', 'Pictures', 'Enemy', 'e6.png')
    texturepath_atk = os.path.join('resources', 'Pictures', 'Enemy', 'e1.png')
    texturepath = os.path.join('resources', 'Pictures', 'Enemy', 'e2.png')
    max_health = 15
    health = 15
    speed = 1 / 30
    attack_value = 2
    attack_speed = 60
    
    def attack(self, attacked_pos, obj_list, player):
        '''
        Особенный вид атаки - издалека.
        attacked_pos - точка, в которую наносится урон.
        obj_list, player - список объектов и игрок. Нужны для единообразия.
        '''
        
        self.look_at(math.atan2(attacked_pos[1]-self.y, attacked_pos[0]-self.x))
        new_arrow = Arrow()
        new_arrow.x = self.x + (self.r + 0.02) * math.cos(self.facing_angle)
        new_arrow.y = self.y + (self.r + 0.02) * math.sin(self.facing_angle)
        new_arrow.angle = self.facing_angle
        new_arrow.damage = self.attack_value
        obj_list += [new_arrow]
        return obj_list, player

class Weapon:
    '''
    Класс оружия.
    '''
    attack_value = 1
    reach = 2
    def attack(self, attack_position, obj_list):
        '''
        Атака оружия.
        attack_position - точка, в которую наносится атака.
        obj_list - лист объектов на уровне.
        '''
        for i in obj_list:
            if self == i or not i.living:
                continue
            if i.point_in_obj(attack_position):
                i.get_damage(attack_value)
        return obj_list
        

class Sword(Weapon):
    '''
    Меч. Наследует от Weapon.
    '''
    type = "sword"
    attack_value = 3
    def attack(self, attack_position, obj_list):
        '''
        Атака мечом. Аналогично Weapon.attack()
        '''
        for i in obj_list:
            if self == i or not i.living:
                continue
            if i.point_in_obj(attack_position):
                i.get_damage(self.attack_value)
        return obj_list

class Bow(Weapon):
    '''
    Лук. Наследует от Weapon.
    '''
    type = "bow"
    attack_value = 1
    def attack(self, attacked_pos, obj_list):
        '''
        Особенный вид атаки - издалека.
        attacked_pos - точка, в которую наносится урон.
        obj_list, player - список объектов.
        '''
        
        new_arrow = Arrow()
        new_arrow.x = self.x + (self.r + 0.02) * math.cos(self.facing_angle)
        new_arrow.y = self.y + (self.r + 0.02) * math.sin(self.facing_angle)
        new_arrow.angle = self.facing_angle
        new_arrow.damage = self.attack_value
        obj_list += [new_arrow]
        return obj_list
    


class Player(Entity):
    '''
    Класс игрока. Наследует от Entity. Подразумевается, что может менять оружие
    через переменную weapon.
    '''
    weapon = Bow()
    speed = 0.1
    texturepath1 = os.path.join('resources', 'Pictures','Main ch', 'm1.png')
    texturepath2 = os.path.join('resources', 'Pictures','Main ch', 'm1_2.png')
    texturepath_atk1 = os.path.join('resources', 'Pictures','Main ch', 'm4.png')
    texturepath_atk2 = os.path.join('resources', 'Pictures','Main ch', 'm2.png')
    texturepath = os.path.join('resources', 'Pictures','Main ch', 'm1.png')

    def changeTexture(self, action):
        if action == "attack":
            if self.weapon.type == "sword":
                self.texturepath = self.texturepath_atk1
            else:
                self.texturepath = self.texturepath_atk2
        elif action == "move":
            if self.texturepath == self.texturepath1:
                self.texturepath = self.texturepath2
            else:
                self.texturepath = self.texturepath1
    
    def attack(self, attack_position, obj_list):
        '''
        Атака через оружие игрока
        '''
        self.weapon.facing_angle = self.facing_angle
        self.weapon.x = self.x
        self.weapon.y = self.y
        self.weapon.r = self.r
        return self.weapon.attack(attack_position, obj_list)

    def toJSON(self, current_level_index):
        player_data = {"health": self.health,
                       "current_level": current_level_index,
                       "x": self.x,
                       "y": self.y,
                       "current_weapon is sword": self.weapon.type == "sword"
                       }
        return player_data

    
class Arrow:
    '''
    Стрела.
    '''
    type = "arrow"
    x = 0
    y = 0
    r = 0.2
    angle = 0
    damage = 1
    speed = 9 / 30
    living = False
    arrow_name = random.choice(['Arr1.png', 'Arr2.png'])
    texturepath = os.path.join('resources', 'Pictures', 'Arrows', arrow_name)

    def move(self, level, player):
        '''
        Передвижение с проверкой на попадание.
        level - весь уровень.
        '''
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        

        for i in level.obj_list:
            if i.point_in_obj((self.x, self.y)):
                level.obj_list.remove(self)
                if i.living:
                    i.get_damage(self.damage)
        
                return level.obj_list, player
        if player.point_in_obj((self.x, self.y)):
            player.get_damage(self.damage)
            level.obj_list.remove(self)
            return level.obj_list, player

        return level.obj_list, player

    def attack(self, obj_list, player):
        '''
        Атака.
        obj_list - список объектов
        player - игрок
        '''
        old_x = self.x
        old_y = self.y
        new_x = self.x + self.speed * math.cos(self.angle)
        new_y = self.y + self.speed * math.sin(self.angle)
        for i in range(1):
            current_x = old_x + i / 4 * new_x
            current_y = old_x + i / 4 * new_y
            for j in obj_list:
                if (j.living) and (j.point_in_obj((current_x, current_y))):
                    print('attack')
                    j.get_damage(self.damage)
                    obj_list.remove(self)
            if player.point_in_obj((current_x, current_y)):
                player.get_damage(self.damage)
                obj_list.remove(self)
        return obj_list, player

    def point_in_obj(self, pos):
        return False
            
class ImmovableObject():
    '''
    Недвижимый объект (например, стена).
    '''
    living = False
    x = 0
    y = 0
    size = 1
    texture = None
    living = False

    def point_in_obj(self, point):
        x, y = point
        return ((0 <= x - self.x) and (x - self.x <= self.size) and
                (0 <= y - self.y) and (y - self.y <= self.size))


    def __init__(self, x, y):
        self.x = x
        self.y = y
        wall_name = random.choice(self.wall_names)
        self.texturepath = os.path.join('resources', 'Pictures', 'Other', wall_name)

class Wall(ImmovableObject):
    living = False
    type = "wall"
    wall_names = ['wall1.png', 'wall2.png', 'wall3.png']
    #texturepath = os.path.join('resources', 'Pictures', 'Other', wall_name)


