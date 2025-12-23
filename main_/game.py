#AMONGUS

# add wall jump (perchance)
# add type ins (def function(num:int))
# add docksins:
"""
function's role
Parameters
----------


Returns
-------


"""

import pygame
import json
import time
from pygame import mixer
from levels import load_levels

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE = 64 #50
SCROLL_THRESH = SCREEN_WIDTH//4
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
        self.volume = 0.2
        self.gravity = 0.75
        self.level_count = 1
        self.level_count_check = 0
        self.screen_scroll=0
        self.world = None
        self.vandi = None
        self.level1 = None

        mixer.music.load('assets/audio/bell_ding.mp3')
        mixer.music.set_volume(self.volume)

    @staticmethod
    def setting_up():
        pygame.init()
        mixer.init()
        pygame.display.set_caption('Myths Of Vandi')

    def start_screen(self):
        while self.menu.starting_menu_flag:
            self.clock.tick(FPS)
            self.input_handling()
            self.menu.start_menu()
            self.endframe()

        mixer.music.play(-1, 0.0)
        self.main_screen()

    def main_screen(self):
        # game loop
        while self.running:
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
        self.screen_scroll=self.vandi.move(keys, self.world)
        self.vandi.wall_collision()
        self.vandi.attack()

        for enemy in self.world.sharks:
            enemy.attack()
            if not enemy.tracking:
                enemy.update()
            enemy.collision(self.world)

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.draw_grid()

        if self.menu.load.active:
            self.menu.loading()
        elif self.level_count!=self.level_count_check:
            self.level_count_check=self.level_count
            self.level_load()

        for shark in self.world.sharks:
            shark.rect.x += self.screen_scroll
        self.world.sharks.draw(self.screen)

        for tile in self.level1:
            tile.img_rect.x=tile.img_rect.x+self.screen_scroll
            self.screen.blit(tile.img, tile.img_rect)

        self.screen.blit(self.vandi.img, self.vandi.rect)

        self.draw_text(f'Health: {self.vandi.health}', (100,20))

    def draw_grid(self):
        for line in range(0, 80):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

    def draw_text(self, text, coordinates):
        text = Text(text, 50, coordinates)
        text.draw(self.screen)

    def level_load(self):
        self.world, self.level1=load_levels(self.level_count, self)
        self.vandi = Player(TILE_SIZE * 6, TILE_SIZE * 9, self)

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

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
        # self.rect=pygame.Rect((x, y), (self.width//2, self.height))

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
        if self.rect.right >SCREEN_WIDTH - SCROLL_THRESH or self.rect.left <SCROLL_THRESH:
            self.rect.move_ip(-self.velocity[0], 0)
            self.screen_scroll = -self.velocity[0]

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

        return self.screen_scroll

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

    def wall_collision(self):
        if self.rect.left < 0:
            self.health = 0
        if self.rect.right > SCREEN_WIDTH:
            self.health = 0
        if self.rect.top <= 0:
            self.health = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.health = 0

    def collision(self, world):
        for tile in world.tile_list:
            # vertical collision
            jump_rect=pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.width, self.height))

            # check for end of level
            if 'finish' in tile.material:
                if rect_collision(tile.img_rect, jump_rect):
                    if self.velocity[1] < 0:
                        self.game.level_count += 1
                        print('load next level')
                    elif self.velocity[1] > 0:
                        self.game.level_count += 1
                        print('load next level')

                walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height)
                if rect_collision(tile.img_rect, walking_rect):
                    self.game.level_count += 1
                    print('load next level')

            # regular collision
            if rect_collision(tile.img_rect, jump_rect):
                if self.velocity[1] < 0:
                    self.velocity[1] = tile.img_rect.bottom - self.rect.top + 1
                elif self.velocity[1] > 0:
                    self.velocity[1] = tile.img_rect.top - self.rect.bottom - 1

            #horizontal collision
            walking_rect=pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height)
            if rect_collision(tile.img_rect, walking_rect):
                self.velocity[0]=0

            #gravity stuff
            gravity_rect=pygame.Rect(self.rect.x, self.rect.y + self.velocity[1] + game.gravity, self.width, self.height)
            if rect_collision(tile.img_rect, gravity_rect):
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
        self.pause_bg = pygame.image.load('assets/menu/background.jpg')
        self.pause_bg = pygame.transform.scale(self.pause_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pause_bg_rect = self.pause_bg.get_rect()
        self.start_bg = pygame.image.load('assets/menu/peak.jpg')
        self.start_bg = pygame.transform.scale(self.start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_bg_rect = self.start_bg.get_rect()

        self.starting_menu_flag=True
        self.settings_flag=False
        self.inventory=False
        self.pause=False

    def start_menu(self):
        if self.settings_flag:
            self.settings_menu()

        else:
            self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
            self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png', 0.2)
            self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/load.png', 0.2)
            self.buttons = [self.start, self.settings, self.load]
            title = Text('The Myths Of Vandi', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

            # self.game.screen.blit(self.start_bg, self.start_bg_rect)
            self.game.screen.fill((0, 0, 0))
            title.draw(self.game.screen)
            for button in self.buttons:
                button.draw_and_collision(self.game.screen)

            if self.start.active:
                for button in self.buttons:
                    del button

                self.starting_menu_flag=False

            if self.settings.active:
                for button in self.buttons:
                    del button

                self.settings_flag=True

            if self.load.active:
                for button in self.buttons:
                    del button

                self.loading()

                self.starting_menu_flag = False

    def pause_menu(self):
        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
        self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png', 0.2)
        self.save = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50, f'assets/menu/buttons/save.png', 0.2)
        self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/load.png', 0.2)
        self.pause=True
        self.buttons = [self.start, self.settings, self.save, self.load]
        paused=Text('Paused', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

        # self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        self.game.screen.fill((0, 0, 0))
        paused.draw(self.game.screen)
        for button in self.buttons:
            button.draw_and_collision(self.game.screen)

        if self.start.active:
            for button in self.buttons:
                del button

            self.pause=False

        if self.settings.active:
            for button in self.buttons:
                del button

            self.settings_flag=True

        if self.settings_flag:
            self.settings_menu()

        if self.save.active:
            self.saving()

        if self.load.active:
            for button in self.buttons:
                del button

            self.loading()

            self.pause = False

    def settings_menu(self):
        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
        self.sounds_plus = Button((SCREEN_WIDTH // 2)+300, (SCREEN_HEIGHT // 2) - 175, f'assets/menu/buttons/plus.png', 0.25)
        self.sounds_minus =Button((SCREEN_WIDTH // 2)+300, (SCREEN_HEIGHT // 2) - 75, f'assets/menu/buttons/minus.png', 0.25)
        self.buttons = [self.start, self.sounds_plus, self.sounds_minus]
        settings = Text('Settings', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
        volume = Text(f'Volume: {int(self.game.volume*100)}', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125))

        self.game.screen.fill((0, 0, 0))
        settings.draw(self.game.screen)
        volume.draw(self.game.screen)
        for button in self.buttons:
            button.draw_and_collision(self.game.screen)
            time.sleep(0.0228)

        if self.start.active:
            for button in self.buttons:
                del button

            self.settings_flag = False
            time.sleep(0.1)

        if self.sounds_plus.active:
            self.game.volume+=0.1
            mixer.music.set_volume(self.game.volume)

        if self.sounds_minus.active:
            self.game.volume-=0.1
            mixer.music.set_volume(self.game.volume)

    def inventory(self):
        pass

    def saving(self):
        write_json({'name': 'Vandi', 'level_count': self.game.level_count}, 'vandi')

    def loading(self):
        data=read_json('vandi')
        self.game.level_count=data['level_count']

        if self.game.level_count!=self.game.level_count_check:
            self.game.level_count_check=self.game.level_count
            self.game.level_load()

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
            if pygame.mouse.get_pressed()[0] and not self.active:
                self.active = True
            if not pygame.mouse.get_pressed()[0]:
                self.active = False

        return self.active

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
    game.start_screen()