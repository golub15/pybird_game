from game.objects import *
from game.utils import *

import pymunk
import pygame
import pymunk.pygame_util

from pymunk import Vec2d


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0] ** 2) + (v[1] ** 2)) ** 0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def load_music():
    s = 'data/angry-birds.ogg'
    pygame.mixer.music.load(s)
    pygame.mixer.music.play(-1)


def main():
    pygame.init()
    size = width, height = 1200, 650
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("data/background3.png")
    bg = pygame.transform.scale(bg, (width, height))
    clock = pygame.time.Clock()

    surf = pygame.Surface((1200, 650))

    space1 = pymunk.Space()
    space1.gravity = 0, 1000
    space1.sleep_time_threshold = 0.5

    draw_options1 = pymunk.pygame_util.DrawOptions(surf)

    l = pymunk.Segment(space1.static_body, (0, 640), (1000, 640), 5)
    l.elasticity = 0.5
    l.friction = 1

    space1.add(l)

    template_box = pymunk.Poly.create_box(pymunk.Body(), (20, 20))
    template_box.mass = 1
    template_box.friction = 1

    # ball.color = load_image("data/red-bird2.png")

    for x in range(10):
        for y in range(5):
            box = template_box.copy()

            box.body.position = 500 + x * 30, 600 - y * 20

            space1.add(box, box.body)

    all_sprites = pygame.sprite.Group()

    x = Catapult(screen, all_sprites)
    # bird = Bird(screen, all_sprites)
    # mouse = Mouse()
    # objects = [bird, mouse]
    running = True

    # load_music()

    x = Bird(screen, space1, 50, 1, 210, 435, all_sprites)
    while running:

        for event in pygame.event.get():

            all_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        clock.tick(60)

        surf.blit(bg, (0, 0))

        space1.debug_draw(draw_options1)
        screen.blit(surf, (0, 0))

        ### Update physics
        fps = 60
        dt = 1.0 / fps
        space1.step(dt)

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
