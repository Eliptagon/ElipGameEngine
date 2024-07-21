import numpy as np
from Engine.objects.base_object import engine_object
from numba import njit, prange
#texture object, acts as both PIL image and an engine object
class texture(engine_object):
    def __init__(self, size_x, size_y):

        super().__init__()

        self.current_size_x = size_x
        self.current_size_y = size_y

        #image parts of the object, i want full control of the methods
        self.image_arr = np.zeros((size_x, size_y, 4), dtype=np.uint8) #the 4 is teh number of channels: R, G, B and A


    #a wrapper function to rescale the texture
    def __reScale__(self, new_x, new_y):
        scaled_image = self._compiledScaler(self.image_arr, new_x, new_y) #passing method into njitted version to ensure speed
        self.image_arr = scaled_image
        self.current_size_y = new_y
        self.current_size_x = new_x



    #TODO: FINISH
    @staticmethod
    @njit(parallel=True)
    def _compiledScaler(image_arr, new_x, new_y):
        scale_factor_x = new_x / image_arr.shape[0]  #getting scale factor for X
        scale_factor_y =  new_y / image_arr.shape[1]     #getting scale factor for Y

        new_image = np.zeros((new_x, new_y, 4)) #making new image arr

        for x_position in prange(new_x):
            for y_position in range(new_y):
                for layer_index in range(4): #looping each layer
                    current_position_x = x_position /
                    new_image[x_position, y_position, layer_index] = 0



    def __onRender__(self) -> np.ndarray:
        self.image_arr
