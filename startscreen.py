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


def start_screen():
    screen.fill((92, 148, 252))
    mushcurs = MushroomCursor(second_sprite)
    coin = Coin(pygame.transform.scale(load_image("coin.png"), (68, 16)), 4, 1, 178, 46)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                all_sprites.update()
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_UP and event.key != pygame.K_DOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill((92, 148, 252))
        bottom = pygame.transform.scale(load_image('start_bottom.png'), (WIDTH, 122))
        screen.blit(bottom, (0, 346))
        play2 = pygame.transform.scale(load_image('2-player.png'), (236, 16))
        screen.blit(play2, (166, 322))
        play1 = pygame.transform.scale(load_image('1-player.png'), (236, 16))
        screen.blit(play1, (166, 287))
        logo = pygame.transform.scale(load_image('Start_logo.png'), (352, 192))
        screen.blit(logo, (82, 64))
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
        all_sprites.draw(screen)
        second_sprite.draw(screen)
        second_sprite.update(event)
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


class MushroomCursor(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('mushroom_cursor.png'), (20, 16))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MushroomCursor.image
        self.rect = self.image.get_rect()
        self.rect.x = 126
        self.rect.y = 287

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_DOWN and self.rect.y == 287:
            self.rect = self.rect.move(0, 322 - 287)
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_UP and self.rect.y == 322:
            self.rect = self.rect.move(0, 287 - 322)


all_sprites = pygame.sprite.Group()
second_sprite = pygame.sprite.Group()
start_screen()
