#AMONGUS
#
# death screen

# add wall jump (perchance)
# add type ins (def function(num:int))
# add docksins:
"""
function's role

Parameters
----------


Methods
-------

"""

import pygame
import time
from pygame import mixer
from utils import *
from levels import load_levels
from inventory import Inventory, Item

SCREEN_WIDTH = 1280  #1600
SCREEN_HEIGHT = 960  #900
TILE_SIZE = 64  #50
SCROLL_THRESH = SCREEN_WIDTH // 8
FPS = 60
INVULNERABILITY_TIME = 0.5

class Game:
    '''
    The class that controls the game screen and behind the scenes processes such as:
    drawing on the screen, taking input, updating different variables etc.

    Attributes
    ----------
        screen : Surface
            an instance of the screen class,
            the place where all objects are displayed

        clock : Clock
            an instance of the clock class,
            helps to set the max frame rate of the program

        font : Font
            an instance of the font class,
            tells the program whether the text is in bold, italic, strikethrough or underlined
            In addition, it states the font and the size of text

        menu : Menu
            an instance of the menu class,
            responsible for managing every single menu used in the game

        running : bool
            a variable that determines whether the game loop should carry on

        volume : int
            a variable responsible for the volume of the sounds and music in-game

        gravity : int
            a variable responsible for the strength of gravity in the game

        level_count :
            a variable used to determine what level the player is currently on

        level_count_check : int
            a flag made to check whether the level count has increased

        screen_scroll : int
            determines by how much should each object on the screen move in relation to the player's movement

        world : World
            an instance of the world class,
            responsible for transformation of the level layout into a usable list of tiles

        vandi : Player
            an instance of the player class,
            which the user controls

        level : list[Tile, Enemy]
            contains every single tile on a level


    Methods
    -------
        __init__():
            constructs all the necessary attributes for the game class

        setting_up():
            initialises pygame and mixer and set the title of the window to "Myths of Vandi"

        start_screen():
            loads up the starting screen with different options before the main game is loaded in

        main_screen():
            executes all the actions that happen in the game

        input_handling():
            gets the state of all keyboard buttons
            and  close the game or open the pause menu if the right keys are pressed

        update(keys):
            responsible for initialising movement, collision and attack methods in enemies and player classes

        draw():
            draws all the objects on the screen

        draw_text(text, coordinates):
            draws text on the screen

        level_load():
            loads the level layout into a list variable as well as creates the player

        endframe():
            flips the updated display and sets max FPS

    '''

    def __init__(self):
        # general setup
        self.setting_up()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.menu = Menu(self)
        self.items = []
        self.running = True
        self.volume = 0.2
        self.gravity = 0.75
        self.level_count = 1
        self.level_count_check = 0
        self.screen_scroll = 0
        self.world = None
        self.level = None
        self.vandi = self.vandi = Player(0,0, self)

        mixer.music.load('assets/audio/bell_ding.mp3')
        mixer.music.set_volume(self.volume)

    @staticmethod
    def setting_up():
        pygame.init()
        mixer.init()
        pygame.display.set_caption('Myths Of Vandi')

    def start_screen(self):
        while self.menu.starting_menu_flag:
            self.input_handling()
            self.menu.start_menu()
            self.endframe()

        mixer.music.play(-1, 0.0)
        self.main_screen()

    def main_screen(self):
        # game loop
        while self.running:
            keys = self.input_handling()

            if self.menu.pause:
                self.menu.pause_menu()
            elif self.menu.death_screen_flag:
                self.menu.death_screen()
            elif self.menu.inventory_flag:
                self.menu.inventory_menu()
            elif self.menu.ending_screen_flag:
                self.menu.ending_screen()
            else:
                if self.world != None:
                    self.draw()
                    self.update(keys)

            self.endframe()

        pygame.quit()

    def input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                    self.vandi.not_press = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.pause = True
                if event.key == pygame.K_i:
                    if not self.menu.inventory_flag:
                        self.menu.inventory_flag = True
                    else:
                        self.menu.inventory_flag = False

        keys = pygame.key.get_pressed()

        return keys

    def update(self, keys):
        self.screen_scroll = self.vandi.move(keys, self.world)

        if keys[pygame.K_SPACE] and self.vandi.on_ground:
            self.vandi.jump()

        # wall jumps
        if keys[pygame.K_SPACE] and self.vandi.air_jumps > 0 and self.vandi.wall_collided:
            self.vandi.jump()
            self.vandi.air_jumps -= 1

        self.vandi.wall_collision()
        self.vandi.attack()

        for enemy in self.world.sharks:
            enemy.attack()
            if not enemy.tracking:
                enemy.update()
            enemy.collision(self.world)

    def draw(self):
        self.screen.fill((50, 50, 50))
        # pygame.draw.rect(self.screen, (255, 255, 255), self.vandi.rect)

        if self.level_count != self.level_count_check:
            self.level_count_check = self.level_count
            self.level_load()

        #draw the updated tiles and enemies
        for shark in self.world.sharks:
            shark.rect.x += self.screen_scroll
            if shark.name=='goblin':
                # surf=pygame.Surface((64,128), pygame.SRCALPHA)
                # surf.fill((255,255,255))
                self.screen.blit(shark.image, shark.rect)
        self.world.sharks.draw(self.screen)

        for tile in self.level:
            tile.img_rect.x = tile.img_rect.x + self.screen_scroll
            self.screen.blit(tile.img, tile.img_rect)

        #dropped item
        for item in self.items:
            item.rect.x = item.rect.x + self.screen_scroll
            self.screen.blit(item.img, item.rect)

            # to avoid going through the list again
            if rect_collision(item.rect, self.vandi.rect):
                self.menu.inventory.add(item)
                self.items.remove(item)

        self.screen.blit(self.vandi.img, self.vandi.img_rect)

        self.draw_text(f'Health: {self.vandi.health}', (100, 20))

    # def draw_grid(self):
    #     for line in range(0, 80):
    #         pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
    #         pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

    def draw_text(self, text, coordinates, screen=None):
        if screen==None:
            screen = self.screen

        text = Text(text, 50, coordinates)
        text.draw(screen)

    def level_load(self):
        self.world, self.level = load_levels(self.level_count, self)
        self.vandi = Player(TILE_SIZE * 5, TILE_SIZE * 8, self)

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)


