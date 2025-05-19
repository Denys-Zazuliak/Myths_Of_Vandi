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
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.sprites=[]

    def create_player(self,x=0,y=0):
        player_image = f'../prototype/assets/player.png'
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.vandi=Player(player_image,self.sprites,PLAYER_WIDTH,PLAYER_HEIGHT, x, y, self.screen)

    def create_enemy(self,x=100,y=100):
        enemy_image = f'../prototype/assets/enemy.png'
        ENEMY_WIDTH= pygame.display.get_window_size()[0] // 200
        ENEMY_HEIGHT = pygame.display.get_window_size()[1] // 200
        enemy = Enemy(enemy_image, ENEMY_WIDTH, ENEMY_HEIGHT, x, y, self.screen)
        self.sprites.append(enemy)

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

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

            keys=self.input_handling()

            self.draw_background()

            self.update_movement(keys)

            #self.update_gravity()

            self.endframe()

        pygame.quit()

    def input_handling(self):
        keys = pygame.key.get_pressed()

        return keys

    def update_movement(self,keys):
        self.vandi.move(keys)
        self.vandi.jump(keys)

        self.screen.blit(self.vandi.img, self.vandi.rect)
        for sprite in self.sprites:
            self.screen.blit(sprite.img, sprite.rect)
            if self.count % (3 * FPS) == 0:
                sprite.movement()

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
    def __init__(self, image, all_sprites, width, height, x, y, screen):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.sprites=all_sprites
        self.velocity = 5
        self.on_ground=True
        self.gravity=1
        self.game_screen=screen

    def move(self, keys):
        for sprite in self.sprites:
            if keys[pygame.K_w]:
                sprite.rect.move_ip(0, self.velocity)
            if keys[pygame.K_s]:
                sprite.rect.move_ip(0, -self.velocity)
            if keys[pygame.K_a]:
                sprite.rect.move_ip(-self.velocity, 0)
            if keys[pygame.K_d]:
                sprite.rect.move_ip(self.velocity, 0)

    def jump(self, key):
        if not self.on_ground:
            for sprite in self.sprites:
                pass

    def get_on_ground(self):
        return self.on_ground


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y, screen):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 3
        self.on_ground=True
        self.gravity = 1
        self.game_screen=screen

    def movement(self):
        choices=[self.velocity, -self.velocity]
        choice=random.choice(choices)
        times=random.randint(2,6)
        for i in range(times):
            self.rect.move_ip(choice,0)
            self.game_screen.blit(self.img, self.rect)

    def get_on_ground(self):
        return self.on_ground

if __name__ == '__main__':
    game = Game()
    game.main_screen()