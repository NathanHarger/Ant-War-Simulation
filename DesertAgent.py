import random as r

class DesertAgent:

    def __init__(self, food,frog, fenced, water):
        self.food = food
        self.frog = frog
        self.fenced = fenced
        self.water = water

        # state cannot be inited to 3 since the hives are set by hand
        selection_rand = r.random()
        if(selection_rand < .009):
            self.state = 2
        elif ( selection_rand < .03):
            self.state = 1
        else:
            self.state = 0
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
    def hasFrog(self):
        return self.frog
    def getType(self):
        return self.state
    def getFrog(self):

        return self.frog

    def setWater(self,water):
        self.water = water

    def getWater(self):
        return self.water

    def getFood(self):
        return self.food

    def setFenced(self,fenced):
        self.fenced = fenced
    def getFenced(self):
        return self.fenced
    def setFood(self,food):
        self.food = food

    def setFrog(self,frog):
        self.frog = frog

    def __float__(self):
        return float(self.food)

    def __str__(self):
        return str(self.state)

        #return self.frog


def make_Desert(food,frog, fenced, water):
    desert = DesertAgent(food,frog, fenced, water)
    return desert