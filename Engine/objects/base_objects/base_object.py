import numpy as np
class engine_object:
    def __init__(self):
        self.location = np.zeros(3) #3 zeros
        self.rotation = np.zeros(3) #3 more zeros
        self.do_updates = True
        self.do_render = True
        self.events_to_listen_for = [] #contains events that this object will respond to

    def __onCreate__ (self, name) -> None: #method that is called when the object is created by the game engine
        pass

    def __onEvent__(self, event_name, event_data) -> None: #can be used for any event as long as the object has a reference to it, e.g: 'KeyDown' as event name and 'D' as teh data_handling, representing the D key being pressed
        pass

    def __onUpdate__(self, local_scene) -> None:    #method that is called every update, scene is passed in so it can easily manipulate objects in that scene
        pass #a base object should do absolutely nothing

    def __onRender__(self) -> None:   #method that is used to return pixel values of the object
        pass

    def __onDelete__(self) -> None: #method that is called when the game engine deletes the object, then the game engine calls del(object)
        pass

    def __onError__(self) -> bool:
        return False       #retrurns a Boolean on whether the program should continue

    def move(self, amount : np.ndarray):
        self.location += amount



    def __repr__(self) -> str:
        return f'Generic object located at {self.location}'