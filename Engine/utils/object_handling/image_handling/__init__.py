import Engine.utils.object_handling.image_handling.greyscale_to_rgb as greyscale_to_rgb
import Engine.utils.object_handling.image_handling.image_scale as image_scale
import Engine.utils.object_handling.image_handling.superimpose as superimpose
from PIL import Image
import numpy as np
#simple function to precompile functions
print('Loading and compiling texture methods')
compiler_image = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=np.uint8)
print('Compiling greyscale to RGB:')
compiler_image_RGBA = greyscale_to_rgb.greyscaleToRGBA(compiler_image)
print('Compiling image scaler:')
scaled_image = image_scale.imageScalerClosest(compiler_image_RGBA, 50, 50)
print('Compiling image superimposer:')
imposed_image = superimpose.superimposeImageOverlay(scaled_image, compiler_image_RGBA, 25, 25)
img = Image.fromarray(imposed_image, mode='RGBA')
img.save('test.png')
print('done compiling')


