from numba import njit, prange
import numpy as np



#TODO: FiX
@njit(cache=True, parallel = True)
def superimposeImageOverlay(image_1: np.ndarray, image_2: np.ndarray, loc_x, loc_y): #Both inputs need to be of the same type:
    new_image_shape = image_2.shape
    original_image_shape = image_1.shape
    if len(image_1.shape) != len(image_2.shape):
        raise Exception('Image type mismatch while superimposing images')
    for x_coordinate in prange(new_image_shape[0]):
        for y_coordinate in range(new_image_shape[1]):
            new_pixel = image_2[x_coordinate, y_coordinate] #getting pixel from new image array
            offset_coordinate_x = x_coordinate + loc_x
            offset_coordinate_y = y_coordinate + original_image_shape[1] - (loc_y + y_coordinate)
            if offset_coordinate_x < original_image_shape[0] and offset_coordinate_x >= 0: #if teh coordinate of teh new pixel is on the old image
                if offset_coordinate_y < original_image_shape[1] and offset_coordinate_y >= 0: #if teh coordinate of teh new pixel is on the old image
                    image_1[offset_coordinate_x, offset_coordinate_y] = new_pixel
    return image_1





