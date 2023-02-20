import pygame
from random import Random

from entity import Entity
from settings import *


class Enemy:
    def __init__(self, name, hp, weapon, drop_list: list, img_path="Assets/Graphics/DG_Vanir.png"):
        # sprite setup
        # image = enemy.png not Aqua
        self.img_path = img_path
        self.surface = pygame.image.load(img_path)

        # entity
        self.type = Entity.Type.ENEMY

        # stats
        self.name = name
        self.hp = hp
        self. weapon = weapon

        # generate loot
        rand = Random()
        self.drop_list = drop_list
        self.drop = rand.choice(drop_list)

        self.can_attack = True

    def copy(self):
        return Enemy(self.name, self.hp, self.weapon.copy(), self.drop_list, self.img_path)

    def kill_enemy(self, pos, groups):
        # spawn drop
        Entity(pos, groups, self.drop)

    def is_alive(self):
        return self.hp > 0

    def get_atk(self):
        return self.weapon.get_atk()

    def take_dmg(self, dmg: int):
        if self.is_alive():
            self.hp -= dmg
#
#
# class Enemy(Entity):
#     def __init__(self, pos, groups, name, hp, weapon):
#         # sprite setup
#
#         # image = enemy.png not Aqua
#         image = pygame.surface.Surface((TILE_SIZE // 1.5, TILE_SIZE // 1.5))
#         image.fill("red")
#
#         super().__init__(pos, groups, image, name)
#
#         # entity
#         self.type = self.Type.ENEMY
#
#         # stats
#         self.hp = hp
#         self. weapon = None
#         self.drop = None
#
#     def is_alive(self):
#         if self.hp > 0:
#             return True
#
#         # kill him xd
#         self.kill()
#         # spawn drop
#
#         return False
#
#     def take_dmg(self, dmg: int):
#         if self.is_alive():
#             self.hp -= dmg