class Player:
    """
    The class to represent a player character

    Atributes
    ----------
        images_right : list[Surface]
            list of player sprites for when he's going right

        images_left : list[Surface]
            list of player sprites for when he's going left

        index : int
            index of the player's sprite in the list

        counter : int
            helps to keep track of how often to update the sprite image

        image_size : list[int]
            the size of the sprite image as it is in the spritesheet (in pixels)

        walking_sprites : SpriteSheet
            an instance of the spritesheet class,
            stores the image of the character's sprites

        animation_steps : int
            tells how many different sprites are in the spritesheet

        game: Game
            an instance of the game class,
            gives access to the main game class attributes such as screen and level_count (only these are used)

        img : Surface
            an instance of the surface class,
            the current sprite of the player

        width : int
            the width of the player rect

        height : int
            the height of the player rect

        rect : Rect
            an instance of the rect class,
            this is a rectangle object that simulates the hitbox of a character

        on_ground : bool
            indicates whether the character is on the ground

        velocity : list[int]
            stores both components of the character's velocity (in pixels)

        direction : int
            shows which way the character is looking (1 means to the right, 0 means to the left)

        attackHitbox : AttackHitbox
            an instance of the attack hitbox class,
            represents the hitbox of the character's attack

        health : int
            character's HP

        invulnerable : bool
            helps determine if the character should be able to get hit

        i_frames : int
            a counter of how many invincibility frames have passed

        screen_scroll : int
            indicates how much should every tile and object on the screen move by

        bg_scroll : int
            not implemented yet


    Methods
    -------
        __init__(x, y, game):
            constructs all the necessary attributes for the game class

        move(keys, world):
            repsonsible for moving the main character as well as managing the animation and screen movement

        update():
            applies gravity to the main character

        jump():
            gives the main character vertical velocity up which simulates jumping

        attack():
            displays the attack and progresses its animation

        wall_collision():
            checks collision with the borders of the screen, if the character is outside the screen, he dies

        collision(world):
            checks collision with every tile in the level

        check_dead():
            checks player's health and deletes the instance if the health is below zero

        invulnerability_update():
            increments the invincibility frame count and if it's larger than the invulnerability time,
            the main character is hittable again

    """

    def __init__(self, x, y, game):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        self.wall_collided = False
        self.air_jumps = 1

        # change the image_size and scale

        self.image_size = [64, 52]
        self.walking_sprites = SpriteSheet(pygame.image.load('assets/vandi/walk.png').convert_alpha())
        self.animation_steps = 9

        for i in range(self.animation_steps):
            img = self.walking_sprites.get_image(i, self.image_size, 2, (0, 0, 0)).convert_alpha()
            self.images_right.append(img)
            img_left = pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.game = game
        self.img = self.images_right[self.index]
        self.width = self.img.get_width()//2.5
        self.height = self.img.get_height()
        # self.rect = self.img.get_rect(center=(x, y))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.rect.center
        # self.rect = pygame.Rect(x, y, self.width // 4, self.height)

        self.on_ground = False
        self.velocity = [0, 0]
        self.direction = 0
        self.attackHitbox = AttackHitbox(self)

        self.health = 5
        self.invulnerable = False
        self.i_frames = 0

        self.screen_scroll = 0
        self.bg_scroll = 0

        self.last_update = 0
        self.not_press = True

    def move(self, keys, world):
        #movement part
        self.screen_scroll = 0
        self.velocity[0] = 0
        self.on_ground = False

        if keys[pygame.K_a]:
            self.velocity[0] = -5

        if keys[pygame.K_d]:
            self.velocity[0] = 5

        self.collision(world)
        self.update()
        self.rect.move_ip(self.velocity[0], 0)
        self.img_rect.move_ip(self.velocity[0], 0)

        #camera scroll part
        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
            self.rect.move_ip(-self.velocity[0], 0)
            self.img_rect.move_ip(-self.velocity[0], 0)
            self.screen_scroll = -self.velocity[0]

        #animation part
        self.counter += 1
        if self.counter > 5:
            self.counter = 0

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
                self.index = 0

            if self.direction == 0:
                self.img = self.images_right[self.index]
            elif self.direction == 1:
                self.img = self.images_left[self.index]

        return self.screen_scroll

    def update(self):
        if not self.on_ground:
            self.velocity[1] += game.gravity
        self.rect.move_ip(0, self.velocity[1])
        self.img_rect.move_ip(0, self.velocity[1])

    def jump(self):
        self.on_ground = False
        self.velocity[1] = -15

    def attack(self):
        delay = 500
        current_time = pygame.time.get_ticks()

        if self.last_update == 0:
            self.last_update = current_time

        if current_time - self.last_update > delay:
            if pygame.mouse.get_pressed()[0] and self.attackHitbox.index < (len(self.attackHitbox.images_right) - 1) and self.not_press == True:
                self.attackHitbox.active = True
                self.not_press = False
                self.last_update = current_time

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

        self.check_dead()

    def collision(self, world):
        self.wall_collided = False
        for tile in world.tile_list:
            collided = False
            jump_rect = pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.width, self.height))

            # vertical collision
            if rect_collision(tile.img_rect, jump_rect):
                if self.velocity[1] < 0:
                    self.velocity[1] = tile.img_rect.bottom - self.rect.top + 1
                elif self.velocity[1] > 0:
                    self.velocity[1] = tile.img_rect.top - self.rect.bottom - 1
                    self.air_jumps = 1
                collided=True

            #horizontal collision
            walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height)
            if rect_collision(tile.img_rect, walking_rect):
                self.velocity[0] = 0
                collided = True
                self.wall_collided = True

            #gravity stuff
            gravity_rect = pygame.Rect(self.rect.x, self.rect.y + self.velocity[1] + game.gravity, self.width, self.height)
            if rect_collision(tile.img_rect, gravity_rect):
                self.on_ground = True
                self.air_jumps = 1
                collided = True

            # check for end of level
            if 'finish' in tile.material and collided:
                self.game.level_count += 1
                print('load next level')

    def check_dead(self):
        dead = False
        if self.health <= 0:
            self.game.menu.death_screen_flag = True
            dead = True
        return dead

    def invulnerability_update(self):
        self.i_frames += 1
        if self.i_frames >= (INVULNERABILITY_TIME * FPS):
            self.invulnerable = False
            self.i_frames = 0


