import pygame
from enum import Enum
from abc import abstractmethod

from settings import *


class Entity(pygame.sprite.Sprite):
    class Type(Enum):
        NONE = 'X'
        ENEMY = '8',
        ITEM = '$',
        PLAYER = 'P'

    def __init__(self, pos, groups, object):
        # entity setup
        if hasattr(object, "type"):
            self.type = object.type
        else:
            self.type = Entity.Type.NONE
        self.x, self.y = pos
        self.object = object
        self.groups = groups

        # sprite setup
        super().__init__(groups)
        if object.surface == None:
            self.image = pygame.surface.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
            self.image.fill("white")
        else:
            self.image = object.surface
        self.rect = self.image.get_rect(bottomleft=(self.x*TILE_SIZE, (self.y+1)*TILE_SIZE))

    def kill_sprite(self):
        self.kill()
        if self.type == Entity.Type.ITEM:
            self.object.pick_up((self.x, self.y), self.groups)
        elif self.type == Entity.Type.ENEMY:
            self.object.kill_enemy((self.x, self.y), self.groups)

# class Entity(pygame.sprite.Sprite):
#     class Type(Enum):
#         NONE = 'X'
#         ENEMY = '8',
#         ITEM = '$',
#         PLAYER = 'P'
#
#     def __init__(self, pos, groups, surface, name):
#         # sprite setup
#         super().__init__(groups)
#         self.image = surface
#         self.rect = self.image.get_rect(bottomleft=(pos[0] * TILE_SIZE, (pos[1]+1)*TILE_SIZE))
#
#         # entity setup
#         self.name = name
#         self.type = Entity.Type.NONE
#         self.x, self.y = pos
