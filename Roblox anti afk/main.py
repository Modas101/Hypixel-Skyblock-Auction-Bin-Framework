import win32gui, win32ui, win32con, win32api
import time

def main():
    window_name = "Roblox"
    #list_window_names()
    hwnd = win32gui.FindWindow(None, window_name)
    get_inner_windows(hwnd)
    win = win32ui.CreateWindowFromHandle(hwnd)

    win.SendMessage(win32con.WM_KEYDOWN, 0x57, 0)
    time.sleep(2)
    win.SendMessage(win32con.WM_KEYUP, 0x57, 0)


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), '"' + win32gui.GetWindowText(hwnd) + '"')
    win32gui.EnumWindows(winEnumHandler, None)


def get_inner_windows(whndl):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds = {}
    win32gui.EnumChildWindows(whndl, callback, hwnds)
    print(hwnds)
    return hwnds


def find_all_windows(name):
    result = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, None)
    return result

main()