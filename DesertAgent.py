import random as r
from enum import Enum

class State(Enum):
    DESERT = 0
    FOOD = 1
    WATER = 2
    HIVE = 3

# This class represents a tile on the grid
# Somebody needs to refactor this to work with our model
class DesertAgent:

    def __init__(self, food,ant,water):
        self.food = food
        self.ant = ant
        self.water = water

        # state cannot be inited to 3 since the hives are set by hand
        selection_rand = r.random()
        if(selection_rand < .009):
            self.state = State.WATER
            self.water = 1
        #elif ( selection_rand < .03):
        #   self.state = State.FOOD
        #    self.food = 1
        else:
            self.state = State.DESERT
        #print self.state


    def getState(self):
        return self.state

    def is_food(self):
        return self.state is State.FOOD

    # set the sate of the spot
    def setState(self, state):

        # cannot overwrite hive or water
        if self.state == State.HIVE or self.state == State.WATER:
            return

        if state is State.FOOD:
            self.food = 1

        self.state = state
        
    #run combat for the cell
    def runCombat(self, desert, loc):
        #get list of ants in the cell
        hives_combat = [] #each element is idex of hive involved in combat
        list_ants_combat = [] #each element is index of and in list_ants
                            #from that index in the hive list
        self.loc = loc
        
        for i in range(len(desert.hives)):
            temp = []
            for j in range(len(desert.hives[i].list_ants)):
               if (desert.hives[i].list_ants[j].outer_x == self.loc[0] 
               and desert.hives[i].list_ants[j].outer_y == self.loc[0]):
                   temp.append(j)  
                   
            if (len(temp) > 0):
                hives_combat.append(i)
                list_ants_combat.append(temp)
        
         #if there are more than 1 hives, do combat 
        if (len(hives_combat) > 1):                   
            print ("Combat in cell " + str(self.loc[0]) + "," + str(self.loc[1]))
           
            #calc strength, apply to other hives
            for i in range(len(hives_combat)):
                #TODO: difference between soldiers and workers
                strength = len(list_ants_combat[i]) 
                strength = strength + r.randint(-1, 1) #some randomness
                strength = strength / (len(hives_combat) - 1)
                
                #print ("Hive " + str(i) + " Strength: " + str(strength))
                
                #apply strength to all other hives
                for j in range(len(hives_combat)):
                    if (i != j):
                        for k in range(len(list_ants_combat[j])):
                           ant_index = list_ants_combat[j][k]
                           
                           #find ant in hive list, set energy to zero to kill
                           desert.hives[hives_combat[j]].list_ants[ant_index].energy = 0
                           
                           desert.hives[hives_combat[j]].kill_count+=1
                           
                           if (k >= strength): break #stop when strenght runs out
    
    def getAnt(self):
        return self.ant

    def setAnt(self,ant):
        self.ant = ant
        
    def getWater(self):
        return self.water

    def setWater(self,water):
        self.water = water
        
    def getFood(self):
        return self.food

    def updateFood(self, delta_food):
        self.food = self.food - delta_food
        if self.food <= 0 :
            self.setState(State.DESERT)

    def setFood(self,food):
        self.food = food

    def __float__(self):
        return float(self.food)
    def __str__(self):
        return str(self.state)
