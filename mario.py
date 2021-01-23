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
    def __init__(self, default_img, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = default_img
        self.rect = self.rect.move(x, y)
        self.v = 1
        self.x = x
        self.start_ticks = 0
        self.flag = "default"
        self.st = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if args:
            self.st = args[0]
        if (args and self.st.type == pygame.KEYDOWN and self.st.key == pygame.K_RIGHT) or self.image == rturn:
            if self.flag == "left" and self.image != rturn and self.image != marimgr:
                self.image = rturn
                self.start_ticks = pygame.time.get_ticks()
                self.cur_frame = 0
            if self.start_ticks and (pygame.time.get_ticks() - self.start_ticks) / 1000 < 0.25:
                return
            self.start_ticks = 0
            self.cur_frame += clock.tick() / 10
            self.rect = self.rect.move((self.v, 0))
            self.image = self.frames[int(self.cur_frame) % 3 + 3]
            self.flag = "right"
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_LEFT or self.image == lturn:
            if self.flag == "right" and self.image != lturn and self.image != marimg:
                self.image = lturn
                self.start_ticks = pygame.time.get_ticks()
                self.cur_frame = 0
            if self.start_ticks and (pygame.time.get_ticks() - self.start_ticks) / 1000 < 0.25:
                return
            self.start_ticks = 0
            self.cur_frame += clock.tick() / 10
            self.rect = self.rect.move((-self.v, 0))
            self.image = self.frames[int(self.cur_frame) % 3]
            self.flag = "left"
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_UP:
            self.image = pygame.transform.scale(load_image("mario_jump.png"), (32, 32))
            self.rect.move((0, self.v * 5))

        if args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_RIGHT and any(
                map(lambda x: x == self.image, self.frames[3:])):
            self.image = marimg
        elif args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_RIGHT and self.flag == "left":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        if args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_LEFT and any(
                map(lambda x: x == self.image, self.frames[:3])):
            self.image = marimgr
        elif args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_LEFT and self.flag == "right":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))


all_sprites = pygame.sprite.Group()
rturn = pygame.transform.scale(load_image("turn_to_rigth.png"), (26, 32))
lturn = pygame.transform.scale(load_image("turn_to_left.png"), (26, 32))
marimg = pygame.transform.scale(load_image("default_mario.png"), (24, 32))
marimgr = pygame.transform.scale(load_image("mario_default_reversed.png"), (24, 32))
jump = pygame.transform.scale(load_image("mario_jump.png"), (32, 32))
mario = Mario(marimg, pygame.transform.scale(load_image("mario_run.png"), (204, 32)), 6, 1, 100, 100)
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
