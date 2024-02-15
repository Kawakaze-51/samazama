import webbrowser
import time
import win32api
import winsound


WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_MAX = 0x0a
APPCOMMAND_VOLUME_MIN = 0x09
win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MAX * 0x10000)

webbrowser.open('https://www.bilibili.com/video/BV1xC4y1k7an/?spm_id_from=333.999.0.0&vd_source=f9b17b48e7f7cc5240a76a93bedc349e')
time.sleep(3)
webbrowser.open('https://webcnstatic.yostar.net/pubplat/gpp/sdkpackage/prod/task_game_apk/official/1.7.1/BlueArchive_official_1.7.1.apk')
