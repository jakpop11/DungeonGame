import pygame

from settings import *
from entity import Entity
from item import Weapon


class Player(Entity):
    def __init__(self, pos, groups, hp, world_map):
        # sprite setup
        self.surface = pygame.image.load("Assets/Graphics/Kazuma_Front.png").convert_alpha()

        super().__init__(pos, groups, self)

        # entity
        self.type = Entity.Type.PLAYER

        # stats
        self.hp = hp
        self.weapon = Weapon("Fists", 7, self)

        self.max_hp = hp

        # movement
        self.is_moving = False
        self.move_cooldown = 200
        self.move_time = None
        self.is_acting = False
        self.can_act = True
        self.action_cooldown = 400
        self.action_time = None

        # board
        self.map = world_map

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.is_moving:
            # movement input
            if keys[pygame.K_UP]:
                self.is_moving = True
                self.move_time = pygame.time.get_ticks()
                self.move((0, -1))
                print("UP")
            elif keys[pygame.K_DOWN]:
                self.is_moving = True
                self.move_time = pygame.time.get_ticks()
                self.move((0, 1))
                print("Down")
            elif keys[pygame.K_LEFT]:
                self.is_moving = True
                self.move_time = pygame.time.get_ticks()
                self.move((-1, 0))
                print("Left")
            elif keys[pygame.K_RIGHT]:
                self.is_moving = True
                self.move_time = pygame.time.get_ticks()
                self.move((1, 0))
                print("Right")
            elif keys[pygame.K_SPACE] and self.can_act:
                self.is_acting = True
                self.can_act = False
                self.action_time = pygame.time.get_ticks()
                print("Action")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.is_moving:
            if current_time - self.move_time >= self.move_cooldown:
                self.is_moving = False
        if not self.can_act:
            if current_time - self.action_time >= self.action_cooldown:
                self.can_act = True

    def update(self):
        self.input()
        self.cooldowns()
        self.animate()

    def is_alive(self):
        return self.hp > 0

    def get_atk(self):
        return self.weapon.get_atk()

    def take_dmg(self, dmg: int):
        if self.is_alive():
            self.hp -= dmg

    def heal(self, heal: int):
        if self.is_alive():
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def move(self, direction: tuple):
        hor, ver = direction
        if self.map[self.y + ver][self.x + hor] not in ('%', '#'):
            self.x += hor
            self.y += ver

    def animate(self):
        self.rect = self.image.get_rect(topleft=(self.x*TILE_SIZE, self.y*TILE_SIZE))
#
#
# class Player(Entity):
#     def __init__(self, pos, groups, world_map):
#         # sprite setup
#         image = pygame.image.load("Assets/Graphics/Kazuma_Front.png").convert_alpha()
#
#         super().__init__(pos, groups, image, "Kazuma")
#
#         # entity
#         self.type = self.Type.PLAYER
#
#         # stats
#         self.hp = 100
#         self.weapon = None
#
#         self.max_hp = 100
#
#         # movement
#         self.moving = False
#         self.move_cooldown = 200
#         self.move_time = None
#
#         # board
#         self.map = world_map
#
#     def input(self):
#         keys = pygame.key.get_pressed()
#
#         if not self.moving:
#             # movement input
#             if keys[pygame.K_UP]:
#                 self.moving = True
#                 self.move_time = pygame.time.get_ticks()
#                 self.move((0, -1))
#                 print("UP")
#             elif keys[pygame.K_DOWN]:
#                 self.moving = True
#                 self.move_time = pygame.time.get_ticks()
#                 self.move((0, 1))
#                 print("Down")
#             elif keys[pygame.K_LEFT]:
#                 self.moving = True
#                 self.move_time = pygame.time.get_ticks()
#                 self.move((-1, 0))
#                 print("Left")
#             elif keys[pygame.K_RIGHT]:
#                 self.moving = True
#                 self.move_time = pygame.time.get_ticks()
#                 self.move((1, 0))
#                 print("Right")
#
#     def cooldowns(self):
#         current_time = pygame.time.get_ticks()
#
#         if self.moving:
#             if current_time - self.move_time >= self.move_cooldown:
#                 self.moving = False
#
#     def update(self):
#         self.input()
#         self.cooldowns()
#         self.animate()
#
#     def is_alive(self):
#         return self.hp > 0
#
#     def take_dmg(self, dmg: int):
#         if self.is_alive():
#             self.hp -= dmg
#
#     def heal(self, heal: int):
#         if self.is_alive():
#             self.hp += heal
#             if self.hp > self.max_hp:
#                 self.hp = self.max_hp
#
#     def move(self, direction: tuple):
#         hor, ver = direction
#         if self.map[self.y + ver][self.x + hor] not in ('%', '#'):
#             self.x += hor
#             self.y += ver
#
#     def animate(self):
#         self.rect = self.image.get_rect(topleft=(self.x*TILE_SIZE, self.y*TILE_SIZE))
