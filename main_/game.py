#AMONGUS

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
import json
import time
from pygame import mixer
from levels import load_levels

SCREEN_WIDTH = 1280  #1600
SCREEN_HEIGHT = 960  #900
TILE_SIZE = 64  #50
SCROLL_THRESH = SCREEN_WIDTH // 4
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
        self.running = True
        self.volume = 0.2
        self.gravity = 0.75
        self.level_count = 1
        self.level_count_check = 0
        self.screen_scroll = 0
        self.world = None
        self.vandi = None
        self.level = None

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
                if event.key == pygame.K_ESCAPE:
                    self.menu.pause = True

        keys = pygame.key.get_pressed()

        return keys

    def update(self, keys):
        self.screen_scroll = self.vandi.move(keys, self.world)

        if keys[pygame.K_SPACE] and self.vandi.on_ground:
            self.vandi.jump()

        self.vandi.wall_collision()
        self.vandi.attack()

        for enemy in self.world.sharks:
            enemy.attack()
            if not enemy.tracking:
                enemy.update()
            enemy.collision(self.world)

    def draw(self):
        self.screen.fill((50, 50, 50))

        if self.level_count != self.level_count_check:
            self.level_count_check = self.level_count
            self.level_load()

        #draw the updated tiles and enemies
        for shark in self.world.sharks:
            shark.rect.x += self.screen_scroll
        self.world.sharks.draw(self.screen)

        for tile in self.level:
            tile.img_rect.x = tile.img_rect.x + self.screen_scroll
            self.screen.blit(tile.img, tile.img_rect)

        self.screen.blit(self.vandi.img, self.vandi.rect)

        self.draw_text(f'Health: {self.vandi.health}', (100, 20))

    # def draw_grid(self):
    #     for line in range(0, 80):
    #         pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
    #         pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

    def draw_text(self, text, coordinates):
        text = Text(text, 50, coordinates)
        text.draw(self.screen)

    def level_load(self):
        self.world, self.level = load_levels(self.level_count, self)
        self.vandi = Player(TILE_SIZE * 6, TILE_SIZE * 9, self)

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

        # change the image_size and scale

        self.image_size = [64, 54]
        self.walking_sprites = SpriteSheet(pygame.image.load('assets/vandi/walk.png').convert_alpha())
        self.animation_steps = 9

        for i in range(self.animation_steps):
            img = self.walking_sprites.get_image(i, self.image_size, 2, (0, 0, 0)).convert_alpha()
            self.images_right.append(img)
            img_left = pygame.transform.flip(img, True, False)
            self.images_left.append(img_left)

        self.game = game
        self.img = self.images_right[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = self.img.get_rect(center=(x, y))
        # self.rect=pygame.Rect((x, y), (self.width//2, self.height))

        self.on_ground = False
        self.velocity = [0, 0]
        self.direction = 0
        self.attackHitbox = AttackHitbox(self)

        self.health = 5
        self.invulnerable = False
        self.i_frames = 0

        self.screen_scroll = 0
        self.bg_scroll = 0

    def move(self, keys, world):
        #movement
        self.screen_scroll = 0
        self.velocity[0] = 0
        self.on_ground = False

        if keys[pygame.K_a]:
            self.velocity[0] = -5

        if keys[pygame.K_d]:
            self.velocity[0] = 5

        self.collision(world)
        # self.wall_collisions()
        self.update()
        self.rect.move_ip(self.velocity[0], 0)

        #camera scroll
        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
            self.rect.move_ip(-self.velocity[0], 0)
            self.screen_scroll = -self.velocity[0]

        #animation
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

    def jump(self):
        self.on_ground = False
        self.velocity[1] = -15

    def attack(self):
        if pygame.mouse.get_pressed()[0] and self.attackHitbox.index < (len(self.attackHitbox.images_right) - 1):
            self.attackHitbox.active = True

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
            jump_rect = pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.width, self.height))

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
            walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.width, self.height)
            if rect_collision(tile.img_rect, walking_rect):
                self.velocity[0] = 0

            #gravity stuff
            gravity_rect = pygame.Rect(self.rect.x, self.rect.y + self.velocity[1] + game.gravity, self.width,
                                       self.height)
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
            img = pygame.transform.rotate(img, -150)
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
                tile.health -= 1
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


class SpriteSheet:
    """
    A class to represent spritesheet images for enemies and the player

    Parameters
    ----------
        image: Surface
            an instance of the surface class,
            an image that contains all the models for the character

    Methods
    -------
        __init__(image):
            constructs all the necessary attributes for the game class

        get_image(frame_count, size, scale, colour):
            outputs a formatted image from the spritesheet based on the inputs

    """
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_count, size, scale, colour):
        img = pygame.Surface((size[0], size[1])).convert_alpha()
        img.blit(self.sheet, (0, 0), (frame_count * size[0], 0, size[0], size[1]))
        img = pygame.transform.scale(img, (size[0] * scale, size[1] * scale))
        img.set_colorkey(colour)

        return img


