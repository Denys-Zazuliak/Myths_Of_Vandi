import random
import pygame

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE=64 #50
FPS = 60
INVULNERABILITY_TIME = 0.5

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
        self.vandi=Player(x, y, self)

    def main_screen(self):
        # game loop
        self.create_player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        while self.running:
            #if self.level_count==1:
            self.clock.tick(FPS)

            keys=self.input_handling()

            self.draw()

            self.update(keys)

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

    def update(self,keys):
        self.vandi.move(keys, self.world)
        self.vandi.attack()

        self.world.sharks.update(keys)
        for enemy in self.world.sharks:
            enemy.attack()

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.draw_grid()

        self.level1_load()
        self.world.sharks.draw(self.screen)

        self.screen.blit(self.vandi.img, self.vandi.rect)

        self.draw_text(f'Health: {self.vandi.health}')

    def draw_grid(self):
        for line in range(0, 80):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

    def draw_text(self, text):
        text = Text(text, 50, (0,0))
        text.draw(self.screen)

    def level1_load(self):
        layout=[
            ['B20'],
            ['B1', 'A17', 'M1', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A9','S1','A8', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B5', 'A13', 'S1', 'B1'],
            ['A16', 'B4'],
            ['A15', 'B5'],
            ['A8', 'S1', 'A5', 'B6'],
            ['A3', 'B17'],
        ]
        if self.level_count==1:
            self.world=World(layout, self)
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
    def __init__(self, data, game):
        self.tile_list=[]
        self.data = data
        self.game=game

        self.block=pygame.image.load(f'assets/blocks/block.jpg')
        self.metal=pygame.image.load(f'assets/blocks/metal.png')
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

                if tile[0]=='M':
                    for i in range(int(tile[1:])):
                        img = pygame.transform.scale(self.metal, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = TILE_SIZE * self.tile_count
                        img_rect.y = TILE_SIZE * self.row_count

                        tile = (img, img_rect)
                        self.tile_list.append(tile)

                        self.tile_count = self.tile_count + 1

                if tile[0]=='S':
                    # (TILE_SIZE * self.row_count - ((TILE_SIZE * (self.row_count)) - (TILE_SIZE * (self.row_count + 1))))
                    shark=Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count), 'shark', 2, self.game)
                    self.sharks.add(shark)

                    self.tile_count += 1

            self.row_count+=1

        return self.tile_list

class Player():
    def __init__(self, x, y, game):
        self.images_right=[]
        self.images_left = []
        self.index=0
        self.counter=0

        self.image_size = [64,52]
        self.walking_sprites=SpriteSheet(pygame.image.load('assets/vandi/walk.png').convert_alpha())
        self.animation_steps=9

        for i in range(self.animation_steps):
            img = self.walking_sprites.get_image(i, self.image_size, 2, (0,0,0)).convert_alpha()
            self.images_right.append(img)
            img_left=pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.game=game
        self.img=self.images_right[self.index]
        self.width=self.img.get_width()
        self.height=self.img.get_height()
        self.rect = self.img.get_rect(center=(x,y))

        self.on_ground = False
        self.velocity = [0, 0]
        self.direction=0
        self.attack_hitbox = Attack_hitbox(self)

        self.health = 5
        self.invulnerable = False
        self.i_frames = 0


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
        if self.counter > 3:
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

    def attack(self):
        if pygame.mouse.get_pressed()[0] and self.attack_hitbox.index < (len(self.attack_hitbox.images_right) - 1):
            self.attack_hitbox.active=True

        if self.attack_hitbox.active:
            self.game.screen.blit(self.attack_hitbox.image, self.attack_hitbox.rect)
            self.attack_hitbox.animation()
            self.attack_hitbox.hit_collision()

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
            jump_rect=pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.width, self.height))
            if rect_collision(tile[1], jump_rect):
                if self.velocity[1] < 0:
                    self.velocity[1] = tile[1].bottom - self.rect.top + 1
                    # self.velocity[1] = 0
                elif self.velocity[1] > 0:
                    self.velocity[1] = tile[1].top - self.rect.bottom - 1
                    # self.velocity[1] = 0

            #horizontal collision
            walking_rect=pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height)
            if rect_collision(tile[1], walking_rect):
                self.velocity[0]=0

            #gravity stuff
            gravity_rect=pygame.Rect(self.rect.x, self.rect.y + self.velocity[1] + game.gravity, self.width, self.height)
            if rect_collision(tile[1], gravity_rect):
                self.on_ground = True

    def check_dead(self):
        dead = False
        if self.health <= 0:
            del self
            dead = True
        return dead

    def invulnerability_update(self):
        self.i_frames += 1
        if self.i_frames >= (INVULNERABILITY_TIME * FPS):
            self.invulnerable = False
            self.i_frames = 0

