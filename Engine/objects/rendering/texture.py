import numpy as np
from Engine.objects.base_object import engine_object
from numba import njit, prange
import imageio, PIL
import Engine.utils.error_types as error_types
import Engine.utils.object_handling.image_handling.image_scale as image_scaler
import Engine.utils.object_handling.image_handling.greyscale_to_rgb as greyscale_to_rgb
import Engine.utils.object_handling.image_handling.superimpose as superimposer
from Engine.utils.object_handling.image_handling.image_check import imageCheck
class texture(engine_object):
    def __init__(self, size_x=1, size_y=1):

        super().__init__()

        self.current_size_x = size_x
        self.current_size_y = size_y

        #image parts of the object, i want full control of the methods
        self.image_arr = np.zeros((size_x, size_y, 4), dtype=np.uint8) #the 4 is teh number of channels: R, G, B and A


    #a wrapper function to rescale the texture
    def __reScale__(self, new_x, new_y, new_image=False):
        scaled_image = image_scaler.imageScalerClosest(self.image_arr, new_x, new_y) #passing method into njitted version to ensure speed
        if not new_image:
            self.image_arr = scaled_image
            self.current_size_y = new_y
            self.current_size_x = new_x
        else:
            new_texture = texture(new_x, new_y)
            new_texture.__setImage__(scaled_image)
            return new_texture

    def __setImage__(self, new_image_arr : np.ndarray):
        self.image_arr = imageCheck(new_image_arr)

    def __clear__(self):
        self.image_arr = np.zeros(self.image_arr.shape, dtype=np.uint8) #sets textuure to just black


    def __asArray__(self):
        return self.image_arr.astype(np.uint8)
    #Method that can superimpose two images
    def __superimpose__(self, new_image, loc_x, loc_y):
        checked_image = imageCheck(new_image) #ensure image is of RGBA format
        superimposer.superimposeImageOverlay(self.image_arr, checked_image, loc_x, loc_y) #this updates the image array

    def __onRender__(self) -> np.ndarray:
        return self.image_arr
