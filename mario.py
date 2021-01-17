import pygame
import os
import sys


pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mario(pygame.sprite.Sprite):
    image = load_image("mario.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Mario.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.v = 1

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_RIGHT:
            self.rect = self.rect.move(self.v, 0)
        if args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_LEFT:
            self.rect = self.rect.move(-self.v, 0)
        if args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_UP:
            self.rect = self.rect.move(0, -self.v)


all_sprites = pygame.sprite.Group()
mario = Mario(all_sprites)
run = True
fps = 60
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update(event)
    clock.tick(fps)
    pygame.display.flip()
terminate()
