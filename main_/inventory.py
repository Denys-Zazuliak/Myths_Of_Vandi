import pygame
from utils import rect_collision

item_per_row = 9
slot_size = (64, 64)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

class Item:
    """
    The class to represent an item that can be held in the inventory.

    Attributes
    ----------
        name : str
            shows what type of weapon the item is

        img_path : str
            points to the sprite file in the directories,
            used when saving

        img : Surface
            an instance of the surface class,
            the model of the item

        rect : Rect
            an instance of the rect class,
            helps with displaying the item in the inventory and when dropped by the enemies

        damage : int
            determines how much damage this weapon deals if equipped

    Methods
    -------
        draw(screen, x, y):
            draws the item onto the given surface at the given coordinates

        details(): Str
            returns a formatted string with the item's name and damage value
    """

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


class Inventory:
    """
    The class to represent the player's inventory.

    Attributes
    ----------
        max_size : int
            maximum amount of items that can fit in the inventory

        rows : int
            how many rows the inventory has

        columns : int
            how many columns the inventory has

        slots : list[Item/None]
            represents each slot of the inventory

        slot_image : Surface
            an instance of the surface class,
            the image of each repeating slot in the inventory menu

        weapon : Item
            an instance of the item class,
            the currently equipped item by the player

    Methods
    -------
        add(item):
            adds an item to the first available empty slot

        drop(item):
            removes an item from its slot, setting that slot to None

        draw(screen):
            draws all inventory slots and their contained items onto the screen

        occupied(slot):
            checks if the given slot is holding an item

        is_full():
            check if the inventory is full

        equip(new_weapon_index):
            swaps the currently equipped weapon with the given item
    """

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