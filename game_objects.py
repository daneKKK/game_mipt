#Этот файл хранит информацию о всех классах

class Level:
    object_list = []

    def line_of_sight(self, pos1, pos2):
        '''
        Поле зрения между двумя точками
        '''
        return False

class Entity:
    x = 0
    y = 0
    r = 0
    health = 0
    speed = 0

    def attack(self, attacked_obj):
        pass

class Spider(Entity): #пример
    #texture = ...
    #health = ...

    def attack(self, attack_position, level):


class SkeletArcher(Entity):
    def attack(self, attack_position):
        level += [flying_arrow]

class Player:
    weapon = Sword()
    def attack(self, attack_position, weapon):
        return weapon.attack(attack_postion):

class Weapon:
    damage = 0
    ...

class Sword(Weapon):
    def attack(self, attack_position, weapon):

class ImmovableObject():
    pass

class MovableObject():
    pass
