import time

import pyautogui
while True:
    print(pyautogui.position())
    time.sleep(4)
    pyautogui.click()
