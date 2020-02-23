import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pynput.mouse import Button, Controller, Listener


chrome_options = Options()
driver = webdriver.Chrome()

positions = []
classes_dictionary = {'water': [],
                      'build-up areas': []}

mouse_controller = Controller()
driver.get("https://www.google.co.in/maps/@18.5339901,73.8642073,15.5z")


def on_click(x, y, button, pressed):
    if pressed:
        positions.append((x, y))


def recorder():
    counter = 1
    for key in classes_dictionary.keys():
        print(f"GROUND VERIFICATION record generation for class: {key}")
        print("First click the 'blank spot' and then 5 consecutive clicks for recording Class Data")

        listener = Listener(on_click=on_click)
        listener.start()
        while len(positions) != counter*6:
            continue
        listener.stop()
        print("Actions Recorded !\n")
        counter += 1


def player():
    for key in classes_dictionary.keys():
        lat_long_list = []
        print(f"\nRECORDING DATA : class {key}\n")
        blank = positions.pop(0)

        for i in range(0, 5):
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
            print(lat_long)
            lat_long_list.append(lat_long)

        classes_dictionary[key] = classes_dictionary.get(key, []) + lat_long_list
    time.sleep(2)


def create_csv(dictionary={}):
    data = []
    values_list = []
    with open('ground_verification.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['lat', 'long', 'class'])

        for key, values in dictionary.items():
            for value in values:
                value_split = value.split(",")
                values_list.extend(value_split)

            for index in range(0, len(values_list), 2):
                data.append([values_list[index], values_list[index + 1], key])
            filewriter.writerows(data)


recorder()
player()
print(classes_dictionary)
create_csv(classes_dictionary)
