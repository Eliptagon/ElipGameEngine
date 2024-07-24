import Engine.utils.data_handling.global_data as global_data #global data_handling that is shared between files

from Engine.objects.base_objects.base_object import engine_object


#method for creating game objects
def createObject(object_class, scene, name): #makes an object and properly distributes it
    object_instance = object_class()
    object_instance.__onCreate__(name)
    global_data.objects.update({name: object_instance})
    scene.objects.update({name: object_instance})
    return object_instance


#method that checks if the object provided is a game engine object
def checkObject(input_object, input_object_name):
    logger = global_data.flags['logger']
    if not isinstance(input_object, engine_object):  # Type check to ensure that the object
        logger.log(
            f'object named {input_object_name} is of type {type(input_object)} (not a game engine object'
            f' / variant of game engine object)', 'FATAL', 2)
    return input_object


#method that can be used to execute a function of an object with extra error handling
def safeExecute(input_object, input_object_name, function, **funcArgs):
    logger = global_data.flags['logger']
    input_object = checkObject(input_object, input_object_name)
    returning_object = None #object that will be returned if the object errors
    try:
         returning_object = function(**funcArgs)
    except Exception as exc1:  # allow the object to try and handle its own error
        logger.log(message = f'Object named {input_object_name} has errored while executing: {function.__name__}!, attempting to let the object to'
                   f' recover', exception = exc1, severity = 'ERROR')
        try:
            recoverable = input_object.__onError__()  # see if the object thinks it can be recovered
            if recoverable:
                logger.log(f'Object named {input_object_name} thinks situation is recoverable, resuming', 'INFO')  #
            else:
                logger.log(f'Object named {input_object_name} thinks situation is NOT recoverable,'
                           f' closing now...', 'FATAL', 3)
        except Exception as exc2:
            logger.log(f'Object named {input_object_name} Errored further when attempting to correct.\n',exc2, 'FATAL', 4)

    return returning_object#returning the output of teh function executed