#Naming sceme for this game engine: methods follow camelCaps,
#Classes follow snake_undercore, and special classes used by the engine follow __class_name__ naming

#main reason for this engine to be written in python is so that the objects can utilise ANY language that can interface with python, ideally

import time
#importing utils
import Engine.utils.logger as logger
import Engine.utils.global_data as global_data
import Engine.utils.object_handling.scene_objects as scene_object_handler
import Engine.utils.misc as misc_utils
#importing engine objects
import Engine.objects.keylogger_object as keylogger_object
import Engine.objects.scene_object as scene_object

#importing main classes for displaying objects
import Engine.objects.rendering.texture as textures #will be used as the screen
import Engine.objects.rendering.mesh as meshes

#renderign apis
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

#creating basic globals for use inside of the engine
global_data.flags.update({'running': True})
global_data.flags.update({'frame_counter': 0})
global_data.flags.update({'delta_time': 0})
global_data.flags.update({'cpu_time': 0})
global_data.flags.update({'gpu_time': 0})
global_data.flags.update({'logger': logger.logger()})
global_data.flags.update({'key_logger': keylogger_object.keyLogger()})
global_data.flags.update({'current_scene': 'main'})

global_data.flags.update({'window_name': 'Sexy window'})
global_data.flags.update({'window_resolution': (500,500)})




#data involving scenes
scene_object_handler.createScene('main', scene_object.scene) #making a basic scene
scene_object_handler.createScene('global', scene_object.scene) #this scene is for all of the global objects
#getting window resolution
window_res = global_data.flags['window_resolution']
display_texture = textures.texture(window_res[0], window_res[1])




#initialising window, need to add options to be able to customise it
glfw.init()
window = glfw.create_window(window_res[0], window_res[1], global_data.flags['window_name'], None, None)
if not window:
    global_data.flags['logger'].log('Unable to make openGL window', 'FATAL', 8)

global_data.flags.update({'window_object': window})





#Main loop
def mainloop():
    try:
        logger = global_data.flags['logger']
        logger.log('Starting Game', 'INFO')
        while global_data.flags['running']:
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

            glfw.poll_events()
            glfw.swap_buffers(global_data.flags['window_object'])
            frame_gpu_end = time.perf_counter()
            #calculating delta times
            global_data.flags['gpu_time'] = frame_gpu_end - frame_gpu_start
            global_data.flags['delta_time'] = global_data.flags['gpu_time'] + global_data.flags['cpu_time']


    except Exception as exc: #if all other error catching methods fail
        global_data.flags['logger'].log(f'An error has occurred, which has caused the program to crash: {exc}\n:'
                                        f'{misc_utils.getTraceback(exc)}')