class Text:
    def __init__(self, text, size, coordinates, colour=(255, 255, 255)):
        self.font = pygame.font.SysFont('Arial', size)
        self.text = self.font.render(text, True, colour)
        self.text_rect = self.text.get_rect(center=coordinates)

    # def draw(self, surface):
    #     temp_surface = pygame.Surface(self.text.get_size())
    #     temp_surface.fill((192, 192, 192))
    #     temp_surface.blit(self.text, self.text_rect)
    #     surface.blit(temp_surface, (0, 0))

    def draw(self, surface):
        pos = self.text_rect.x, self.text_rect.y
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

        self.starting_menu_flag = True
        self.settings_flag = False
        self.inventory = False
        self.pause = False

    def start_menu(self):
        if self.settings_flag:
            self.settings_menu()

        else:
            self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
            self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png',
                                   0.2)
            self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/load.png', 0.2)
            self.exit = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 150, f'assets/menu/buttons/exit.png', 0.2)
            self.buttons = [self.start, self.settings, self.load, self.exit]
            title = Text('The Myths Of Vandi', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

            self.game.screen.blit(self.start_bg, self.start_bg_rect)
            # self.game.screen.fill((0, 0, 0))
            title.draw(self.game.screen)
            for button in self.buttons:
                button.draw_and_collision(self.game.screen)

            if self.start.active:
                for button in self.buttons:
                    del button

                self.starting_menu_flag = False

            if self.settings.active:
                for button in self.buttons:
                    del button

                self.settings_flag = True

            if self.load.active:
                for button in self.buttons:
                    del button

                self.loading()

                self.starting_menu_flag = False

            if self.exit.active:
                self.game.running = False
                self.starting_menu_flag = False

    def pause_menu(self):
        self.pause = True
        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
        self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png', 0.2)
        self.save = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50, f'assets/menu/buttons/save.png', 0.2)
        self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/load.png', 0.2)
        self.exit = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 150, f'assets/menu/buttons/exit.png', 0.2)
        self.buttons = [self.start, self.settings, self.save, self.load, self.exit]
        paused = Text('Paused', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

        self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        # self.game.screen.fill((0, 0, 0))
        paused.draw(self.game.screen)
        for button in self.buttons:
            button.draw_and_collision(self.game.screen)

        if self.start.active:
            for button in self.buttons:
                del button

            self.pause = False

        if self.settings.active:
            for button in self.buttons:
                del button

            self.settings_flag = True

        if self.settings_flag:
            self.settings_menu()

        if self.save.active:
            self.saving()

        if self.load.active:
            for button in self.buttons:
                del button

            self.loading()

            self.pause = False

        if self.exit.active:
            self.game.running = False
            self.pause = False

    def settings_menu(self):
        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 0.2)
        self.sounds_plus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 175,
                                  f'assets/menu/buttons/plus.png', 0.25)
        self.sounds_minus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 75,
                                   f'assets/menu/buttons/minus.png', 0.25)
        self.buttons = [self.start, self.sounds_plus, self.sounds_minus]
        settings = Text('Settings', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
        volume = Text(f'Volume: {int(self.game.volume * 100)}', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125))

        self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        # self.game.screen.fill((0, 0, 0))
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
            self.game.volume += 0.1
            mixer.music.set_volume(self.game.volume)

        if self.sounds_minus.active:
            self.game.volume -= 0.1
            mixer.music.set_volume(self.game.volume)

    def inventory(self):
        pass

    def saving(self):
        write_json({'name': 'Vandi', 'level_count': self.game.level_count}, 'vandi')

    def loading(self):
        data = read_json('vandi')
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
    if rect1.right >= rect2.left and rect1.left <= rect2.right and rect1.bottom >= rect2.top and rect1.top <= rect2.bottom:
        colliding = True
    else:
        colliding = False

    return colliding


def point_collision(point_pos, rect):
    if point_pos[0] >= rect.left and point_pos[0] <= rect.right and point_pos[1] >= rect.top and point_pos[
        1] <= rect.bottom:
        colliding = True
    else:
        colliding = False
    return colliding


def read_json(file):
    file = file + ".json"
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def write_json(data, file='Save'):
    file = file + '.json'
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(", ", " : "), sort_keys=True)
    return file


if __name__ == '__main__':
    game = Game()
    game.start_screen()



