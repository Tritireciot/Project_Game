import pygame
import os
import sys

pygame.init()
size = width, height = 7000, 448
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 250)
FPS = 60
positions = open('poss.txt', encoding='utf8').readlines()
positions = list(map(lambda x: (int(x[1:x.find(",")]), int(x[x.find(" ") + 1:x.find(")")])), positions))


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


def nothing_under(x, y, width):
    pass


tile_images = {
    "outworld base": pygame.transform.scale(load_image('outworld_base.png'), (32, 32)),
    "big hillock": pygame.transform.scale(load_image('big_hillock.png'), (160, 70)),
    "hillock": pygame.transform.scale(load_image('hillock.png'), (96, 38)),
    "bush": pygame.transform.scale(load_image('bush.png'), (64, 32)),
    "double bush": pygame.transform.scale(load_image('double_bush.png'), (96, 32)),
    "triple bush": pygame.transform.scale(load_image('triple_bush.png'), (128, 32)),
    "cloud": pygame.transform.scale(load_image('cloud.png'), (64, 48)),
    "double cloud": pygame.transform.scale(load_image('double_cloud.png'), (96, 48)),
    "triple cloud": pygame.transform.scale(load_image('triple_cloud.png'), (128, 48)),
    "short pipe": pygame.transform.scale(load_image('short_pipe.png'), (64, 64)),
    "medium pipe": pygame.transform.scale(load_image('medium_pipe.png'), (64, 96)),
    "tall pipe": pygame.transform.scale(load_image('tall_pipe.png'), (64, 128)),
    "small ladder": pygame.transform.scale(load_image('small_ladder.png'), (128, 128)),
    "small ladder reversed": pygame.transform.scale(load_image('small_ladder_reversed.png'), (128, 128)),
    "middle ladder": pygame.transform.scale(load_image('middle_ladder.png'), (160, 128)),
    "big ladder": pygame.transform.scale(load_image('big_ladder.png'), (288, 256)),
    "castle": pygame.transform.scale(load_image('castle.png'), (160, 160)),
    "post": pygame.transform.scale(load_image('post.png'), (32, 336)),
    "flag": pygame.transform.scale(load_image('flag.png'), (32, 32)),
    "? block": pygame.transform.scale(load_image('question_box.png'), (136, 32)),
    "brick": pygame.transform.scale(load_image('block_outworld.png'), (32, 32)),
    "mushroom": pygame.transform.scale(load_image('mushroom_walk.png'), (64, 32)),
}


def terminate():
    pygame.quit()
    sys.exit()


def drawing_map():
    f = open('map.txt', encoding='utf8')
    level = f.readlines()
    base = level[0].split()
    x = 0
    size_tile = 32
    y = height - size_tile * 2
    for i in range(len(base)):
        if i % 2:
            x += size_tile * int(base[i])
            continue
        for j in range(int(base[i])):
            block = Object("outworld base", x, y)
            block = Object("outworld base", x, y + size_tile)
            x += size_tile
    last = level[1:]
    for j in range(len(last)):
        m = last[j].split(";")
        for i in last[j].split(";"):
            s = i.split()
            if s[0] == "bh":
                hillock = Object("big hillock", int(s[1]), y - 70, 0)
            elif s[0] == "h":
                hillock = Object("hillock", int(s[1]), y - 38, 0)
            elif s[0] == "b":
                bush = Object("bush", int(s[1]), y - 32, 0)
            elif s[0] == "b2":
                bush = Object("double bush", int(s[1]), y - 32, 0)
            elif s[0] == "b3":
                bush = Object("triple bush", int(s[1]), y - 32, 0)
            elif s[0] == "c":
                cloud = Object("cloud", int(s[1]), int(s[2]), 0)
            elif s[0] == "c2":
                cloud = Object("double cloud", int(s[1]), int(s[2]), 0)
            elif s[0] == "c3":
                cloud = Object("triple cloud", int(s[1]), int(s[2]), 0)
            elif s[0] == "t":
                pipe = Object("short pipe", int(s[1]), y - 64)
            elif s[0] == "t2":
                pipe = Object("medium pipe", int(s[1]), y - 96)
            elif s[0] == "t3":
                pipe = Object("tall pipe", int(s[1]), y - 128)
            elif s[0] == "l":
                ladder = Object("small ladder", int(s[1]), y - 128)
            elif s[0] == "l2":
                ladder = Object("middle ladder", int(s[1]), y - 128)
            elif s[0] == "l3":
                ladder = Object("big ladder", int(s[1]), y - 256)
            elif s[0] == "lr":
                ladder = Object("small ladder reversed", int(s[1]), y - 128)
            elif s[0] == "cstl":
                castle = Object("castle", int(s[1]), y - 160)
            elif s[0] == "p":
                post = Object("post", int(s[1]), y - 336)
            elif s[0] == "f":
                flag = Object("flag", int(s[1]), int(s[2]))
            elif s[0] == "?":
                question = Question(tile_images["? block"], 4, 1, int(s[1]), int(s[2]))
            elif s[0] == "k":
                brick = Object("brick", int(s[1]), int(s[2]))
            elif s[0] == "m":
                mushroom = Mushroom(tile_images["mushroom"], 2, 1, int(s[1]), y - 32)
    screen.fill((92, 148, 252))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                animated_group.update()
                enemy_group.update(event)
        screen.fill((92, 148, 252))
        untouchable_group.draw(screen)
        objects_group.draw(screen)
        animated_group.draw(screen)
        enemy_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Object(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, touchable=1):
        if touchable:
            super().__init__(objects_group, all_sprites)
        else:
            super().__init__(untouchable_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Question(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, animated_group)
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


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, enemy_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.v = -500
        self.x = x
        self.start_ticks = pygame.time.get_ticks()
        self.gravity = 0

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
            if not pygame.sprite.spritecollideany(self, all_sprites):
                self.gravity = 5
            else:
                self.gravity = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if pygame.sprite.spritecollideany(self, objects_group):
                self.v = -self.v
            self.x += self.v / 100
            self.rect.x = self.x
            self.rect.y += self.gravity


all_sprites = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
animated_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
untouchable_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
drawing_map()
