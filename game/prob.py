from game.objects import *
from game.utils import *


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


def sling_action():
    """Set up sling behavior"""
    print('sl')
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1 * rope_lenght + sling_x, uv2 * rope_lenght + sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1 * bigger_rope + sling_x, uv2 * bigger_rope + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1 * mouse_distance + sling_x, uv2 * mouse_distance + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy)) / dx)


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

    all_sprites = pygame.sprite.Group()

    x = Catapult(screen, all_sprites)
    bird = Bird(screen, all_sprites)
    #mouse = Mouse()
   # objects = [bird, mouse]
    running = True

    load_music()

    while running:
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():

            all_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
            else:
                pass

        clock.tick(60)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
