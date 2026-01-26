class Item:
    def __init__(self, name):#, img):
        self.name = name
        self.img = None


class Inventory:
    def __init__(self, max_size, slots=[]):
        self.max_size = max_size

        self.slots = slots
        if len(self.slots) == 0:
            for i in range(self.max_size):
                self.slots.append(None)

    def add(self, item):
        free = False
        index = 0

        if not self.is_full():
            while free == False:
                if self.occupied(self.slots[index]):
                    free = True
                else:
                    index += 1

            self.slots[index] = item

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

        if count == 0:
            full = True
        else:
            full = False

        return full


a = Item('spear')
b = Item('sword')

c = Inventory(10)

c.add(a)
c.add(b)
