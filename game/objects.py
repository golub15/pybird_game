import game. prob
from game.utils import *

import pygame
import pymunk
import pymunk.pygame_util
import math
from pymunk import Vec2d

from random import randint


class Catapult(pygame.sprite.Sprite):

    def __init__(self, screen, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)

        img = load_image("data/sling.png")
        self.image = img
        self.id = 20000

        # self.image = pygame.transform.scale(, (40, 40))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 435

        self.state = 0

        self.bx, self.by = 0, 0

    def draw(self, *args):
        # pygame.draw.line(screen, '#ff0000', ((0, 0), (100, 100)))
        print('pass')

    def update(self, *args):
        if args and type(args[0]) == type(pygame.event.Event(0)):
            event = args[0]

            if event.type == pygame.MOUSEMOTION:
                pass

            if hasattr(event, "birdid"):
                bid = event.birdid

                if event.type == bid - 1:  # собыите о рождении птички
                    # отпрровляем  кординаты рогатки

                    e = pygame.event.Event(self.id, catapult=1, args=(self.rect.x, self.rect.y))
                    pygame.event.post(e)

                if event.type == bid + 1 or event.type == bid + 2:
                    self.bx, self.by = event.args
                    self.state = 1
                elif event.type == bid + 3:
                    self.state = 0

        if self.state == 1:
            pygame.draw.line(self.screen, '#000000', (self.rect.x + 5, self.rect.y + 10), (self.bx + 20, self.by + 30),
                             5)
            pygame.draw.line(self.screen, '#000000', (self.rect.x + 55, self.rect.y + 10), (self.bx + 40, self.by + 30),
                             5)
        elif self.state == 0:
            pygame.draw.line(self.screen, '#000000', (self.rect.x + 5, self.rect.y + 20),
                             (self.rect.x + 70, self.rect.y + 20),
                             5)


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen, space, st, id, count, x, y, *group):
        super().__init__(*group)

        self.screen = screen
        self.spites = group[0]
        self.trails = []
        self.catapult_cord = (0, 0)

        self.trail_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.trail_color = (255, 255, 255)

        self.bird_id = id
        self.bird_count = count

        self.img1 = load_image("data/red-bird2.png")
        self.img2 = load_image("data/red-bird21.png")

        self.image = self.img1
        self.rect = self.image.get_rect()
        self.mouse_on_click = False
        self.nach_coord = x, y
        self.life = 20
        self.rect.x = x
        self.rect.y = y
        self.radius = 100
        self.little_radius = 40

        self.svx = randint(20, 30)
        self.sdt = 0

        self.body = None
        self.shape = None

        self.space = space
        self.state = st

        self.send_event(-1, ())  # собыите о рождении птички

        pygame.time.set_timer(self.bird_id + 9, 3000)

        h = self.space.add_collision_handler(12, self.bird_id)  # обработка столкновения с консрукиий
        h.begin = self.bird_on_collision

    def bird_on_collision(self, space, arbiter, arg):

        if self.state != 4:
            self.state = 4
            self.send_event(self.state, (self.rect.x, self.rect.y))
            pygame.time.set_timer(self.bird_id + 10, 0)

            #x = Bird(self.screen, self.space, 1, self.bird_id + 20, self.catapult_cord[0], self.catapult_cord[1],
             #        self.spites)
            e = pygame.event.Event(self.bird_id + 12, bird_next=self.bird_count + 1)
            pygame.event.post(e)

        return True

    def send_event(self, n, attr):

        e = pygame.event.Event(self.bird_id + n, birdid=self.bird_id, args=attr)
        pygame.event.post(e)

    def ballistik(self, distance, angle):
        if self.state == 2:
            self.state = 3
            self.send_event(self.state, ())

            pygame.time.set_timer(self.bird_id + 10, 50)

            mass = 10
            radius = 10
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.friction = 10
            body.position = self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2
            power = distance * 1.2

            impulse = power * Vec2d(1, 0)
            angle = -angle
            body.apply_impulse_at_local_point(impulse.rotated(angle))

            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.3
            shape.friction = 1
            shape.collision_type = self.bird_id

            self.body = body
            self.shape = shape

            self.space.add(self.body, self.shape)

    def update(self, *args):

        if args and type(args[0]) == type(pygame.time.Clock()):
            # pygame.time.Clock.
            self.sdt += 1.5 / 60

            if self.state == 0:

                self.rect.y -= (self.svx * self.sdt - ((100 * self.sdt ** 2) / 2))
                if self.rect.y > 580:
                    self.sdt = 0

            # print(self.sdt)




        if args and type(args[0]) == type(pygame.event.Event(0)):
            event = args[0]

            if hasattr(event, "catapult"):  # событие от катапульты
                self.catapult_cord = event.args

                if self.state == 1:
                    self.rect.x = self.catapult_cord[0]
                    self.rect.y = self.catapult_cord[1]
                    self.nach_coord = self.catapult_cord
                    self.send_event(self.state, (self.rect.x, self.rect.y))

            def dd(x1, x2, y1, y2):
                return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

            if hasattr(event, "bird_next"):  # событие от катапульты
                if event.bird_next == self.bird_count:
                    if self.state == 0:
                        self.state = 1
                        self.rect.x = self.catapult_cord[0]
                        self.rect.y = self.catapult_cord[1]
                        self.nach_coord = self.catapult_cord
                        self.send_event(self.state, (self.rect.x, self.rect.y))


            if event.type == self.bird_id + 10:
                if dd(self.rect.x, self.catapult_cord[0], self.rect.y, self.catapult_cord[1]) > 50:
                    self.trails.append(
                        (self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2))

            if event.type == self.bird_id + 9 or event.type == self.bird_id + 8:
                pygame.time.set_timer(self.bird_id + 8, 0)

                if self.image == self.img1:
                    self.image = self.img2
                    pygame.time.set_timer(self.bird_id + 8, 500)
                else:
                    self.image = self.img1

            if 1 <= self.state <= 2:
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (event.pos[0] - self.nach_coord[0] - self.image.get_width() / 2) ** 2 + \
                        (event.pos[1] - self.nach_coord[1] - self.image.get_height() / 2) ** 2 \
                        <= self.image.get_width() ** 2 / 4:
                    self.mouse_on_click = True

                    self.state = 2
                    self.send_event(self.state, (self.rect.x, self.rect.y))




                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_on_click = False
                    d = (self.rect.x - self.nach_coord[0]) ** 2 + (
                            self.rect.y - self.nach_coord[1]) ** 2

                    if d <= self.little_radius ** 2:

                        self.rect.x = self.nach_coord[0]
                        self.rect.y = self.nach_coord[1]

                        self.state = 1
                        self.send_event(self.state, (self.rect.x, self.rect.y))
                    else:
                        self.ballistik(d, math.pi * 3 / 2 - get_ungle(self.rect.x, self.rect.y, *self.nach_coord))

                if event.type == pygame.MOUSEMOTION and self.mouse_on_click:

                    mouse_x, mouse_y = event.pos[0] - self.image.get_width() / 2, event.pos[
                        1] - self.image.get_height() / 2
                    if event.pos != self.nach_coord:
                        if (mouse_x - self.nach_coord[0]) ** 2 + (
                                mouse_y - self.nach_coord[1]) ** 2 <= self.radius ** 2:
                            self.rect.x = mouse_x
                            self.rect.y = mouse_y
                        else:
                            ungle = get_ungle(mouse_x, mouse_y, *self.nach_coord) % (math.pi * 2)
                            self.rect.x = self.nach_coord[0] + math.sin(ungle) * self.radius
                            self.rect.y = self.nach_coord[1] - math.cos(ungle) * self.radius
                        self.now_speed = ((self.rect.x - self.nach_coord[0]) ** 2
                                          + (self.rect.y - self.nach_coord[1]) ** 2) ** 0.5
                    self.send_event(self.state, (self.rect.x, self.rect.y))

        def to_pygame(p):
            return int(p.x), int(p.y)

        for x, y in self.trails:
            pygame.draw.circle(self.screen, self.trail_color, (x, y), 5)

        for s in self.space.shapes:
            if isinstance(s, pymunk.Circle) and s.body != None and s.collision_type == self.bird_id:
                p = to_pygame(s.body.position)
                x, y = p

                x -= 30
                y -= 30

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
