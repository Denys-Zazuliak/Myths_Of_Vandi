import pytest
from levels import World

layouts=[['a1'],
         ['A0'],
         ['AAA'],
         ['B1']]

class TestWorld:
    @pytest.fixture(scope='class')
    def world1(self):
        return World(layouts[0], None)

    @pytest.fixture(scope='class')
    def world2(self):
        return World(layouts[1], None)

    @pytest.fixture(scope='class')
    def world3(self):
        return World(layouts[2], None)

    @pytest.fixture(scope='class')
    def world4(self):
        return World(layouts[3], None)

    def test_attributes(self, world1):
        assert world1.game is None
        assert world1.data == ['a1']

    def test_level_creation(self, world1, world4):
        world1.load_level()
        world4.load_level()
        assert len(world1.tile_list) == 0
        assert len(world1.tile_list) > 0


if __name__ == '__main__':
    test=TestWorld()
