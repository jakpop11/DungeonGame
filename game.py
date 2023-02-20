import pygame
from random import Random

from settings import *
from tile import Tile
from player import Player
from entity import Entity
from enemy import Enemy
from item import Item, Weapon, Potion
from maze import Maze, FieldType, Field
from ui import UI


class Game:
    def __init__(self, pause_menu, difficulty):
        self.display_surface = pygame.display.get_surface()

        # game setup
        self.difficulty = difficulty
        # self.level = Level(self.difficulty)
        self.player = None

        # sprite groups setup
        self.visible_sprites = CameraGroup()
        self.entities_sprites = pygame.sprite.Group()

        # map / level / maze setup
        self.maze = None
        self.create_map()

        # UI
        self.ui = UI()
        self.is_paused = False
        self.pause_menu = pause_menu

    def create_map(self):
        # maze = [
        #     ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'],
        #     ['%', '_', '_', '_', '_', '_', '_', '+', '_', '_', '%'],
        #     ['%', '_', '#', '#', '#', '#', '#', '_', '#', '_', '%'],
        #     ['%', '_', '#', '_', '_', '_', '_', '_', '#', '?', '%'],
        #     ['%', '_', '#', '_', '#', '#', '#', '#', '#', '#', '%'],
        #     ['%', '_', '#', '_', '_', '_', '_', '_', '?', '_', '%'],
        #     ['%', '_', '#', '#', '#', '#', '#', '#', '#', '_', '%'],
        #     ['%', '_', '_', '_', '_', '_', '#', '=', '#', '_', '%'],
        #     ['%', '#', '#', '#', '#', '_', '#', '_', '#', '_', '%'],
        #     ['%', '=', '_', '_', '_', '+', '_', '_', '#', 'F', '%'],
        #     ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%']
        # ]

        self.maze = Maze(15, 15)
        maze = self.maze.get_maze()

        graphics = {
            "path": pygame.image.load("Assets/Graphics/DG_Path.png"),
            "border": pygame.image.load("Assets/Graphics/DG_Border.png"),
            "wall": pygame.image.load("Assets/Graphics/DG_Wall.png"),
            "crossroads": pygame.image.load("Assets/Graphics/DG_Crossroads.png"),
            "dead_end": pygame.image.load("Assets/Graphics/DG_DeadEnd.png"),
            "grass": pygame.image.load("Assets/Graphics/DG_Grass.png"),
            "water": pygame.image.load("Assets/Graphics/Water_basic.png")
        }
        # potions and enemies dic

        # Floor tiles creation
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                if col == '_':
                    # Path
                    Tile((x, y), tuple([self.visible_sprites]), graphics["path"])
                elif col == '%':
                    # Border
                    Tile((x, y), tuple([self.visible_sprites]), graphics["border"])
                elif col == '#':
                    # Wall
                    Tile((x, y), tuple([self.visible_sprites]), graphics["wall"])
                elif col == '+':
                    # Crossroads
                    Tile((x, y), tuple([self.visible_sprites]), graphics["crossroads"])
                elif col == '=':
                    # Dead-End
                    Tile((x, y), tuple([self.visible_sprites]), graphics["dead_end"])
                elif col == 'F':
                    Tile((x, y), tuple([self.visible_sprites]), graphics["grass"])
                else:
                    Tile((x, y), tuple([self.visible_sprites]), graphics["grass"])

        # Player creation
        self.player = Player((1, 1), tuple([self.visible_sprites]), 100, maze)

        # Entity creation
        self.generate_entities()

    def generate_entities(self):
        rand = Random()

        graphics = {
            "Cabbage": "Assets/Graphics/DG_Cabbage.png",
            "Frog": "Assets/Graphics/DG_Frog.png",
            "Vanir": "Assets/Graphics/DG_Vanir.png",
        }

        items = [
            Weapon("Rusty Sword", 10, self.player),
            Potion("Tasty Mushrooms", 10, self.player),

            Weapon("Hunting Knife", 15, self.player),
            Potion("Blue Berries", 25, self.player),

            Weapon("Great Sword", 30, self.player),
            Potion("Healing Herbs", 40, self.player),

            Weapon("Scythe of Death", 50, self.player),
            Potion("Real Potion", 50, self.player)
        ]

        enemies = [
            Enemy("Cabbage", 50, Weapon("Cabbages Leaf", 5, self.player), items[0:4], graphics["Cabbage"]),
            Enemy("Frog", 60, Weapon("Frogs Salvia", 10, self.player), items[2:6], graphics["Frog"]),
            Enemy("Frog 2", 35, Weapon("Frogs Tongue", 20, self.player), items[4:6], graphics["Frog"]),
            Enemy("Vanir", 80, Weapon("Warlock Staff", 40, self.player), [
                      Weapon("Warlock Stuff", 40, self.player),
                      Weapon("Scythe of Death", 50, self.player),
                      Potion("Real Potion", 50, self.player)],
                  graphics["Vanir"])
        ]

        # Enemies
        i = 0
        while i < (self.maze.X*self.maze.Y)//20:
            x = rand.randrange(1, self.maze.X-2, 2)
            y = rand.randrange(1, self.maze.Y-2, 2)
            if (x, y) != (1, 1) and not self.maze.get_maze()[y][x] in ['#', '%', '?']:
                if x < self.maze.X//2:
                    if y < self.maze.Y//2:
                        # I quater
                        r = rand.randint(0, len(enemies)-3)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               enemies[r].copy())
                    else:
                        # II quater
                        r = rand.randint(0, len(enemies) - 2)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               enemies[r].copy())
                else:
                    if y < self.maze.Y//2:
                        # II quater
                        r = rand.randint(0, len(enemies) - 2)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               enemies[r].copy())
                    else:
                        # III quater
                        r = rand.randint(2, len(enemies) - 1)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               enemies[r].copy())
                self.maze.fields[y][x].type = FieldType.ENTITY
                i += 1

        # Items
        i = 0
        while i < (self.maze.X * self.maze.Y) // 20:
            x = rand.randrange(1, self.maze.X - 2, 2)
            y = rand.randrange(1, self.maze.Y - 2, 2)
            if (x, y) != (1, 1) and not self.maze.get_maze()[y][x] in ['#', '%', '?']:
                if x < self.maze.X // 2:
                    if y < self.maze.Y // 2:
                        # I quater
                        r = rand.randint(0, len(items) - 7)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               items[r].copy())
                    else:
                        # II quater
                        r = rand.randint(2, len(items) - 3)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               items[r].copy())
                else:
                    if y < self.maze.Y // 2:
                        # II quater
                        r = rand.randint(2, len(items) - 3)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               items[r].copy())
                    else:
                        # III quater
                        r = rand.randint(4, len(items) - 1)
                        # print(f"i: {i}, r: {r}")
                        Entity((x, y), tuple([self.visible_sprites, self.entities_sprites]),
                               items[r].copy())
                self.maze.fields[y][x].type = FieldType.ENTITY
                i += 1

    def entities_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.entities_sprites, False)
        if collision_sprites:
            for sp in collision_sprites:
                if hasattr(sp, "type"):
                    # draw entity description dialog
                    if sp.type == Entity.Type.ENEMY:
                        self.ui.add_dialog(f"You've bumped on {sp.object.name} hp: {sp.object.hp}. Look out for its attack! Atk: {sp.object.get_atk()}")
                        if self.killed_enemy(sp.object):
                            self.ui.add_dialog(f"You've slain {sp.object.name}.", 2000)
                            sp.kill_sprite()
                            print("Kill Sprite")
                    elif sp.type == Entity.Type.ITEM:
                        if sp.object.item_type == Weapon.ItemType.WEAPON:
                            self.ui.add_dialog(f"{sp.object.name} Atk: {sp.object.atk}")
                            if self.player.is_acting:
                                self.ui.add_dialog(f"You've equip {sp.object.name}. Your attack increases to {sp.object.atk}.", 2000)
                                self.player.is_acting = False
                                print("Player:")
                                print(f"<=={self.player.weapon.name}=|--")
                                print(f"</ {self.player.weapon.atk} /3")
                                print("Weapon:")
                                print(f"<=={sp.object.name}=|--")
                                print(f"</ {sp.object.atk} /3")
                                sp.kill_sprite()

                        elif sp.object.item_type == Potion.ItemType.POTION:
                            self.ui.add_dialog(f"{sp.object.name} <3 {sp.object.heal} <3")
                            if self.player.is_acting:
                                self.ui.add_dialog(f"You've used {sp.object.name}. Your health regenerate by {sp.object.heal}.", 2000)
                                self.player.is_acting = False
                                print(f"(_{sp.object.name}_)")
                                print(f"*% {sp.object.heal} %*")
                                sp.kill_sprite()
        self.player.is_acting = False

    def killed_enemy(self, enemy: Enemy):
        # player step on enemy field
        if self.player.is_moving:
            if enemy.can_attack:
                enemy.can_attack = False
                # player take dmg
                self.player.take_dmg(enemy.get_atk())
                print(f"{enemy.name} attacks you")
        else:
            enemy.can_attack = True

        # player attacks
        if self.player.is_acting:
            self.player.is_acting = False
            enemy.can_attack = True

            # enemy take dmg
            enemy.take_dmg(self.player.get_atk())
            print(f"__{enemy.name}__")
            print(f"<3 {enemy.hp}")
            # if enemy is alive
            if enemy.is_alive():
                print(f"{enemy.name} attacks you")
                # attack Player
                self.player.take_dmg(enemy.get_atk())
                print(f"P HP: {self.player.hp}")
                return False
            else:
                return True

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # Game pause
        if self.is_paused:
            self.pause_menu.run()

        else:
            self.visible_sprites.update()
            self.entities_collision()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        # setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.center_x = self.display_surface.get_size()[0] // 2
        self.center_y = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # self.vignette_surf = pygame.image.load("Assets/Graphics/Vignette.png").convert_alpha()
        # self.vignette_rect = self.vignette_surf.get_rect(center=(self.center_x, self.center_y))
        self.bg = pygame.image.load("Assets/Graphics/DG_BG.png")
        self.bg_rect = self.bg.get_rect()

    def custom_draw(self, player):
        # get offset
        self.offset.x = player.rect.centerx - self.center_x
        self.offset.y = player.rect.centery - self.center_y

        self.display_surface.blit(self.bg, self.bg_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottomleft):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
