import pygame
import math

import game.prob




G = 5 / 12


def get_ungle(x1, y1, x2, y2):
    if x1 >= x2 and y1 >= y2:
        chetvert = 1
    elif x1 <= x2 and y1 >= y2:
        chetvert = 2
    elif x1 <= x2 and y1 <= y2:
        chetvert = 3
    else:
        chetvert = 4
    r = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return math.asin((x1 - x2) / r) if chetvert in (4, 3) else (math.pi - math.asin((x1 - x2) / r))


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()

    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    game.prob.main()
