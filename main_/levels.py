import pygame
from random import randint
from inventory import Item
from utils import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
TILE_SIZE = 64
SCROLL_THRESH = SCREEN_WIDTH//4
FPS = 60
INVULNERABILITY_TIME = 0.5

level_dict={
    3: {'layout':[
        ['M65'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A63', 'M1'],
        ['M1', 'A14', 'M2', 'A2', 'M1', 'A2', 'M2', 'A9', 'M3', 'A13', 'M1', 'A9', 'S1', 'A4', 'M1'],
        ['M8', 'A3', 'M3', 'A16', 'M1', 'A16', 'M1', 'A10', 'M2', 'A4', 'M1'],
        ['M9', 'A20', 'M2', 'A13', 'M2', 'A18', 'M1'],
        ['M10', 'A18', 'M3', 'A7', 'S1', 'A3', 'M1', 'A15', 'G1', 'A2', 'S1', 'P1', 'A1', 'M1'],
        ['M17', 'A7', 'M41']
        ],
        'bg': 'assets/menu/what_the_hell_am_i_doing.png'
    },

    2: {'layout':[
        ['R20'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A9', 'S1', 'A8', 'R1'],
        ['R1', 'A9', 'R1', 'A8', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R1', 'A18', 'R1'],
        ['R5', 'A13', 'S1', 'R1'],
        ['A20'],
        ['A20'],
        ['A8', 'S1', 'A20', 'P1'],
        ['A3', 'R61'],
        ],
        'bg': 'assets/menu/bg_sky.png'
    },

    1: {'layout':[
        ['A64'],
        ['A64'],
        ['A64'],
        ['A64'],
        ['A64'],
        ['A64'],
        ['A10','F1','A53'],
        ['A10', 'D1', 'A53'],
        ['A64'],
        ['A64'],
        ['D5', 'A13', 'F1', 'D1'],
        ['A16', 'D4'],
        ['A15', 'D5'],
        ['A8', 'F1', 'A5', 'P1', 'D5'],
        ['A3', 'D17'],
        ],
        'bg': 'assets/menu/background_layer_1.png'
    }
}

def load_levels(level_count, game):
    """
    Loads the layout, background and world of the current level.

    Parameters
    ----------
    level_count : int
        the current level number
    game : Game
        an instance of the game class,
        gives access to the main game class attributes such as menu and items

    Returns
    -------
    world : World
        an instance of the world class,
        responsible for transformation of the level layout into a usable list of tiles

    level : list[Tile]
        a list of all tiles in the level

    bg : Surface
        an instance of the surface class,
        contains the background of the level
    """

    bg = None
    world = None
    level = None

    if level_count not in level_dict.keys():
        game.menu.ending_screen_flag = True
    else:
        layout = level_dict[level_count]['layout']
        bg = pygame.image.load(level_dict[level_count]['bg']).convert_alpha()
        world = World(layout, game)
        game.items = []
        level = world.load_level()

    return world, level, bg

class World:
    """
    Responsible for transformation of the level layout into a usable list of tiles

    Attributes
    ----------
        tile_list : list[Tile]
            contains every single tile in the level

        data : list[list[str]]
            the raw layout data used to construct the level

        game : Game
            an instance of the game class,
            gives access to the main game class attributes

        block : Surface
            an instance of the surface class,
            the image used to represent a block tile

        metal : Surface
            an instance of the surface class,
            the image used to represent a metal tile

        portal : Surface
            an instance of the surface class,
            the image used to represent a portal tile

        enemies : Group
            an instance of the sprite group class,
            contains every enemy in the level

        tile_count : int
            keeps track of the current tile's horizontal position when loading the level

        row_count : int
            keeps track of the current row's vertical position when loading the level

    Methods
    -------
        __init__(data, parent_class):
            constructs all the necessary attributes for the world class

        load_level():
            iterates through the layout data and creates tiles and enemies,
            returns a list of all tiles in the level

        tile_load(image, material):
            creates a tile at the current position and appends it to tile_list
    """

    def __init__(self, data, parent_class):
        self.tile_list=[]
        self.data = data
        self.game = parent_class

        self.block = pygame.image.load(f'assets/blocks/brick.png')
        self.dirt = pygame.image.load(f'assets/blocks/dirt.png')
        self.metal = pygame.image.load(f'assets/blocks/metal.png')
        self.rock = pygame.image.load(f'assets/blocks/rock.png')
        self.portal = pygame.image.load(f'assets/blocks/portal.png')
        self.enemies=pygame.sprite.Group()

        self.tile_count=0
        self.row_count=0

    def load_level(self):
        self.row_count=0
        for row in self.data:
            self.tile_count=0
            for tile in row:
                if tile[0]=='A':
                    if tile[1:].isdigit():
                        self.tile_count+=int(tile[1:])

                if tile[0]=='B':
                    if tile[1:].isdigit():
                        for i in range(int(tile[1:])):
                            self.tile_load(self.block, 'block')

                if tile[0]=='D':
                    if tile[1:].isdigit():
                        for i in range(int(tile[1:])):
                            self.tile_load(self.dirt, 'dirt')

                if tile[0]=='R':
                    if tile[1:].isdigit():
                        for i in range(int(tile[1:])):
                            self.tile_load(self.rock, 'rock')

                if tile[0]=='M':
                    if tile[1:].isdigit():
                        for i in range(int(tile[1:])):
                            self.tile_load(self.metal, 'metal')

                if tile[0]=='S':
                    if tile[1:].isdigit():
                        for i in range(int(tile[1:])):
                            shark=Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count) - 1, 'shark', 2, self.game, 3, 1)
                            self.enemies.add(shark)

                    self.tile_count += 1

                if tile[0]=='G':
                    goblin = Boss(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count) - 1, 'goblin', 2, self.game, 5, 2, f'assets/enemy/goblin_walk.png', (35, 37))
                    self.enemies.add(goblin)

                    self.tile_count += 1

                if tile[0]=='F':
                    fox = Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count) - 1, 'fox', 2, self.game, 2, 1, f'assets/enemy/fox_walk.png', (32,22))
                    self.enemies.add(fox)

                    self.tile_count += 1

                if tile[0]=='P':
                    for i in range(int(tile[1:])):
                        self.tile_load(self.portal, 'portal')

                else:
                    pass

            self.row_count+=1

        return self.tile_list

    def tile_load(self, image, material):
        x = TILE_SIZE * self.tile_count
        y = TILE_SIZE * self.row_count

        tile = Tile(image, x, y, material)
        self.tile_list.append(tile)

        self.tile_count += 1


