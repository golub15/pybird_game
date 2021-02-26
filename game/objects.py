import game.prob
from game.utils import *

import pygame
import pymunk
import pymunk.pygame_util
import math
from pymunk import Vec2d


class Catapult(pygame.sprite.Sprite):

    def __init__(self, screen, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)

        img = load_image("data/sling.png")
        self.image = img
        #

        # self.image = pygame.transform.scale(, (40, 40))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 435

        self.bx, self.by = 0, 0

    def draw(self, *args):
        # pygame.draw.line(screen, '#ff0000', ((0, 0), (100, 100)))
        print('pass')

    def update(self, *args):

        if args:
            event = args[0]
            if event.type == pygame.MOUSEMOTION:
                pass

            elif event.type == pygame.USEREVENT:
                self.bx, self.by = event.attr1
                print(event)

        pygame.draw.line(self.screen, '#000000', (self.rect.x + 5, self.rect.y + 10), (self.bx, self.by), 5)
        pygame.draw.line(self.screen, '#000000', (self.rect.x + 55, self.rect.y + 10), (self.bx + 20, self.by), 5)


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen, space, distance, angle, x, y, *group):
        super().__init__(*group)

        self.image = load_image("data/red-bird2.png")
        self.rect = self.image.get_rect()
        self.mouse_on_click = False
        self.nach_coord = x, y
        self.life = 20
        self.rect.x = x
        self.rect.y = y
        self.radius = 100
        self.little_radius = 40

        self.body = None
        self.shape = None

        self.space = space

    def make_projectile(self):
        pass

    def ballistik(self, distance, angle):
        mass = 10
        radius = 12
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
       # body.friction = 100000000
        body.position = self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2
        power = distance * 1.9
        impulse = power * Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))

        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 10
        shape.collision_type = 1


        self.body = body
        self.shape = shape



        self.space.add(self.body, self.shape)

    def update(self, *args):

        if args:
            event = args[0]
            """if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                d = math.sqrt((self.rect.x - mx) ** 2 + (self.rect.y - my) ** 2)
                if d < 20:
                    print('JOK')
                    self.make_projectile()"""
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    (event.pos[0] - self.nach_coord[0] - self.image.get_width() / 2) ** 2 + \
                    (event.pos[1] - self.nach_coord[1] - self.image.get_height() / 2) ** 2 \
                    <= self.image.get_width() ** 2 / 4:
                self.mouse_on_click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_on_click = False
                d = (self.rect.x - self.nach_coord[0]) ** 2 + (
                        self.rect.y - self.nach_coord[1]) ** 2

                if d <= self.little_radius ** 2:
                    self.rect.x = self.nach_coord[0]
                    self.rect.y = self.nach_coord[1]
                else:
                    self.ballistik(d, math.pi * 3 / 2 - get_ungle(self.rect.x, self.rect.y, *self.nach_coord))

            if event.type == pygame.MOUSEMOTION and self.mouse_on_click:
                mouse_x, mouse_y = event.pos[0] - self.image.get_width() / 2, event.pos[1] - self.image.get_height() / 2
                if event.pos != self.nach_coord:
                    if (mouse_x - self.nach_coord[0]) ** 2 + (mouse_y - self.nach_coord[1]) ** 2 <= self.radius ** 2:
                        self.rect.x = mouse_x
                        self.rect.y = mouse_y
                    else:
                        ungle = get_ungle(mouse_x, mouse_y, *self.nach_coord) % (math.pi * 2)
                        self.rect.x = self.nach_coord[0] + math.sin(ungle) * self.radius
                        self.rect.y = self.nach_coord[1] - math.cos(ungle) * self.radius
                    self.now_speed = ((self.rect.x - self.nach_coord[0]) ** 2
                                      + (self.rect.y - self.nach_coord[1]) ** 2) ** 0.5
            # self.make_projectile()

        def to_pygame(p):

            return int(p.x), int(p.y)

        for s in self.space.shapes:
            if isinstance(s, pymunk.Circle) and s.body != None:
                p = to_pygame(s.body.position)
                x, y = p

                x -= 30
                y -= 30
                print(x, y)

                self.rect.x = x
                self.rect.y = y


class Mouse:
    def __init__(self):
        self.mouse = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("data/arrow.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (40, 40))
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = 0
        self.sprite.rect.y = 0
        self.mouse.add(self.sprite)
        pygame.mouse.set_visible(False)
        self.mouse_is_on = True

    def draw(self, screen):
        self.mouse.draw(screen)

    def mouse_off(self):
        pygame.mouse.set_visible(True)
        self.mouse_is_on = False

    def mouse_on(self):
        pygame.mouse.set_visible(False)
        self.mouse_is_on = True

    def mouse_move(self, event):
        pos = event.pos
        self.sprite.rect.x = pos[0]
        self.sprite.rect.y = pos[1]
        self.mouse.add(self.sprite)

    def draw(self, screen):
        self.mouse.draw(screen)

    def getting_event(self, event):
        if self.mouse_is_on and event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            self.mouse_move(event)
        elif event.type == pygame.MOUSEMOTION:
            self.mouse.remove(self.sprite)


if __name__ == '__main__':
    game.prob.main()
