import time

from Engine import main
from Engine.utils import global_data as data
from Engine.objects.base_object import engine_object
from Engine.utils.object_handling.base_objects import createObject


main_scene = data.scenes['main']
global_scene = data.scenes['global']


class testObj(engine_object):
    def __init__(self):
        super().__init__()
    def __onUpdate__(self, local_scene) -> None:
        pass


    def __onEvent__(self, event_name, event_data) -> None:
        if event_name == 'onKeyEvent':
            print(event_data)


createObject(testObj, main_scene, 'test')



main.mainloop()