class AttackHitbox():
    """
    The class that controls the player's attack hitbox

    Parameters
    ----------
        index : int
            index of the hitbox's sprite image in the image list

        images_right : list[Surface]
            list of the hitbox sprites for when the attacker is going right

        images_left : list[Surface]
            list of the hitbox sprites for when attacker is going left

        active : bool
            determines whether the hitbox should be active or not

        attacker : Player
            player who initiated the attack

        last_update : int
            helps to enforce a cooldown on changing the attacks image

        image : Surface
            an instance of the surface class,
            the current sprite of the attack

        rect : Rect
            an instance of the rect class,
            this is a rectangle object that simulates the hitbox of the attack

    Methods
    -------
        __init__(attacker):
            constructs all the necessary attributes for the game class

        hit_collision():
            checks collision with enemies to determine if they are hit

        animation():
            manages the animation (image updating) and updates the location of the attack0

    """

    def __init__(self, attacker):
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(1, 7):
            img = pygame.image.load(f'assets/attack/attack{i}.png').convert_alpha()
            img = pygame.transform.rotate(img, -180)
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            self.images_right.append(img)
            img_left = pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.active = False
        self.attacker = attacker

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
                tile.health -= self.attacker.game.menu.inventory.weapon.damage
                tile.invulnerable = True
                print(tile.health)
                if tile.check_dead():
                    self.attacker.game.world.sharks.remove(tile)

            tile.invulnerability_update()

    def animation(self):
        delay = 100

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

