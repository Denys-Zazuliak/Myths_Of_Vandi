import pytest
from main_.inventory import Inventory, Item

class TestInventory:
    @pytest.fixture(scope='class')
    def inventory(self):
        return Inventory(10)

    @pytest.fixture(scope='class')
    def item(self):
        return Item('flamberge', 'main_/assets/items/flamberge.png', 3)

    def test_add(self, inventory, item):
        inventory.add(item)
        assert inventory.slots[0] == item

    def test_drop(self, inventory, item):
        inventory.add(item)
        inventory.drop(item)
        assert inventory.slots[0] is None

    def test_occupied(self, inventory, item):
        inventory.add(item)
        assert inventory.occupied(inventory.slots[0]) == True
        inventory.drop(item)
        assert inventory.occupied(inventory.slots[0]) == False

    def test_is_full(self, inventory, item):
        for i in range(inventory.max_size):
            inventory.add(item)
        assert inventory.is_full() == True
        inventory.drop(item)
        assert inventory.is_full() == False

    def test_equip(self, inventory, item):
        old_weapon=inventory.weapon
        inventory.add(item)
        inventory.equip(0)
        assert inventory.weapon == item
        inventory.equip(0)
        assert inventory.weapon == old_weapon

if __name__ == '__main__':
    test=TestInventory()
