from Engine.objects.base_object import engine_object #the base object
import Engine.utils.global_data as global_data
from Engine.utils.misc import getTraceback
from Engine.utils.object_handling.base_objects import safeExecute

class scene(engine_object):
    def __init__(self):
        super().__init__()

        self.active_camera = int()

        self.objects = dict()

        self.render_layers = list() #list of render layer objects

        self.local_vars = dict()
    def toAll(self, func_name, **func_kwargs):
        for  object_name, object_instance in self.objects.items():
            try:
                safeExecute(object_instance, object_name, getattr(object_instance, func_name), **func_kwargs)
            except Exception as exc:
                logger = global_data.flags['logger']
                logger.log(f'An error has occurred while attempting to execute object.{func_name},'
                           f' as it has not got the specified function. Traceback: {getTraceback(exc)}', 'FATAL', 8)

    def __repr__(self):
        return 'Scene'
        repr_str = 'A generic scene object with locals:'
        for local_value_name, local_var_value in self.local_vars.items():
            repr_str += f'\n{local_value_name}: {local_var_value}'
        repr_str += '\nAnd objects:'
        for object_name, local_object in self.objects.items():
            repr_str += f'\n{object_name}: {local_object}'
        return repr_str




