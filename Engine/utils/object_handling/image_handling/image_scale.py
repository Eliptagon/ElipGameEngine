from numba import njit, prange
import numpy as np


#method that can scale any RGBA image to any resolution using closest scaling
@njit(parallel=True, cache=True)
def imageScalerClosest(image_arr, new_x, new_y):
    original_x = image_arr.shape[0]
    original_y = image_arr.shape[1]

    new_image = np.zeros((new_x, new_y, 4), dtype=np.uint8)  # making new image arr

    for x_position in prange(new_x):
        for y_position in range(new_y):
            for layer_index in range(4):  # looping each layer
                current_position_x = int(
                    np.floor((x_position / new_x) * original_x))  # getting index of old image for the new one
                current_position_y = int(
                    np.floor((y_position / new_y) * original_y))  # getting index of old image for the new one
                pixel_val = image_arr[current_position_x, current_position_y]
                new_image[x_position, y_position] = pixel_val
    return new_image