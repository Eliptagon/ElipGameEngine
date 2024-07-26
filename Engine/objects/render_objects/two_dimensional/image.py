
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
        self.y_size = y
        self.x_size = x

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
        self.__setLayer__('r', np.zeros(self.shape, dtype=np.uint8))
        self.__setLayer__('g', np.zeros(self.shape, dtype=np.uint8))
        self.__setLayer__('b', np.zeros(self.shape, dtype=np.uint8))
        self.__setLayer__('a', np.zeros(self.shape, dtype=np.uint8)*255)


    def __setLayer__(self, layer_name:str, layer_data:np.ndarray) -> None:
        if layer_data.shape != self.shape:
            raise error_types.ImageSizeError(f'shape of new layer {layer_data.shape} data does not match layer data of original image. {self.shape}\nNew data: {layer_data}')

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

    #function that sets the image data from a numpy array.
    def __fromArray__(self, arr:np.ndarray):
        channels = ['r', 'g', 'b', 'a']
        for channel_index, channel_letter in zip(range(4), channels):
            self.__setLayer__(channel_letter, arr[:, :, channel_index])

    def __fromFile__(self, filepath):
        #load into a PIL image
        opened_img = Image.open(filepath)
        #convert to RGBA
        image_rgba = opened_img.convert('RGBA')
        #rotating it
        image_rotated = image_rgba.rotate(90)
        #flipping image
        flipped_image = image_rotated.transpose(Image.FLIP_TOP_BOTTOM)
        #conver to an array
        image_arr = np.array(flipped_image)
        self.__fromArray__(image_arr)





    #adds an image to compositing layers
    def __addCompositeLayer__(self, loc_x, loc_y, composite_image):
        if isinstance(composite_image, imageRGBA):
            self.composite_images.append(composite_image)
            self.composite_image_locations.append((loc_x, self.__fix_y__(loc_y)))
        else:
            raise TypeError(f'Type of image while adding composite layer is n')

    #can be used to reduce overdraw, as it will check each pixel to see if it has already been drawn on by a pixel with
    # 255 in the alpha channel or a pixel that does not have an alpha channel

    def __executeCompositing__(self, mode='YX'):
        base_channels = self.channels
        mask=None #mask is automatically created
        #looping all objects
        for image_object, image_location in zip(self.composite_images, self.composite_image_locations):
            if mode == 'XY':
                image_loc_x = int(image_location[1])
                image_loc_y = int(image_location[0])
            else:
                image_loc_x = int(image_location[0])
                image_loc_y = int(image_location[1])

            new_image_channels = image_object.channels

            has_mask_been_set = isinstance(mask, np.ndarray)
            try:
                result = self.__compiledCompositeArray__(base_channels, new_image_channels, image_loc_x, image_loc_y, mask, has_mask_been_set)
            except:
                result = (self.channels, None)
            base_channels = result[0]
        mask = result[1]

        channel_ids = ['r', 'g', 'b', 'a']
        #applying the channels to self
        for channel, channel_id in zip(base_channels, channel_ids):
            self.__setLayer__(channel_id, channel)
        self.channels = base_channels
        #resetting composite image locations
        self.composite_image_locations = []
        self.composite_images = []
        return mask


    #called this because it was originally compiled, but then i improved it and it could no longer be compiled with Numba
    @staticmethod
    def __compiledCompositeArray__(host_channels, new_channels, y_offset, x_offset, mask = None, has_mask = False):
        #host channels is a python list of all 4 channels, same with new_channels
        output_channels = [] #will be a list of nthe new channels

        #this is the size of the channel
        channel_shape = host_channels[0].shape
        composite_shape = new_channels[0].shape

        # if no mask is passed in, then create one
        if not has_mask: mask = np.ones(channel_shape, dtype=np.bool_)

        # getting the part of the base channels that overlap the image
        x_end = np.minimum(x_offset + composite_shape[0], channel_shape[0])
        y_end = np.minimum(y_offset + composite_shape[1], channel_shape[1])

        # defining teh actual image size that is onscreen
        actual_x_size = x_end - x_offset
        actual_y_size = y_end - y_offset

        #getting region of mask before changing it, to allow all channels to be calculated with teh same mask
        mask_region = mask[x_offset:x_end, y_offset:y_end]

        for channel_index in range(len(host_channels)):
            #getting per channel data
            channel = host_channels[channel_index]
            composite_channel = new_channels[channel_index]

            #getting teh overlapping region from the new channel (not including bits that fall off)
            composite_overlap = composite_channel[:actual_x_size, :actual_y_size]

            #getting the part of where the composite image overlaps the original image
            channel_region = channel[x_offset:x_end, y_offset:y_end]

            channel_region[mask_region] = composite_overlap[mask_region]

            #copying data
            channel[x_offset:x_end, y_offset:y_end] = channel_region

            output_channels.append(channel)

        #updating the mask
        mask[x_offset:x_end, y_offset:y_end] = False
        return output_channels, mask







    #converting teh image to an array with alpha channel included
    def __asArrayRGBA__(self):
        stacked_arr = np.stack((self.red_channel, self.green_channel, self.blue_channel, self.alpha_channel), axis=-1)
        return stacked_arr

    def __asArrayRGB__(self):
        stacked_arr = np.stack((self.red_channel, self.green_channel, self.blue_channel), axis=-1)
        return stacked_arr

    def __fix_y__(self, y_val):
        return self.y_size - y_val

    def __fix_x__(self, x_val):
        return self.x_size - x_val

    # converting teh image to an array without the alpha channel


#simple function that validates the image channel's shape
    def __check__(self):
        expected_shape = self.shape
        for channel in self.channels:
            if channel.shape != expected_shape:
                raise error_types.ImageSizeError(f'Channel shape: {channel.shape}, expected shape: {expected_shape}')






