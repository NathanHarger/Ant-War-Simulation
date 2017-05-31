import random as r
import numpy as n
import Desert as d
import DesertAgent as da
from enum import Enum

ANT_WOULD_LIKE_DRINK = 0.9  # water level at which ANT would like to drink
ANT_WOULD_LIKE_EAT = 0.9  # food level at which ANT would like to eat
# FRACTION_WATER = 0.6  # fraction of prey that is water
AMT_MIN_INIT = 0.88  # minimum initial ANT energy and water values
INIT_RANGE = .12  # range of initial ANT energy and water values
# MAY_FIGTH = 0.5 #probability of entering combat if not thirsty or hungry
MAY_CRAWL = 0.5
DESICCATE = 0.6 #level at which desiccation occurs
STARVE = 0.6 #level at which starvation occurs
NUMBER_OF_FIGHTS_STARTED = 0

ENERGY_COMBAT = 0.05 #maximum energy used by ant in combat
WATER_COMBAT = 0.05 #maximum water used by ant in combat
SITTING_ENERGY = .01 #maximum energy used by ant inside of Hive
SITTING_WATER = .01 #maximum water used by ant inside of Hive
WATER_CRAWL = .03 #maximum water used by ant when crawling
ENERGY_CRAWL = .003 #maximum energy used by ant when crawling

AMT_EAT = .01
ANT_MAX_FOOD = 2
AMT_DRINK = .05

class JOB(Enum):
    GATHERER = 0        # go out find food and bring it home
    WARRIOR = 1         # go out find enemy and kill it
    QUEEN = 2           # stay home reproduce
    SCOUT = 3           # scout ant to find food locations better
    GENERICINITIAL = 4

class ACTION(Enum):
    RETURN = 0          # ant is coming home
    SEARCH = 1          # and is going out to do something
    COMBAT = 2          # ant is in combat
    HOME = 3            # ant is in base  

