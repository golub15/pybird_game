import game.prob
from game.utils import *

import pygame


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
    def __init__(self, screen, *group):
        super().__init__(*group)

        self.image = load_image("data/red-bird2.png")
        # self.sprite.image = pygame.transform.scale(self.sprite.image, (40, 40))
        self.is_fly = False

        self.rect = self.image.get_rect()
        self.rect.x = 210
        self.rect.y = 435
        self.nach_coord = (self.rect.x, self.rect.y)
        self.mid_x = self.rect.x + 30
        self.mid_y = self.rect.y + 30
        self.mouse_if_clicked = False
        self.radius = 50
        self.v_x = 0
        self.v_y = 0
        self.a_y = 0
        self.now_speed = 0
        self.mouse_if_clicked = False

    def move(self, x_coord, y_coord):
        self.rect.x += x_coord
        self.rect.y += y_coord

    def update(self, *args):

        # Event1 = pygame.event.Event(pygame.USEREVENT, attr1=(self.rect.x, self.rect.y))
        # pygame.event.post(Event1)

        if self.rect.x > 1200:
            self.rect.x = 210
            self.rect.y = 435
            self.v_x = 0
            self.v_y = 0

        self.move(self.v_x, self.v_y)
        self.v_y += self.a_y

        if args:
            event = args[0]
            self.getting_event(event)

    # def draw(self, screen):

    # self.bird.draw(screen)
    # if self.mouse_if_clicked and self.now_speed:
    # self.write_the_way(self.now_speed / 3, 3 * math.pi / 2
    #  - get_ungle(self.sprite.rect.x, self.sprite.rect.y, *self.nach_coord), screen)

    def ballistic(self, v, ungle):
        ungle = math.pi / 2 - ungle + math.pi
        self.v_x = v * math.cos(ungle)
        self.v_y = -v * math.sin(ungle)
        self.a_y = G

    def getting_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_if_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_if_clicked = False

            self.ballistic(self.now_speed / 3, get_ungle(self.rect.x, self.rect.y, *self.nach_coord))
            if self.now_speed < 5:
                self.rect.x = self.nach_coord[0]
                self.rect.y = self.nach_coord[1]
        if event.type == pygame.MOUSEMOTION and self.mouse_if_clicked:

            mouse_x, mouse_y = event.pos
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

    def write_the_way(self, v, ungle, screen):
        color1 = pygame.Color((0, 0, 0))
        for i in range(0, 30, 5):
            t = i
            pygame.draw.circle(screen, color1, (self.nach_coord[0] + 60 + v * math.cos(ungle) * t,
                                                self.nach_coord[0] + 60 - v * math.sin(ungle) * t + G * t ** 2 / 2), 5)


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
