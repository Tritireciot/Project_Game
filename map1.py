import pygame
import os
import sys

pygame.init()
size = width, height = 7000, 448
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
positions = open('poss.txt', encoding='utf8').readlines()
positions = list(map(lambda x: (int(x[1:x.find(",")]), int(x[x.find(" ") + 1:x.find(")")])), positions))
size_tile = 32
y = height - size_tile * 2


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
    "mushroom": pygame.transform.scale(load_image('mushroom_walk.png'), (68, 36)),
    "turtle": pygame.transform.scale(load_image("turtle_walk.png"), (128, 50)),
    "mario_jump": pygame.transform.scale(load_image("mario_jump.png"), (36, 36)),
    "mario_jump_reversed": pygame.transform.scale(load_image("mario_jump_reversed.png"), (36, 36)),
    "mario_default_reversed": pygame.transform.scale(load_image("mario_default_reversed.png"), (24, 34)),
    "mario_default": pygame.transform.scale(load_image("default_mario.png"), (24, 34)),
    "mario_left_turn": pygame.transform.scale(load_image("turn_to_left.png"), (26, 32)),
    "mario_right_turn": pygame.transform.scale(load_image("turn_to_rigth.png"), (26, 32)),
    "mario_run": pygame.transform.scale(load_image("mario_run.png"), (204, 32)),
    "stair_block": pygame.transform.scale(load_image('stair_block.png'), (32, 32)),
    "used_block": pygame.transform.scale(load_image("used_block.png"), (32, 32)),
    "flipping_coin": pygame.transform.scale(load_image("flipping_coin.png"), (64, 32))
}


def terminate():
    pygame.quit()
    sys.exit()


def drawing_map():
    f = open('map.txt', encoding='utf8')
    level = f.readlines()
    base = level[0].split()
    x = 0
    for i in range(len(base)):
        if i % 2:
            x += size_tile * int(base[i])
            continue
        for j in range(int(base[i])):
            block = Object("outworld base", x, y, 0, 1)
            block = Object("outworld base", x, y + size_tile, 0, 1)
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
                pipe = Object("short pipe", int(s[1]), y - 64, 1, 1)
            elif s[0] == "t2":
                pipe = Object("medium pipe", int(s[1]), y - 96, 1, 1)
            elif s[0] == "t3":
                pipe = Object("tall pipe", int(s[1]), y - 128, 1, 1)
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
                flag = Flag("flag", int(s[1]), int(s[2]))
            elif s[0] == "?":
                question = Question(tile_images["? block"], 4, 1, int(s[1]), int(s[2]))
            elif s[0] == "k":
                brick = Object("brick", int(s[1]), int(s[2]), 0, 1)
            elif s[0] == "m":
                mushroom = Mushroom(tile_images["mushroom"], 2, 1, int(s[1]), y - 32)
            elif s[0] == "trtl":
                turtle = Turtle(tile_images["turtle"], 4, 1, int(s[1]), y - 48)
            elif s[0] == "mu":
                mushroom = Mushroom(tile_images["mushroom"], 2, 1, int(s[1]), int(s[2]))
            elif s[0] == "mar":
                mario = Mario(tile_images["mario_default"], tile_images["mario_run"], 6, 1, int(s[1]), y - 32)
            elif s[0] == "sb":
                stair_block = Object("stair_block", int(s[1]), int(s[2]) - 32, 0, 1)
    screen.fill((92, 148, 252))
    while player_group.sprites()[0].rect.x < 3264 * 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((92, 148, 252))
        enemy_group.update(event)
        objects_group.update()
        mario_bases_group.update()
        untouchable_group.draw(screen)
        bases_group.draw(screen)
        objects_group.draw(screen)
        animated_group.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)
        player_group.update(event)
        pygame.display.flip()
        clock.tick(FPS)


