#can't debug the jump function properly for some reason


import math
import random
import pygame
from pygame import K_SPACE

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
FPS = 60

class Game:
    def __init__(self):
        # general setup
        self.pygame_init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.count = 1
        self.sprites=[]

    def create_player(self):
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.player=Player()


    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        self.create_player()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys=self.input_handling()

            self.draw_background()

            self.player.jump(keys)

            self.update_gravity()

            self.endframe()

        pygame.quit()

    def input_handling(self):
        keys = pygame.key.get_pressed()

        return keys

    def draw_background(self):
        self.screen.fill((135, 200, 235))
        self.screen.blit(self.player.surf, self.player.rect)

    def update_gravity(self):
        if self.player.get_on_ground() and self.player.gravity < 11:
            self.player.gravity += 1
        self.player.rect.move_ip(0, self.player.gravity)

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = pygame.Rect(500, 500, 64, 64)
        self.on_ground = True
        self.gravity=0
        self.velocity=1

    #need to delete the last (self.on_ground=True) from here and add it to the collisions function when i make it
    def jump(self, key):
        if key[pygame.K_SPACE]:
            self.gravity=0
            self.on_ground = False
            for i in range(10,0,-1):
                self.rect.move_ip(0, -i)
                game.draw_background()
        self.on_ground = True

    def collisions(self):
        pass

    def get_on_ground(self):
        return self.on_ground

if __name__ == '__main__':
    game = Game()
    game.main_screen()