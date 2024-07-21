from Engine.objects.base_object import engine_object #base object
import asyncio
from pynput import keyboard

class keyLogger(engine_object): #Dont worry: nothing malicious, just something that records key inputs for use in the game engine
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.listener = keyboard.Listener(on_press=self._addKeyDown, on_release=self._addKeyUp)
        self.listener.start()
        self.stacked_key_inputs = []

    def clear(self):
        self.stacked_key_inputs = []
    def _addKeyDown(self, key):
        self.stacked_key_inputs.append(f'{str(key).replace("'", '')}_down')
        print(self.stacked_key_inputs)
    def _addKeyUp(self, key):
        self.stacked_key_inputs.append(f'{str(key).replace("'", '')}_up')

    def __repr__(self):
        return f'A keylogger object'
