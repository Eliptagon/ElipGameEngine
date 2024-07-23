from Engine.objects.base_object import engine_object
class mesh(engine_object):
    def __init__(self):
        super().__init__()
        #none of these are of known length, so cant be numpy array
        self.points = []
        self.edges = []
        self.faces = []
