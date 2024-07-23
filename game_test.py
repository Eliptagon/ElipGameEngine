import random
import sys
import time

import numpy as np
from numba import njit

from Engine import main
from Engine.utils import global_data as data
from Engine.objects.base_object import engine_object
from Engine.utils.object_handling.base_objects import createObject
from Engine.objects.rendering.texture import texture
import pygame
pygame.mixer.init()






main.mainloop()