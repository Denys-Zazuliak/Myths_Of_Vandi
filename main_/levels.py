import pygame

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE = 64 #50
SCROLL_THRESH = SCREEN_WIDTH//4
FPS = 60
INVULNERABILITY_TIME = 0.5

LAYOUT1 = [
    ['B20'],
    ['B1', 'A17', 'M1', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B1', 'A9','S1','A8', 'B1'],
    # ['B1', 'A18', 'B1'],
    ['B1', 'A9', 'B1', 'A8', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B1', 'A18', 'B1'],
    ['B5', 'A13', 'S1', 'B1'],
    ['A16', 'B4'],
    ['A15', 'B5'],
    ['A8', 'S1', 'A5', 'F1', 'B5'],
    ['A3', 'B17'],
]

LAYOUT2 = [
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
    ['A8', 'S1', 'A20', 'F1'],
    ['A3', 'B200'],
]

# TUTORIAL LEVEL
LAYOUT3= [
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
    ['M9', 'A20', 'M2', 'A13', 'M2', 'A16', 'F1', 'A1', 'M1'],
    ['M10', 'A18', 'M3', 'A7', 'S1', 'A3', 'M1', 'A15', 'S1', 'A2', 'S1', 'F1', 'A1', 'M1'],
    ['M17', 'A4', 'M44']
]











#https://www.spritefusion.com/editor
# to preview levels











def load_levels(level_count, game):
    if level_count == 1:
        world = World(LAYOUT1, game)
        level = world.load_level()

    elif level_count == 2:
        world = World(LAYOUT2, game)
        level = world.load_level()

    elif level_count == 3:
        world = World(LAYOUT3, game)
        level = world.load_level()

    return world, level

def tile_load(self, image, material):
    x = TILE_SIZE * self.tile_count
    y = TILE_SIZE * self.row_count

    tile = Tile(image, x, y, material)
    self.tile_list.append(tile)

    self.tile_count = self.tile_count + 1

def rect_collision(rect1, rect2):
    if rect1.right>=rect2.left and rect1.left<=rect2.right and rect1.bottom>=rect2.top and rect1.top<=rect2.bottom:
        colliding=True
    else:
        colliding=False

    return colliding

class World:
    def __init__(self, data, parent_class):
        self.tile_list=[]
        self.data = data
        self.game=parent_class

        self.block=pygame.image.load(f'assets/blocks/block.jpg')
        self.metal=pygame.image.load(f'assets/blocks/metal.png')
        self.finish = pygame.image.load(f'assets/blocks/metal.png')
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
                        tile_load(self, self.block, 'block')

                if tile[0]=='M':
                    for i in range(int(tile[1:])):
                        tile_load(self, self.metal, 'metal')

                if tile[0]=='S':
                    # (TILE_SIZE * self.row_count - ((TILE_SIZE * (self.row_count)) - (TILE_SIZE * (self.row_count + 1))))
                    shark=Enemy(TILE_SIZE * self.tile_count, (TILE_SIZE * self.row_count), 'shark', 2, self.game)
                    self.sharks.add(shark)

                    self.tile_count += 1

                if tile[0]=='F':
                    for i in range(int(tile[1:])):
                        tile_load(self, self.finish, 'finish')

            self.row_count+=1

        return self.tile_list

    def draw(self, screen):
        pass

class Tile:
    def __init__(self, image, x, y, material):
        self.img = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.img = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.material = material

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
        self.game.screen.blit(vision_box_surface, vision_box)

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
            if rect_collision(tile.img_rect, gravity_rect):
                if self.velocity[1] > 0:
                    self.velocity[1] = tile.img_rect.top - self.rect.bottom - 1

            # horizontal collision
            walking_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)
            if rect_collision(tile.img_rect, walking_rect):
                self.velocity[0] *= -1

        self.rect.move_ip(self.velocity)
        self.velocity[1] += self.game.gravity
