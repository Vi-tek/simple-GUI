from matrix import *
import math


def line(start_: Vector2, end_: Vector2):
    width = start_.x - end_.x if start_.x > end_.x else end_.x - start_.x
    height = start_.y - end_.y if start_.y > end_.y else end_.y - start_.y

    # diagonals does not work

    if start_.y == end_.y:
        for i in range(abs(width)):
            yield start_.x + i, start_.y

    if start_.x == end_.x:
        for i in range(abs(height)):
            yield start_.x, start_.y + i


class Square:
    def __init__(self, pos_: Vector2, size_: Size):
        self.width, self.height, self.pos = size_.size[0], size_.size[0], pos_
        self.top_left = Vector2(pos_.x, pos_.y)
        self.top_right = Vector2(pos_.x + self.width, pos_.y)
        self.bottom_left = Vector2(pos_.x, pos_.y + self.height)
        self.bottom_right = Vector2(pos_.x + self.width, pos_.y + self.height)

    def __iter__(self):
        return iter((self.top_left, self.top_right, self.bottom_left, self.bottom_right))


def ellipse(pos_: Vector2, r_: int):
    for i in range(361):
        x = pos_.x + r_ * math.cos(math.pi * i / 180)
        y = pos_.y + r_ * math.sin(math.pi * i / 180)

        yield int(x), int(y)

# def rectangle(pos: Vector2, sizex: int, sizey: int):
#     pass
