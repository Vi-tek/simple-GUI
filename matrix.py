class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    def __del__(self):
        del self.x, self.y, self.pos


class Size:
    def __init__(self, *args: int):
        self.__size_ = args

    def __del__(self):
        del self.__size_

    @property
    def size(self):
        return self.__size_


class Color:
    def __new__(cls, crColor: tuple):
        if len(crColor) == 3:
            if 0 <= crColor[0] < 256 and 0 <= crColor[1] < 256 and 0 <= crColor[2] < 256:
                return crColor[2] << 16 | crColor[1] << 8 | crColor[0]
        return None

    def __init__(self, crColor: tuple):
        self.__init__(crColor)