class Object(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, touchable=1, base=0):
        if touchable and not base:
            super().__init__(objects_group, all_sprites)
        elif base and touchable:
            super().__init__(objects_group, bases_group, all_sprites, mario_bases_group)
        elif base:
            super().__init__(bases_group, all_sprites, mario_bases_group)
        else:
            super().__init__(untouchable_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.flag = "default"
        self.basey = pos_y

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group) and player_group.sprites()[0].rect.y - 4 <= self.rect.y \
                + 32 and self.flag == "default" and \
                (self.rect.x < player_group.sprites()[0].rect.x + player_group.sprites()[0].rect.w - 2 < self.rect.x
                 + self.rect.w and player_group.sprites()[0].flag == "jumpedr" or
                 self.rect.x < player_group.sprites()[0].rect.x + 2 < self.rect.x + self.rect.w and
                 player_group.sprites()[0].flag == "jumpedl") and\
                player_group.sprites()[0].rect.y + player_group.sprites()[0].rect.h > self.rect.y + self.rect.h:
            self.rect = self.rect.move(0, -15)
            self.flag = "upper"
            return
        if self.flag == "upper":
            if self.rect.y != self.basey:
                self.rect = self.rect.move(0, 1.5)
            else:
                self.flag = "default"


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, animated_group, mario_bases_group)
        self.frames = []
        self.cut_sheet(tile_images["flipping_coin"], 4, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.basey = y
        self.flag = "up"

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame == round(self.cur_frame):
            self.cur_frame = int(self.cur_frame % len(self.frames))
            self.image = self.frames[self.cur_frame]
        self.cur_frame += 1 / 8
        if self.rect.y > self.basey - 64 and self.flag == "up":
            self.rect = self.rect.move(0, -3)
        else:
            self.flag = "down"
        if self.rect.y < self.basey and self.flag == "down":
            self.rect = self.rect.move(0, 3)
        if self.rect.y == self.basey and self.flag == "down":
            self.kill()


class Flag(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        if player_group.sprites()[0].rect.x + 32 >= 3168 * 2:
            if self.rect.y < 176 * 2 - 32:
                self.rect = self.rect.move(0, 5)


class Question(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, animated_group, mario_bases_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.flag = "default"
        self.basey = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame == round(self.cur_frame) and self.flag == "default":
            self.cur_frame = int(self.cur_frame % len(self.frames))
            self.image = self.frames[self.cur_frame]
        self.cur_frame += 1 / 8
        if pygame.sprite.spritecollideany(self, player_group) and player_group.sprites()[0].rect.y - 4 <= self.rect.y \
                + 32 and self.flag == "default" and \
                (self.rect.x < player_group.sprites()[0].rect.x + player_group.sprites()[0].rect.w - 2 < self.rect.x
                 + self.rect.w and player_group.sprites()[0].flag == "jumpedr" or
                 self.rect.x < player_group.sprites()[0].rect.x + 2 < self.rect.x + self.rect.w and
                 player_group.sprites()[0].flag == "jumpedl"):
            coin = Coin(self.rect.x + 8, self.rect.y - 32)
            self.rect = self.rect.move(0, -15)
            self.image = tile_images["used_block"]
            self.flag = "upper"
            return
        if self.flag == "upper":
            if self.rect.y != self.basey:
                self.rect = self.rect.move(0, 1.5)
            else:
                self.flag = "used"


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, enemy_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.v = -60
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
        if player_group.sprites()[0].rect.x + 1700 >= self.rect.x:
            others = pygame.sprite.Group([i for i in enemy_group.sprites() if i.rect.x != self.rect.x])
            if not pygame.sprite.spritecollideany(self, bases_group):
                self.gravity = 10
                self.v = 0
            elif self.gravity:
                self.gravity = 0
                self.v = -20
            self.cur_frame += 1 / 10
            if int(round(self.cur_frame)) == int(self.cur_frame):
                self.cur_frame = self.cur_frame % len(self.frames)
            elif self.cur_frame <= len(self.frames):
                self.image = self.frames[int(self.cur_frame)]
            else:
                self.image = self.frames[int(self.cur_frame) - 1]
            if pygame.sprite.spritecollideany(self, objects_group):
                self.v = -self.v
            if pygame.sprite.spritecollideany(self, others):
                self.v = -self.v
            self.rect.x += self.v / 60
            self.rect.y += self.gravity / 2.5


class Turtle(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, enemy_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.v = -1
        self.isdead = 0
        self.start_ticks = 0
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
        if player_group.sprites()[0].rect.x + 1664 >= self.rect.x:
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
                if pygame.sprite.spritecollideany(self, objects_group):
                    self.v = -self.v
                if not pygame.sprite.spritecollideany(self, bases_group):
                    self.gravity = 10
                if self.v == 1:
                    self.cur_frame += 1 / 8
                    if self.cur_frame == round(self.cur_frame):
                        self.image = self.frames[int(self.cur_frame) % 2 + 2]
                    self.rect = self.rect.move((self.v, self.gravity / 2.5))
                else:
                    self.cur_frame += 1 / 8
                    if self.cur_frame == round(self.cur_frame):
                        self.image = self.frames[int(self.cur_frame) % 2]
                    self.rect = self.rect.move((self.v, self.gravity / 2.5))


class Mario(pygame.sprite.Sprite):
    def __init__(self, default_img, sheet, columns, rows, x, y):
        super().__init__(player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = default_img
        self.rect = self.rect.move(x, y)
        self.v = 2
        self.x = x
        self.start_ticks = 0
        self.flag = "default"
        self.st = 0
        self.gravity = 0
        self.base = y
        self.vx = 0
        self.vy = 0
        self.prev_x = x

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(objects_group.sprites()[-1])):
            self.flag = "end"
        if self.flag == "end":
            self.start_ticks = 0
            self.cur_frame += clock.tick() / 12
            self.image = self.frames[int(self.cur_frame) % 3 + 3]
            self.rect = self.rect.move(self.v, 0)
        if self.flag == "end" and self.rect.x < 3264 * 2:
            return
        if args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_RIGHT and any(
                map(lambda x: x == self.image, self.frames[3:])):
            self.image = marimg
            self.flag = "defaultr"
            self.vx = 0
        elif args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_RIGHT and self.flag == "left":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        if args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_LEFT and any(
                map(lambda x: x == self.image, self.frames[:3])):
            self.image = tile_images["mario_default_reversed"]
            self.flag = "defaultl"
            self.vx = 0
        elif args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_LEFT and self.flag == "right":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

        if (args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_RIGHT) or self.image == rturn or \
                args[0].type == pygame.USEREVENT and self.flag == "right":
            if self.flag == "left" and self.image != tile_images["mario_right_turn"] and \
                    self.image != tile_images["mario_default_reversed"]:
                self.image = tile_images["mario_right_turn"]
                self.start_ticks = pygame.time.get_ticks()
                self.cur_frame = 0
            self.flag = "right"
            if self.start_ticks and (pygame.time.get_ticks() - self.start_ticks) / 1000 < 0.25:
                return
            self.start_ticks = 0
            self.cur_frame += clock.tick() / 12
            self.image = self.frames[int(self.cur_frame) % 3 + 3]
            self.vx = self.v
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_LEFT or self.image == lturn or \
                args[0].type == pygame.USEREVENT and self.flag == "left":
            if self.flag == "right" and self.image != lturn and self.image != marimg:
                self.image = lturn
                self.start_ticks = pygame.time.get_ticks()
                self.cur_frame = 0
            self.flag = "left"
            if self.start_ticks and (pygame.time.get_ticks() - self.start_ticks) / 1000 < 0.25:
                return
            self.start_ticks = 0
            self.cur_frame += clock.tick() / 12
            self.vx = -self.v
            self.image = self.frames[int(self.cur_frame) % 3]
        if args and args[0].type == pygame.KEYDOWN and args[
            0].key == pygame.K_UP and self.flag != "jumpedr" and self.flag != "jumpedl":
            if self.flag == "right" or self.flag == "jumpedr" or self.flag == "defaultr":
                self.image = tile_images["mario_jump"]
                self.flag = "jumpedr"
            elif self.flag == "left" or self.flag == "jumpedl" or self.flag == "defaultl":
                self.image = tile_images["mario_jump_reversed"]
                self.flag = "jumpedl"
            if self.rect.y > self.base - 200:
                self.vy = -17.5

        if (args and args[0].type == pygame.KEYUP and args[0].key == pygame.K_UP) or self.rect.y <= self.base - 200:
            self.vy = 0

        if not pygame.sprite.spritecollideany(self, mario_bases_group):
            self.gravity += 0.35
            self.rect = self.rect.move(0, self.gravity)
        if pygame.sprite.spritecollideany(self, mario_bases_group) and \
                pygame.sprite.spritecollideany(self, mario_bases_group).rect.y > self.rect.y + self.rect.height - 2 and \
                (pygame.sprite.spritecollideany(self,
                                                mario_bases_group).rect.x <= self.rect.x + self.rect.width <= pygame.sprite.spritecollideany(
                    self, mario_bases_group).rect.x + pygame.sprite.spritecollideany(self,
                                                                                     mario_bases_group).rect.width or pygame.sprite.spritecollideany(
                    self,
                    mario_bases_group).rect.x <= self.rect.x <= pygame.sprite.spritecollideany(
                    self, mario_bases_group).rect.x + pygame.sprite.spritecollideany(self,
                                                                                     mario_bases_group).rect.width) \
                and (self.flag == "jumpedr" or self.flag == "jumpedl"):
            self.gravity = 0
            self.base = self.rect.y
            if self.flag == "jumpedr":
                self.image = tile_images["mario_default"]
                self.flag = "defaultr"
                self.vx = 0
            else:
                self.image = tile_images["mario_default_reversed"]
                self.flag = "defaultl"
                self.vx = 0

        if pygame.sprite.spritecollideany(self, mario_bases_group) and \
                self.rect.y + 32 > pygame.sprite.spritecollideany(self, mario_bases_group).rect.y > self.rect.y \
                and (pygame.sprite.spritecollideany(self,
                                                    mario_bases_group).rect.x <= self.rect.x <= pygame.sprite.spritecollideany(
            self, mario_bases_group).rect.x + pygame.sprite.spritecollideany(self, mario_bases_group).rect.width or
                     pygame.sprite.spritecollideany(self,
                                                    mario_bases_group).rect.x <= self.rect.x + self.rect.width <= pygame.sprite.spritecollideany(
                    self, mario_bases_group).rect.x + pygame.sprite.spritecollideany(self,
                                                                                     mario_bases_group).rect.width):
            self.rect = self.rect.move(0, -self.rect.y - 32 + pygame.sprite.spritecollideany(self,
                                                                                             mario_bases_group).rect.y)
            self.gravity = 0

        if pygame.sprite.spritecollideany(self, mario_bases_group) and pygame.sprite.spritecollideany(self,
                                                                                                      mario_bases_group) \
                .rect.y + pygame.sprite.spritecollideany(
            self,
            mario_bases_group).rect.height >= self.rect.y and self.rect.y + self.rect.height > pygame.sprite. \
                spritecollideany(
            self, mario_bases_group).rect.y + pygame.sprite.spritecollideany(self, mario_bases_group).rect.height:
            self.rect = self.rect.move(0, pygame.sprite.spritecollideany(self,
                                                                         mario_bases_group).rect.y + pygame.sprite.spritecollideany(
                self, mario_bases_group).rect.height - self.rect.y + 2)
            self.vy = 0

        if pygame.sprite.spritecollideany(self, mario_bases_group) and \
                pygame.sprite.spritecollideany(self,
                                               mario_bases_group).rect.x < self.rect.x < pygame.sprite.spritecollideany(
            self,
            mario_bases_group).rect.x + pygame.sprite.spritecollideany(self, mario_bases_group).rect.width and \
                self.rect.x + self.rect.width >= pygame.sprite.spritecollideany(self,
                                                                                mario_bases_group).rect.x + pygame.sprite.spritecollideany(
            self, mario_bases_group).rect.width and \
                (pygame.sprite.spritecollideany(self,
                                                mario_bases_group).rect.y <= self.rect.y <= pygame.sprite.spritecollideany(
                    self, mario_bases_group).rect.y + pygame.sprite.spritecollideany(self,
                                                                                     mario_bases_group).rect.height or
                 pygame.sprite.spritecollideany(self,
                                                mario_bases_group).rect.y <= self.rect.y
                 + self.rect.height - 2 <= pygame.sprite.spritecollideany(
                            self, mario_bases_group).rect.y
                 + pygame.sprite.spritecollideany(self,
                                                  mario_bases_group).rect.height or
                 (self.rect.y < pygame.sprite.spritecollideany(self,
                                                               mario_bases_group).rect.y < self.rect.y
                  + self.rect.height and
                  self.rect.y < pygame.sprite.spritecollideany(self,
                                                               mario_bases_group).rect.y + pygame.sprite.spritecollideany(
                             self, mario_bases_group).rect.width < self.rect.y + self.rect.height)):
            self.rect = self.rect.move(
                pygame.sprite.spritecollideany(self, mario_bases_group).rect.width +
                pygame.sprite.spritecollideany(self, mario_bases_group).rect.x - self.rect.x,
                0)

        if pygame.sprite.spritecollideany(self, mario_bases_group) and \
                pygame.sprite.spritecollideany(self,
                                               mario_bases_group).rect.x < self.rect.x + self.rect.width < pygame.sprite.spritecollideany(
            self,
            mario_bases_group).rect.x + pygame.sprite.spritecollideany(self, mario_bases_group).rect.width and \
                self.rect.x <= pygame.sprite.spritecollideany(self, mario_bases_group).rect.x and \
                (pygame.sprite.spritecollideany(self,
                                                mario_bases_group).rect.y <= self.rect.y <= pygame.sprite.spritecollideany(
                    self, mario_bases_group).rect.y + pygame.sprite.spritecollideany(self,
                                                                                     mario_bases_group).rect.height or
                 pygame.sprite.spritecollideany(self,
                                                mario_bases_group).rect.y <= self.rect.y
                 + self.rect.height - 2 <= pygame.sprite.spritecollideany(
                            self, mario_bases_group).rect.y
                 + pygame.sprite.spritecollideany(self,
                                                  mario_bases_group).rect.height or
                 (self.rect.y < pygame.sprite.spritecollideany(self,
                                                               mario_bases_group).rect.y < self.rect.y
                  + self.rect.height and
                  self.rect.y < pygame.sprite.spritecollideany(self,
                                                               mario_bases_group).rect.y + pygame.sprite.spritecollideany(
                             self, mario_bases_group).rect.width < self.rect.y + self.rect.height)):
            self.rect = self.rect.move(
                pygame.sprite.spritecollideany(self, mario_bases_group).rect.x
                - self.rect.x - self.rect.width,
                0)

        self.rect = self.rect.move(self.vx, self.vy)


all_sprites = pygame.sprite.Group()
bases_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
animated_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
untouchable_group = pygame.sprite.Group()
mario_bases_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
rturn = pygame.transform.scale(load_image("turn_to_rigth.png"), (26, 32))
lturn = pygame.transform.scale(load_image("turn_to_left.png"), (26, 32))
marimg = pygame.transform.scale(load_image("default_mario.png"), (24, 32))
marimgr = pygame.transform.scale(load_image("mario_default_reversed.png"), (24, 32))
jump = pygame.transform.scale(load_image("mario_jump.png"), (32, 32))
drawing_map()
