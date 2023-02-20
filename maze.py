from enum import Enum
from random import Random

import pygame.time


class FieldType(Enum):
    DEFAULT = '.'
    PATH = '_'
    BORDER = '%'
    WALL = '#'
    CROSSROADS = '+'
    DEAD_END = '='
    ITEM = '$'
    ENTITY = '?'
    FINISH = 'F'


class Field:
    def __init__(self, pos, field_type: FieldType):
        self.x, self.y = pos
        self.type = field_type


class Maze:
    def __init__(self, x: int, y: int):
        if x % 2 == 0:
            self.X = x + 1
        else:
            self.X = x
        if y % 2 == 0:
            self.Y = y + 1
        else:
            self.Y = y

        self.fields = []

        self.generate_board()
        # start point / exit (X-2, Y-2)
        self.generate_maze(self.X-2, self.Y-2)

    def generate_board(self):
        for y in range(self.Y):
            row = []
            for x in range(self.X):
                if x == 0 or y == 0 or x == self.X-1 or y == self.Y-1:
                    col = Field((x, y), FieldType.BORDER)
                else:
                    col = Field((x, y), FieldType.DEFAULT)
                row.append(col)
            self.fields.append(row)

    def generate_maze(self, start_x: int, start_y: int):
        # out of scope exception
        x_oos = start_x <= 0 or self.X-1 <= start_x
        y_oos = start_y <= 0 or self.Y-1 <= start_y

        if x_oos or y_oos:
            raise ValueError()

        # Generate maze based on push, pop stack method
        stack = []

        self.fields[start_y][start_x].type = FieldType.FINISH
        stack.append(self.fields[start_y][start_x])

        x = start_x
        y = start_y
        dead_end = True

        first_do = True

        while not (x, y) == (start_x, start_y) or first_do:
            neighbours = self.get_neighbours(x, y)

            if len(neighbours) != 0:
                # Continue path

                # Crossroads
                if not dead_end:
                    stack[-1].type = FieldType.CROSSROADS

                # Choose neighbour
                rand = Random()
                neighbour = rand.choice(neighbours)

                # Draw path
                neighbour[0].type = FieldType.PATH

                if neighbour[1] == 0:
                    self.fields[y-1][x].type = FieldType.PATH
                elif neighbour[1] == 1:
                    self.fields[y][x+1].type = FieldType.PATH
                elif neighbour[1] == 2:
                    self.fields[y+1][x].type = FieldType.PATH
                elif neighbour[1] == 3:
                    self.fields[y][x-1].type = FieldType.PATH

                # Push random neighbour to stack
                stack.append(neighbour[0])

                # Reset dead-end flag
                dead_end = True

                # # Run-time visuals here
                # self.get_maze()
                # print(f"{x, y}")
                # pygame.time.wait(500)

            else:
                if dead_end:
                    # Dead-End
                    stack[-1].type = FieldType.DEAD_END
                dead_end = False

                # Pop back
                stack.pop()

            x = stack[-1].x
            y = stack[-1].y

            # after first loop
            if first_do:
                first_do = False

        # Walls
        for y in self.fields:
            for x in y:
                if x.type == FieldType.DEFAULT:
                    x.type = FieldType.WALL

    def get_neighbours(self, x, y):
        neighbours = []

        # Top
        if y > 1 and self.fields[y-2][x].type == FieldType.DEFAULT:
            neighbours.append((self.fields[y-2][x], 0))

        # Right
        if x < self.X-2 and self.fields[y][x+2].type == FieldType.DEFAULT:
            neighbours.append((self.fields[y][x+2], 1))

        # Bottom
        if y < self.Y-2 and self.fields[y+2][x].type == FieldType.DEFAULT:
            neighbours.append((self.fields[y+2][x], 2))

        # Left
        if x > 1 and self.fields[y][x-2].type == FieldType.DEFAULT:
            neighbours.append((self.fields[y][x-2], 3))

        return neighbours

    def get_maze(self):
        maze = []
        for y in self.fields:
            row = []
            for x in y:
                row.append(x.type.value)
            #     print(f" {x.type.value} ", end='')
            # print()
            maze.append(row)

        return maze
