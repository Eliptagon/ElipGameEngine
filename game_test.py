import random
import time

import numpy as np
import sys

from Engine import main
from Engine.objects.base_objects.base_object import engine_object
import Engine.utils.data_handling.global_data as data
import Engine.utils.object_handling.base_objects as obj_handler
import Engine.objects.render_objects.two_dimensional.image as image_handler
import numba

import pygame
pygame.mixer.init()
base_scene = data.scenes['main']
data.flags['LU'] = time.perf_counter()

data.flags['particleAmount'] = 5
data.flags['particle_x_pos'] = 0

data.flags['gravity'] = [0,1,0]

data.flags['clear_display'] = True
class testObj(engine_object):
    def __init__(self):
        super().__init__()
        self.start_time = time.perf_counter()
        self.velocity = np.array([0, 0, 0], dtype=np.float64)
        x_pos = data.flags['particle_x_pos']
        data.flags['particle_x_pos'] += data.flags['window_resolution'][0] / data.flags['particleAmount']
        self.location = np.array([x_pos, 300, 0], dtype=np.float64)
        self.bounce_texture = image_handler.imageRGBA((3, 3))
        self.baseArray = np.random.randint(0, 255, (3,3))
        self.bounce_texture.__setLayer__('r',self.baseArray)
        self.bounce_texture.__setLayer__('g', self.baseArray)
        self.bounce_texture.__setLayer__('b', self.baseArray)
        #self.bounce_texture.__fromFile__('test_assets/ballNormal.png')
        self.rebound_texture = image_handler.imageRGBA((3, 3))
        self.bounciness = random.random()/3 + 0.5

        self.texture = self.bounce_texture





    def __onUpdate__(self, local_scene) -> None:
        if time.perf_counter() > data.flags['LU'] + 1:
            data.flags['LU'] = time.perf_counter()
            self.start_time = time.perf_counter()
            try:
                print(f'{data.flags['cpu_time']*1000}ms for CPU,\n'
                    f'{data.flags['gpu_time']*1000}ms for GPU.\n'
                    f'FPS: {1/data.flags['delta_time']}\n')
                print(data.flags['gpu_diagnostic'])
            except:
                pass
        self.location += self.velocity
        #adding gravity
        self.velocity -= np.array(data.flags['gravity']) *5* np.array(data.flags['delta_time'])
        if self.location[0] < 10:
            self.collide([10, self.location[1], self.location[2]], 0)
        if self.location[0] > 990:
            self.collide([990, self.location[1], self.location[2]], 0)
        if self.location[1] < 10:
            self.location[1] = 10
            self.velocity[1] = 0-self.velocity[1] * self.bounciness
        if self.location[1] > 990:
            self.location[1] = 990
            self.velocity[1] = 0-self.velocity[1] * self.bounciness

    def collide(self, reset_loc, axis):
        self.location = reset_loc
        self.velocity[axis] = 0 - (self.velocity[axis]*self.bounciness)

    def __onEvent__(self, event_name, event_data) -> None:
        if event_data == 'Key.esc_down':
            sys.exit()
        if event_data == 'd_up':
            data.flags['gravity'] += np.array([-1, 0, 0])
        if event_data == 'a_up':
            data.flags['gravity'] += np.array([1, 0, 0])
        if event_data == 'w_up':
            data.flags['gravity'] += np.array([0, -1, 0])
        if event_data == 's_up':
            data.flags['gravity'] += np.array([0, 1, 0])
        if event_data == 'Key.space_up':
            data.flags['gravity'] = [0, 0, 0]

    def __onRender__(self) -> None:
        return self.texture

class testObj2(engine_object):
    def __init__(self):
        self.texture = image_handler.imageRGBA((1000,1000))
        super().__init__()
        self.mouse = data.flags['mouse']
        self.location = [0,1000,0]
    def __onUpdate__(self, local_scene) -> None:
        self.mouse.__onUpdate__('')
        if time.perf_counter() > data.flags['LU'] + 1:
            data.flags['LU'] = time.perf_counter()
            try:
                print(f'{data.flags['cpu_time']*1000}ms for CPU,\n'
                    f'{data.flags['gpu_time']*1000}ms for GPU.\n'
                    f'FPS: {1/data.flags['delta_time']}\n')
                print(data.flags['gpu_diagnostic'])
            except:
                pass

        crosshairtexture =  self.getCrosshair((1000,1000), self.mouse.screen_loc)
        self.texture.__setLayer__('r', crosshairtexture)
        self.texture.__setLayer__('g', crosshairtexture)
        self.texture.__setLayer__('b', crosshairtexture)
        self.texture.__setLayer__('a', crosshairtexture)


    def __onRender__(self) -> None:
        return self.texture
    @staticmethod
    #@numba.njit
    def getCrosshair(size, mouse_loc):
        crosshair_arr = np.zeros(size)
        print(mouse_loc)
        for row in range(size[0]):
            crosshair_arr[row,mouse_loc[1]] = 128
        for col in range(size[1]):
            crosshair_arr[mouse_loc[0], col] = 255
        return crosshair_arr

    def __onEvent__(self, event_name, event_data) -> None:
        if event_data == 'Key.esc_down':
            sys.exit()









obj_handler.createObject(testObj2, data.scenes['main'], 'bob')
for x in range(data.flags['particleAmount']):
    obj_handler.createObject(testObj, data.scenes['main'], f'bob2{x}')



main.mainloop()