class Attack_hitbox(pygame.sprite.Sprite):
    def __init__(self, attacker):
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(1,7):
            img = pygame.image.load(f'assets/attack/attack{i}.png').convert_alpha()
            img=pygame.transform.rotate(img, -150)
            img = pygame.transform.scale(img,  (img.get_width(), img.get_height()))
            self.images_right.append(img)
            img_left = pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.active=False
        self.attacker=attacker

        self.last_update = 0

        if self.attacker.direction == 0:
            self.image = self.images_right[0]
            self.rect = self.image.get_rect(midleft=self.attacker.rect.midright)
        elif self.attacker.direction == 1:
            self.image = self.images_left[0]
            self.rect = self.image.get_rect(midright=self.attacker.rect.midleft)

    def hit_collision(self):
        for tile in self.attacker.game.world.sharks:
            if not tile.invulnerable and rect_collision(tile.rect, self.rect):
                tile.health-=1
                tile.invulnerable=True
                print(tile.health)
                if tile.check_dead():
                    self.attacker.game.world.sharks.remove(tile)

            tile.invulnerability_update()

    def animation(self):
        delay=100

        current_time = pygame.time.get_ticks()
        if self.last_update == 0:
            self.last_update = current_time

        if current_time - self.last_update > delay:
            self.index += 1
            self.last_update = current_time

        if self.index >= len(self.images_right):
            self.index = 0
            self.active = False

        if self.attacker.direction == 0:
            self.image = self.images_right[self.index]
            self.rect.left = self.attacker.rect.right
            self.rect.y = self.attacker.rect.midtop[1]
        elif self.attacker.direction == 1:
            self.image = self.images_left[self.index]
            self.rect.right = self.attacker.rect.left
            self.rect.y = self.attacker.rect.top


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name, size_scale, game):
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

        self.game = game
        self.image = self.images_right[self.index]
        self.rect=self.image.get_rect(center=(x,y))
        self.rect.y += y + 64 - self.rect.bottom
        self.velocity = [1,0]
        self.velocity = [1,0]
        self.direction = 1
        self.distance_tracker = 0

        self.health=3
        self.invulnerable=False
        self.i_frames=0


    def update(self, keys):
        self.collision(self.game.world)
        self.distance_tracker += self.velocity[0]

        if abs(self.distance_tracker) >= 64:
            self.velocity[0] *= -1
            self.distance_tracker = 0

        if self.velocity[0] < 0:
            self.direction = -1
        elif self.velocity[0] > 0:
            self.direction = 1

        self.counter += 1
        if self.counter > 10:
            self.counter = 0

            if self.direction>0:
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index]


            elif self.direction<0:
                self.index += 1
                if self.index >= len(self.images_left):
                    self.index = 0
                self.image = self.images_left[self.index]

            self.rect.move_ip(self.velocity[0], 0)

    def check_dead(self):
        dead=False
        if self.health <= 0:
            del self
            dead=True
        return dead

    def invulnerability_update(self):
        self.i_frames += 1
        if self.i_frames >= (INVULNERABILITY_TIME * FPS):
            self.invulnerable=False
            self.i_frames = 0

    def attack(self):
        width=TILE_SIZE*4
        height=TILE_SIZE*3
        if not rect_collision(self.game.vandi.rect, self.rect):
            #make it midleft= instead (ask AI on how to do it and note it in the write up
            vision_box=pygame.Rect((self.rect.x+self.rect.width//2), (self.rect.y-height//2), width, height)
            vision_box_surface=pygame.Surface((width, height)).convert_alpha()
            vision_box_surface.fill((250,50,50,200))
            self.game.screen.blit(vision_box_surface, vision_box)

        if not self.game.vandi.invulnerable and rect_collision(self.game.vandi.rect, self.rect):
            self.game.vandi.health -= 1
            self.game.vandi.invulnerable = True
            print(self.game.vandi.health)
            if self.game.vandi.check_dead():
                print('Game Over')

        self.game.vandi.invulnerability_update()

    def collision(self, world):
        for tile in world.tile_list:
            # vertical collision
            gravity_rect = pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.rect.width, self.rect.height))
            if rect_collision(tile[1], gravity_rect):
                if self.velocity[1] > 0:
                    self.velocity[1] = tile[1].top - self.rect.bottom - 1

            # horizontal collision
            walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)
            if rect_collision(tile[1], walking_rect):
                self.velocity[0] *= -1

        self.rect.move_ip(self.velocity)
        self.velocity[1] += self.game.gravity

class SpriteSheet():
    def __init__(self, image):
        self.sheet=image

    def get_image(self, frame_count, size, scale, colour):
        img = pygame.Surface((size[0], size[1])).convert_alpha()
        img.blit(self.sheet, (0, 0), (frame_count * size[0], 0, size[0], size[1]))
        img = pygame.transform.scale(img, (size[0] * scale, size[1] * scale))
        img.set_colorkey(colour)

        return img

class Text():
    def __init__(self, text, size, coordinates,colour=(0,0,0)):
        self.font = pygame.font.SysFont('Arial', size)
        self.text=self.font.render(text, True, colour)
        self.text_rect=self.text.get_rect(topleft=(coordinates))

    def draw(self, surface):
        temp_surface = pygame.Surface(self.text.get_size())
        temp_surface.fill((192, 192, 192))
        temp_surface.blit(self.text, self.text_rect)
        surface.blit(temp_surface, (0, 0))

def rect_collision(rect1, rect2):
    if rect1.right>=rect2.left and rect1.left<=rect2.right and rect1.bottom>=rect2.top and rect1.top<=rect2.bottom:
        colliding=True
    else:
        colliding=False

    return colliding

if __name__ == '__main__':
    game = Game()
    game.main_screen()