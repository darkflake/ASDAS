import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pynput.mouse import Button, Controller
from pynput.mouse import Listener as ml
from pynput.keyboard import Key
from pynput.keyboard import Listener as kl

chrome_options = Options()
driver = webdriver.Chrome()

key_pressed = [0]
positions = []

mouse_controller = Controller()
driver.get("https://www.google.co.in/maps/@18.5308356,73.8618938,15.21z")


def on_click(x, y, button, pressed):
    if pressed:
        positions.append((x, y))


def on_press(key):
    if key == Key.caps_lock:
        key_pressed[0] = 1
    elif key == Key.esc:
        key_pressed[0] = 2


def recorder():
    while True:
        try:
            satellite = driver.find_element_by_xpath('//*[@id="minimap"]/div/div[2]/button')
            break
        except Exception:
            time.sleep(0.1)
            continue
    satellite.click()

    class_label = input("Enter the class label for GROUND VERIFICATION record generation : ")
    print("Press CAPS LOCK to start and ESC to end the recording.")

    key_listener = kl(on_press=on_press)
    mouse_listener = ml(on_click=on_click)
    is_pressed = False

    key_listener.start()

    while key_pressed[0] == 0 or key_pressed[0] == 1:
        time.sleep(1)
        if key_pressed[0] == 1 and not is_pressed:
            mouse_listener.start()
            print("Starting the recorder")
            is_pressed = True
            continue
        if key_pressed[0] == 2 and is_pressed:
            mouse_listener.stop()
            key_listener.stop()
            print("\nActions recorded !")
            break
        else:
            continue
    return class_label


def player():
    lat_long_list = []
    print(f"\nRecording Data Now\n")
    blank = positions.pop(0)
    mouse_listener = ml(on_click=on_click)
    mouse_listener.start()

    for i in range(len(positions)):
        pos = positions.pop(0)

        time.sleep(1)

        mouse_controller.position = blank
        mouse_controller.press(Button.left)
        mouse_controller.release(Button.left)

        time.sleep(1)
        mouse_controller.position = pos
        mouse_controller.press(Button.left)
        mouse_controller.release(Button.left)

        time.sleep(2)
        lat_long = driver.find_element_by_xpath('//*[@id="reveal-card"]/div/div[2]/button[2]').get_attribute("aria-label")
        coordinates = lat_long.split(",")
        lat_long_list.append(coordinates)
        mouse_listener.stop()

    return lat_long_list


def create_csv():
    class_label = recorder()
    lat_long_list = player()
    data = []
    entry_list = []

    with open('ground_verification.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['coordinates', 'class'])

        for entry in lat_long_list:
            data.clear()
            data.append(entry)
            data.append(class_label)
            entry_list.append(data)
        filewriter.writerows(entry_list)
    print("Done !")


create_csv()
