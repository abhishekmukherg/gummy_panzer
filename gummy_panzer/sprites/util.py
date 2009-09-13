import pkg_resources, pygame, os

def load_image(file_name, colorkey=False):
    """Loads an image, file_name, from image_directory, for use in pygame"""
    file = pkg_resources.resource_stream("gummy_panzer",
            os.path.join("images", file_name))
    _image = pygame.image.load(file, file_name)
    if colorkey:
        if colorkey == -1: 
        # If the color key is -1, set it to color of upper left corner
            colorkey = _image.get_at((0, 0))
        _image.set_colorkey(colorkey)
        _image = _image.convert()
    else: # If there is no colorkey, preserve the image's alpha per pixel.
        _image = _image.convert_alpha()
    return _image