class Text:
    def __init__(self, text, size, coordinates, colour=(255, 255, 255)):
        if '\n' in text:
            self.lines = text.split("\n")
        else:
            self.lines = None

        self.font = pygame.font.SysFont('Arial', size)
        self.text = self.font.render(text, True, colour)
        self.coordinates = coordinates
        self.text_rect = self.text.get_rect(center=self.coordinates)

    # def draw(self, surface):
    #     temp_surface = pygame.Surface(self.text.get_size())
    #     temp_surface.fill((192, 192, 192))
    #     temp_surface.blit(self.text, self.text_rect)
    #     surface.blit(temp_surface, (0, 0))

    def draw(self, surface):
        if self.lines!=None:
            x, y = self.coordinates[0], self.coordinates[1]
            line_height = self.font.get_height()

            for i, line in enumerate(self.lines):
                rendered_line = self.font.render(line, True, (255, 255, 255))
                surface.blit(rendered_line, (x, y + i * line_height))
        else:
            pos = (self.text_rect.x, self.text_rect.y)
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
        self.death_bg = pygame.image.load('assets/menu/death_screen.jpg')
        self.death_bg = pygame.transform.scale(self.death_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.death_bg_rect = self.death_bg.get_rect()

        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
        self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png', 0.2)
        self.save = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50, f'assets/menu/buttons/save.png', 0.2)
        self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/load.png', 0.2)
        self.exit = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 150, f'assets/menu/buttons/exit.png', 0.2)
        self.sounds_plus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 175,
                                  f'assets/menu/buttons/plus.png', 0.25)
        self.sounds_minus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 75,
                                   f'assets/menu/buttons/minus.png', 0.25)

        self.starting_menu_flag = True
        self.settings_flag = False
        self.death_screen_flag = False
        self.ending_screen_flag = False
        self.inventory_flag = False
        self.tooltip_flag = False
        self.pause = False
        self.saved = 0

        self.inventory = Inventory(27)
        self.inventory.add(Item('spear', 'assets/items/spear.png', 5))

        self.tooltip_surf = pygame.Surface((500,200), pygame.SRCALPHA).convert_alpha()
        self.tooltip_rect = self.tooltip_surf.get_rect()
        self.tooltip_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def start_menu(self):
        if self.settings_flag:
            self.settings_menu()

        else:
            self.buttons = [self.start, self.settings, self.load, self.exit]
            title = Text('The Myths Of Vandi', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

            self.game.screen.blit(self.start_bg, self.start_bg_rect)
            # self.game.screen.fill((0, 0, 0))
            title.draw(self.game.screen)
            for button in self.buttons:
                button.collision = True
                button.draw_and_collision(self.game.screen)

            if self.start.active:
                self.starting_menu_flag = False

            if self.settings.active:
                self.settings_flag = True

            if self.load.active:
                self.loading()

                self.starting_menu_flag = False

            if self.exit.active:
                self.game.running = False
                self.starting_menu_flag = False

            for button in self.buttons:
                button.collision=False

    def pause_menu(self):
        self.pause = True
        self.buttons = [self.start, self.settings, self.save, self.load, self.exit]
        paused = Text('Paused', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

        # self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        self.game.screen.fill((0, 0, 0))
        paused.draw(self.game.screen)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)

        if self.start.active and not self.settings_flag:
            self.pause = False

        if self.settings.active:
            self.settings_flag = True

        if self.settings_flag:
            self.settings_menu()

        if self.save.active:
            self.saving()

        if self.saved*FPS>0:
            text = Text('Saved Successfully', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 400))
            text.draw(self.game.screen)
            self.saved-=1

        if self.load.active:
            self.loading()

            self.pause = False

        if self.exit.active:
            self.game.running = False
            self.pause = False

        for button in self.buttons:
            button.collision = False

    def settings_menu(self):
        self.buttons = [self.start, self.sounds_plus, self.sounds_minus]
        settings = Text('Settings', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
        volume = Text(f'Volume: {int(self.game.volume * 100)}', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125))

        # self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        self.game.screen.fill((0, 0, 0))
        settings.draw(self.game.screen)
        volume.draw(self.game.screen)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)
            time.sleep(0.0228)

        if self.start.active:
            self.settings_flag = False
            time.sleep(0.1)

        if self.sounds_plus.active:
            if self.game.volume + 0.05 <= 1:
                self.game.volume += 0.05
            mixer.music.set_volume(self.game.volume)

        if self.sounds_minus.active:
            if self.game.volume - 0.05 >= 0:
                self.game.volume -= 0.05
            mixer.music.set_volume(self.game.volume)

        for button in self.buttons:
            button.collision = False
            button.active = False

    def death_screen(self):
        self.buttons = [self.settings, self.load, self.exit]
        title = Text('Failure', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

        self.game.screen.blit(self.death_bg, self.death_bg_rect)
        # self.game.screen.fill((0, 0, 0))
        title.draw(self.game.screen)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)

        if self.settings.active:
            self.settings_flag = True
        if self.settings_flag:
            self.settings_menu()

        if self.load.active:
            self.loading()

            self.death_screen_flag = False

        if self.exit.active:
            self.game.running = False
            self.death_screen_flag = False

        for button in self.buttons:
            button.collision = False

    def inventory_menu(self):
        self.game.screen.fill((0,0,0))
        self.inventory.draw(self.game.screen)

        mouse_pos = pygame.mouse.get_pos()
        count=0
        for item in self.inventory.slots:
            if item!=None:
                if point_collision(mouse_pos, item.rect) and pygame.mouse.get_pressed()[0]:
                    self.inventory.equip(count)

                if point_collision(mouse_pos, item.rect) and pygame.mouse.get_pressed()[2]:
                    self.inventory.drop(item)

                if point_collision(mouse_pos, item.rect):
                    self.tooltip_flag=True
                    self.tooltip_text = Text(item.details(), 50, ((SCREEN_WIDTH // 2-self.tooltip_rect.center[0], SCREEN_HEIGHT // 2-self.tooltip_rect.center[1])), (255,255,255))
                    break
                else:
                    self.tooltip_flag=False
            count += 1

        if self.tooltip_flag:
            self.tooltip_surf.fill((255,255,255,100))
            self.tooltip_text.draw(self.tooltip_surf)
            self.game.screen.blit(self.tooltip_surf, self.tooltip_rect)

    def ending_screen(self):
        text = Text('Thank you for playing', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game.screen.fill((0,0,0))
        text.draw(self.game.screen)

    def saving(self):
        item_list=[]
        for item in self.inventory.slots:
            if item != None:
                item_list.append({'name': item.name, 'img_path': item.img_path, 'damage': item.damage})
        write_json({'name': 'Vandi', 'level_count': self.game.level_count, 'inventory': item_list, 'weapon': {'name': self.inventory.weapon.name, 'img_path': self.inventory.weapon.img_path, 'damage': self.inventory.weapon.damage}}, 'vandi')
        self.saved=10

    def loading(self):
        for item in self.inventory.slots:
            self.inventory.drop(item)
        data = read_json('vandi')
        for dict in data['inventory']:
            self.inventory.add(Item(dict['name'], dict['img_path'], dict['damage']))
        self.inventory.weapon = Item(data['weapon']['name'], data['weapon']['img_path'], data['weapon']['damage'])
        self.game.level_count = data['level_count']
        self.game.level_count_check = 0

        if self.game.level_count != self.game.level_count_check:
            self.game.level_count_check = self.game.level_count
            self.game.level_load()


class Button:
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.active = False
        self.collision = False

    def draw_and_collision(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        mouse_pos = pygame.mouse.get_pos()

        self.active = False
        if point_collision(mouse_pos, self.rect) and self.collision:
            if pygame.mouse.get_pressed()[0] and not self.active:
                self.active = True

        return self.active

if __name__ == '__main__':
    game = Game()
    game.start_screen()