import Engine.utils.global_data as global_data
from Engine.objects.scene_object import scene

def getSceneFromName(scene_name):
    logger = global_data.flags['logger']

    try:  # check to do a proper crash if the specified scene does not exist
        current_scene = global_data.scenes[scene_name]  # Sets variable current_scene to the current scene

        if not isinstance(current_scene, scene):  # if the current scene object is not a scene object
            logger.log(f'Error while executing Mainloop: Scene object {scene_name}, it'
                       f' is of type: {type(current_scene)}, not a scene / variant of scene.')

        return current_scene #returns scene if it is valid
    except KeyError as exc:
        logger.log(f'Error while executing Mainloop: Scene {scene_name} does not exist.', exc, 'FATAL', 1)

def createScene(name, scene_class):
    scene = scene_class()
    global_data.scenes.update({name: scene})
    return scene