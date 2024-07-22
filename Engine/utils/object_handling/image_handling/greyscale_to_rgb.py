from numba import njit, prange
import numpy as np

#method that converts a greyscale, 2d numpy asrray into an RGBA image
@njit(parallel=True, cache=True)
def greyscaleToRGBA(greyscale_img: np.ndarray):
    image_size_x = greyscale_img.shape[0]
    image_size_y = greyscale_img.shape[1]
    rgb_image = np.zeros((image_size_x, image_size_y, 4))
    for x_position in prange(image_size_x):
        for y_position in range(image_size_y):
            greyscale_pixel_value = greyscale_img[x_position, y_position]
            # setting each colour channel to the value of teh greyscale image
            rgb_image[x_position, y_position] = [greyscale_pixel_value,
                                                 greyscale_pixel_value,
                                                 greyscale_pixel_value, 255]
    return rgb_image