class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)


class Size:
    def __init__(self, *args: int):
        self.__size_ = args

    @property
    def size(self):
        return self.__size_
