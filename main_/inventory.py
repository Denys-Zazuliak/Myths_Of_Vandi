import pygame
from utils import rect_collision

item_per_row = 9
slot_size = (64, 64)
SCREEN_WIDTH = 1280  #1600
SCREEN_HEIGHT = 960  #900

class Item:
    def __init__(self, name, img, damage):
        self.name = name
        self.img_path = img
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, slot_size)
        self.rect = self.img.get_rect()
        self.damage=damage

    def draw(self, screen, x, y):
        screen.blit(self.img, (x, y))

    def details(self):
        return f"""Name: {self.name}\nDamage: {self.damage}"""

    # def collision(self, world):
    #     for tile in world.tile_list:
    #         # vertical collision
    #         gravity_rect = pygame.Rect((self.rect.x, self.rect.y + world.game.gravity), (self.rect.width, self.rect.height))
    #         if not rect_collision(tile.img_rect, gravity_rect):
    #             self.rect.y += world.game.gravity

class Inventory:
    def __init__(self, max_size, slots=None):
        if slots is None:
            slots=[]

        self.max_size = max_size
        self.rows=self.max_size//item_per_row
        self.columns=item_per_row

        self.slots = slots
        if len(self.slots) == 0:
            for i in range(self.max_size):
                self.slots.append(None)

        self.slot_image = pygame.image.load('assets/menu/slot_image.png').convert_alpha()
        self.slot_image = pygame.transform.scale(self.slot_image, slot_size)

        self.weapon=Item('spear', 'assets/items/spear.png', 1)

    def add(self, item):
        free = False
        index = 0

        while free == False:
            if not self.is_full():
                if not self.occupied(self.slots[index]):
                    free = True
                    self.slots[index] = item
                else:
                    index += 1
                    if index >= len(self.slots):
                        index = 0
            else:
                print('inventory full')
                break

    def drop(self, item):
        for i in range(len(self.slots)):
            if self.slots[i] == item:
                self.slots[i] = None
                break

    def draw(self, screen):
        row=0
        column=0

        for slot in self.slots:
            column += 1

            x=SCREEN_WIDTH - column*slot_size[0]
            y=row*slot_size[1]

            screen.blit(self.slot_image, (x, y))

            if self.occupied(slot):
                screen.blit(slot.img, (x, y))
                slot.rect.topleft=(x,y)

            if column>=item_per_row:
                row+=1
                column=0

    def occupied(self, slot):
        if slot != None:
            occupied = True
        else:
            occupied = False

        return occupied

    def is_full(self):
        count = 0

        for slot in self.slots:
            if slot != None:
                count += 1

        if count == self.max_size:
            full = True
        else:
            full = False

        return full

    def equip(self, new_weapon_index):
        temp=self.slots[new_weapon_index]
        self.slots[new_weapon_index] = self.weapon
        self.weapon = temp