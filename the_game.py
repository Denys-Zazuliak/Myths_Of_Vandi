import math
import random

import pygame

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
FPS = 60

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.sprites=[]

    def create_player(self,x=0,y=0):
        player_image = 'player.png'
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.vandi=Player(player_image,self.sprites,PLAYER_WIDTH,PLAYER_HEIGHT, x, y)

    def create_enemy(self,x=100,y=100):
        enemy_image = 'enemy.png'
        ENEMY_WIDTH = pygame.display.get_window_size()[0] // 200
        ENEMY_HEIGHT = pygame.display.get_window_size()[1] // 200
        enemy = Enemy(enemy_image, ENEMY_WIDTH, ENEMY_HEIGHT, x, y)
        self.sprites.append(enemy)

    def main_screen(self):
        # game loop
        self.create_player()
        self.create_enemy()
        self.create_enemy(200,200)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys = pygame.key.get_pressed()

            self.vandi.move(keys)

            self.screen.fill((135, 200, 235))

            self.screen.blit(self.vandi.img, self.vandi.rect)
            for sprite in self.sprites:
                self.screen.blit(sprite.img, sprite.rect)
                if self.count%FPS==0:
                    sprite.movement()

            # updating display and game
            pygame.display.flip()
            self.clock.tick(FPS)
            self.count += 1

        pygame.quit()

class Player(pygame.sprite.Sprite):
    def __init__(self, image, all_sprites, width, height, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.sprites=all_sprites
        self.velocity = 5

    def move(self, keys):
        for sprite in self.sprites:
            if keys[pygame.K_w]:
                sprite.rect.move_ip(0, -self.velocity)
            if keys[pygame.K_s]:
                sprite.rect.move_ip(0, self.velocity)
            if keys[pygame.K_a]:
                sprite.rect.move_ip(-self.velocity, 0)
            if keys[pygame.K_d]:
                sprite.rect.move_ip(self.velocity, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 3

    def movement(self):
        choices=[self.velocity, -self.velocity]
        choice=random.choice(choices)
        for i in range(random.randint(5,15)):
            self.rect.move_ip(choice,0)

if __name__ == '__main__':
    game = Game()
    game.main_screen()