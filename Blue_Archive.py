import webbrowser
import time
import pyautogui
import win32api
import winsound
import ctypes


def set_resolution(width, height):
    class DEVMODE(ctypes.Structure):
        _fields_ = [("dmSize", ctypes.c_uint32),
                    ("dmDriverExtra", ctypes.c_uint32),
                    ("dmFields", ctypes.c_uint32),
                    ("dmPosition", ctypes.c_int),
                    ("dmPelsWidth", ctypes.c_long),
                    ("dmPelsHeight", ctypes.c_long),
                    ("dmDisplayFrequency", ctypes.c_long),
                    ("dmDisplayFlags", ctypes.c_long),
                    ("dmDisplayOrientation", ctypes.c_long),
                    ("dmDisplayFixedOutput", ctypes.c_long)]

    # 获取当前显示器设置
    current_settings = DEVMODE()
    current_settings.dmSize = ctypes.sizeof(DEVMODE)
    ctypes.windll.user32.EnumDisplaySettingsW(None, ctypes.c_uint32(0), ctypes.byref(current_settings))

    # 修改分辨率设置
    new_settings = DEVMODE()
    new_settings.dmSize = ctypes.sizeof(DEVMODE)
    new_settings.dmPelsWidth = width
    new_settings.dmPelsHeight = height
    new_settings.dmFields = 0x1 | 0x2

    # 尝试修改显示器分辨率
    result = ctypes.windll.user32.ChangeDisplaySettingsExW(None, ctypes.byref(new_settings), None, 0x2, None)
    if result == 0:
        print("屏幕分辨率已成功修改为 {}x{}".format(width, height))
    else:
        print("无法修改屏幕分辨率")

def get_resolution():
    sX = win32api.GetSystemMetrics(0)
    sY = win32api.GetSystemMetrics(1)
    if sX == 1920 and sY == 1080:
        pyautogui.moveTo(1550, 864, duration=1)
        pyautogui.click()
    else:
        set_resolution(1920, 1080)
        webbrowser.open('https://bluearchive-cn.com/')
        time.sleep(4)
        get_resolution()

WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_MAX = 0x0a
APPCOMMAND_VOLUME_MIN = 0x09
win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MAX * 0x10000)

webbrowser.open('https://www.bilibili.com/video/BV1xC4y1k7an/?spm_id_from=333.999.0.0&vd_source=f9b17b48e7f7cc5240a76a93bedc349e')
time.sleep(3)
webbrowser.open('https://bluearchive-cn.com/')
time.sleep(4)
get_resolution()
