from flags import *
from drawing import *
from matrix import *
from base import *
import itertools

CW_USEDEFAULT = -2147483648
CS_HREDRAW = 2
CS_VREDRAW = 1


class Window:
    def __init__(self, posx: int = 0, posy: int = 0, width: int = 800, height: int = 600, title: str = "Python",
                 color: tuple = (255, 255, 255)):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.title = title
        self.back_color = color
        self.hdc = w.HDC
        self.dwExStyle = 0
        self.dwStyle = WindowStyles.WS_OVERLAPPEDWINDOW

    def show(self, *, mode=ShowModes.SW_SHOW):
        wc = WNDCLASSW()
        wc.style = CS_HREDRAW | CS_VREDRAW
        wc.lpfnWndProc = WNDPROC(self.__WndProc)
        wc.cbClsExtra = wc.cbWndExtra = 0
        wc.hInstance = kernel32.GetModuleHandleW(None)
        wc.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
        wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
        wc.hbrBackground = gdi32.CreateSolidBrush(self.color(self.back_color))
        wc.lpszMenuName = None
        wc.lpszClassName = 'Window'

        user32.RegisterClassW(byref(wc))

        hwnd = user32.CreateWindowExW(self.dwExStyle,  # window ex style
                                      wc.lpszClassName,
                                      self.title,  # window title
                                      self.dwStyle,  # window style
                                      self.posx,  # pos x
                                      self.posy,  # pos y
                                      self.width,  # width
                                      self.height,  # height
                                      None,
                                      None,
                                      wc.hInstance,
                                      None)

        user32.ShowWindow(hwnd, mode)
        user32.UpdateWindow(hwnd)

        msg = w.MSG()
        while user32.GetMessageW(byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))

        return msg.wParam

    def resize(self, width, heigt):
        self.width = width
        self.height = heigt

    def moveTo(self, x, y):
        self.posx = x
        self.posy = y

    def backColor(self, red: int, green: int, blue: int):
        self.back_color = (red, green, blue)

    def setTitle(self, title):
        self.title = title

    def setdwExStyleFlags(self, flag):
        self.dwExStyle = flag

    def setdwStyleFlags(self, flag):
        self.dwStyle = flag

    def maximize(self):
        self.dwStyle += WindowStyles.WS_MAXIMIZE

    def minimize(self):
        self.dwStyle += WindowStyles.WS_MINIMIZE

    def __WndProc(self, hwnd, message, wParam, lParam):
        ps = PAINTSTRUCT()
        rect = w.RECT()

        if message == WindowMessages.WM_PAINT:
            self.hdc = user32.BeginPaint(hwnd, byref(ps))
            user32.GetClientRect(hwnd, byref(rect))
            # user32.DrawTextW(self.hdc, "Hello from scheme", -1, byref(rect), 0x00000020 | 0x00000001 | 0x00000004)

            self.drawSquare(Vector2(self.width//2 - 40, self.height//2 - 40), Size(80), Window.color((255, 255, 255)))

            user32.EndPaint(hwnd, byref(ps))
        if message == WindowMessages.WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0

        return user32.DefWindowProcW(hwnd, message, wParam, lParam)

    @staticmethod
    def color(crColor: tuple):
        if len(crColor) == 3:
            if 0 <= crColor[0] < 256 and 0 <= crColor[1] < 256 and 0 <= crColor[2] < 256:
                return crColor[2] << 16 | crColor[1] << 8 | crColor[0]
        return None

    # @staticmethod
    # def __RGBAToColor(crColor: tuple):
    #     if len(crColor) == 4:
    #         if 0 <= crColor[0] < 256 and 0 <= crColor[1] < 256 |
    #     return None

    @staticmethod
    def createBrush(color):
        return gdi32.CreateSolidBrush(Window.color(color))

    @staticmethod
    def createPen(solid, width, color):
        return gdi32.CreatePen(solid, width, Window.color(color))

    def drawEllipse(self, pos: Vector2, r: int, color_: color):
        for x_, y_, in ellipse(pos, r):
            gdi32.SetPixel(self.hdc, x_, y_, color_)

    def drawSquare(self, pos: Vector2, sizex: Size, color_: color):
        for x in itertools.combinations(Square(pos, sizex), 2):
            self.drawLine(x[0], x[1], color_)

    def drawLine(self, start: Vector2, end: Vector2, color_: color):
        for x, y in line(start, end):
            gdi32.SetPixel(self.hdc, x, y, color_)


if __name__ == '__main__':
    window = Window()
    window.setTitle("sadasd")
    window.resize(800, 600)
    window.moveTo(0, 0)
    window.backColor(0, 0, 0)
    # window.maximize()
    window.show()
