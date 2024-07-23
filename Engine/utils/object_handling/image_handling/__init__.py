import time

import Engine.utils.object_handling.image_handling.greyscale_to_rgb as greyscale_to_rgb
import Engine.utils.object_handling.image_handling.image_scale as image_scale
import Engine.utils.object_handling.image_handling.superimpose as superimpose


import numpy as np
#simple function to precompile functions
print('Loading and compiling texture methods')
compiler_image = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=np.uint8)
compositor_image = np.array([[100,110,120],[130,140,150],[160,170,180]], dtype=np.uint8)
print('Compiling greyscale to RGB:')
compiler_image_RGBA = greyscale_to_rgb.greyscaleToRGBA(compiler_image)
compositor_image_RGBA = greyscale_to_rgb.greyscaleToRGBA(compositor_image)
print('Compiling image scaler:')
scaled_image = image_scale.imageScalerClosest(compiler_image_RGBA, 10, 10)
print('Compiling image superimposer:')
imposed_image = superimpose.superimposeImageOverlay(scaled_image, compositor_image_RGBA, 1, 1)


