import sys
import time
import random
from typing import Union, Sequence

import log21
import pygame
from pygame.math import Vector2 as _Vector2

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BLUE = pygame.Color(0, 0, 255)


class Vector2(_Vector2):

    def __init__(
        self, x: Union[str, float, Sequence[float], 'Vector2'] = 0, y: float = None
    ):
        if y is not None:
            super().__init__(x, y)
        else:
            super().__init__(x)

    def __getitem__(self, i):
        return int(super().__getitem__(i))


# Arrow directions
NOWHERE = Vector2(0, 0)
UP = Vector2(-1, 0)
DOWN = Vector2(1, 0)
LEFT = Vector2(0, -1)
RIGHT = Vector2(0, 1)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)


class Game:
    """Maze algorithm: https://www.youtube.com/watch?v=zbXKcDVV4G0"""

    def __init__(self, width: int = 500, height: int = 500, size: int = 10):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            log21.error(
                f'Had {check_errors[1]} errors when initialising game, exiting...'
            )
            sys.exit(-1)
        else:
            log21.info('Game successfully initialised')
        pygame.display.set_caption("PyMaze")
        self.game_window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.running = False

        self.size = size
        self.maze_paths = [[RIGHT] * (size - 1) + [DOWN] for _ in range(size)]
        self.maze_paths[size - 1][size - 1] = NOWHERE
        self.origin_pos = Vector2(size - 1, size - 1)
        # self.update_maze(random.randint(1000, 2100))

        self.path_size = (min(width, height)) // (size + 3)
        if self.path_size < 1:
            raise RuntimeError("size is too big for this width and height!")

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw()
            self.update_maze(1)
            time.sleep(0.1)

    def draw(self):
        self.game_window.fill(BLACK)
        pygame.draw.circle(
            self.game_window, BLUE, (
                self.path_size * 2 + self.origin_pos[0] * self.path_size,
                self.path_size * 2 + self.origin_pos[1] * self.path_size
            ), self.path_size // 4
        )
        for i in range(self.size):
            for j in range(self.size):
                direction = self.maze_paths[j][i]
                if direction == NOWHERE:
                    continue
                start_pos = (
                    self.path_size * 2 + j * self.path_size,
                    self.path_size * 2 + i * self.path_size
                )
                end_pos = start_pos + self.path_size * direction
                pygame.draw.line(self.game_window, WHITE, start_pos, tuple(end_pos), 3)
                points = (
                    end_pos, end_pos - direction * self.path_size // 5 +
                    Vector2(direction[1] * self.path_size // 10, direction[0] * self.path_size // 10),
                    end_pos - direction * self.path_size // 5 -
                    Vector2(direction[1] * self.path_size // 10, direction[0] * self.path_size // 10)
                )
                pygame.draw.polygon(self.game_window, WHITE, points)
        pygame.display.update()

    def update_maze(self, n: int):
        """Change the origin and update the maze.

        :param n: Number of times to update the maze.
        """
        for _ in range(n):
            while True:
                direction = random.choice(DIRECTIONS)
                if (max(self.origin_pos + direction) >= self.size
                        or min(self.origin_pos + direction) < 0):
                    continue
                self.maze_paths[self.origin_pos[0]][self.origin_pos[1]] = direction
                self.origin_pos = self.origin_pos + direction
                self.maze_paths[self.origin_pos[0]][self.origin_pos[1]] = NOWHERE
                break

    def run(self):
        self.running = True
        self.main_loop()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log21.critical("Exiting...")
