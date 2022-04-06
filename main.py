from matrix import *
from base import *
from flags import *
from drawing import *

import abc
from ctypes import byref

CW_USEDEFAULT = -2147483648
CS_HREDRAW = 2
CS_VREDRAW = 1

SRCCOPY = 0x00CC0020
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40


class Window(abc.ABC):
    def __init__(self, posx: int = 0, posy: int = 0, width: int = 800, height: int = 600, title: str = "Python",
                 iconPath: str = "", color: Color = Color((255, 255, 255))):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.title = title
        self.iconPath = iconPath
        self.back_color = color
        self.hdc = HDC
        self.dwExStyle = 0
        self.dwStyle = WindowStyles.WS_OVERLAPPEDWINDOW
        self.hwnd = HWND
        self.msg = MSG

    def show(self, *, mode=ShowModes.SW_SHOW):
        wc = WNDCLASSW()
        wc.style = CS_HREDRAW | CS_VREDRAW
        wc.lpfnWndProc = WNDPROC(self.__WndProc)
        wc.cbClsExtra = wc.cbWndExtra = 0
        wc.hInstance = kernel32.GetModuleHandleW(None)
        wc.hIcon = self.LoadIcon(self.iconPath)
        wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
        wc.hbrBackground = gdi32.CreateSolidBrush(self.back_color)
        wc.lpszMenuName = None
        wc.lpszClassName = 'Window'

        user32.RegisterClassW(byref(wc))

        self.hwnd = user32.CreateWindowExW(self.dwExStyle,  # window ex style
                                           wc.lpszClassName,  # window classname
                                           self.title,  # window title
                                           self.dwStyle,  # window style
                                           self.posx,  # window position x
                                           self.posy,  # window position y
                                           self.width,  # width
                                           self.height,  # height
                                           None,  # window parent
                                           None,  # menu
                                           wc.hInstance,  # application handle
                                           None)  # used with multiple windows

        user32.ShowWindow(self.hwnd, mode)

        self.msg = MSG()

        while user32.GetMessageW(byref(self.msg), None, 0, 0) != 0:
            user32.TranslateMessage(byref(self.msg))
            user32.DispatchMessageW(byref(self.msg))
        return self.msg

    def resize(self, width: int, heigt: int):
        self.width = width
        self.height = heigt

    def moveTo(self, pos: Vector2):
        self.posx = pos.x
        self.posy = pos.y

    def setBackColor(self, color: Color):
        self.back_color = color

    def setTitle(self, title: str):
        self.title = title

    def setdwExStyleFlags(self, flag: WindowExStyles):
        self.dwExStyle = flag

    def setdwStyleFlags(self, flag: WindowStyles):
        self.dwStyle = flag

    def maximize(self):
        self.dwStyle += WindowStyles.WS_MAXIMIZE

    def minimize(self):
        self.dwStyle += WindowStyles.WS_MINIMIZE

    def setIcon(self, path):
        self.iconPath = path

    @staticmethod
    def __LoadRes(res_type, path):
        """

        :param res_type: resource type (1 >> icon | 0 >> bitmap | 2 >> curosr)
        :param path: resource path
        :return: resource handler
        """
        return user32.LoadImageW(0, path, res_type, 0, 0, LR.LR_LOADFROMFILE | LR.LR_DEFAULTSIZE)

    def LoadIcon(self, path):
        """

        :param path: icon path
        :return: icon handler
        """
        return self.__LoadRes(1, path)

    def LoadImage(self, path):
        """

        :param path: image path
        :return: image handler
        """
        return self.__LoadRes(0, path)

    def beginPaint(self, ps):
        self.hdc = user32.BeginPaint(self.hwnd, byref(ps))
        del ps
        return self.hdc

    def endPaint(self, ps):
        user32.EndPaint(self.hwnd, byref(ps))
        del ps

    def paintEvent(self):
        ...

    def keyPressEvent(self, event):
        ...

    def mouseClickEvent(self, event):
        ...

    def resizeEvent(self, event):
        ...

    def mouseMoveEvent(self, event):
        ...

    def __WndProc(self, hwnd: HWND, message: MSG, wParam: WPARAM, lParam: LPARAM):

        if message == WindowMessages.WM_PAINT:
            self.paintEvent()

        if message == WindowMessages.WM_DESTROY:
            user32.PostQuitMessage(0)
        if message == WindowMessages.WM_CHAR:
            self.keyPressEvent(event=self.msg.wParam)
        if message == WindowMessages.WM_SIZE:
            self.resizeEvent(event=self.msg)
        if message == WindowMessages.WM_MOUSEMOVE:
            self.mouseMoveEvent(event=Vector2(GET_X_LPARAM(self.msg.lParam), GET_Y_LPARAM(self.msg.lParam)).pos)
        return user32.DefWindowProcW(hwnd, message, wParam, lParam)

    @staticmethod
    def createBrush(color: Color):
        return gdi32.CreateSolidBrush(color)

    @staticmethod
    def createPen(solid, width: int, color: Color):
        return gdi32.CreatePen(solid, width, color)

    def drawText(self, text: str, rect: RECT, textFormat: DrawText):
        user32.DrawTextW(self.hdc, text, -1, byref(rect), textFormat)

    def drawEllipse(self, pos: Vector2, r: int, color_: Color):
        for x, y, in Ellipse(pos, r):
            gdi32.SetPixel(self.hdc, x, y, color_)

    def drawSquare(self, pos: Vector2, sizex: Size, color_: Color):
        for x, y in Square(pos, sizex):
            self.drawLine(x, y, color_)

    def drawLine(self, start: Vector2, end: Vector2, color_: Color):
        for x, y in line(start, end):
            gdi32.SetPixel(self.hdc, x, y, color_)

    def drawImage(self, image: LoadImage, width, height):
        hdcMem = gdi32.CreateCompatibleDC(self.hdc)
        hbmOld = gdi32.SelectObject(hdcMem, image)

        gdi32.BitBlt(self.hdc, 0, 0, width, height, hdcMem, 0, 0, SRCCOPY)
        gdi32.SelectObject(hdcMem, hbmOld)
        gdi32.DeleteDC(hdcMem)


class Test(Window):
    def __init__(self):
        super(Test, self).__init__()
        self.setTitle("test window")
        self.setIcon("asd.ico")
        self.setBackColor(Color((0, 0, 0)))
        self.setdwExStyleFlags(WindowExStyles.WS_EX_OVERLAPPEDWINDOW)
        self.ps = PAINTSTRUCT()
        self.image = self.LoadImage("asd.bmp")

    def paintEvent(self):
        # rect = RECT(0, 0, self.width - 16, self.height)
        self.beginPaint(self.ps)
        self.drawImage(self.image, 1000, 1000)

        # self.drawText("Hello", rect, DrawText.DT_SINGLELINE | DrawText.DT_VCENTER | DrawText.DT_CENTER)
        self.endPaint(self.ps)

    def mouseMoveEvent(self, event):
        # print(event)
        ...


if __name__ == '__main__':
    m = Test()
    m.show()
