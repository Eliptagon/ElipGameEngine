'''This is a script that allows transferring global variables between scripts,
Useful for custom scripts written in other langs'''

#dict of all objects
objects = dict()
#dict of scenes, and the objects for that scene will be held in here as well
scenes = dict()
#global variables that can be accesses by any script
flags = dict()
#objects that are always updated
global_objects = dict()