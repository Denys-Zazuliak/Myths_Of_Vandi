#AMONGUS

# add wall jump

import pygame
import json

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE = 64 #50
SCROLL_THRESH = 216
FPS = 60
INVULNERABILITY_TIME = 0.5

class Game:
    def __init__(self):
        # general setup
        self.setting_up()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.menu = Menu(self)
        self.running = True
        self.count = 1
        self.gravity = 0.75
        self.level_count = 1
        self.world = None
        self.vandi = None
        self.level1 = None

    @staticmethod
    def setting_up():
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def create_player(self,x,y):
        self.vandi=Player(x, y, self)

    def main_screen(self):
        # game loop
        self.create_player(TILE_SIZE*3, TILE_SIZE*7)
        while self.running:
            #if self.level_count==1:
            self.clock.tick(FPS)

            keys=self.input_handling()

            if self.menu.pause or self.menu.inventory:
                self.menu.pause_menu()
            else:
               self.draw()
               self.update(keys)


            self.endframe()

        pygame.quit()

    def input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.menu.pause = True
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.vandi.on_ground:
            self.vandi.jump()

        return keys

    def update(self,keys):
        # screen_scroll=self.vandi.move(keys, self.world)
        self.vandi.move(keys, self.world)
        # print(screen_scroll)
        self.vandi.attack()

        for enemy in self.world.sharks:
            enemy.attack()
            if not enemy.tracking:
                enemy.update()
            enemy.collision(self.world)

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
        # layout=[
        #     ['B20'],
        #     ['B1', 'A17', 'M1', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B1', 'A9','S1','A8', 'B1'],
        #     # ['B1', 'A18', 'B1'],
        #     ['B1', 'A9', 'B1', 'A8', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B1', 'A18', 'B1'],
        #     ['B5', 'A13', 'S1', 'B1'],
        #     ['A16', 'B4'],
        #     ['A15', 'B5'],
        #     ['A8', 'S1', 'A5', 'B6'],
        #     ['A3', 'B17'],
        # ]

        layout = [
            ['B20'],
            ['B1', 'A17', 'M1', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A9', 'S1', 'A8', 'B1'],
            # ['B1', 'A18', 'B1'],
            ['B1', 'A9', 'B1', 'A8', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B5', 'A13', 'S1', 'B1'],
            ['A20'],
            ['A20'],
            ['A8', 'S1', 'A11'],
            ['A3', 'B20'],
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

class World:
    def __init__(self, data, parent_class):
        self.tile_list=[]
        self.data = data
        self.game=parent_class

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
                        tile_load(self, self.block)

                if tile[0]=='M':
                    for i in range(int(tile[1:])):
                        tile_load(self, self.metal)

                if tile[0]=='S':
                    # (TILE_SIZE * self.row_count - ((TILE_SIZE * (self.row_count)) - (TILE_SIZE * (self.row_count + 1))))
                    shark=Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count), 'shark', 2, self.game)
                    self.sharks.add(shark)

                    self.tile_count += 1

            self.row_count+=1

        return self.tile_list

class Player:
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
        self.attackHitbox = AttackHitbox(self)

        self.health = 5
        self.invulnerable = False
        self.i_frames = 0

        self.screen_scroll=0
        self.bg_scroll=0

    def move(self, keys, world):
        #movement
        self.screen_scroll=0
        self.velocity[0]=0
        self.on_ground=False

        if keys[pygame.K_a]:
            self.velocity[0]=-5

        if keys[pygame.K_d]:
            self.velocity[0]=5

        self.collision(world)
        # self.wall_collisions()
        self.update()
        self.rect.move_ip(self.velocity[0], 0)

        #camera scroll
        # if self.rect.right >SCREEN_WIDTH - SCROLL_THRESH or self.rect.left <SCROLL_THRESH:
        #     self.rect.move_ip(-self.velocity[0], 0)
        #     self.screen_scroll = -self.velocity[0]
        #
        # return self.screen_scroll


        #animation
        self.counter+=1
        if self.counter > 3:
            self.counter=0

            if keys[pygame.K_d]:
                self.index += 1
                self.direction = 0
                if self.index >= len(self.images_right):
                    self.index = 0

            elif keys[pygame.K_a]:
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
        if pygame.mouse.get_pressed()[0] and self.attackHitbox.index < (len(self.attackHitbox.images_right) - 1):
            self.attackHitbox.active=True

        if self.attackHitbox.active:
            self.game.screen.blit(self.attackHitbox.image, self.attackHitbox.rect)
            self.attackHitbox.animation()
            self.attackHitbox.hit_collision()

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

class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, attacker):
        super().__init__()
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

        self.velocity = [2,0]
        self.direction = 1
        self.distance_tracker = 0
        self.tracking = False

        self.health=3
        self.invulnerable=False
        self.i_frames=0


    def update(self):
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

        y=self.rect.y - height // 2
        if self.direction > 0:
            x=self.rect.midright[0]
            self.velocity[0]=abs(self.velocity[0])
        else:
            x=self.rect.midleft[0]-width
            self.velocity[0]=abs(self.velocity[0])*-1

        vision_box = pygame.Rect(x, y, width, height)
        vision_box_surface = pygame.Surface((width, height)).convert_alpha()
        vision_box_surface.fill((250, 50, 50, 200))
        # self.game.screen.blit(vision_box_surface, vision_box)

        if (not rect_collision(self.game.vandi.rect, self.rect)) and rect_collision(self.game.vandi.rect, vision_box):
            self.tracking=True

            if self.velocity[0] < 0:
                self.direction = -1
            elif self.velocity[0] > 0:
                self.direction = 1

            self.counter += 1
            if self.counter > 10:
                self.counter = 0

                if self.direction > 0:
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    self.image = self.images_right[self.index]


                elif self.direction < 0:
                    self.index += 1
                    if self.index >= len(self.images_left):
                        self.index = 0
                    self.image = self.images_left[self.index]

            self.rect.x+=self.velocity[0]
        else:
            self.tracking=False

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

