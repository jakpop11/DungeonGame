import pygame
from enum import Enum
from abc import abstractmethod

from entity import Entity
from settings import *


class Item:
    class ItemType(Enum):
        WEAPON = 'T'
        POTION = 'U'

    def __init__(self, name):
        # sprite setup
        # image = enemy.png not Aqua
        if self.surface == None:
            self.surface = pygame.surface.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
            self.surface.fill("yellow")

        # entity
        self.type = Entity.Type.ITEM
        self.item_type = None

        # item
        self.name = name

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def pick_up(self, pos, groups):
        pass


class Weapon(Item):
    def __init__(self, name, atk, player):
        # sprite setup
        # image = enemy.png not Aqua
        # self.surface = pygame.surface.Surface((TILE_SIZE // 2.5, TILE_SIZE // 1.5))
        # self.surface.fill("blue")

        # weapon icon ???
        self.surface = pygame.image.load("Assets/Graphics/DG_Chunchumaru.png")
        self.surface = pygame.transform.scale(self.surface, (48, 48))

        # item
        super().__init__(name)
        self.item_type = Item.ItemType.WEAPON
        self.player = player

        # stats
        self.atk = atk

    def copy(self):
        return Weapon(self.name, self.atk, self.player)

    def pick_up(self, pos, groups):
        # spawn current player weapon
        Entity(pos, groups, self.player.weapon)
        self.player.weapon = self

    def get_atk(self):
        return self.atk


class Potion(Item):
    def __init__(self, name, heal, player):
        # sprite setup
        # image = enemy.png not Aqua
        self.surface = pygame.surface.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
        self.surface.fill("green")

        # item
        super().__init__(name)
        self.item_type = Item.ItemType.POTION
        self.player = player

        # stats
        self.heal = heal

    def copy(self):
        return Potion(self.name, self.heal, self.player)

    def pick_up(self, pos, groups):
        self.player.heal(self.get_heal())

    def get_heal(self):
        return self.heal
#
# class Item(Entity):
#     class ItemType(Enum):
#         WEAPON = 'T'
#         POTION = 'U'
#
#     def __init__(self, pos, groups, surface, name):
#         # sprite setup
#
#         # image = enemy.png not Aqua
#         if surface == None:
#             image = pygame.surface.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
#             image.fill("yellow")
#         else:
#             image = surface
#
#         super().__init__(pos, groups, image, name)
#
#         # entity
#         self.type = self.Type.ITEM
#         self.item_type = None
#
#     def pick_up(self):
#         # kill?
#         self.kill()
#         # aa
#
#
# class Weapon(Item):
#     def __init__(self, pos, groups, name, atk):
#         # sprite setup
#
#         # image = enemy.png not Aqua
#         image = pygame.surface.Surface((TILE_SIZE // 2.5, TILE_SIZE // 1.5))
#         image.fill("blue")
#         super().__init__(pos, groups, image, name)
#
#         # item
#         self.item_type = self.ItemType.WEAPON
#
#         # stats
#         self.atk = atk
#
#     def get_atk(self):
#         return self.atk
#
#
# class Potion(Item):
#     def __init__(self, pos, groups, name, heal):
#         # sprite setup
#
#         # image = enemy.png not Aqua
#         image = pygame.surface.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
#         image.fill("green")
#         super().__init__(pos, groups, image, name)
#
#         # item
#         self.item_type = self.ItemType.POTION
#
#         # stats
#         self.heal = heal
#
#     def get_heal(self):
#         return self.heal
