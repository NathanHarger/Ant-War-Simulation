import random as r
import numpy as n
from enum import Enum

class State(Enum):
    DESERT = 0
    FOOD = 1
    WATER = 2
    HIVE = 3

# This class represents a tile on the grid
# Somebody needs to refactor this to work with our model
class DesertAgent:
    
    

    def __init__(self, food,ant,water, loc):
        self.food = food
        self.ant = ant
        self.water = water
        
        self.loc = loc

        # state cannot be inited to 3 since the hives are set by hand
        selection_rand = r.random()
        if(selection_rand < .009):
            self.state = State.WATER
            self.water = 1
        elif ( selection_rand < .03):
            self.state = State.FOOD
            self.food = 1
        else:
            self.state = State.DESERT
        #print self.state

    #subtract the food
    def updateFood(self, d_food, d_water):
        self.food = self.food - d_food

        self.water = self.water - d_water
        if self.water < 0:
            self.water = 0
        if self.food < 0:
            self.food = 0
    
    #run combat for the cell
    def runCombat(self, desert):
        #get list of ants in the cell
        list_hives_combat = [] #each element is idex of hive involved in combat
        list_ants_combat = [] #each element is index of and in list_ants
                            #from that index in the hive list
        
        for i in range(len(desert.list_hives)):
            temp = []
            for j in range(len(desert.list_hives[i].list_ants)):
               if (desert.list_hives[i].list_ants[j].x == self.loc[0] 
               and desert.list_hives[i].list_ants[j].y == self.loc[0]):
                   temp.append(j)  
                   
            if (len(temp) > 0):
                list_hives_combat.append(i)
                list_ants_combat.append(temp)
        
         #if there are more than 1 hives, do combat 
        if (len(list_hives_combat) > 1):                   
            
            #calc strength, apply to other hives
            for i in range(len(list_hives_combat)):
                #TODO: difference between soldiers and workers
                strength = len(list_ants_combat[i]) 
                strength = strength + r.randint(-1, 1) #some randomness
                strength = strength / (len(list_hives_combat) - 1)
                
                
                #apply strength to all other hives
                for j in range(len(list_hives_combat)):
                    if (i != j):
                        for k in range(len(list_ants_combat[j])):
                           ant_index = list_ants_combat[j][k]
                           
                           #find ant in hive list, set energy to zero to kill
                           desert.list_hives[list_hives_combat[j]].list_ants[ant_index].energy = 0
                           
                           desert.list_hives[list_hives_combat[j]].kill_count+=1
                           
                           if (k >= strength): break #stop when strenght runs out
                           
        
                        
            
            
            



    def getState(self):
        return self.state

    #TODO state change need to change food and water levels
    def setState(self, state):
        self.state = state
        
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

    def setFood(self,food):
        self.food = food

    def __float__(self):
        return float(self.food)
    def __str__(self):
        return str(self.state)
