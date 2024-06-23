import PIL.ImageGrab
import pytesseract
import numpy as np
import cv2
import time
from discord_webhook import DiscordWebhook
from pynput.keyboard import Key
import pyautogui

import pynput

from PIL import Image, ImageDraw
import PIL.ImageOps

keyboard = pynput.keyboard.Controller()
#mouse = pynput.mouse.Controller()

cropRect = (299, 274, 502, 288)
#cropRect = (169, 631, 357, 646)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def getMerchantResult():
    img = PIL.ImageGrab.grab().crop(cropRect)

    r, g, b = img.getpixel((202, 13))

    pixels = img.load()

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            if pixels[i, j] == (r, g, b):
                # change to black if not red
                pixels[i, j] = (0, 0, 0)

    threshold = 40

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]

            if abs((r + g + b) - (255 + 255 + 255)) > threshold:
                # change to black if not red
                pixels[i, j] = (0, 0, 0)

    img = PIL.ImageOps.invert(img)
    img.save("image.png")

    values = pytesseract.image_to_string(img, config="-l eng --psm 6")

    result = values.lower()
    return result

def pressKey(c):
    keyboard.press(c)
    time.sleep(0.1)
    keyboard.release(c)

def ResetPlayer():
    img = PIL.ImageGrab.grab().crop((125, 216, 126, 217))
    r1, g1, b1 = img.getpixel((0, 0))

    pressKey(Key.esc)
    time.sleep(1)
    pressKey("r")
    time.sleep(1)
    pressKey(Key.enter)

    while True:
        time.sleep(2)
        img = PIL.ImageGrab.grab().crop((125, 216, 126, 217))
        r2, g2, b2 = img.getpixel((0, 0))
        print("respawned", r2, g2, b2, r1, g1, b1)
        if r2 == r1 and g2 == g1 and b2 == b1:
            break

def RejoinServer():
    pressKey(Key.esc)
    time.sleep(1)
    pressKey("l")
    time.sleep(1)
    pressKey(Key.enter)

    time.sleep(5)

    #pyautogui.dragTo(160, 450)

    #time.sleep(0.1)
    #pressKey(Key.cmd)
    #time.sleep(0.1)

    #pyautogui.click(160, 450, 1)
    #time.sleep(0.1)
    #pyautogui.click(160, 450, 1)

    #time.sleep(1)

    #time.sleep(0.1)
    #pressKey(Key.cmd)
    #time.sleep(0.1)

    #pyautogui.click(160, 450, 1)
    #time.sleep(0.1)
    #pyautogui.click(160, 450, 1)

    #time.sleep(1)

    for i in range(0, 12):
        pyautogui.scroll(-5000)
    pyautogui.scroll(5000)

    pyautogui.moveTo(190, 170)

    time.sleep(0.5)

    pressKey(Key.cmd)
    time.sleep(0.1)
    pressKey(Key.cmd)
    time.sleep(0.5)

    pyautogui.click(190, 170, 1)
    time.sleep(0.1)
    pyautogui.click(190, 170, 1)

    time.sleep(5)

    pyautogui.moveTo(100, 490)
    time.sleep(0.2)
    pyautogui.click(100, 490, 1)
    time.sleep(0.1)
    pyautogui.click(100, 490, 1)

def typeWord(str):
    for c in str:
        pressKey(c)

def JoinAzureRest():
    pressKey("0")

    time.sleep(0.2)

    pyautogui.click(270, 80, 1)

    time.sleep(5)

    typeWord("/Confirm")
    pressKey(Key.enter)

def SetupAzureRest():
    typeWord("//skipall")
    pressKey(Key.enter)

    while True:
        SummonEverything()
        time.sleep(10)

def UseAllAbility():
    pressKey("z")
    pressKey("x")
    pressKey("c")

def SummonEverything():
    for i in range(1, 7):
        pressKey(str(i))
        pyautogui.click(270, 80, 1)
        UseAllAbility()

def GoToRainMerchant():
    ResetPlayer()

    keyboard.press("d")
    time.sleep(2.5)
    keyboard.release("d")

    keyboard.press("s")
    time.sleep(0.25)
    keyboard.release("s")


#RejoinServer()

#ResetPlayer()
time.sleep(3)
#result = getMerchantResult()
#print(result)
GoToRainMerchant()
#GoToRainMerchant()

#while(True):
    #result = getMerchantResult()

    #webhook = DiscordWebhook(
    #    url="removed",
    #    content=result)
    #response = webhook.execute()
    #webhook.delete()

    #if result.find("arb") != -1:
    #    webhook = DiscordWebhook(url="removed", content="arb found @everyone")
    #    response = webhook.execute()
    #    webhook.delete()

    #    print("Arbitration found")

    #time.sleep(1)
