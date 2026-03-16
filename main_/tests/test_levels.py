import pytest
from main_.levels import World

layouts=[[['a1']],
         [['Z0']],
         [['AAA']],
         [['B1']]]

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
        assert world1.data == [['a1']]

    def test_level_creation(self, world1, world2, world3, world4):
        world1.load_level()
        world2.load_level()
        world3.load_level()
        world4.load_level()
        assert len(world1.tile_list) == 0
        assert len(world2.tile_list) == 0
        assert len(world3.tile_list) == 0
        assert len(world4.tile_list) > 0
        assert world4.row_count == 1 or world4.tile_count != 1

    def test_tile_creation(self, world1, world4):
        world1.tile_load(world1.block, 'block')
        world1.tile_load(world1.metal, 'metal')
        world1.tile_load(world1.finish, 'finish')
        assert world1.tile_list[0].material == 'block'
        assert world1.tile_list[1].material == 'metal'
        assert world1.tile_list[2].material == 'finish'


if __name__ == '__main__':
    test=TestWorld()
