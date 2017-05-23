import numpy as n
from DesertAgent import DesertAgent, State
from Ant import ANT
from HiveClass import Hive


class Arena:
        
    def __init__(self, list_hives):
        self.list_hives = list_hives 
        self.cell = DesertAgent(0, 0, 0, (0,0))
    
    # will run a combat test for a list of hives in a single cell. 
    # Only ants in cell 0,0 will fight.
    def run_arena_test(self):
        print("Welcome to the Arena!")
        self.print_num_combatants()  
        print("Let the games begin!\n")
        
        self.cell.runCombat(self)
        
        print("....\n")
        print("The battle is over!")
        self.print_num_combatants()
        
        print("Kill Counts:")
        
        for i in range(len(self.list_hives)):
            print("Hive " + str(i) + ": " + str(self.list_hives[i].kill_count))
            
        
    def print_num_combatants(self):
        num_combatants = 0
        
        for i in range(len(self.list_hives)):    
            for j in range(len(self.list_hives[i].list_ants)):
                    if (self.list_hives[i].list_ants[j].x == 0 
                    and self.list_hives[i].list_ants[j].y == 0
                    and self.list_hives[i].list_ants[j].dead() == False):
                        num_combatants += 1 
                     
            print("Hive " + str(i) + ": " + str(num_combatants) + " combatants")
            num_combatants = 0 
    
    
#Demo
if __name__ == '__main__':
    hives = []
    
    #Hive 0 init
    ants = []
    for i in range(10):
        ants.append(ANT(0,0,0))
    for i in range(3):
        ants.append(ANT(1,1,0))
        
    hives.append(Hive())
    hives[0].list_ants = ants
    
    #Hive 1 init
    ants = []
    for i in range(5):
        ants.append(ANT(0,0,0))
    for i in range(3):
        ants.append(ANT(1,1,0))
        
    hives.append(Hive())
    hives[1].list_ants = ants
    
    #Hive 2 init
    ants = []
    for i in range(10):
        ants.append(ANT(0,0,0))
    for i in range(5):
        ants.append(ANT(1,1,0))
        
    hives.append(Hive())
    hives[2].list_ants = ants
    
    a = Arena(hives)
    a.run_arena_test()