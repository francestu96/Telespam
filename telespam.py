import pyautogui as pya
import pyperclip
import argparse
import requests
import json
import time
import sys
import re

def write_message(username, name):
  pya.write("Hi " + name + "!", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("You requested for a password reset for you account via Telegram.", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Your Telegram ID: " + username, interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Your new password:", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write(PASSWORD, interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Login to " + URL + "/auth to change it.", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Please, if you don't request for a password reset, discard this message!", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Sincerly,", interval=0.001)
  pya.keyDown('shift')
  pya.hotkey('enter')
  pya.keyUp('shift')
  pya.write("Your ProtonCash support Team!", interval=0.001)

  pya.moveTo(tuple(env["username_pos"].values()))
  pya.doubleClick()
  time.sleep(0.2)
  pya.moveTo(tuple(env["username_bold_pos"].values()))
  pya.click()
  pya.move(env["button_offset"], 0)
  pya.click()

  pya.moveTo(tuple(env["password_pos"].values()))
  pya.click()
  time.sleep(0.25)
  pya.doubleClick()
  time.sleep(0.2)
  pya.moveTo(tuple(env["password_bold_pos"].values()))
  pya.click()
  pya.move(env["button_offset"], 0)
  pya.click()

parser = argparse.ArgumentParser(prog='Telespam', description='Spam messages on Telegram')
parser.add_argument('chats', type=int, help='how many chats spam the message to')
parser.add_argument('-e', '--env', default="full_hd-125x", help='the resolution of the screen')
args = parser.parse_args()

URL = "https://protoncash.vercel.app"
PASSWORD = "25397346"

with open("environments.json") as env_file:
  env = json.load(env_file)[args.env]

pya.moveTo(tuple(env["title_pos"].values()))
pya.click()

scroll_value = env["scroll_value_init"]
for _ in range(int(sys.argv[1])):
  pya.moveTo(tuple(env["group_pos"].values()), duration=0.1)
  time.sleep(0.25)
  pya.scroll(scroll_value)
  time.sleep(0.25)
  pya.click()

  time.sleep(0.25)
  at = pya.locateCenterOnScreen('at.png', grayscale=True, confidence=0.78)
  time.sleep(0.25)

  if at:
    pya.moveTo(at, duration=0.1)
    pya.click()

    username = pyperclip.paste()

    try:
      name_match = re.search("[A-Z][a-z]+", username)
      if(not name_match):
        name_match = re.search("[a-z]+", username)

      name = name_match.group()
      if(len(name) < 3):
        name += "96"

      if name == username:
        name = username[0:3]

      registration = requests.post(URL + "/api/register", {"name": name.capitalize(), "telegramId": username, "password": PASSWORD })

      if registration.status_code != 200:
        raise Exception(registration.text)

      write_message(username, name)
      # pya.press('enter')
    except Exception as e:
      print("Exception for username: " + username)
      print(e)

  back = pya.locateCenterOnScreen('back.png', grayscale=True, confidence=0.78)

  if not back:
    raise Exception("Cannot locate back arrow image")

  pya.moveTo(back, duration=0.1)
  pya.click()
  scroll_value += env["scroll_value"]