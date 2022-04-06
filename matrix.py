class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    def setPos(self, x, y):
        self.x = x
        self.y = y
        return self


class Size:
    def __new__(cls, size: int) -> int:
        return size

    def __init__(self, size: int):
        self.__init__(size)


class Color:
    def __new__(cls, crColor: tuple) -> int:
        if 0 <= crColor[0] < 256 and 0 <= crColor[1] < 256 and 0 <= crColor[2] < 256:
            return crColor[2] << 16 | crColor[1] << 8 | crColor[0]

    def __init__(self, crColor: tuple):
        self.__init__(crColor)
