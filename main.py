# Copyright 2020 Dorian Turba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Created the 21/05/2020
import timeit
from collections import defaultdict
from math import floor
from pprint import pprint
from random import randint, randrange
from time import time
from typing import Any, List, Tuple

import arcade
from arcade import set_background_color, start_render, \
    run, Window, draw_text_2, ShapeElementList, create_ellipse_filled
from arcade.color import BLACK, RED
from arcade.key import SPACE, LEFT, RIGHT

from CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND, \
    DEBUG
from Snake import Snake


def do_nothing():
    pass


class Apple:
    pos: Tuple
    power: int

    def __init__(self):
        self.pos = (randrange(SCREEN_WIDTH), randrange(SCREEN_HEIGHT))
        self.power = randint(5, 20)


def snake_collide_apple(snake: Snake, apples: List[Apple]):
    for i, apple in enumerate(apples):
        x, y = snake.head
        if -15 < apple.pos[0] - x < 15 and -15 < apple.pos[1] - y < 15:
            print(snake.head, i)
            return i
    return -1


class Welcome(Window):
    """
    Main welcome window
    """
    snake: Snake
    left: bool
    right: bool
    action_factory: dict
    end: bool
    apples: List[Apple]
    draw_time: float = 0.
    fps_start_timer: float = 0.
    fps: float = 0.
    processing_time: float = 0

    def __init__(self):
        """
        Initialize the window
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        set_background_color(BACKGROUND)
        self.set_update_rate(1 / 60)
        self.snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.left = False
        self.right = False
        self.end = False
        self.action_factory = {
            "press": {
                LEFT: self.left_true,
                RIGHT: self.right_true,
            },
            "release": {
                LEFT: self.left_false,
                RIGHT: self.right_false,
            },
        }
        self.apples = [Apple(), Apple(), Apple()]
        self.apples_shapes = ShapeElementList()
        self.apples_shapes_cpy = list()
        for apple in self.apples:
            shape = create_ellipse_filled(apple.pos[0], apple.pos[1], 10, 10,
                                          RED)
            self.apples_shapes.append(shape)
            self.apples_shapes_cpy.append(shape)

    def on_draw(self):
        """
        Called whenever you need to draw your window
        """
        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        start_render()
        self.snake.draw()
        self.apples_shapes.draw()

        if DEBUG:
            # Print the timing
            output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 40,
                             arcade.color.WHITE, 18)
            # Display timings
            output = f"Processing time: {self.processing_time:.3f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 20,
                             arcade.color.WHITE, 16)
        else:
            output = f"Score: {self.snake.size} points"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 40,
                             arcade.color.WHITE, 18)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time: float):
        start_time = timeit.default_timer()

        if self.left:
            self.snake.left()
        if self.right:
            self.snake.right()
        if self.snake.check_collision():
            self.snake.update()
        else:
            self.end = True
        if (apple_i := snake_collide_apple(self.snake, self.apples)) != -1:
            eaten_apple = self.apples.pop(apple_i)
            to_remove = self.apples_shapes_cpy.pop(apple_i)
            self.apples_shapes.remove(to_remove)
            apple = Apple()
            self.apples.append(apple)
            shape = create_ellipse_filled(apple.pos[0], apple.pos[1], 10, 10,
                                          RED)
            self.apples_shapes.append(shape)
            self.apples_shapes_cpy.append(shape)

            self.snake.eat(eaten_apple)

        self.processing_time = timeit.default_timer() - start_time

    def left_true(self):
        self.left = True

    def left_false(self):
        self.left = False

    def right_true(self):
        self.right = True

    def right_false(self):
        self.right = False

    def on_key_press(self, symbol: int, modifiers: int):
        self.action_factory["press"].setdefault(symbol, do_nothing)()

    def on_key_release(self, symbol: int, modifiers: int):
        self.action_factory["release"].setdefault(symbol, do_nothing)()


# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    run()
