import pygame

from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = surface
        pos = (pos[0]*TILE_SIZE, (pos[1]+1)*TILE_SIZE)
        self.rect = self.image.get_rect(bottomleft=pos)
