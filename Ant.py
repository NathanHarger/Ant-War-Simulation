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
    def __init__(self,x,y, i_x, i_y, shape, myHive):
        self.my_hive = myHive
        self.foodLevel = 1
        self.AMT_DRINK = .05
        self.AMT_EAT = 0.01
        self.outer_x = x
        self.outer_y = y
        self.inner_x = i_x
        self.inner_y = i_y

        global AMT_MIN_INIT, INIT_RANGE
        self.energy = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.water = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.IsInHive = True
        self.shape = shape

    # determine the next change in x and change in y
    def move(self, dim):
        self.foodLevel -= self.AMT_EAT

        myHiveX = self.my_hive.getLocation()[1]
        myHiveY = self.my_hive.getLocation()[0]
        print  self.my_hive.get_food()
        # is at hive and will request the food he needs
        if myHiveY == self.outer_y and myHiveX == self.outer_x and self.foodLevel < .5 and self.my_hive.get_food() != 0:
            #print("Eating")
            self.foodLevel += self.my_hive.eatFood(1.0-self.foodLevel)

        print(self.foodLevel)
        print(str(myHiveY) + " " +str(self.outer_y))
        print(str(myHiveX) + " " +str(self.outer_x))
        print( self.foodLevel < .5 )
        # they need to go twards hive
        if(self.foodLevel < .5):
            if(myHiveY < self.outer_y):
                 rand_y = -1
            elif(myHiveY > self.outer_y):
                 rand_y = 1
            else:
                rand_y = 0

            if(myHiveX < self.outer_x):
                 rand_x = -1
            elif(myHiveX > self.outer_x):
                 rand_x = 1
            else:
                rand_x = 0  
        else:
            rand_x = r.randint(-1,1)
            rand_y = r.randint(-1,1)        

        self.outer_x += (rand_x)
        self.outer_y += (rand_y)

        self.inner_x += rand_x
        self.inner_y += rand_y

        if self.inner_x > dim:
            self.inner_x = 0
        elif self.inner_x < 0:
            self.inner_x = dim

        if self.inner_y > dim:
            self.inner_y = 0
        elif self.inner_y < 0:
            self.inner_y = dim

        return [rand_x ,rand_y ]

    def getShape(self):
        return self.shape
    def consume():
        #TODO
        return
    def getX(self):
        return self.outer_x

    def getY(self):
        return self.outer_y

    def getPos(self):
        return [self.outer_x, self.outer_y]
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
        return str(self.outer_x) + " " + str(self.outer_y) + " (" + str(self.inner_x) + ", " + str(self.inner_y )+ " ) "

    def __str__(self):
        return str(self.outer_x) + " " + str(self.outer_y) + " (" + str(self.inner_x) + ", " + str(self.inner_y) + " ) "
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
        if grid[self.outer_y+padding, self.outer_x+padding].getWater() != 0:
            self.stayHere()
        elif grid[self.outer_y+1 +padding, self.outer_x+padding].getWater() ==0: #the ANT is above another desert agent could fail if ANT is at last row
            self.lookForMoisture(grid, padding)
        elif self.outer_x == (len(grid)-padding*2) and grid[self.outer_y+padding, self.outer_x -1+padding].getWater() ==0 and not grid[self.outer_y+padding, self.outer_x -1+padding].hasANT():
            self.CRAWLW()
        elif self.outer_x == (len(grid)-padding*2):
           self.stayHere()
           
    def CRAWLW(self,grid,padding):
        
        grid[self.outer_y + padding, self.outer_x + padding].setANT(False)
        
        grid[self.outer_y + padding, self.outer_x - 1 + padding].setANT(True)


        self.outer_x = self.outer_x - 1


        self.water = self.water - WATER_CRAWL
        self.energy = self.energy - ENERGY_CRAWL


    def getX(self):
        return self.outer_x

    def getY(self):
        return self.outer_y
    def getFreeNeighbors(self,grid,padding):
        y = self.outer_y + padding
        x = self.outer_x + padding
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

        if not grid[self.outer_y+padding, self.outer_x -1 +padding].getANT():
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
        grid[self.outer_y + padding, self.outer_x + padding].setANT(False)

        grid[self.outer_y + delta_y + padding, self.outer_x + delta_x + padding].setANT(True)
        self.outer_x = self.outer_x + delta_x
        self.outer_y = self.outer_y + delta_y

        self.water = self.water - WATER_CRAWL
        self.energy = self.energy - ENERGY_CRAWL

    def dead(self):
        global DESICCATE,STARVE
        return self.water < DESICCATE or self.energy < STARVE

    def migrated(self):
        return self.outer_x <= 1

    def isInHive(self):
        return self.IsInHive

