import pygame
import os
import sys
import random
pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 600
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Aria', 100)
lvl_game = 1
from load import *


def game_lvl():
    fon.update()
    player2_group.draw(sc)
    player2_group.update()
    player1_group.draw(sc)
    player1_group.update()
    pygame.display.update()

class Fon:
    def __init__(self):
        self.timer = 0
        self.frame = 0
        self.image = fon_image

    def update(self):
        self.timer += 2
        sc.blit(self.image[self.frame], (0,0))
        if self.timer / FPS > 0.1:
            if self.frame == len(self.image) - 1:
                self.frame = 0
            else:
                self.frame += 1
            self.timer = 0

class Player_1(pygame.sprite.Sprite):
    def __init__(self, image_lists):
        pygame.sprite.Sprite.__init__(self)
        self.image_lists = image_lists
        self.image = self.image_lists['idle'][0]
        self.current_list_image = self.image_lists['idle']
        self.rect = self.image.get_rect()
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.frame = 0
        self.timer_anime = 0
        self.dir = 'right'
        self.hp = 100
        self.jump_step = -20
        self.jump = False
        self.flag_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        self.rect.center = (200, 380)
        self.hp_bar = 'blue'
        self.text = False
        self.key = pygame.key.get_pressed()

    def move(self):
        if self.key[pygame.K_d]:
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif self.key[pygame.K_a]:
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False


    def jumps(self):
        if self.key[pygame.K_w]:
            self.jump = True
        if self.jump:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -20

    def attack(self):
        if self.key[pygame.K_e] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_run = False
            self.anime_idle = False
            self.flag_damage = True

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = player1_image_idle
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0
        if self.anime_idle:
            self.current_list_image = self.image_lists['idle']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        elif self.anime_run:
            self.current_list_image = self.image_lists['run']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        elif self.anime_atk:
            self.current_list_image = self.image_lists['atk']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        try:
            if self.dir == 'right':
                self.image = self.current_list_image[self.frame]
            else:
                self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)
        except:
            self.frame = 0

    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (0,0, 600 * self.hp / 100, 50))

    def maska_k(self):
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        for point in self.mask_list:
            x = point[0]
            y = point[1]
            pygame.draw.circle(sc, 'red', (x, y), 3)

    def life(self):
        if len(set(self.mask_list) & set(player2.mask_list)) > 0 and self.flag_damage:
            self.hp += 10
            self.flag_damage = False


    def winner(self):
        if self.hp <= 0:
            # text_render = font.render('player 2 is winner!', True, 'black')
            # sc.blit(text_render, (370, 300))
            player2.text = True
            self.kill()
            player2.anime_idle = False
            player2.anime_atk = False
            player2.anime_run = False
            player2.flag_damage = False
            player2.jump = False
        elif self.hp >= 200:
            # text_2 = font.render('player 1 is winner!', True, 'black')
            # sc.blit(text_2, (370, 300))
            self.text = True
            self.anime_idle = False
            self.anime_atk = False
            self.anime_run = False
            self.flag_damage = False
            self.jump = False
            player2.kill()


    def tex_render(self):
        if self.text:
            text_2 = font.render('player 1 is winner!', True, 'black')
            sc.blit(text_2, (300, 150))


    def update(self):
        if self.rect.center[0] - player2.rect.center[0] < 0:
            self.dir = 'right'
        else:
            self.dir = 'left'
        self.key = pygame.key.get_pressed()
        self.winner()
        self.tex_render()
        self.move()
        self.animation()
        self.attack()
        self.jumps()
        self.draw_hp_bar()
        self.maska_k()
        self.life()





class Player_2(pygame.sprite.Sprite):
    def __init__(self, image_lists):
        pygame.sprite.Sprite.__init__(self)
        self.image_lists = image_lists
        self.image = self.image_lists['idle'][0]
        self.current_list_image = self.image_lists['idle']
        self.rect = self.image.get_rect()
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.frame = 0
        self.timer_anime = 0
        self.dir = 'left'
        self.hp = 100
        self.jump_step = -20
        self.jump = False
        self.flag_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        self.rect.center = (1000, 380)
        self.hp_bar = 'red'
        self.text = False
        self.key = pygame.key.get_pressed()

    def move(self):
        if self.key[pygame.K_RIGHT]:
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif self.key[pygame.K_LEFT]:
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False


    def jumps(self):
        if self.key[pygame.K_UP]:
            self.jump = True
        if self.jump:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -20

    def attack(self):
        if self.key[pygame.K_SPACE] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_run = False
            self.anime_idle = False
            self.flag_damage = True

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = player2_image_idle
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0
        if self.anime_idle:
            self.current_list_image = self.image_lists['idle']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        elif self.anime_run:
            self.current_list_image = self.image_lists['run']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        elif self.anime_atk:
            self.current_list_image = self.image_lists['atk']
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
        try:
            if self.dir == 'right':
                self.image = self.current_list_image[self.frame]
            else:
                self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)
        except:
            self.frame = 0

    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (0,0, 1200, 50))


    def maska_k(self):
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        for point in self.mask_list:
            x = point[0]
            y = point[1]
            pygame.draw.circle(sc, 'green', (x, y), 3)

    def life(self):
        if len(set(self.mask_list) & set(player1.mask_list)) > 0 and self.flag_damage:
            player1.hp -= 10
            self.flag_damage = False

    def tex_render(self):
        if self.text:
            text_1 = font.render('player 2 is winner!', True, 'black')
            sc.blit(text_1, (300, 150))

    def update(self):
        if self.rect.center[0] - player1.rect.center[0] < 0:
            self.dir = 'right'
        else:
            self.dir = 'left'
        self.key = pygame.key.get_pressed()
        self.tex_render()
        self.move()
        self.animation()
        self.attack()
        self.jumps()
        self.draw_hp_bar()
        self.maska_k()
        self.life()



def restart():
    global fon, player1_group, player2_group, player1, player2
    fon = Fon()
    player1_group = pygame.sprite.Group()
    player1 = Player_1({'idle':player1_image_idle, 'run': player1_image_run, 'atk': player1_image_attack})
    player1_group.add(player1)
    player2_group = pygame.sprite.Group()
    player2 = Player_2({'idle': player2_image_idle, 'run': player2_image_run, 'atk': player2_image_attack})
    player2_group.add(player2)



restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)
