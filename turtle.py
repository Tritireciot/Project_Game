import pygame

import os
import sys

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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


def terminate():
    pygame.quit()
    sys.exit()



class Turtle(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.v = 1
        self.isdead = 0
        self.start_ticks = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_UP and self.isdead == 0:
            self.image = pygame.transform.scale(load_image("death_turtle.png"), (56, 48))
            self.start_ticks = pygame.time.get_ticks()
            self.isdead = 1
        if self.isdead == 1 and (pygame.time.get_ticks() - self.start_ticks) // 1000 == 3:
            self.image = pygame.transform.scale(load_image("reborn_turtle.png"), (56, 48))
            self.isdead = 2
        if self.isdead == 2 and (pygame.time.get_ticks() - self.start_ticks) // 1000 == 4:
            self.isdead = 0
        elif not self.isdead:
            if self.rect.x == 0:
                self.v = 1
            elif self.rect.x == width:
                self.v = -1
            if self.v == 1:
                self.cur_frame += clock.tick() / 10
                self.rect = self.rect.move((self.v, 0))
                self.image = self.frames[int(self.cur_frame) % 2 + 2]
            else:
                self.cur_frame += clock.tick() / 10
                self.rect = self.rect.move((self.v, 0))
                self.image = self.frames[int(self.cur_frame) % 2]



all_sprites = pygame.sprite.Group()
turtle = Turtle(pygame.transform.scale(load_image("turtle_walk.png"), (224, 48)), 4, 1, 100, 100)
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 255))
    all_sprites.draw(screen)
    all_sprites.update(event)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()

