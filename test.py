import unittest
from Ant import *
from Desert import *
from viz import *



class TestAnt(unittest.TestCase):
    def test_ant_spawn_on_hill(self):
        TestDesert = Desert(10, 1)

        h = TestDesert.getHives()[0]
        test_ant = ANT(0,0,0,0,None,h,TestDesert)
        self.assertEqual(h.getLocation(), test_ant.getPos())

    def test_ant_eat_when_home(self):
        TestDesert = Desert(10, 1)
        h = TestDesert.getHives()[0]
        test_ant = ANT(0, 0, 0, 0, None, h, TestDesert)
        test_ant.set_food(0)

        vizTest = viz(10, 500, 500, 1)
        vizTest.Run_Sim(TestDesert)

        #vizTest.dispViz()


        self.assertGreater(test_ant.getFood(), 0)

    def test_ants_eat_on_food_grid(self):
        test_Desert = Desert(1,0)
        test_Desert.getItem(0,0).setState(State.FOOD)
        test_ant = ANT(0, 0, 0, 0, None, None, test_Desert)
        test_ant.set_food(0)

        vizTest = viz(10, 500, 500, 1)

        vizTest.Run_Sim(test_Desert)

        self.assertGreater(test_ant.getFood(), 0)

    def test_ants_stay_in_bounds(self):
        TestDesert = Desert(1, 1)
        h = TestDesert.getHives()[0]
        test_ant = ANT(0, 0, 0, 0, None, h, TestDesert)
        test_ant.set_food(0)

        vizTest = viz(1, 500, 500, 1)
        vizTest.Run_Sim(TestDesert)

        test_ant.__test_move__(-100,-100)
        # vizTest.dispViz()

        print TestDesert
        self.assertEquals(test_ant.getX(), 0)

class TestHive(unittest.TestCase):

    def test_food_not_negative(self):
        TestDesert = Desert(1, 1)
        h = TestDesert.getHives()[0]

        for i in range(10):
            ANT(0, 0, 0, 0, None, h, TestDesert).set_food(0)

        vizTest = viz(1, 500, 500, 1)
        vizTest.Run_Sim(TestDesert)
        h.setFoodLevel(0)
        # vizTest.dispViz()


        self.assertEquals(h.getFoodLevel(), 0)


if __name__ == '__main__':
    unittest.main()