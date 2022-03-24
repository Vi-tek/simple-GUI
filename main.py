from ctypes import *
from ctypes import wintypes as w

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
# user32.BeginPaint.argtypes = w.HWND, POINTER(PAINTSTRUCT)
user32.BeginPaint.restype = w.HDC
user32.BeginPaint.errcheck = errcheck
user32.GetClientRect.argtypes = w.HWND, POINTER(w.RECT)
user32.GetClientRect.restype = w.BOOL
user32.GetClientRect.errcheck = errcheck
user32.DrawTextW.argtypes = w.HDC, w.LPCWSTR, c_int, POINTER(w.RECT), w.UINT
user32.DrawTextW.restype = c_int
# user32.EndPaint.argtypes = w.HWND, POINTER(PAINTSTRUCT)
user32.EndPaint.restype = w.BOOL
user32.PostQuitMessage.argtypes = c_int,
user32.PostQuitMessage.restype = None
user32.DefWindowProcW.argtypes = w.HWND, w.UINT, w.WPARAM, w.LPARAM
user32.DefWindowProcW.restype = LRESULT

# win32api = kernel32
# win32gui = user32
# win32con ?


CW_USEDEFAULT = -2147483648
CS_HREDRAW = 2
CS_VREDRAW = 1

IDI_APPLICATION = MAKEINTRESOURCEW(32512)
IDC_ARROW = MAKEINTRESOURCEW(32512)


class Flags:
    class dwExStyles:
        WS_EX_TOPMOST = 0x00000008
        WS_EX_TOOLWINDOW = 0x00000080
        WS_EX_STATICEDGE = 0x00020000
        WS_EX_RTLREADING = 0x00002000
        WS_EX_LEFT = 0x00000000
        WS_EX_RIGHT = 0x00001000
        WS_EX_WINDOWEDGE = 0x00000100
        WS_EX_CLIENTEDGE = 0x00000200
        WS_EX_ACCEPTFILES = 0x00000010
        WS_EX_OVERLAPPEDWINDOW = WS_EX_WINDOWEDGE | WS_EX_CLIENTEDGE

    class dwStyles:
        WS_BORDER = 0x00800000
        WS_CAPTION = 0x00C00000
        WS_CHILD = 0x40000000
        WS_DISABLED = 0x08000000
        WS_MAXIMIZE = 0x01000000
        WS_MAXIMIZEBOX = 0x00010000
        WS_MINIMIZE = 0x20000000
        WS_MINIMIZEBOX = 0x00020000
        WS_OVERLAPPED = 0x00000000
        WS_SYSMENU = 0x00080000
        WS_THICKFRAME = 0x00040000
        WS_OVERLAPPEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
        WS_POPUP = 0x80000000
        WS_POPUPWINDOW = WS_POPUP | WS_BORDER | WS_SYSMENU
        WS_VISIBLE = 0x10000000

    class showModes:
        SW_HIDE = 0
        SW_SHOWNORMAL = 1
        SW_NORMAL = 1
        SW_SHOWMINIMIZED = 2
        SW_SHOWMAXIMIZED = 3
        SW_MAXIMIZE = 3
        SW_SHOWNOACTIVATE = 4
        SW_SHOW = 5
        SW_MINIMIZE = 6
        SW_SHOWMINNOACTIVE = 7
        SW_SHOWNA = 8
        SW_RESTORE = 9
        SW_SHOWDEFAULT = 10
        SW_FORCEMINIMIZE = 11

    class windowMessages:
        WM_DESTROY = 0x0002


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
        self.dwStyle = Flags.dwStyles.WS_OVERLAPPEDWINDOW

    def show(self, *, mode=Flags.showModes.SW_SHOW):
        wc = WNDCLASSW()
        wc.style = CS_HREDRAW | CS_VREDRAW
        wc.lpfnWndProc = WNDPROC(self.__WndProc)
        wc.cbClsExtra = wc.cbWndExtra = 0
        wc.hInstance = kernel32.GetModuleHandleW(None)
        wc.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
        wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
        wc.hbrBackground = gdi32.CreateSolidBrush(self.__RGBToColor(self.back_color))
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
        self.dwStyle += Flags.dwStyles.WS_MAXIMIZE

    def minimize(self):
        self.dwStyle += Flags.dwStyles.WS_MINIMIZE

    @staticmethod
    def __WndProc(hwnd, message, wParam, lParam):
        if message == Flags.windowMessages.WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0

        return user32.DefWindowProcW(hwnd, message, wParam, lParam)

    @staticmethod
    def __RGBToColor(crColor: tuple):
        if len(crColor) == 3:
            if 0 < crColor[0] < 256 and 0 < crColor[1] < 256 and 0 < crColor[2] < 256:
                return crColor[2] << 16 | crColor[1] << 8 | crColor[0]

        return None


if __name__ == '__main__':
    flex = Flags.dwExStyles
    fl = Flags.dwStyles

    window = Window()
    window.setTitle("sadasd")
    window.resize(800, 600)
    window.moveTo(0, 0)
    window.backColor(202, 10, 20)
    window.setdwExStyleFlags(flex.WS_EX_TOPMOST)
    window.setdwStyleFlags(fl.WS_DISABLED)
    # window.maximize()
    window.show()
