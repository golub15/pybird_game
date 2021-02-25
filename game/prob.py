import pygame


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
bg = pygame.image.load("data/back_ground.png")
bg = pygame.transform.scale(bg, (width, height))


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


class Mouse:
    def __init__(self):
        self.mouse = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("data/arrow.png")
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = 0
        self.sprite.rect.y = 0
        pygame.mouse.set_visible(False)
        self.mouse_is_on = True

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


mouse = Mouse()
running = True
while running:
    #screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if mouse.mouse_is_on and event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            mouse.mouse_move(event)
        elif event.type == pygame.MOUSEMOTION:
            mouse.mouse.remove(mouse.sprite)
    mouse.mouse.draw(screen)

    pygame.display.flip()