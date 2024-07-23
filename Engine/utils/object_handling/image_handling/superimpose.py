from numba import njit, prange
import numpy as np
#structured in this way to enable compositing multiple images at once in the future
#remember Numpy arrays follow Row, Col, depth
@njit(parallel = False, cache = True)
def superimposeImageOverlay(image_1: np.ndarray, image_2: np.ndarray, loc_x, loc_y): #
    image_shape = image_1.shape
    new_image_shape = image_2.shape
    for new_image_x in prange(new_image_shape[1]):
        for new_image_y in range(new_image_shape[0]):
            pixel_location_x = new_image_x + loc_x
            pixel_location_y = image_shape[0] - (new_image_y + loc_y)
            if pixel_location_x >= 0 and pixel_location_x < image_shape[1]: #if the X coordinate is in the original image
                if pixel_location_y >= 0 and pixel_location_y < image_shape[0]:
                    image_1[pixel_location_y, pixel_location_x] = image_2[new_image_y, new_image_x]






