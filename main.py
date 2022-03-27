from ctypes import *
from ctypes import wintypes as w

import flags

user32 = WinDLL("user32", use_last_error=True)
kernel32 = WinDLL("kernel32", use_last_error=True)
gdi32 = WinDLL("gdi32", use_last_error=True)


def errcheck(result, func, args):
    if result is None or result == 0:
        raise WinError(get_last_error())
    return result


LRESULT = c_int64
HCURSOR = c_void_p

WNDPROC = WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)


class WNDCLASSW(Structure):
    _fields_ = [('style', w.UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', w.HINSTANCE),
                ('hIcon', w.HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', w.HBRUSH),
                ('lpszMenuName', w.LPCWSTR),
                ('lpszClassName', w.LPCWSTR)]


class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', w.HDC),
                ('fErase', w.BOOL),
                ('rcPaint', w.RECT),
                ('fRestore', w.BOOL),
                ('fIncUpdate', w.BOOL),
                ('rgbReserved', w.BYTE * 32)]


def MAKEINTRESOURCEW(x):
    return w.LPCWSTR(x)


user32.CreateWindowExW.argtypes = w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD, c_int, c_int, c_int, c_int, w.HWND, w.HMENU, w.HINSTANCE, w.LPVOID
user32.CreateWindowExW.restype = w.HWND
user32.CreateWindowExW.errcheck = errcheck
user32.LoadIconW.argtypes = w.HINSTANCE, w.LPCWSTR
user32.LoadIconW.restype = w.HICON
user32.LoadIconW.errcheck = errcheck
user32.LoadCursorW.argtypes = w.HINSTANCE, w.LPCWSTR
user32.LoadCursorW.restype = HCURSOR
user32.LoadCursorW.errcheck = errcheck
user32.RegisterClassW.argtypes = POINTER(WNDCLASSW),
user32.RegisterClassW.restype = w.ATOM
user32.RegisterClassW.errcheck = errcheck
user32.ShowWindow.argtypes = w.HWND, c_int
user32.ShowWindow.restype = w.BOOL
user32.UpdateWindow.argtypes = w.HWND,
user32.UpdateWindow.restype = w.BOOL
user32.UpdateWindow.errcheck = errcheck
user32.GetMessageW.argtypes = POINTER(w.MSG), w.HWND, w.UINT, w.UINT
user32.GetMessageW.restype = w.BOOL
user32.TranslateMessage.argtypes = POINTER(w.MSG),
user32.TranslateMessage.restype = w.BOOL
user32.DispatchMessageW.argtypes = POINTER(w.MSG),
user32.DispatchMessageW.restype = LRESULT
user32.BeginPaint.argtypes = w.HWND, POINTER(PAINTSTRUCT)
user32.BeginPaint.restype = w.HDC
user32.BeginPaint.errcheck = errcheck
user32.GetClientRect.argtypes = w.HWND, POINTER(w.RECT)
user32.GetClientRect.restype = w.BOOL
user32.GetClientRect.errcheck = errcheck
user32.DrawTextW.argtypes = w.HDC, w.LPCWSTR, c_int, POINTER(w.RECT), w.UINT
user32.DrawTextW.restype = c_int
user32.EndPaint.argtypes = w.HWND, POINTER(PAINTSTRUCT)
user32.EndPaint.restype = w.BOOL
user32.PostQuitMessage.argtypes = c_int,
user32.PostQuitMessage.restype = None
user32.DefWindowProcW.argtypes = w.HWND, w.UINT, w.WPARAM, w.LPARAM
user32.DefWindowProcW.restype = LRESULT
gdi32.SelectObject.argtypes = w.HDC, w.HGDIOBJ
gdi32.LineTo.argtypes = w.HDC, c_int, c_int
gdi32.MoveToEx.argtypes = w.HDC, c_int, c_int, w.LPPOINT
gdi32.Ellipse.argtypes = w.HDC, c_int, c_int, c_int, c_int
gdi32.SetPixel.argtypes = w.HDC, c_int, c_int, w.COLORREF

CW_USEDEFAULT = -2147483648
CS_HREDRAW = 2
CS_VREDRAW = 1

IDI_APPLICATION = MAKEINTRESOURCEW(32512)
IDC_ARROW = MAKEINTRESOURCEW(32512)


class Window:
    def __init__(self, posx: int = 0, posy: int = 0, width: int = 800, height: int = 600, title: str = "Python",
                 color: tuple = (255, 255, 255)):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.title = title
        self.back_color = color
        self.hwnd = None
        self.dwExStyle = 0
        self.dwStyle = flags.WindowStyles.WS_OVERLAPPEDWINDOW

    def show(self, *, mode=flags.ShowModes.SW_SHOW):
        wc = WNDCLASSW()
        wc.style = CS_HREDRAW | CS_VREDRAW
        wc.lpfnWndProc = WNDPROC(self.__WndProc)
        wc.cbClsExtra = wc.cbWndExtra = 0
        wc.hInstance = kernel32.GetModuleHandleW(None)
        wc.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
        wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
        wc.hbrBackground = gdi32.CreateSolidBrush(self.__RGBToColor(self.back_color))
        # wc.hbrBackground = None
        wc.lpszMenuName = None
        wc.lpszClassName = 'MainWin'

        user32.RegisterClassW(byref(wc))

        hwnd = user32.CreateWindowExW(self.dwExStyle,  # always on top
                                      wc.lpszClassName,
                                      self.title,  # window title
                                      self.dwStyle,
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
        self.dwStyle += flags.WindowStyles.WS_MAXIMIZE

    def minimize(self):
        self.dwStyle += flags.WindowStyles.WS_MINIMIZE

    @staticmethod
    def __WndProc(hwnd, message, wParam, lParam):
        ps = PAINTSTRUCT()
        rect = w.RECT()

        if message == flags.WindowMessages.WM_PAINT:
            hdc = user32.BeginPaint(hwnd, byref(ps))
            user32.GetClientRect(hwnd, byref(rect))
            user32.DrawTextW(hdc, "Hello from scheme", -1, byref(rect), 0x00000020 | 0x00000001 | 0x00000004)

            Window.drawLine(hdc, 0, 0, 100, 200)
            user32.EndPaint(hwnd, byref(ps))
        if message == flags.WindowMessages.WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        if message == flags.WindowMessages.WM_LBUTTONUP:
            print("clicked")
            # kernel32.MessageBox()
            # user32.SetWindowPos(hwnd, 0, 100, 100, 100, 100, 0)
            return 0
        return user32.DefWindowProcW(hwnd, message, wParam, lParam)

    @staticmethod
    def __RGBToColor(crColor: tuple):
        if len(crColor) == 3:
            if 0 <= crColor[0] < 256 and 0 <= crColor[1] < 256 and 0 <= crColor[2] < 256:
                return crColor[2] << 16 | crColor[1] << 8 | crColor[0]

        return None

    @staticmethod
    def createBrush(color):
        return gdi32.CreateSolidBrush(Window.__RGBToColor(color))

    @staticmethod
    def createPen(solid, width, color):
        return gdi32.CreatePen(solid, width, Window.__RGBToColor(color))

    @staticmethod
    def drawLine(hdc, start_x, start_y, end_x, end_y):
        pen = Window.createPen(0, 5, (0, 255, 255))
        gdi32.SelectObject(hdc, pen)
        gdi32.LineTo(hdc, end_x, end_y)
        gdi32.MoveToEx(hdc, start_x, start_y, None)
        gdi32.DeleteObject(pen)


if __name__ == '__main__':
    flex = flags.WindowExStyles
    fl = flags.WindowStyles

    window = Window()
    window.setTitle("sadasd")
    window.resize(800, 600)
    window.moveTo(0, 0)
    window.backColor(200, 10, 0)

    window.setdwExStyleFlags(flex.WS_EX_TOPMOST)
    # window.setdwStyleFlags(fl.WS_OVERLAPPEDWINDOW)
    # window.maximize()
    window.show()
