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

    #TODO state change need to change food and water levels
    def setState(self, state):
        if state is State.FOOD:
            self.food = 1
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
