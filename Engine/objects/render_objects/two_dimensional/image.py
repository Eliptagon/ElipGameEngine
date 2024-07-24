from Engine.objects.base_objects.base_object import engine_object
import Engine.utils.error_handling.error_types as error_types
import numpy as np
from PIL import Image
#new image object that allows for easier management of image objects
#also allow it to be more robust

class imageRGBA(engine_object):
    def __init__(self, size):
        x = size[0]
        y = size[1]
        #specifying each channel individually, so that they can be more easily manipulated
        self.resolution = (x, y)
        self.shape = (y, x)

        self.red_channel = np.zeros(self.shape, dtype=np.uint8)
        self.green_channel = np.zeros(self.shape, dtype=np.uint8)
        self.blue_channel = np.zeros(self.shape, dtype=np.uint8)
        self.alpha_channel = np.full(self.shape, 255, dtype=np.uint8)
        self.channels = [self.red_channel, self.green_channel,
                         self.blue_channel, self.alpha_channel] #all channels in one place
        #for things that


        #used for composite images, last image in this list will be the first composited
        self.composite_images = []
        self.composite_image_locations = [] #locations of the composite

    #method that can set a pixel both by a fraction and also by pixel coordinates
    def __setPixel__(self, x: int | float, y:int | float, pixel : np.ndarray, fractional:bool = False):
        if fractional == True:
            pass

    #function that resets the image to its default state
    def __clear__(self):
        self.red_channel = np.zeros(self.shape, dtype=np.uint8)
        self.green_channel = np.zeros(self.shape, dtype=np.uint8)
        self.blue_channel = np.zeros(self.shape, dtype=np.uint8)
        self.alpha_channel = np.full(self.shape, 255, dtype=np.uint8)
        self.channels = [self.red_channel, self.green_channel,
                         self.blue_channel, self.alpha_channel]  # all channels in one place

    def __getPixel__(self, x, y):
        pixel_array = np.zeros(4, dtype=np.uint8) #setting up a pixel
        channel_depth = 0
        for channel in self.channels:
            pixel_array[channel_depth] = channel[y,x]
            channel_depth += 1
            #print(f'\nGrabbing from channel:\n {channel}\nPixel array is now: {pixel_array}\n')
        return pixel_array.astype(np.uint8)

    def __setLayer__(self, layer_name:str, layer_data:np.ndarray) -> None:
        if layer_data.shape != self.shape:
            raise error_types.ImageSizeError('shape of new layer data does not match layer data of original image.')

        type_converted_data = layer_data.astype(np.uint8)

        #actually setting the data
        match layer_name.lower():
            case 'r':
                self.red_channel = type_converted_data
                self.channels[0] = type_converted_data
            case 'g':
                self.green_channel = type_converted_data
                self.channels[1] = type_converted_data
            case 'b':
                self.blue_channel = type_converted_data
                self.channels[2] = type_converted_data
            case 'a':
                self.alpha_channel = type_converted_data
                self.channels[3] = type_converted_data






    #adds an image to compositing layers
    def __addCompositeLayer__(self, loc_x, loc_y, composite_image):
        if isinstance(composite_image, imageRGBA):
            self.composite_images.append(composite_image)
            self.composite_image_locations.append((loc_x, self.__fix_y__(loc_y)))
        else:
            raise TypeError(f'Type of image while adding composite layer is n')

    #can be used to reduce overdraw, as it will check each pixel to see if it has already been drawn on by a pixel with
    # 255 in the alpha channel or a pixel that does not have an alpha channel
    def __executeCompositing__(self):
        #boolean mask on whether that pixel should be updated
        composite_mask = np.ones(self.shape, dtype=np.bool_)
        #looping both locations of teh compositing images, and also teh image instance
        for composite_image, composite_loc in zip(self.composite_images, self.composite_image_locations):
            composite_image_shape = composite_image.shape
            for image_coordinate_y in range(composite_image_shape[0]): #remember, images go y, x
                for image_coordinate_x in range(composite_image_shape[1]):
                    composite_loc_x = image_coordinate_x+ composite_loc[0]
                    composite_loc_y = image_coordinate_y + composite_loc[1]
                    if composite_loc_y < 0 or composite_loc_y >= self.shape[0]:
                        pass #compositing went off of the screen, its fine
                    elif composite_loc_x < 0 or composite_loc_x >= self.shape[1]:
                        pass #compositing went off of the screen, its fine
                    else:
                        if composite_mask[composite_loc_y, composite_loc_x]:  #if the image at that location is not occluded:
                            pixel_at_location = composite_image.__getPixel__(image_coordinate_x, image_coordinate_y) #pixel in image that is being added
                            if pixel_at_location[3] == 255:
                                composite_mask[composite_loc_y, composite_loc_x] = False #so if the image will be occluded, that pixel will not be overwritten
                            for channel_value, respective_arr in zip(pixel_at_location, self.channels): #remember pixel at location is list of
                                respective_arr[composite_loc_y, composite_loc_x] = channel_value

        return composite_mask
    #converting teh image to an array with alpha channel included
    def __asArrayRGBA__(self):
        stacked_arr = np.stack((self.red_channel, self.green_channel, self.blue_channel, self.alpha_channel), axis=-1)
        return stacked_arr

    def __asArrayRGB__(self):
        stacked_arr = np.stack((self.red_channel, self.green_channel, self.blue_channel), axis=-1)
        return stacked_arr

    def __fix_y__(self, y_val):
        y_size = self.shape[0]
        return y_size - y_val

    # converting teh image to an array without the alpha channel


#simple function that validates the image channel's shape
    def __check__(self):
        expected_shape = self.shape
        for channel in self.channels:
            if channel.shape != expected_shape:
                raise error_types.ImageSizeError(f'Channel shape: {channel.shape}, expected shape: {expected_shape}')








