import time

from Engine import main
from Engine.objects.base_objects.base_object import engine_object
import Engine.utils.data_handling.global_data as data
import Engine.utils.object_handling.base_objects as obj_handler

import pygame
pygame.mixer.init()
base_scene = data.scenes['main']


class testObj(engine_object):
    def __init__(self):
        super().__init__()
        self.start_time = time.perf_counter()
    def __onUpdate__(self, local_scene) -> None:
        if time.perf_counter() > self.start_time + 1:
            self.start_time = time.perf_counter()
            print(f'{data.flags['cpu_time']*1000}ms for CPU,\n'
                  f'{data.flags['gpu_time']*1000}ms for GPU.\n'
                  f'FPS: {1/data.flags['delta_time']}\n')

obj_handler.createObject(testObj, base_scene, 'Bob')


main.mainloop()