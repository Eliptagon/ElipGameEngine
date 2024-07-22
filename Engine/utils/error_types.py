#special error types


class LengthError(Exception):
    pass

class ImageSizeError(Exception):
    pass

class ImageShapeError(Exception):
    pass

class ArrayShapeError(Exception):
    pass

class ImageMismatchError(Exception):
    pass
