""" Created to control the clicks of the mouse to gather data from GEE"""

from pynput.mouse import Button, Controller
import time

# Time for changing the window to browser
time.sleep(2)

mouse = Controller()

# Hardcoded values for mouse to click
run_position = (1490, 200)
dialogue_position = (602, 596)

# Changing mouse position to click Run Button in Tasks Bar
mouse.position = run_position

for i in range(73):
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)

    # Changing mouse position to click Run button in Dialogue Box
    mouse.position = dialogue_position
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)

    mouse.position = run_position

    # Scroll for next Run button
    mouse.scroll(0, -0.284)
    time.sleep(1)

    # Adjusting the scroll
    if i == 55:
        mouse.scroll(0, 0.21)
        time.sleep(1)