import random
import pygame

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE=64 #50
FPS = 60

class Game:
    def __init__(self):
        # general setup
        self.setting_up()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.gravity = 0.5

    def setting_up(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def create_player(self,x,y):
        player_image = f'assets/vandi/player.png'
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.vandi=Player(player_image,PLAYER_WIDTH,PLAYER_HEIGHT, x, y)

    def main_screen(self):
        # game loop

        self.create_player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        while self.running:
            self.clock.tick(FPS)

            keys=self.input_handling()

            self.draw()

            self.vandi.update()
            self.update_movement(keys)
            self.vandi.wall_collisions()

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

        if keys[pygame.K_SPACE] and self.vandi.on_ground:
            self.vandi.jump()

        return keys

    def update_movement(self,keys):
        self.vandi.move(keys)

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.draw_grid()

        self.level1()

        self.screen.blit(self.vandi.img, self.vandi.rect)

    def draw_grid(self):
        for line in range(0, 80):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))


    def level1(self):
        layout=[
            ['B20'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A9', 'B1', 'A8', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['A3', 'B17'],
        ]
        world=World(layout)
        level1=world.load_level()

        for tile in level1:
            self.screen.blit(tile[0], tile[1])

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

class World():
    def __init__(self, data):
        self.tile_list=[]
        self.data = data

        self.block=pygame.image.load(f'assets/blocks/block.jpg')

        self.tile_count=0
        self.row_count=0

    def load_level(self):
        self.row_count=0
        for row in self.data:
            self.tile_count=0
            for tile in row:
                if tile[0]=='A':
                    self.tile_count+=int(tile[1:])
                if tile[0]=='B':
                    for i in range(int(tile[1:])):
                        img=pygame.transform.scale(self.block,(TILE_SIZE,TILE_SIZE))
                        img_rect=img.get_rect()
                        img_rect.x = TILE_SIZE*self.tile_count
                        img_rect.y= TILE_SIZE*self.row_count

                        tile=(img, img_rect)
                        self.tile_list.append(tile)

                        self.tile_count = self.tile_count + 1

            self.row_count+=1

        return self.tile_list

class Player(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y):
        self.images_right=[]
        self.index=0
        self.counter=0
        for num in range(1,5)
        self.img = pygame.image.load(image).convert_alpha()
        self.rect = self.img.get_rect(center=(x, y))
        self.on_ground = False
        self.on_top = False
        self.velocity = [5, 0]

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.move_ip(-self.velocity[0], 0)
        if keys[pygame.K_d]:
            self.rect.move_ip(self.velocity[0], 0)

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

if __name__ == '__main__':
    game = Game()
    game.main_screen()