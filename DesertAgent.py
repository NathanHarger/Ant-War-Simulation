# Where there is a frog:
#         # availableFood, availableMoisture,food, and water = -1


class DesertAgent:

    def __init__(self, food,frog, fenced, water):
        self.food = food
        self.frog = frog
        self.fenced = fenced
        self.water = water

    #subtract the food
    def updateFood(self, d_food, d_water):
        self.food = self.food - d_food

        self.water = self.water - d_water
        if self.water < 0:
            self.water = 0
        if self.food < 0:
            self.food = 0

    def hasFrog(self):
        return self.frog

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
        return "(" + self.food.__str__() + ", " + self.frog.__str__() + str(self.fenced) + " " + str(float(self.water)) + " )"

        #return self.frog


def make_Desert(food,frog, fenced, water):
    desert = DesertAgent(food,frog, fenced, water)
    return desert