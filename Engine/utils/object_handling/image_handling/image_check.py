import numpy as np
import Engine.utils.error_types as error_types
import Engine.utils.object_handling.image_handling.greyscale_to_rgb as greyscale_to_rgb
def imageCheck(image_arr : np.ndarray):
    image_shape = image_arr.shape
    if len(image_shape) != 2 and len(image_shape) != 3:
        raise error_types.ImageSizeError(f'Shape of image: {image_shape} does not match any of the correct formats:\n'
                                         f'(x, y)'
                                         f'(x, y, colour_channels)')
    if len(image_shape) == 3:
        if image_shape[2] != 4 and image_shape[2] != 1:
            raise error_types.ImageShapeError(f'Invalid number of colour channels: {image_shape[2]},'
                                              f' valid colour channels are: 1(Greyscale) and 4(RGBA)')
    if len(image_shape) == 2 or image_shape[2] == 1: #if the image is greyscale, return RGBA version of it
        return greyscale_to_rgb.greyscaleToRGBA(image_arr)
    else: #else just return teh already RGBA image
        return image_arr