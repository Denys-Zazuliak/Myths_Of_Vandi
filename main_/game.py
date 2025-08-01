import random
import pygame

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE=64 #50
FPS = 60

class Game():
    def __init__(self):
        # general setup
        self.setting_up()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.gravity = 0.75
        self.level_count = 1

    def setting_up(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def create_player(self,x,y):
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.vandi=Player(PLAYER_WIDTH,PLAYER_HEIGHT, x, y)

    def main_screen(self):
        # game loop
        self.create_player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        while self.running:
            #if self.level_count==1:
            self.clock.tick(FPS)

            keys=self.input_handling()

            self.draw()

            self.update_movement(keys)

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
        self.vandi.move(keys, self.world)
        self.world.sharks.update(keys)

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.draw_grid()

        self.level1_load()
        self.world.sharks.draw(self.screen)

        self.screen.blit(self.vandi.img, self.vandi.rect)

    def draw_grid(self):
        for line in range(0, 80):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))


    def level1_load(self):
        layout=[
            ['B20'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A17', 'S1', 'B1'],
            ['A16', 'B4'],
            ['A15', 'B5'],
            ['A8', 'S1', 'A5', 'B6'],
            ['A3', 'B17'],
        ]
        if self.level_count==1:
            self.world=World(layout)
            self.level1=self.world.load_level()

        for tile in self.level1:
            self.screen.blit(tile[0], tile[1])

        self.level_count+=1

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
        self.sharks=pygame.sprite.Group()

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

                if tile[0]=='S':
                    # (TILE_SIZE * self.row_count - ((TILE_SIZE * (self.row_count)) - (TILE_SIZE * (self.row_count + 1))))
                    shark=Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count), 'shark', 2)
                    self.sharks.add(shark)

                    self.tile_count += 1

            self.row_count+=1

        return self.tile_list

class Player():
    def __init__(self, width, height, x, y):
        self.images_right=[]
        self.images_left = []
        self.index=0
        self.counter=0
        for i in range(1,3):
            img = pygame.image.load(f'assets/vandi/idle/vandi{i}.png').convert_alpha()
            img=pygame.transform.scale(img,(96,192))#(img.get_width()*2.5, img.get_height()*2.5))
            self.images_right.append(img)
            img_left=pygame.transform.flip(img,True,False)
            self.images_left.append(img_left)

        self.img=self.images_right[self.index]
        self.width=self.img.get_width()
        self.height=self.img.get_height()
        self.rect = self.img.get_rect(center=(x,y))
        self.on_ground = False
        self.velocity = [0, 0]
        self.direction=0

    def move(self, keys, world):
        self.velocity[0]=0
        self.on_ground=False

        if keys[pygame.K_a]:
            self.velocity[0]=-5

        if keys[pygame.K_d]:
            self.velocity[0]=5

        self.collision(world)
        self.wall_collisions()
        self.update()
        self.rect.move_ip(self.velocity[0], 0)

        self.counter+=1
        if self.counter > 5:
            self.counter=0

            if keys[pygame.K_d] == True:
                self.index += 1
                self.direction = 0
                if self.index >= len(self.images_right):
                    self.index = 0

            elif keys[pygame.K_a] == True:
                self.index += 1
                self.direction = 1
                if self.index >= len(self.images_left):
                    self.index = 0

            else:
                self.index=0

            if self.direction==0:
                self.img = self.images_right[self.index]
            elif self.direction==1:
                self.img = self.images_left[self.index]

    def update(self):
        if not self.on_ground:
            self.velocity[1] += game.gravity
        self.rect.move_ip(0, self.velocity[1])

    def jump(self):
        self.on_ground = False
        self.velocity[1] = -15

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

    def collision(self, world):
        for tile in world.tile_list:
            # vertical collision
            if tile[1].colliderect(self.rect.x, self.rect.y + self.velocity[1], self.width, self.height):
                if self.velocity[1] < 0:
                    self.velocity[1] = tile[1].bottom - self.rect.top
                elif self.velocity[1] > 0:
                    self.velocity[1] = tile[1].top - self.rect.bottom

            #horizontal collision
            if tile[1].colliderect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height):
                self.velocity[0]=0

            #gravity stuff
            if tile[1].colliderect(self.rect.x, self.rect.y + self.velocity[1] + game.gravity, self.width, self.height):
                self.on_ground = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name, size_scale):
        pygame.sprite.Sprite.__init__(self)

        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for i in range(1, 3):
            img = pygame.image.load(f'assets/enemy/idle/{name}{i}.png').convert_alpha()
            img = pygame.transform.scale(img,  (img.get_width()*size_scale, img.get_height()*size_scale))
            self.images_right.append(img)
            img_left = pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect=self.image.get_rect(center=(x,y))
        self.rect.y += y + 64 - self.rect.bottom
        self.direction = 1
        self.distance_tracker = 0

    def update(self, keys):
        self.rect.x += self.direction
        self.distance_tracker += 1

        if abs(self.distance_tracker) >= 64:
            self.direction *= -1
            self.distance_tracker *= -1

        self.counter += 1
        if self.counter > 5:
            self.counter = 0

            if self.direction>0:
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0

            elif self.direction<0:
                self.index += 1
                if self.index >= len(self.images_left):
                    self.index = 0

            if self.direction > 0:
                self.image = self.images_right[self.index]
            elif self.direction < 0:
                self.image = self.images_left[self.index]


if __name__ == '__main__':
    game = Game()
    game.main_screen()