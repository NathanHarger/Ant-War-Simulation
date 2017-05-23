import random as r
import numpy as n

ANT_WOULD_LIKE_DRINK = 0.9  # water level at which ANT would like to drink
ANT_WOULD_LIKE_EAT = 0.9  # food level at which ANT would like to eat
FRACTION_WATER = 0.6  # fraction of prey that is water
AMT_MIN_INIT = 0.88  # minimum initial ANT energy and water values
INIT_RANGE = .12  # range of initial ANT energy and water values
MAY_FIGTH = 0.5 #probability of entering combat if not thirsty or hungry
MAY_CRAWL = 0.5
DESICCATE = 0.6 #level at which desiccation occurs
STARVE = 0.6 #level at which starvation occurs
NUMBER_OF_FIGHTS_STARTED = 0

ENERGY_COMBAT = 0.05 #maximum energy used by ant in combat
WATER_COMBAT = 0.05 #maximum water used by ant in combat
SITTING_ENERGY = .01 #maximum energy used by ant inside of Hive
SITTING_WATER = .01 #maximum water used by ant inside of Hive
WATER_CRAWL = .03 #maximum water used by ant when crawling
ENERGY_CRAWL = .03 #maximum energy used by ant when crawling

class ANT:
    def __init__(self,x,y, shape):
        self.AMT_DRINK = .05
        self.AMT_EAT = 0.01
        self.x = x
        self.y = y
        global AMT_MIN_INIT, INIT_RANGE
        self.energy = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.water = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.IsInHive = True
        self.shape = shape

    # determine the next change in x and change in y
    def move(self):

        rand_x = r.randint(-1,1)
        rand_y = r.randint(-1,1)
        self.x += rand_x
        self.y += rand_y
        return [rand_x,rand_y]
    def getShape(self):
        return self.shape
    def consume():
        #TODO
        return
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return [self.x,self.y]
    def eat(self, availableFood):
        self.AMT_EAT = min(self.energy, availableFood,  1 - self.energy)
        self.energy = self.energy + self.energy

        global FRACTION_WATER
        self.water = min(self.water + FRACTION_WATER * self.water, 1)
    def getFood(self):
        return self.energy

    def getWater(self):
        return self.water




    def __repr__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.getFood()) + " " + str(self.getWater())

    def __str__(self):
       return str(self.x) + " " + str(self.y) + " " + str(self.getFood()) + " " + str(self.getWater())
    def __float__(self):
        return 0.0

    def ANTMayEat(self,spotAt):
        
        self.water = spotAt.getWater()
        if self.energy < ANT_WOULD_LIKE_EAT:
            self.eat(spotAt.getFood())
        else:
            self.AMT_EAT = 0


    def ANTCRAWL(self, grid, padding):
        rand = r.uniform(0,1)

        if self.water < ANT_WOULD_LIKE_DRINK:
            self.thirsty(grid,padding)
        elif self.energy < ANT_WOULD_LIKE_EAT:
            self.lookForFood(grid, padding)

        elif rand < MAY_CRAWL:
            self.CRAWLForFun(grid,padding)
        else:
            self.stayHere()
        return  grid[2:-2, 2:-2]

    def stayHere(self):
        self.water = self.water - SITTING_WATER
        self.energy = self.energy - SITTING_ENERGY


    def thirsty(self, grid,padding):
        if grid[self.y+padding, self.x+padding].getWater() != 0:
            self.stayHere()
        elif grid[self.y+1 +padding, self.x+padding].getWater() ==0: #the ANT is above another desert agent could fail if ANT is at last row
            self.lookForMoisture(grid, padding)
        elif self.x == (len(grid)-padding*2) and grid[self.y+padding, self.x -1+padding].getWater() ==0 and not grid[self.y+padding, self.x -1+padding].hasANT():
            self.CRAWLW()
        elif self.x == (len(grid)-padding*2):
           self.stayHere()
           
    def CRAWLW(self,grid,padding):
        
        grid[self.y + padding, self.x + padding].setANT(False)
        
        grid[self.y + padding,self.x-1+padding].setANT(True)


        self.x = self.x - 1


        self.water = self.water - WATER_CRAWL
        self.energy = self.energy - ENERGY_CRAWL


    def getX(self):
        return self.x

    def getY(self):
        return self.y
    def getFreeNeighbors(self,grid,padding):
        y = self.y + padding
        x = self.x + padding
        neigbors = n.array([grid[y -1, x].hasANT(),

        grid[y-1, x +1].hasANT(),

        grid[y, x+1].hasANT(),
        grid[y+1, x+1].hasANT(),
        grid[y+1, x].hasANT(),
        grid[y+1, x-1].hasANT(),
        grid[y, x-1].hasANT(),
        grid[y-1, x-1].hasANT()])

        directions = n.array([[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]])
        availNeigbors = n.where(neigbors == True, False, True)
        return directions[availNeigbors]
        
    def CRAWLForFun(self, grid,padding):
        desertNeighbors = self.getFreeNeighbors(grid,padding)

        if not grid[self.y+padding, self.x -1 +padding].getANT():
            self.CRAWLW(grid,padding)
        elif len(desertNeighbors) == 0:
            self.stayHere()
        else:
            randIndex = r.randint(0, len(desertNeighbors)-1)
            direction = desertNeighbors[randIndex]
            self.CRAWLHere(direction[0], direction[1],grid, padding)

    def lookForFood(self,grid, padding):
        self.CRAWLForFun(grid, padding)

    def lookForMoisture(self,grid, padding):
        self.CRAWLForFun(grid, padding)

    def CRAWLHere(self, delta_x, delta_y,grid,padding):
        grid[self.y + padding, self.x+padding].setANT(False)

        grid[self.y + delta_y +padding, self.x +delta_x+padding].setANT(True)
        self.x = self.x + delta_x
        self.y = self.y + delta_y

        self.water = self.water - WATER_CRAWL
        self.energy = self.energy - ENERGY_CRAWL

    def dead(self):
        #global DESICCATE,STARVE
        return self.water < DESICCATE or self.energy < STARVE

    def migrated(self):
        return self.x <= 1

    def isInHive(self):
        return self.IsInHive

