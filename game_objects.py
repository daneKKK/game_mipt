import math

#Этот файл хранит информацию о всех классах

class Level:
    '''
    Класс уровень. Должен хранить информацию о всех объектах на нём.
    '''

    x_border = 20
    y_border = 20
    
    object_list = []

    def line_of_sight(self, pos1, pos2):
        '''
        Проверка на то, видна ли точка pos1 из точки pos2
        pos1, pos2 - пары чисел (координат)
        '''
        x1, y1 = pos1
        x2, y2 = pos2
        distance = math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2)
        for i in range(0, distance, 1):
            current_point = (x1 - i * (x1 - x2) / distance,
                             y1 - i * (y1 - y2) / distance)
            for obj in object_list:
                if obj.point_in_obj(current_point):
                    return False
        return not (abs(x1 - x_border // 2) > x_border or abs(y1 - x_border // 2) > y_border
                    or abs(x2 - x_border // 2) > x_border or abs(y2 - x_border // 2) > y_border)
        return True

#Подход к объектам: в целях упрощения просчёта столкновений объектов сделаем их
#минимальный размер, равный 0.5

class Entity:
    '''
    Класс всех живых объектов.
    '''
    x = 0
    y = 0
    r = 0.5
    health = 10
    speed = 1
    facing_angle = 0
    attack_value = 1
    attack_speed = 30
    living = True
    texture = None

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
            if i.point_in_obj(attacked_pos):
                i.get_damage(attack_value)
        if player.point_in_obj(attacked_pos) and not (self is player):
            player.get_damage(attack_value)
        return obj_list, player
            

    def point_in_obj(self, point):
        '''
        Проверяет, находится ли точка в объекте
        point - кортеж с 2 координатами
        '''
        x, y = point
        distance = (x - self.x) ** 2 + (y - self.y) ** 2
        return distance <= r * r

    def move(self, angle):
        '''
        Передвижение по направлению на угол angle
        angle - угол в радианах
        '''
        self.x += speed * math.cos(angle)
        self.y += speed * math.sin(angle)

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
        facing_angle = angle

    def draw(self, screen):
        pass

class Spider(Entity):
    '''
    Класс Паук. Наследует от Entity
    '''
    texture = None



class SkeletArcher(Entity):
    '''
    Скелет-лучник. Наследует от Entity. Атакует издалека.
    '''
    health = 15
    speed = 1
    attack_value = 2
    attack_speed = 60
    
    def attack(self, attacked_pos, obj_list, player):
        '''
        Особенный вид атаки - издалека.
        attacked_pos - точка, в которую наносится урон.
        obj_list, player - список объектов и игрок. Нужны для единообразия.
        '''
        self.look_at(math.atan2(attacked_pos[1]-self.x, attacked_pos[2]-self.y))
        new_arrow = Arrow()
        new_arrow.x = self.x + (self.r + 0.02) * math.cos(self.angle)
        new_arrow.y = self.y + (self.r + 0.02) * math.cos(self.angle)
        new_arrow.angle = self.angle
        new_arrow.damage = self.damage
        obj_list += [new_arrow]
        return obj_list, player

class Player(Entity):
    '''
    Класс игрока. Наследует от Entity. Подразумевается, что может менять оружие
    через переменную weapon.
    '''
    weapon = Sword()
    def attack(self, attack_position, obj_list):
        '''
        Атака через оружие игрока
        '''
        return self.weapon.attack(attack_postion, obj_list):

class Weapon:
    '''
    Класс оружия.
    '''
    damage = 1
    reach = 1.5
    def attack(self, attack_position, obj_list):
        '''
        Атака оружия.
        attack_position - точка, в которую наносится атака.
        obj_list - лист объектов на уровне.
        '''
        for i in obj_list:
            if self == i or not i.living:
                continue
            if i.point_in_obj(attacked_pos):
                i.get_damage(attack_value)
        return obj_list
        

class Sword(Weapon):
    '''
    Меч. Наследует от Weapon.
    '''
    def attack(self, attack_position, obj_list):
        '''
        Атака мечом. Аналогично Weapon.attack()
        '''
        for i in obj_list:
            if self == i or not i.living:
                continue
            if i.point_in_obj(attacked_pos):
                i.get_damage(self.attack_value)
        return obj_list
    
class Arrow:
    '''
    Стрела.
    '''
    x = 0
    y = 0
    angle = 0
    damage = 1
    speed = 3
    living = False

    def move(self, level):
        '''
        Передвижение с проверкой на попадание.
        level - весь уровень.
        '''
        old_x = self.x
        old_y = self.y
        new_x = self.x + speed * math.cos(self.angle)
        new_y = self.y + speed * math.sin(self.angle)
        if not level.line_of_sight((new_x, new_y), (self.x, self.y)):
            level.obj_list.remove(self)
            return
        self.x = new_x
        self.y = new_y
        return level

    def attack(self, obj_list, player):
        '''
        Атака.
        obj_list - список объектов
        player - игрок
        '''
        old_x = self.x
        old_y = self.y
        new_x = self.x + speed * math.cos(self.angle)
        new_y = self.y + speed * math.sin(self.angle)
        for i in range(4):
            current_x = old_x + i / 4 * new_x
            current_y = old_x + i / 4 * new_y
            for j in obj_list:
                if (j.living) and (j.point_in_obj((current_x, current_y))):
                    j.get_damage(self.damage)
                    obj_list.remove(self)
            if player.point_in_obj((current_x, current_y)):
                player.get_damage(self.damage)
                obj_list.remove(self)
        return obj_list, player

    def draw(self, screen):
        pass
            
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
        return ((0 <= x - self.x) and (x - self.x <= size) and
                (0 <= y - self.y) and (y - self.y <= size))


    def draw(self, screen):
        pass
