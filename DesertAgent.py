import random as r
from enum import Enum

class State(Enum):
    DESERT = 0
    FOOD = 1
    WATER = 2
    HIVE = 3

class DesertAgent:

    def __init__(self, food,ant,fenced,water):
        self.food = food
        self.ant = ant
        self.fenced = fenced
        self.water = water

        # state cannot be inited to 3 since the hives are set by hand
        selection_rand = r.random()
        if(selection_rand < .009):
            self.state = State.WATER
        elif ( selection_rand < .03):
            self.state = State.FOOD
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

    def getState(self):
        return self.state        
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
        
    def getFenced(self):
        return self.fenced
    def setFenced(self,fenced):
        self.fenced = fenced
        
    def getFood(self):
        return self.food
    def setFood(self,food):
        self.food = food

    def __float__(self):
        return float(self.food)
    def __str__(self):
        return str(self.state)

def make_Desert(food,ant,fenced,water):
    desert = DesertAgent(food,ant,fenced,water)
    return desert