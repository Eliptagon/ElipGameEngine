#Naming sceme for this game engine: methods follow camelCaps,
#Classes follow snake_undercore, and special classes used by the engine follow __class_name__ naming

#main reason for this engine to be written in python is so that the objects can utilise ANY language that can interface with python, ideally

import time

import numpy as np
import pygame.display

#importing utils
import Engine.utils.error_handling.logger as logger
import Engine.utils.data_handling.global_data as global_data
import Engine.utils.object_handling.scene_objects as scene_object_handler
import Engine.utils.misc as misc_utils
#importing engine objects
import Engine.objects.IO_objects.keylogger_object as keylogger_object
import Engine.objects.base_objects.scene_object as scene_object
from Engine.objects.render_objects.two_dimensional.image import imageRGBA

#importing main classes for displaying objects

#renderign apis

window_resolution= (1920,1080)

#creating basic globals for use inside of the engine
global_data.flags.update({'running': True})
global_data.flags.update({'frame_counter': 0})
global_data.flags.update({'delta_time': 0})
global_data.flags.update({'clear_display': True})
global_data.flags.update({'cpu_time': 0})
global_data.flags.update({'gpu_time': 0})
global_data.flags.update({'logger': logger.logger()})
global_data.flags.update({'key_logger': keylogger_object.keyLogger()})
global_data.flags.update({'current_scene': 'main'})

global_data.flags.update({'window_name': 'Sexy window'})
global_data.flags.update({'window_resolution': window_resolution})
#making screen textur of correct size
global_data.flags.update({'screen_image': imageRGBA(window_resolution)})





#data_handling involving scenes
scene_object_handler.createScene('main', scene_object.scene) #making a basic scene
scene_object_handler.createScene('global', scene_object.scene) #this scene is for all of the global objects
#getting window resolution
window_res = global_data.flags['window_resolution']




#making the window:
pygame.init()
screen_object = pygame.display.set_mode(window_resolution)
global_data.flags.update({'screen_object': screen_object})
pygame.display.set_caption(global_data.flags['window_name'])



#TODO: Add buttons
#TODO: Add sound engine
#TODO: Juliafication - Converting some scripts into julia
#TODO: Add 3d
#Main loop
def mainloop():
    try:
        logger = global_data.flags['logger']
        logger.log('Starting Game', 'INFO')
        while global_data.flags['running']:
            pygame.event.get() #to ensure window does not close
            frame_cpu_start = time.perf_counter() #cpu time of when the frame started
            global_data.flags['frame_counter'] += 1
            local_scene_name = global_data.flags['current_scene'] #getting current scene name
            local_scene = scene_object_handler.getSceneFromName(local_scene_name)
            global_scene = scene_object_handler.getSceneFromName('global')
            #doing all updates of all of the objects
            global_scene.toAll('__onUpdate__', local_scene = global_scene)
            local_scene.toAll('__onUpdate__', local_scene = local_scene)


            #sending key inputs to objects
            for keyEvent in global_data.flags['key_logger'].stacked_key_inputs:
                global_scene.toAll('__onEvent__', event_name='onKeyEvent', event_data=keyEvent)
                local_scene.toAll('__onEvent__', event_name = 'onKeyEvent', event_data = keyEvent)
            #clearing the key events for this frame
            global_data.flags['key_logger'].clear()

            #calculating cpu delta time
            frame_cpu_end = time.perf_counter()
            global_data.flags['cpu_time'] = frame_cpu_end - frame_cpu_start
            frame_gpu_start = time.perf_counter()
            #calling onRender for all objects
            current_screen_texture = global_data.flags['screen_image']

            # actually displaying whats in the screen

            display_texture_as_arr = current_screen_texture.__asArrayRGB__()
            pygame_display_texture = pygame.surfarray.make_surface(display_texture_as_arr) #we cant use alpha channel so we discard it
            global_data.flags['screen_object'].blit(pygame_display_texture, (0, 0))
            pygame.display.flip() #actually updating screen
            if global_data.flags['clear_display']:
                current_screen_texture.__clear__() #clearing display texture

            frame_gpu_end = time.perf_counter()


            #calculating delta times
            global_data.flags['gpu_time'] = frame_gpu_end - frame_gpu_start
            global_data.flags['delta_time'] = global_data.flags['gpu_time'] + global_data.flags['cpu_time']





    except Exception as exc: #if all other error catching methods fail
        global_data.flags['logger'].log(f'An error has occurred, which has caused the program to crash: {exc}\n:'
                                        f'{misc_utils.getTraceback(exc)}')