class Tile:
    '''
    A helping class which makes it easier to identify what kind of tile it is and its position

    Attributes
    ----------
    img: Surface
        an instance of the surface class,
        indicates what to draw to represent this tile

    img_rect: Rect
        an instance of the rect class,
        helps with positioning the tile on the screen

    material: Str
        helps identify what tile it is
    '''

    def __init__(self, image, x, y, material):
        self.img = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.img = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.material = material


class Enemy(pygame.sprite.Sprite):
    """
    The class to represent an enemy character in the game.

    Attributes
    ----------
        name : str
            contains the type of the enemy

        images_right : list[Surface]
            list of enemy sprites for when they are going right

        images_left : list[Surface]
            list of enemy sprites for when they are going left

        index : int
            index of the enemy's sprite in the list

        counter : int
            helps to keep track of how often to update the sprite image

        image_size : list[int]
            the size of the sprite image as it is in the spritesheet (in pixels)

        walking_sprites : SpriteSheet
            an instance of the spritesheet class,
            stores the image of the enemy's sprites

        animation_steps : int
            tells how many different sprites are in the spritesheet

        game : Game
            an instance of the game class,
            gives access to the main game class attributes

        image : Surface
            an instance of the surface class,
            the current sprite of the enemy

        rect : Rect
            an instance of the rect class,
            this is a rectangle object that simulates the hitbox of an enemy

        velocity : list[int]
            stores both components of the enemy's velocity (in pixels)

        distance_tracker : int
            tracks distance walked in one direction

        direction : int
            shows which way the enemy is looking (1 means to the right, -1 means to the left)

        tracking : bool
            shows if the enemy is currently chasing the player

        health : int
            enemy's HP

        invulnerable : bool
            helps determine if the enemy should be able to get hit

        i_frames : int
            a counter of how many invincibility frames have passed

        damage : int
            how much damage does the enemy's hit deals

    Methods
    -------
        __init__(x, y, name, size_scale, game, health, damage, spritesheet):
            constructs all the necessary attributes for the enemy class

        update():
            moves the enemy back and forth and updates its animation

        check_dead():
            checks the enemy's health and triggers item drops if health is below zero,
            returns True if the enemy is dead

        item_drops():
            randomly selects and spawns an item drop at the enemy's position on death

        invulnerability_update():
            increments the invincibility frame count and resets invulnerability when expired

        attack():
            checks if the player is within the vision box and chases them,
            deals damage to the player on contact

        collision(world):
            checks collision with every tile in the level and applies gravity
    """

    def __init__(self, x, y, name, size_scale, game, health, damage, spritesheet=None, size=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        if spritesheet!=None:
            self.image_size = size
            self.walking_sprites = SpriteSheet(pygame.image.load(spritesheet).convert_alpha())
            self.animation_steps = 6

            for i in range(self.animation_steps):
                img = self.walking_sprites.get_image(i, self.image_size, size_scale, (0, 0, 0)).convert_alpha()
                self.images_right.append(img)
                img_left = pygame.transform.flip(img, True, False)
                self.images_left.append(img_left)

        else:
            for i in range(1, 3):
                img = pygame.image.load(f'assets/enemy/idle/{self.name}{i}.png').convert_alpha()
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

        self.health=health
        self.damage=damage
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
            self.item_drops()
            del self
            dead=True

        return dead

    def item_drops(self):
        if randint(1, 100) >= 50:
            if randint(1, 100) >= 95:
                drop = Item('spear', 'assets/items/spear.png', 3)
                drop.rect.center = self.rect.center
                self.game.items.append(drop)
            elif randint(1, 100) >= 85 and self.name == 'goblin':
                drop = Item('flamberge', 'assets/items/flamberge.png', 3)
                drop.rect.center = self.rect.center
                self.game.items.append(drop)
            elif randint(1, 100) >= 75:
                drop = Item('rapier', 'assets/items/rapier.png', 2)
                drop.rect.center = self.rect.center
                self.game.items.append(drop)
            elif randint(1, 100) >= 65:
                drop = Item('executioner’s sword', 'assets/items/executioner’s sword.png', 2)
                drop.rect.center = self.rect.center
                self.game.items.append(drop)
            else:
                drop = Item('stick', 'assets/items/stick.png', 1)
                drop.rect.center = self.rect.center
                self.game.items.append(drop)

    def invulnerability_update(self):
        self.i_frames += 1
        if self.i_frames >= (INVULNERABILITY_TIME * FPS):
            self.invulnerable=False
            self.i_frames = 0

    def attack(self):
        width=TILE_SIZE*6
        height=TILE_SIZE*3

        y=self.rect.y - height // 2
        if self.direction > 0:
            x=self.rect.midleft[0]
            self.velocity[0]=abs(self.velocity[0])
        else:
            x=self.rect.midright[0]-width
            self.velocity[0]=abs(self.velocity[0])*-1

        vision_box = pygame.Rect(x, y, width, height)
        vision_box_surface = pygame.Surface((width, height)).convert_alpha()
        vision_box_surface.fill((250, 50, 50, 200))

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

            self.rect.move_ip(self.velocity[0], 0)
        else:
            self.tracking=False

        if not self.game.vandi.invulnerable and rect_collision(self.game.vandi.rect, self.rect):
            self.game.vandi.health -= self.damage
            self.game.vandi.invulnerable = True
            if self.game.vandi.check_dead():
                self.game.menu.death_screen_flag = True
                self.game.misc_channel.play(pygame.mixer.Sound('assets/audio/game_over.mp3'))

        self.game.vandi.invulnerability_update()

    def collision(self, world):
        on_ground = False
        for tile in world.tile_list:
            # vertical collision
            gravity_rect = pygame.Rect((self.rect.x, self.rect.y + self.velocity[1]), (self.rect.width, self.rect.height))
            if rect_collision(tile.img_rect, gravity_rect):
                if self.velocity[1] >= 0:
                    if tile.img_rect.top >= self.rect.centery:
                        self.velocity[1] = tile.img_rect.top - self.rect.bottom - 1
                        on_ground = True

            # horizontal collision
            walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)
            if rect_collision(tile.img_rect, walking_rect):
                self.velocity[0] *= -1

        self.rect.move_ip(self.velocity)

        if not on_ground:
            self.velocity[1] += self.game.gravity
        else:
            self.velocity[1] = 0


class Boss(Enemy):
    def __init__(self, x, y, name, size_scale, game, health, damage, spritesheet, size):
        super().__init__(x, y, name, size_scale, game, health, damage, spritesheet, size)

    def update(self):
        self.distance_tracker += self.velocity[0]

        if abs(self.distance_tracker) >= 128:
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
