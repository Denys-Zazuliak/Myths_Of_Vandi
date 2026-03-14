import pytest
from levels import World

layouts=[['a1'],
         ['A0'],
         ['AAA'],
         ['A1']]

class TestWorld():
    # @pytest.fixture(scope='class')
    # def world(self):
    #     return World(layouts[0], None)

    def test_attributes(self):
        world=World(layouts[0], None)
        assert world.game == None
        assert world.data == ['a1']


if __name__ == '__main__':
    test=TestWorld()
    test.test_attributes()
