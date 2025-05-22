import random
import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
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
        self.blocks = []
        self.gravity = 0.5

    def create_player(self,x=0,y=0):
        player_image = f'../assets/player.png'
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.vandi=Player(player_image,self.sprites,PLAYER_WIDTH,PLAYER_HEIGHT, x, y)

    def create_enemy(self,x=100,y=100):
        enemy_image = f'../assets/enemy.png'
        ENEMY_WIDTH= pygame.display.get_window_size()[0] // 200
        ENEMY_HEIGHT = pygame.display.get_window_size()[1] // 200
        enemy = Enemy(enemy_image, ENEMY_WIDTH, ENEMY_HEIGHT, x, y)
        self.sprites.append(enemy)

    def create_block(self, x, y, width, height, colour=(0,0,0)):
        block_image = f'../assets/block.jpg'
        block=Block(x, y, width, height, colour, block_image)
        self.blocks.append(block)

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        self.create_player(SCREEN_WIDTH//200, SCREEN_HEIGHT//200)
        self.create_enemy()
        self.create_enemy(200,200)
        self.create_block(500, 1000, 100, 50)

        while self.running:
            keys=self.input_handling()

            self.draw()

            # player update
            self.vandi.update()
            self.update_movement(keys)
            self.vandi.wall_collisions()
            self.vandi.collision(self.blocks)
            if keys[pygame.K_SPACE] and self.vandi.on_ground:
                self.vandi.jump()

            for sprite in self.sprites:
                sprite.wall_collisions()
                sprite.collision(self.blocks)

            self.endframe()

        pygame.quit()

    def input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()

        return keys

    def update_movement(self,keys):
        self.vandi.move(keys)

        self.screen.blit(self.vandi.img, self.vandi.rect)
        for sprite in self.sprites:
            self.screen.blit(sprite.img, sprite.rect)
            if self.count % (3 * FPS) == 0:
                sprite.movement()

    def draw(self):
        self.screen.fill((135, 200, 235))
        # self.screen.blit(self.vandi.img, self.vandi.rect)
        pygame.draw.rect(self.screen, (255, 255, 255, 0), self.vandi.rect)
        # for sprite in self.sprites:
        #     pygame.draw.rect(self.screen, (0,0,0,0), sprite.rect)
        for block in self.blocks:
            self.screen.blit(block.img, block.rect)

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
    def __init__(self, image, all_sprites, width, height, x=SCREEN_WIDTH//200, y=SCREEN_HEIGHT//200):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = self.img.get_rect(center=(SCREEN_WIDTH//200, SCREEN_HEIGHT//200))
        self.sprites=all_sprites
        self.on_ground = True
        self.velocity = [5, 0]

    def move(self, keys):
        for sprite in self.sprites:
            # if keys[pygame.K_w]:
            #     sprite.rect.move_ip(0, self.velocity[1])
            # if keys[pygame.K_s]:
            #     sprite.rect.move_ip(0, -self.velocity[1])
            if keys[pygame.K_a]:
                sprite.rect.move_ip(-self.velocity[0], 0)
            if keys[pygame.K_d]:
                sprite.rect.move_ip(self.velocity[0], 0)

    def update(self):
        if not self.on_ground:
            self.velocity[1] += game.gravity
        self.rect.move_ip(0, self.velocity[1])

    def jump(self):
        self.on_ground = False
        self.velocity[1] = -10

    def wall_collisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True

    def collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block):
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.velocity[1] = 0



#add gravity to enemy
#make this pygame.sprite.Group and change movement and rect
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 3

    def movement(self):
        choices=[self.velocity, -self.velocity]
        choice=random.choice(choices)
        times=random.randint(2,6)
        for i in range(times):
            self.rect.move_ip(choice,0)

    def wall_collisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True

    def collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block):
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.velocity[1] = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour, image):
        self.img = pygame.image.load(image).convert_alpha()
        self.rect=self.img.get_rect(center=(x, y))
        # self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour

if __name__ == '__main__':
    game = Game()
    game.main_screen()