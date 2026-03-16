import json
import pygame

class SpriteSheet:
    """
    A class to represent spritesheet images for enemies and the player

    Parameters
    ----------
        image: Surface
            an instance of the surface class,
            an image that contains all the models for the character

    Methods
    -------
        __init__(image):
            constructs all the necessary attributes for the game class

        get_image(frame_count, size, scale, colour):
            outputs a formatted image from the spritesheet based on the inputs

    """
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_count, size, scale, colour):
        img = pygame.Surface((size[0], size[1])).convert_alpha()
        img.blit(self.sheet, (0, 0), (frame_count * size[0], 0, size[0], size[1]))
        img = pygame.transform.scale(img, (size[0] * scale, size[1] * scale))
        img.set_colorkey(colour)

        return img

def rect_collision(rect1, rect2):
    """
        Checks whether two rectangles are colliding.

        Parameters
        ----------
        rect1 : Rect
            the first rectangle
        rect2 : Rect
            the second rectangle

        Returns
        -------
        bool
            True if the rectangles are colliding and False if they are not
    """
    if rect1.right >= rect2.left and rect1.left <= rect2.right and rect1.bottom >= rect2.top and rect1.top <= rect2.bottom:
        colliding = True
    else:
        colliding = False

    return colliding


def point_collision(point_pos, rect):
    """
        Checks whether a point is inside/colliding with the rectangle.

        Parameters
        ----------
        point_pos : tuple(int, int)
            coordinates of the point
        rect : Rect
            the rectangle to check

        Returns
        -------
        bool
            True if the point is inside the rectangle and False if it is not
    """
    if point_pos[0] >= rect.left and point_pos[0] <= rect.right and point_pos[1] >= rect.top and point_pos[
        1] <= rect.bottom:
        colliding = True
    else:
        colliding = False
    return colliding


def read_json(file):
    """
        reads data from a JSON file.

        Parameters
        ----------
        file : str
            the name of the file to read from

        Returns
        -------
        dict
            the serialised data read from the JSON file
    """
    file = file + ".json"
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def write_json(data, file):
    """
        saves data to a JSON file.

        Parameters
        ----------
        data : dict
            the data to write to the file
        file : str
            the name of the file to write to

        Returns
        -------
        str
            the name of the file written to, with the .json extension
    """
    file = file + '.json'
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(", ", " : "), sort_keys=True)
    return file

