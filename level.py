import pygame


class Level:
    def __init__(self, difficulty: int):
        self.display_surface = pygame.display.get_surface()

        # maze setup
        if difficulty == 1:
            # self.maze = Maze(10, 10)
            pass
        elif difficulty == 2:
            # self.maze = Maze(15, 15)
            pass
        elif difficulty == 3:
            # self.maze = Maze(25, 25)
            pass


