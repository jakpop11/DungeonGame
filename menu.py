import pygame
from abc import abstractmethod

from settings import *
from game import Game


class MenuCommand:
    @abstractmethod
    def get_name(self) -> str:
        return "None"

    @abstractmethod
    def execute(self):
        pass


class MenuItem:
    def __init__(self, command: MenuCommand, index, font, r_left, r_top, r_width, r_height):
        self.rect = pygame.Rect(r_left, r_top, r_width, r_height)
        self.title = command.get_name()
        self.command = command
        self.index = index
        self.font = font

    def display(self, surface, selection_num):
        is_selected = self.index == selection_num

        # draw button
        if is_selected:
            pygame.draw.rect(surface, MENU_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, MENU_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, MENU_BG_COLOR, self.rect)
            pygame.draw.rect(surface, MENU_BORDER_COLOR, self.rect, 4)
        # draw text
        self.display_title(surface, is_selected)

    def display_title(self, surface, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surf = self.font.render(self.title, False, color)
        title_rect = title_surf.get_rect(center=self.rect.center)

        # draw
        surface.blit(title_surf, title_rect)


class Menu:
    def __init__(self, commands: list):
        self.display_surface = pygame.display.get_surface()

        # menu setup
        self.font = pygame.font.Font(UI_FONT, MENU_FONT_SIZE)

        # items setup
        self.width = MENU_ITEM_WIDTH
        self.height = MENU_ITEM_HEIGHT
        self.items = []
        self.create_items(commands)

        # selection
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_UP] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN] and self.selection_index < len(self.items) - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.items[self.selection_index].command.execute()
                pygame.time.delay(300)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.can_move = True

    def create_items(self, commands: list):
        for i, cmd in enumerate(commands):
            # horizontal position
            left = (self.display_surface.get_size()[0] - self.width) / 2

            # vertical
            list_offset = MENU_ITEM_HEIGHT
            margin = self.height * 0.1
            top = i*(self.height+margin) + list_offset

            # create item
            item = MenuItem(cmd, i, self.font, left, top, self.width, self.height)
            self.items.append(item)

    def run(self):
        self.input()
        self.selection_cooldown()

        for i, item in enumerate(self.items):
            item.display(self.display_surface, self.selection_index)


class ExitCommand(MenuCommand):
    def __init__(self, program, exit_state):
        self.program = program
        self.exit_state = exit_state

    def get_name(self) -> str:
        return "Exit"

    def execute(self):
        print("Exit")
        self.program.state = self.exit_state


class ResumeGameCommand(MenuCommand):
    def __init__(self, program):
        self.program = program

    def get_name(self) -> str:
        return "Resume"

    def execute(self):
        self.program.game.is_paused = False


class BackMenuCommand(MenuCommand):
    def __init__(self, program, previous_menu: Menu):
        self.program = program
        self.previous_menu = previous_menu

    def get_name(self) -> str:
        return "<"

    def execute(self):
        print("Going back")
        self.program.main_menu = self.previous_menu


class SettingsCommand(MenuCommand):
    def __init__(self, program):
        self.program = program

    def get_name(self) -> str:
        return "Settings"

    def execute(self):
        print(f"state: {self.program.state}")
        print(f"no game: {self.program.game == None}")
        print(f"width: {self.program.window.get_width()}")
        print(f"height: {self.program.window.get_height()}")


class SelectDifficultyCommand(MenuCommand):
    def __init__(self, program, game_state, main_menu, name: str, difficulty: int):
        self.program = program
        self.game_state = game_state
        self.main_menu = main_menu
        self.difficulty = difficulty
        self.name = name

    def get_name(self) -> str:
        return self.name

    def execute(self):
        self.program.game = Game(self.program.pause_menu, self.difficulty)
        self.program.state = self.game_state
        self.program.main_menu = self.main_menu
        print("New Game\nPress [ESC] to back to main menu")


class StartGameCommand(MenuCommand):
    def __init__(self, program, game_state):
        self.program = program
        self.game_state = game_state

    def get_name(self) -> str:
        return "START GAME"

    def execute(self):
        neasted_menu = Menu([
            SelectDifficultyCommand(self.program, self.game_state, self.program.main_menu, "Easy", 1),
            SelectDifficultyCommand(self.program, self.game_state, self.program.main_menu, "Medium", 2),
            SelectDifficultyCommand(self.program, self.game_state, self.program.main_menu, "Hard", 3),
            BackMenuCommand(self.program, self.program.main_menu)])
        self.program.main_menu = neasted_menu


# Commands container
class Commands:
    ExitCommand = ExitCommand
    StartGameCommand = StartGameCommand
    SettingsCommand = SettingsCommand
    ResumeGameCommand = ResumeGameCommand