class ANT:
    def __init__(self,x,y, i_x, i_y, shape, myHive, myEnvir, job):
        self.my_hive = myHive

        if not self.my_hive is None:
            self.myHiveX = self.my_hive.getLocation()[0]
            self.myHiveY = self.my_hive.getLocation()[1]
            self.outer_x = self.myHiveX
            self.outer_y = self.myHiveY
        self.my_envi = myEnvir
        self.shape = shape

        self.inner_x = i_x
        self.inner_y = i_y


        chance = r.randint(-1,1)
        if(job == JOB.GENERICINITIAL):
            if ( chance is 1):
                self.job = JOB.SCOUT
                
            elif (chance == -1):
                self.job = JOB.WARRIOR
            else:
                self.job = JOB.GATHERER
        else: 
            self.job = job
        
        #self.job = JOB.WARRIOR

        
                
        self.action = ACTION.HOME
        
        self.job_switch = {0 : self.DoGatherer, 1 : self.DoWarrior, 2 : self.DoQueen, 3 : self.DoScout}   

        self.foodLevel = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.energy = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.water = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.return_to_hive = False
        self.IsInHive = True
        
        # when ant is soldier, this is target hive
        #can be own hive by design, if target is own hive soldier will defend
        self.target_hive = r.randint(0, len(self.my_envi.hives) - 1)
        self.targetX = self.my_envi.hives[self.target_hive].getLocation()[0]
        self.targetY = self.my_envi.hives[self.target_hive].getLocation()[1]
        self.prevAction = self.action #sets prevAction
        

    def random_move_in_bounds(self, dim):
        x_moves = [-1, 1]
        y_moves = [-1, 1]

        x = self.getX()
        y = self.getY()

        if x == 0:
            x_moves.remove(-1)
        elif x == dim - 1:
            x_moves.remove(1)

        if y == 0:
            y_moves.remove(-1)
        elif y == dim - 1:
            y_moves.remove(1)
        return (r.choice(x_moves), r.choice(y_moves))

    # determine the next change in x and change in y
    def move(self, dim, desert):
        self.foodLevel -= ENERGY_CRAWL

        # Do your job based on what you are assigned
        rand_x, rand_y = self.job_switch[self.job.value]()

        current_spot = self.my_envi.getItem(rand_x,rand_y)
        if current_spot.getState() is d.State.WATER:
             rand_x, rand_y = (0,0)

        # if hungry go home no matter what
        if(self.foodLevel < .4 and  self.action != ACTION.HOME):
             self.action = ACTION.RETURN

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

    # JOB.GATHERER move function
    def DoGatherer(self):


        if (self.action == ACTION.HOME):
            self.foodLevel += self.my_hive.eatFood(1.0-self.foodLevel)
            if self.foodLevel > 1:                                         
                amount_food = self.foodLevel - 1
                self.foodLevel - amount_food
                self.my_hive.add_food(amount_food)            
            self.action = ACTION.SEARCH
            return (0,0)

        elif (self.action == ACTION.RETURN):
            if(self.myHiveY == self.outer_y and self.myHiveX == self.outer_x ):       
                self.action = ACTION.HOME
            if(self.myHiveY < self.outer_y):
                 rand_y = -1
            elif(self.myHiveY > self.outer_y):
                 rand_y = 1
            else:
                rand_y = 0
            if(self.myHiveX < self.outer_x):
                 rand_x = -1
            elif(self.myHiveX > self.outer_x):
                 rand_x = 1
            else:
                rand_x = 0  
            return (rand_x, rand_y)

        elif(self.action == ACTION.SEARCH):
               current_spot = self.my_envi.getItem(self.outer_x,self.outer_y)
               if current_spot.getState() is d.State.FOOD:
                    self.eat(current_spot.getFood(), current_spot)
                    self.action = ACTION.RETURN
                    return (0,0)
               else:
                    f = self.get_neighbour_with_food(self.outer_x, self.outer_y, self.my_envi)
                    if (f != None):
                        if not len(f) == 0:
                            return r.choice(f)
        
        return self.random_move_in_bounds(self.my_envi.get_size())

           

          
    def DoWarrior(self): 
             
        
        #if in nest, eat, fill up stores, then go back out to search
        if (self.action == ACTION.HOME):
            self.foodLevel += self.my_hive.eatFood(1.0-self.foodLevel)
            if self.foodLevel > 1:                                         
                amount_food = self.foodLevel - 1
                self.foodLevel - amount_food
                self.my_hive.add_food(amount_food)            
            self.action = ACTION.SEARCH
            return (0,0)
         
        #if returning, move towards nest each tick       
        elif (self.action == ACTION.RETURN):
            if(self.myHiveY == self.outer_y and self.myHiveX == self.outer_x ):       
                self.action = ACTION.HOME
            if(self.myHiveY < self.outer_y):
                 rand_y = -1
            elif(self.myHiveY > self.outer_y):
                 rand_y = 1
            else:
                rand_y = 0
            if(self.myHiveX < self.outer_x):
                 rand_x = -1
            elif(self.myHiveX > self.outer_x):
                 rand_x = 1
            else:
                rand_x = 0  
            return (rand_x, rand_y)
            
        #if searching, move towards enemy hive
        #has a chance to defend own hive instead
        #target based on target_hive
        elif(self.action == ACTION.SEARCH):
                       
            if(self.targetY == self.outer_y and self.targetX == self.outer_x ):       
                self.action = ACTION.RETURN
            if(self.targetY < self.outer_y):
                 rand_y = -1
            elif(self.targetY > self.outer_y):
                 rand_y = 1
            else:
                rand_y = 0
            if(self.targetX < self.outer_x):
                 rand_x = -1
            elif(self.targetX > self.outer_x):
                 rand_x = 1
            else:
                rand_x = 0  
            return (rand_x, rand_y)
            
        #don't move, restore previous action
        elif(self.action == ACTION.COMBAT):
           print ("soldier ant in combat, cell " + str(self.outer_x) + "," + str(self.outer_y))
           self.action = ACTION.RETURN
           return (0,0)
           
        
        return  self.random_move_in_bounds(self.my_envi.get_size())


    def DoQueen(self):
        # TODO 
        return  self.random_move_in_bounds(self.my_envi.get_size())


    def DoScout(self): 
        if (self.action == ACTION.HOME):
            self.foodLevel += self.my_hive.eatFood(1.0-self.foodLevel)
            if self.foodLevel > 1:                                         
                amount_food = self.foodLevel - 1
                self.foodLevel - amount_food
                self.my_hive.add_food(amount_food)            
            self.action = ACTION.SEARCH
            return (0,0)

        elif (self.action == ACTION.RETURN):
            if(self.myHiveY == self.outer_y and self.myHiveX == self.outer_x ):       
                self.action = ACTION.HOME
            if(self.myHiveY < self.outer_y):
                 rand_y = -1
            elif(self.myHiveY > self.outer_y):
                 rand_y = 1
            else:
                rand_y = 0
            if(self.myHiveX < self.outer_x):
                 rand_x = -1
            elif(self.myHiveX > self.outer_x):
                 rand_x = 1
            else:
                rand_x = 0  
            return (rand_x, rand_y)

        elif(self.action == ACTION.SEARCH):
            current_spot = self.my_envi.getItem(self.outer_x,self.outer_y)
            if current_spot.getState() is d.State.FOOD:
                 self.my_hive.setFoodLoc(self.outer_x, self.outer_y)

            f = self.get_neighbour_with_food(self.outer_x, self.outer_y, self.my_envi)
            if (f != None and not len(f) == 0):
                return r.choice(f)            
        
            return self.random_move_in_bounds(self.my_envi.get_size())


    def get_neighbour_with_food(self, x,y, grid):
        y = self.outer_y
        x = self.outer_x
        if y > grid.get_size() or x > grid.get_size():
            return
        neigbors = n.array([grid.getItem(x,y-1).is_food(),
                            grid.getItem(x+1,y-1).is_food(),
                            grid.getItem(x+1,y).is_food(),
                            grid.getItem(x+1,y+1).is_food(),
                            grid.getItem(x,y+1).is_food(),
                            grid.getItem(x-1,y+1).is_food(),
                            grid.getItem(x-1,y).is_food(),
                            grid.getItem(x-1,y-1).is_food()])

        directions = n.array([[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]])
        availNeigbors = n.where(neigbors == True, True, False)
        return directions[availNeigbors]

    def getShape(self):
        return self.shape
    def consume():
        #TODO
        return
    def getX(self):
        return self.outer_x

    def getY(self):
        return self.outer_y

    def set_food(self, food):
        self.foodLevel = food

    def getPos(self):
        return (self.outer_x, self.outer_y)

    def eat(self, availableFood, spot):
        # an ant takes up to 1.5 units of food
        AMT_EAT = min( availableFood,  ANT_MAX_FOOD - self.foodLevel)
        self.foodLevel = self.foodLevel+ AMT_EAT
        spot.updateFood(AMT_EAT)

    def getFood(self):
        return self.energy

    def getWater(self):
        return self.water


    def ANTMayEat(self,spotAt):
        
        self.water = spotAt.getWater()
        if self.energy < ANT_WOULD_LIKE_EAT:
            self.eat(spotAt.getFood())
        else:
            AMT_EAT = 0


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
        return self.foodLevel <= 0 or self.energy < STARVE

    def setShape(self, shape):
        self.shape = shape

    def migrated(self):
        return self.outer_x <= 1

    def isInHive(self):
        return self.IsInHive

    def __repr__(self):
        return str(self.outer_x) + " " + str(self.outer_y) + " f: " + str(self.foodLevel)

    def __str__(self):
        return str(self.outer_x) + " " + str(self.outer_y) + " f: " + str(self.foodLevel)

    def __float__(self):
        return 0.0

    def __test_move__(self,dx,dy):
        self.outer_x += dx
        self.outer_y += dy