class SpriteSheet:
    def __init__(self, image):
        self.sheet=image

    def get_image(self, frame_count, size, scale, colour):
        img = pygame.Surface((size[0], size[1])).convert_alpha()
        img.blit(self.sheet, (0, 0), (frame_count * size[0], 0, size[0], size[1]))
        img = pygame.transform.scale(img, (size[0] * scale, size[1] * scale))
        img.set_colorkey(colour)

        return img

class Text:
    def __init__(self, text, size, coordinates,colour=(255,255,255)):
        self.font = pygame.font.SysFont('Arial', size)
        self.text=self.font.render(text, True, colour)
        self.text_rect=self.text.get_rect(center=coordinates)

    # def draw(self, surface):
    #     temp_surface = pygame.Surface(self.text.get_size())
    #     temp_surface.fill((192, 192, 192))
    #     temp_surface.blit(self.text, self.text_rect)
    #     surface.blit(temp_surface, (0, 0))

    def draw(self, surface):
        pos=self.text_rect.x,self.text_rect.y
        surface.blit(self.text, pos)

class Menu:
    def __init__(self, parent_class):
        self.game = parent_class
        self.bg=pygame.image.load('assets/menu/background.jpg')
        self.bg=pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_rect=self.bg.get_rect()

        self.close=False
        self.inventory=False
        self.pause=False

        self.start=Button(SCREEN_WIDTH//2,(SCREEN_HEIGHT//2)-250, f'assets/menu/buttons/start.png', 0.2)
        self.settings=Button(SCREEN_WIDTH//2,(SCREEN_HEIGHT//2)-150, f'assets/menu/buttons/settings.png', 0.2)

    def pause_menu(self):
        self.pause=True
        paused=Text('Paused', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
        # self.game.screen.blit(self.bg, self.bg_rect)
        self.game.screen.fill((0, 0, 0))

        paused.draw(self.game.screen)
        self.start.draw_and_collision(self.game.screen)
        self.settings.draw_and_collision(self.game.screen)

        if self.start.active:
            self.pause=False

        if self.settings.active:
            self.settings_menu()


    def settings_menu(self):
        print('settings Menu')
        self.game.screen.fill((255, 255, 255))

    def inventory(self):
        pass

    def save(self):
        write_json({'name': self.game.vandi, 'level_count': self.game.level_count}, self.game.vandi)


class Button:
    def __init__(self, x, y, image, scale):
        self.image=pygame.image.load(image)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(x,y))
        self.active = False

    def draw_and_collision(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        mouse_pos = pygame.mouse.get_pos()

        if point_collision(mouse_pos, self.rect):
            if self.active == False and pygame.mouse.get_pressed()[0]==True:
                self.active = True
            else:
                self.active = False

        return self.active

def tile_load(self, material):
    img = pygame.transform.scale(material, (TILE_SIZE, TILE_SIZE))
    img_rect = img.get_rect()
    img_rect.x = TILE_SIZE * self.tile_count
    img_rect.y = TILE_SIZE * self.row_count

    tile = (img, img_rect)
    self.tile_list.append(tile)

    self.tile_count = self.tile_count + 1

def rect_collision(rect1, rect2):
    if rect1.right>=rect2.left and rect1.left<=rect2.right and rect1.bottom>=rect2.top and rect1.top<=rect2.bottom:
        colliding=True
    else:
        colliding=False

    return colliding

def point_collision(point_pos, rect):
    if point_pos[0]>=rect.left and point_pos[0]<=rect.right and point_pos[1]>=rect.top and point_pos[1]<=rect.bottom:
        colliding=True
    else:
        colliding=False
    return colliding

def read_json(file):
    file=file+".json"
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def write_json(data, file='Save'):
    file=file+'.json'
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(", ", " : "), sort_keys=True)
    return file

if __name__ == '__main__':
    game = Game()
    game.main_screen()