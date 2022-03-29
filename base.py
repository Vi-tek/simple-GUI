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


IDI_APPLICATION = MAKEINTRESOURCEW(32512)
IDC_ARROW = MAKEINTRESOURCEW(32512)
