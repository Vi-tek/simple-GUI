from ctypes import WinDLL, WinError, get_last_error, \
    c_void_p, c_ubyte, c_int, c_short, Structure, WINFUNCTYPE, c_int64, POINTER
from ctypes.wintypes import *

user32 = WinDLL("user32", use_last_error=True)
kernel32 = WinDLL("kernel32", use_last_error=True)
gdi32 = WinDLL("gdi32", use_last_error=True)


def errcheck(result, func, args):
    if result is None or result == 0:
        raise WinError(get_last_error(), str(func, args))
    return result


LRESULT = c_int64
HCURSOR = c_void_p

WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)


class WNDCLASSW(Structure):
    _fields_ = [('style', UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', HINSTANCE),
                ('hIcon', HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', HBRUSH),
                ('lpszMenuName', LPCWSTR),
                ('lpszClassName', LPCWSTR)]


class RECT(Structure):
    _fields_ = [("Left", LONG),
                ("Top", LONG),
                ("Right", LONG),
                ("Bottom", LONG)]


class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', HDC),
                ('fErase', BOOL),
                ('rcPaint', RECT),
                ('fRestore', BOOL),
                ('fIncUpdate', BOOL),
                ('rgbReserved', BYTE * 32)]


# TEST
class RGBQUAD(Structure):
    _fields_ = [
        ('rgbRed', c_ubyte),
        ('rgbGreen', c_ubyte),
        ('rgbBlue', c_ubyte),
        ('rgbReserved', c_ubyte)
    ]


class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPlanes', WORD),  # 1
        ('biBitCount', WORD),  # 8
        ('biCompression', DWORD),  # BI_RGB = 0 for uncompressed format
        ('biSizeImage', DWORD),  # 0
        ('biXPelsPerMeter', LONG),  # 0
        ('biYPelsPerMeter', LONG),  # 0
        ('biClrUsed', DWORD),  # 0
        ('biClrImportant', DWORD)  # 0
    ]


class BITMAPINFO(Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', RGBQUAD * 256)
    ]


# TEST


def MAKEINTRESOURCEW(x):
    return LPCWSTR(x)


def LOWORD(long):
    return long & 0xFFFF


def HIWORD(long):
    return long >> 16


def GET_X_LPARAM(lp):
    return int(c_short(LOWORD(lp)).value)


def GET_Y_LPARAM(lp):
    return int(c_short(HIWORD(lp)).value)


user32.CreateWindowExW.argtypes = DWORD, LPCWSTR, LPCWSTR, DWORD, c_int, c_int, \
                                  c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID
user32.CreateWindowExW.restype = HWND
user32.CreateWindowExW.errcheck = errcheck
user32.LoadIconW.argtypes = HINSTANCE, LPCWSTR
user32.LoadIconW.restype = HICON
user32.LoadIconW.errcheck = errcheck
user32.LoadCursorW.argtypes = HINSTANCE, LPCWSTR
user32.LoadCursorW.restype = HCURSOR
user32.LoadCursorW.errcheck = errcheck
user32.RegisterClassW.argtypes = POINTER(WNDCLASSW),
user32.RegisterClassW.restype = ATOM
user32.RegisterClassW.errcheck = errcheck
user32.ShowWindow.argtypes = HWND, c_int
user32.ShowWindow.restype = BOOL
user32.UpdateWindow.argtypes = HWND,
user32.UpdateWindow.restype = BOOL
user32.UpdateWindow.errcheck = errcheck
user32.GetMessageW.argtypes = POINTER(MSG), HWND, UINT, UINT
user32.GetMessageW.restype = BOOL
user32.TranslateMessage.argtypes = POINTER(MSG),
user32.TranslateMessage.restype = BOOL
user32.DispatchMessageW.argtypes = POINTER(MSG),
user32.DispatchMessageW.restype = LRESULT
user32.BeginPaint.argtypes = HWND, POINTER(PAINTSTRUCT)
user32.BeginPaint.restype = HDC
user32.BeginPaint.errcheck = errcheck
user32.GetClientRect.argtypes = HWND, POINTER(RECT)
user32.GetClientRect.restype = BOOL
user32.GetClientRect.errcheck = errcheck
user32.DrawTextW.argtypes = HDC, LPCWSTR, c_int, POINTER(RECT), UINT
user32.DrawTextW.restype = c_int
user32.EndPaint.argtypes = HWND, POINTER(PAINTSTRUCT)
user32.EndPaint.restype = BOOL
user32.PostQuitMessage.argtypes = c_int,
user32.PostQuitMessage.restype = None
user32.DefWindowProcW.argtypes = HWND, UINT, WPARAM, LPARAM
user32.DefWindowProcW.restype = LRESULT
gdi32.SetPixel.argtypes = HDC, c_int, c_int, COLORREF
gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.BitBlt.argtypes = HDC, c_int, c_int, c_int, c_int, HDC, c_int, c_int, DWORD
IDC_ARROW = MAKEINTRESOURCEW(32512)
