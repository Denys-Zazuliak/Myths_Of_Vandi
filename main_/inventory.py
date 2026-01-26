import pygame

item_per_row = 9
slot_size = (64, 64)
SCREEN_WIDTH = 1280  #1600
SCREEN_HEIGHT = 960  #900

class Item:
    def __init__(self, name, img):
        self.name = name
        self.img = None


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

        self.slot_image=pygame.image.load('assets/menu/slot_image.png').convert_alpha()
        self.slot_image = pygame.transform.scale(self.slot_image, slot_size)

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
            else:
                print('inventory full')

    def remove(self, item):
        for slot in self.slots:
            if slot == item:
                slot = None

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

    def draw(self, screen):
        row=0
        column=0

        for slot in self.slots:
            x=SCREEN_WIDTH - column*slot_size[0]
            y=row*slot_size[1]

            screen.blit(self.slot_image, (x, y))

            if self.occupied(slot):
                img=pygame.image.load(slot.img).convert_alpha()
                screen.blit(img, (x, y))

            if column>=item_per_row:
                row+=1
                column=0
            column+=1

#
# a = Item('spear', 'assets/blocks/metal.png')
# b = Item('sword', 'assets/blocks/block.png')
#
# c = Inventory(10)
#
# c.add(a)
# c.add(b)
