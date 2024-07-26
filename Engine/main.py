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
import Engine.objects.base_objects.base_object as base_objects
from Engine.objects.render_objects.two_dimensional.image import imageRGBA
from Engine.objects.render_objects.three_dimensional.mesh import mesh
from Engine.objects.IO_objects.mouse_object import mouse
import pygame.locals
import ctypes

#importing main classes for displaying objects

#renderign apis

window_resolution= (1000,1000)

#creating basic globals for use inside of the engine
global_data.flags.update({'running': True})
global_data.flags.update({'frame_counter': 0})
global_data.flags.update({'delta_time': 0})
global_data.flags.update({'clear_display': True})
global_data.flags.update({'cpu_time': 0})
global_data.flags.update({'gpu_time': 0})
global_data.flags.update({'logger': logger.logger()})
global_data.flags.update({'key_logger': keylogger_object.keyLogger()})
global_data.flags.update({'mouse_logger': 'main'})
global_data.flags.update({'current_scene': 'main'})
global_data.flags.update({'mouse': mouse()})
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
screen_object = pygame.display.set_mode(window_resolution) #pygame.locals.DOUBLEBUF | pygame.locals.OPENGL)
global_data.flags.update({'screen_object': screen_object})
pygame.display.set_caption(global_data.flags['window_name'])



#TODO: Add buttons
#TODO: Add sound engine
#TODO: Juliafication - Converting some scripts into julia
#TODO: Add 3d
#Main loop
def mainloop(func=''):
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
            #getting instance of current screen texture
            current_screen_texture = global_data.flags['screen_image']
            #calling onRender for all objects
            global_scene_render_data = global_scene.toAll('__onRender__')
            local_scene_render_data = local_scene.toAll('__onRender__')
            #adding renderdata from local objects to screen (local first)
            for object_instance, render_data in local_scene_render_data.items():
                if not isinstance(object_instance, base_objects.engine_object):
                    logger.log('Non-engine object encountered while Rendering, skipping this object.', 'ERROR')
                else:
                    if isinstance(render_data, imageRGBA): #if the output is an image
                        object_location_x = object_instance.location[0]
                        object_location_y = object_instance.location[1]
                        current_screen_texture.__addCompositeLayer__(object_location_x, object_location_y, render_data)
                    if isinstance(render_data, mesh):
                        raise NotImplementedError('Not implemented 3d mesh rendering')

            #now adding renderdata from global objects
            t1 = time.perf_counter()
            for object_instance, render_data in global_scene_render_data.items():
                if not isinstance(object_instance, base_objects.engine_object):
                    logger.log('Non-engine object encountered while Rendering, skipping this object.', 'ERROR')
                else:
                    if isinstance(render_data, imageRGBA): #if the output is an image
                        object_location_x = object_instance.location[0]
                        object_location_y = object_instance.location[1]
                        current_screen_texture.__addCompositeLayer__(object_location_x, object_location_y, render_data)
                    if isinstance(render_data, mesh):
                        raise NotImplementedError('Not implemented 3d mesh rendering')
            t2 = time.perf_counter()
            # actually displaying whats in the screen
            current_screen_texture.__executeCompositing__(mode='XY')
            t4 = time.perf_counter()
            display_texture_as_arr = current_screen_texture.__asArrayRGB__()
            t5 = time.perf_counter()
            pygame_display_texture = pygame.surfarray.make_surface(display_texture_as_arr) #we cant use alpha channel so we discard it
            t6 = time.perf_counter()
            global_data.flags['screen_object'].blit(pygame_display_texture, (0, 0))
            t7 = time.perf_counter()
            pygame.display.flip() #actually updating screen
            t8 = time.perf_counter()
            if global_data.flags['clear_display']:
                current_screen_texture.__clear__() #clearing display texture
            t9 = time.perf_counter()

            frame_gpu_end = time.perf_counter()


            #calculating delta times
            global_data.flags['gpu_time'] = frame_gpu_end - frame_gpu_start
            global_data.flags['delta_time'] = global_data.flags['gpu_time'] + global_data.flags['cpu_time']
            global_data.flags['gpu_diagnostic'] = (f'{(t2-t1)*1000}ms to add all objects to object buffer\n'
                                                   f'{(t4-t2)*1000}ms to composite all objects to image\n'
                                                   f'{(t5-t4)*1000}ms to convert image to RGB array\n'
                                                   f'{(t6-t5)*1000}ms to convert image to pygame surface to display\n'
                                                   f'{(t7-t6)*1000}ms to add the new image to the display\n'
                                                   f'{(t8-t7)*1000}ms to refresh the display\n'
                                                   f'{(t9-t8)*1000}ms to clear the screen')
            #to allow custom per-loop logic
            try:
                if func != '':
                    func()
            except:
                logger.log('While attempting to execute main function, an error occurred', 'FATAL')





    except Exception as exc: #if all other error catching methods fail
        global_data.flags['logger'].log(f'An error has occurred, which has caused the program to crash: {exc}\n:'
                                        f'{misc_utils.getTraceback(exc)}')











