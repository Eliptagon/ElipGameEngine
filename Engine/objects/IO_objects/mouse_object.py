import time
from Engine.objects.base_objects.base_object import engine_object
import Engine.utils.data_handling.global_data as data
import pyautogui
import pygetwindow as gw
import numpy as np

class mouse(engine_object):
    def __click__(self, location, amount, interval):
        pyautogui.click()

    def __onUpdate__(self, local_scene) -> None:
        # setting location of mouse object to location of actual mouse cursor
        screen_res = pyautogui.size()
        try:
            pygame_window_size = data.flags['window_resolution']
            window_name = data.flags['window_name']
        except KeyError:
            pygame_window_size = (500, 500)
            window_name = ''

        win = gw.getWindowsWithTitle(window_name)
        if win:
            window_x, window_y = win[0].topleft
            window_y = screen_res[1] - window_y
        else:
            window_x = 0
            window_y = 0

        pointer_location = [
            pyautogui.position()[0],
            screen_res[1] - pyautogui.position()[1],
            0
        ]

        checked_loc = [max(axis, 0) for axis in pointer_location]

        screen_loc = np.zeros(3, dtype=np.int64)

        if window_x <= checked_loc[0] <= window_x + pygame_window_size[0] - 1:
            screen_loc[0] = checked_loc[0] - window_x
        else:
            screen_loc[0] = -1

        if window_y >= checked_loc[1] <= window_y + pygame_window_size[0] - 1:
            screen_loc[1] = window_y - checked_loc[1]
        else:
            screen_loc[1] = -1

        self.screen_loc = screen_loc
        self.loc = np.array(checked_loc)

    def __setLocation__(self, position: tuple | list):
        pyautogui.moveTo(position[0], position[1])
        self.__onUpdate__('')  # refreshing mouse location









