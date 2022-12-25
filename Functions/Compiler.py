import sys
from time import sleep
import webbrowser, pyautogui
from pywinauto.keyboard import send_keys

def executar(code):
    codeObject = compile(code, 'sumstring', 'exec')
    exec(codeObject)


