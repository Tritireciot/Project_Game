import pygame
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 512, 448
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 500)
FPS = 60


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


def intro():
    screen.fill((0, 0, 0))
    coin = Coin(pygame.transform.scale(load_image("coin_black.png"), (68, 16)), 4, 1, 178, 46)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_UP and event.key != pygame.K_DOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill((0, 0, 0))
        titles = pygame.transform.scale(load_image('titles.png'), (414, 16))
        screen.blit(titles, (50, 26))
        zero = pygame.transform.scale(load_image('0.png'), (16, 16))
        for i in range(6):
            screen.blit(zero, (50 + i * 16, 46))
        crestic = pygame.transform.scale(load_image('X.png'), (16, 16))
        screen.blit(crestic, (198, 46))
        screen.blit(zero, (216, 46))
        screen.blit(zero, (232, 46))
        one = pygame.transform.scale(load_image('1.png'), (16, 16))
        hyphen = pygame.transform.scale(load_image('-.png'), (16, 16))
        screen.blit(one, (300, 46))
        screen.blit(hyphen, (320, 46))
        screen.blit(one, (340, 46))
        mario = pygame.transform.scale(load_image('mario_intro.png'), (48, 48))
        screen.blit(mario, (156, 224))
        crestic = pygame.transform.scale(load_image('X.png'), (32, 32))
        screen.blit(crestic, (226, 234))
        three = pygame.transform.scale(load_image('3.png'), (48, 48))
        screen.blit(three, (276, 229))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Coin(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


all_sprites = pygame.sprite.Group()
intro()
