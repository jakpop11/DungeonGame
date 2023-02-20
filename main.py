import pygame
import sys
from enum import Enum

from settings import *
from menu import Menu, Commands


class State(Enum):
    QUIT = 0,
    MAIN_MENU = 1,
    GAME = 2


class Program:
    def __init__(self):
        pygame.init()

        # setup
        self.window = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("DungeonGame")
        self.clock = pygame.time.Clock()

        self.state = State.MAIN_MENU

        # game
        self.game = None

        # main menu
        self.main_menu = Menu([
            Commands.StartGameCommand(self, State.GAME),
            Commands.SettingsCommand(self),
            Commands.SettingsCommand(self),
            Commands.ExitCommand(self, State.QUIT)
        ])

        # pause menu
        self.pause_menu = Menu([
            Commands.ResumeGameCommand(self),
            Commands.SettingsCommand(self),
            Commands.ExitCommand(self, State.MAIN_MENU)
        ])

    def run(self):
        while self.state != State.QUIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN and self.state == State.GAME:
                    if event.key == pygame.K_ESCAPE:
                        self.game.is_paused = not self.game.is_paused
                        print("open game menu")
                        # self.state = State.MAIN_MENU

            if self.state == State.MAIN_MENU:
                self.game = None
                self.window.fill("#555555")
                self.main_menu.run()
            elif self.state == State.GAME:
                self.game.run()

            pygame.display.update()
            self.clock.tick(FPS)
        self.close()

    def close(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    program = Program()
    program.run()


# TODO:
# [^] -Entities
# [^] --Enemies
# [^] --Items
# [^] --Player update
# [ ] -Level and game fin
# [ ] --Item "END"?
# [^] -Maze generator
# [^] --Entities spawn
# [^] --Entities destroy
# [^] -UI
# [ ] --Weapon image in ui
# [^] --Dialogs text wrapping
# [^] -Player interactions
# [^] --Item pickup
# [^] --Fight
# [ ] --Map (see entities or not?)
# [ ] -Game over
# [ ] --Players death
# [^] -Pause menu
# [^] -Dialogs ("You've bumped on a wall", etc.)
# [^] -Remake item class so Weapon and Potion are not sprites but are in class that is sprite
# [ ] -Runtime map aka "maze" update
# [ ] -Add ItemType.FINISH with pick_up() { end_game() }
# [ ] -Fix Entities spawn
# [ ] -Smooth camera movement
# [ ] -Add image dictionary in settings
# [ ] -Enemies, Items balance
# [ ] -
