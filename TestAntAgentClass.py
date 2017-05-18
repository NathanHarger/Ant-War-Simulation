import unittest

class TestAntAgent(unittest.TestCase):
    
    #intial unit testing framework 
    def test_antCanMove(self):
        agent.position = 0
        agent.move(1,1)
        self.assertEqual(agent.position, (1,1))

    def test_antCanFight(self):
        agent1.fight = true; 
        agent2.fight = true;
        agent1.fighting(agent2.alwaysWin())
        self.assertTrue(agent1.isDead())
        self.assertFalse(agent1.isAlive())
        self.assertTrue(agent2.isAlive)

    def test_antCanEatandRaiseEnergyLevel(self):
        energyLevel = agent.getEnergyLevel()
        agent.drinkWater(1); 
        self.assertEqual(agent.getEnergyLevel(), energyLevel + someConstant)
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()