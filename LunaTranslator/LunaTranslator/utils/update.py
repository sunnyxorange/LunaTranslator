
import win32utils,os,win32con
def update():
    with open('./cache/update/update.bat','w',encoding='utf8') as ff:
                
                ff.write(r''' 

:start 
timeout 1
tasklist|find /i "Lunatranslator_main.exe" 
if %errorlevel%==0 goto start 

xcopy .\cache\update\LunaTranslator\ .\ /s /e /c /y /h /r 
exit
                
                ''') 
    win32utils.ShellExecute(None, "open", 'cache\\update\\update.bat', "", os.path.dirname('.'), win32con.SW_HIDE)