# Copyright 2020 Dorian Turba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Created the 21/05/2020
import sys
from math import cos, radians, sin, log
from typing import List, Tuple

from arcade import Color, ShapeElementList, Shape, create_ellipse_filled, \
    create_rectangle_filled
from arcade.color import GREEN, RED

# 40A819
from CONSTANTS import SCREEN_HEIGHT, SCREEN_WIDTH


class Point:
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def __repr__(self):
        return f'x:{self.x}, y:{self.y}'


class Snake:
    shape_list: ShapeElementList
    shape_list_copy: List[Shape]
    tail: List[Tuple[float, float]]
    size: int
    color: Color
    radius: int
    angle: int
    head_shape: Shape

    def __init__(self, x, y, color: Color = GREEN, radius: int = 20,
                 angle: int = 0):
        self.tail = [(x, y)]

        self.shape_list = ShapeElementList()
        self.shape_list_copy = list()

        new_seg = create_ellipse_filled(x, y, 10, 10, color)
        self.head_shape = create_rectangle_filled(x, y, 10, 15, RED)
        self.shape_list.append(new_seg)
        self.shape_list_copy.append(new_seg)
        self.shape_list.append(self.head_shape)

        self.size = 10
        self.color = color
        self.radius = radius
        self.angle = angle

    def draw(self):
        self.shape_list.draw()

    def eat(self, apple):
        self.size += apple.power

    def _move(self):
        x = (self.head[0] + cos(radians(self.angle)) * (
                log(self.size) + 1)) % SCREEN_WIDTH
        y = (self.head[1] + sin(radians(self.angle)) * (
                log(self.size) + 1)) % SCREEN_HEIGHT
        self.tail.append((x, y))
        new_seg = create_ellipse_filled(x, y, 10, 10, self.color)
        self.shape_list.append(new_seg)
        self.shape_list_copy.append(new_seg)
        if len(self.tail) > self.size:
            self.tail.pop(0)
            to_remove = self.shape_list_copy.pop(0)
            self.shape_list.remove(to_remove)

        # move head
        self.shape_list.remove(self.head_shape)
        center_x = x + cos(radians(self.angle)) * 15
        center_y = y + sin(radians(self.angle)) * 15
        self.head_shape = create_rectangle_filled(center_x,
                                                  center_y,
                                                  10, 4, RED, self.angle)
        self.shape_list.append(self.head_shape)

    def update(self):
        self._move()

    def right(self):
        self.angle -= 5

    def left(self):
        self.angle += 5

    def check_collision(self):
        if len(self.tail) < 20:
            return True
        x = self.head[0]
        y = self.head[1]
        for x_, y_ in self.tail[:-20]:
            if -10 < x_ - x < 10 and -10 < y_ - y < 10:
                return False
        return True

    @property
    def head(self):
        return self.tail[-1]
