import random as r
import numpy as n
WOULD_LIKE_DRINK = 0.9  # water level at which toad would like to drink
WOULD_LIKE_EAT = 0.9  # food level at which toad would like to eat
FRACTION_WATER = 0.6  # fraction of prey that is water
AMT_MIN_INIT = 0.88  # minimum initial toad energy and water values
INIT_RANGE = .12  # range of initial toad energy and water values
MAY_HOP = 0.5 #probability of hopping if not thirsty or hungry
DESICCATE = 0.6 #level at which desiccation occurs
STARVE = 0.6 #level at which starvation occurs

ENERGY_HOPPING = 0.02 #maximum energy used by toad in a hop
WATER_HOPPING = 0.02 #maximum water used by toad in a hop
SITTING_ENERGY = .01 #maximum energy used by toad sitting
SITTING_WATER = .01 # max energy used by toad sitting in desert
class Frog:


    def __init__(self,x,y):
        self.AMT_DRINK = .05
        self.AMT_EAT = 0.01
        self.x = x
        self.y = y
        global AMT_MIN_INIT, INIT_RANGE
        self.energy = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)
        self.water = r.uniform(AMT_MIN_INIT, AMT_MIN_INIT + INIT_RANGE)

        # Function to update a toad's energy and water after it eats
        # Pre: The agent is a toad, and AMT_EAT and FRACTION_WATER are global variables.
        # Post: The toad's energy and water levels have been adjusted after eating.
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
        if self.x == -1:
            return "N"
        else:
            return "F"

    def __str__(self):
       return str(self.x) + " " + str(self.y) + " " + str(self.getFood()) + " " + str(self.getWater())
    def __float__(self):
        return 0.0

    # Toad behavior regarding eating
    # Pre: The agent is a toad, and the phase is 1.
    # Post: The toad may have eaten. Its amtEat state variable has an updated value.
    def toadMayEat(self,spotAt):
        # frog is in desert if water is 0
        water = spotAt.getWater()
        global WOULD_LIKE_EAT
        if self.energy < WOULD_LIKE_EAT:
            self.eat(spotAt.getFood())
        else:
            self.AMT_EAT = 0


    #  toadMove Possibly have the toad move
    #  Pre: The agent is a toad, and phase is 2.
    # Post: The toad has moved or decided to remain in its current location.
    def toadMove(self, grid, padding):
        global WOULD_LIKE_DRINK, WOULD_LIKE_EAT, MAY_HOP
        rand = r.uniform(0,1)

        if self.water < WOULD_LIKE_DRINK:
            self.thirsty(grid,padding)
        elif self.energy < WOULD_LIKE_EAT:
            self.lookForFood(grid, padding)

        elif rand < MAY_HOP:
            self.hopForFun(grid,padding)
        else:
            self.stayHere()
        return  grid[2:-2, 2:-2]

    def stayHere(self):
        global SITTING_ENERGY,SITTING_WATER
        self.water = self.water - SITTING_WATER
        self.energy = self.energy - SITTING_ENERGY

    # thirsty Function to change the position of a very thirsty toad
    # Pre: The agent is a toad.
    # The crappy unfactored else if block is artifacts from the books pseudocode
    def thirsty(self, grid,padding):
        if grid[self.y+padding, self.x+padding].getWater() != 0:
            self.stayHere()
        elif grid[self.y+1 +padding, self.x+padding].getWater() ==0: #the toad is above another desert agent could fail if frog is at last row
            self.lookForMoisture(grid, padding)
        elif self.x == (len(grid)-padding*2) and grid[self.y+padding, self.x -1+padding].getWater() ==0 and not grid[self.y+padding, self.x -1+padding].hasFrog():
            self.moveW()
        elif self.x == (len(grid)-padding*2):
           self.stayHere()

    #  moveW Procedure to move toad west and update its state variables
    #   Pre: The agent is a toad and cell to the west is unoccupied.
    #   Post: The toad was moved west, and its state variables have been updated.
    def moveW(self,grid,padding):
        #print "curr loc: " + str(self.getPos())
        grid[self.y + padding, self.x + padding].setFrog(False)
        #print "Setting " + str(self.y + padding) + " " +  str(self.x + padding) + " False"
        grid[self.y + padding,self.x-1+padding].setFrog(True)

        #print "Setting " + str(self.y + padding) + " " +  str(self.x-1+padding) + " True"


        self.x = self.x - 1


        self.water = self.water - WATER_HOPPING
        self.energy = self.energy - ENERGY_HOPPING


    def getX(self):
        return self.x

    def getY(self):
        return self.y
    def getFreeNeighbors(self,grid,padding):
        y = self.y + padding
        x = self.x + padding
        neigbors = n.array([grid[y -1, x].hasFrog(),

        grid[y-1, x +1].hasFrog(),

        grid[y, x+1].hasFrog(),
        grid[y+1, x+1].hasFrog(),
        grid[y+1, x].hasFrog(),
        grid[y+1, x-1].hasFrog(),
        grid[y, x-1].hasFrog(),
        grid[y-1, x-1].hasFrog()])

        directions = n.array([[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]])
        availNeigbors = n.where(neigbors == True, False, True)
        return directions[availNeigbors]
    #  hopForFun Function to update a toad's location to hop in a random "legal" direction if possible
    #  Pre: The agent is a toad.
    # Post: The toad may have moved at random on top of a vacant Desert neigh- bor.
    def hopForFun(self, grid,padding):
        desertNeighbors = self.getFreeNeighbors(grid,padding)

        if not grid[self.y+padding, self.x -1 +padding].getFrog():
            self.moveW(grid,padding)
        elif len(desertNeighbors) == 0:
            self.stayHere()
        else:
            randIndex = r.randint(0, len(desertNeighbors)-1)
            direction = desertNeighbors[randIndex]
            self.hopHere(direction[0], direction[1],grid, padding)

    def lookForFood(self,grid, padding):
        self.hopForFun(grid, padding)

    def lookForMoisture(self,grid, padding):
        self.hopForFun(grid, padding)

    def hopHere(self, delta_x, delta_y,grid,padding):
        grid[self.y + padding, self.x+padding].setFrog(False)

        grid[self.y + delta_y +padding, self.x +delta_x+padding].setFrog(True)
        self.x = self.x + delta_x
        self.y = self.y + delta_y

        self.water = self.water - WATER_HOPPING
        self.energy = self.energy - ENERGY_HOPPING

    # changeCounts Method to eliminate a toad that should be dead or migrated
    # Pre: The agent is a Toad agent. DESICCATE and STARVE are global constants. numAlive are the number of live toads.
    # numCroaked are the number of toads that have died.
    #  numMigrated are the number of toads that have migrated.
    #  If the toad has desiccated or starved, the agent has been erased,
    # num Alive has been decremented by 1, and numCroaked has been incre mented by 1.
    #  If the toad has migrated off the grid to the west, the agent has been erased, numAlive has been decremented by 1,
    #  and numMigrated has been incremented by 1.
    def dead(self):
        global DESICCATE,STARVE
        return self.water < DESICCATE or self.energy < STARVE

    def migrated(self):
        return self.x <= 1

