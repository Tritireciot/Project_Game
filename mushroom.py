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


#
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.v = 1
        self.x = x

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_UP:
            self.image = pygame.transform.scale(load_image("mushroom_death.png"), (32, 32))
        else:
            if self.rect.x == 0:
                self.v = 1
            elif self.rect.x == width:
                self.v = -1
            self.cur_frame += clock.tick() / 10
            self.rect = self.rect.move((self.v, 0))
            self.image = self.frames[int(self.cur_frame) % len(self.frames)]


all_sprites = pygame.sprite.Group()
mushroom = Mushroom(pygame.transform.scale(load_image("mushroom_walk.png"), (92, 32)), 2, 1, 100, 100)
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update(event)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
