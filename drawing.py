import copy
from matrix import Vector2, Size
from math import cos, sin

pi = 3.141592653589793


def line(start_: Vector2, end_: Vector2):
    width = end_.x - start_.x + 1 if start_.x >= end_.x else end_.x - start_.x - 1
    height = end_.y - start_.y + 1 if start_.y >= end_.y else end_.y - start_.y - 1

    ratio = abs(width // height)
    abs_height = abs(height)
    abs_width = abs(width)

    # diagonals does work thanks goes to @ma-tes
    if start_.y != end_.y:
        for i in range(abs_height):
            for x in range(ratio):
                yield ((i * (ratio * (width // abs_width))) + start_.x + (x * (width // abs_width)), start_.y + (
                        i * (height // abs_height)))

    if start_.y == end_.y:
        for i in range(abs_width + 1):
            yield start_.x + i, start_.y

    if start_.x == end_.x:
        for i in range(abs_height + 2):
            yield start_.x, start_.y + i


class Square(object):
    def __new__(cls, pos_, size_):
        x, y = pos_.x, pos_.y
        a = copy.deepcopy(pos_)

        yield a, pos_.setPos(x + size_, y)
        yield a.setPos(x + size_, y), pos_.setPos(x + size_, y + size_)
        yield a.setPos(x, y), pos_.setPos(x, y + size_)
        yield a.setPos(x, y + size_), pos_.setPos(x + size_, y + size_)
        del x, y, a

    def __init__(self, pos_: Vector2, size_: Size):
        self.__init__(pos_, size_)


class Ellipse(object):
    def __init__(self, pos: Vector2, r: int):
        self.n = 0
        self.pos = pos
        self.r = r

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < 361:
            x = self.pos.x + self.r * cos(pi * self.n / 180)
            y = self.pos.y + self.r * sin(pi * self.n / 180)
            self.n += 1
            return int(x), int(y)
        raise StopIteration()

# def rectangle(pos: Vector2, sizex: int, sizey: int):
#     pass
