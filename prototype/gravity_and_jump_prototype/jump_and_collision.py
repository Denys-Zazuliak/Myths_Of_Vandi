import math
import random
import pygame


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


    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys=self.input_handling()

            self.draw_background()




            #self.update_gravity()

            self.endframe()

        pygame.quit()

    def input_handling(self):
        keys = pygame.key.get_pressed()

        return keys

    def draw_background(self):
        self.screen.fill((135, 200, 235))

    def update_gravity(self):
        for sprite in self.sprites:
            if sprite.get_on_ground() and sprite.gravity < 5:
                sprite.gravity += 1
            sprite.rect.move_ip(0, sprite.gravity)

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
        self.rect = self.surf.get_rect()
        self.on_ground = False

    def jump(self, key):
        pass

    def collisions(self):
        pass

    def get_on_ground(self):
        return self.on_ground

if __name__ == '__main__':
    game = Game()
    game.main_screen()