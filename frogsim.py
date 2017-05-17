import numpy as n
import DesertAgent as da
import Frog as f
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Cane Toad Simulation Variables
AMT_AWP = 1 #moisture value for water, such as an AWP
AMT_AWP_ADJACENT = 0.4 #moisture value of neighboring cell to water
AMT_AWP_OVER2 = 0.2 #moisture value of cell 2 cells away from water
AMT_DRINK = 0.05  #maximum amount toad drinks in 1 time step
AMT_EAT = 0.01 #maximum amount toad eats in 1 time step
AMT_MIN_INIT = 0.88 #minimum initial toad energy and water values
DESICCATE = 0.6 #level at which desiccation occurs
ENERGY_HOPPING = 0.002 #maximum energy used by toad in a hop
FOOD_CELL = 0.05 #food value for initializing constant food grid
FRACTION_WATER = 0.6 #fraction of prey that is water
INIT_PERCENT_TOADS = .80 #(%) percent chance a StartBorder agent forms a toad
INIT_RANGE = 0.12 #range of initial toad energy and water values
MAY_HOP = 0.5 #probability of hopping if not thirsty or hungry
PERCENT_AWPS = .02 #(%) percent chance a desert cell has an AWP
PERCENT_AWPS_FENCED = .45 #(%) percent chance an AWP is fenced
INIT_RANGE = .12 #range of initial toad energy and water values
STARVE = 0.6 #level at which starvation occurs
WATER_HOPPING = 0.002 #maximum water used by toad in a hop
WOULD_LIKE_DRINK = 0.9 #water level at which toad would like to drink
WOULD_LIKE_EAT = 0.9 #food level at which toad would like to eat
SIZE = 50

FROGS = n.array([], dtype=object)
GRID = n.empty((SIZE+2,SIZE+2), dtype=object)

# Global Simulation Variables

numFrogs = 0
numCroaked = 0 #number of dead toads
numMigrated = 0 #number of toads that have migrated off the grid phase simulation phase


# Simulation Driver to Be Executed Each Time Step
def run_sim():
    global numFrogs,numCroaked,numMigrated,FROGS,GRID
    phase = 1
    numFrogs = 0
    numCroaked = 0
    numMigrated = 0
    FROGS = n.array([], dtype=object)
    GRID = n.empty((SIZE + 2, SIZE + 2), dtype=object)
    initGrid()
    drawFrame(GRID)

    # put a iteration limit for simulations not ending
    iter1 = 0
    while phase != -1 and iter1 < 3000 and len(FROGS) >0:
        iter1 = iter1 +1
        plt.show()

        if phase ==  1:
            phase1()
            phase = 2
        elif phase == 2:
            phase2()
            phase = 3.
        elif phase == 3:
            phase3()
            if numFrogs == 0:
                phase = -1
            else:

                phase = 1
            drawFrame(GRID)
            #printFrogs()


def drawFrame(GRID):
    fig1 = plt.figure(1)

    ax1 = fig1.add_subplot(111, aspect='equal')

    ax1.set_xlim(2, SIZE + 2)
    ax1.set_ylim(2, SIZE + 2)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)

    list = []
    for i in range(2,len(GRID)-2):
        for j in range(2,len(GRID)-2):

            food = GRID[i,j].getFood() *1.3
            if GRID[i, j].getFenced() and GRID[i,j].getWater() != 0:

               list.append(ax1.add_patch(
                    patches.Rectangle(
                        (j, i),  # (x,y)
                        1,  # width
                       1,  # height

                        hatch ='x',
                        alpha = food,
                        color="blue"
                    )))
            elif GRID[i,j].getWater() != 0:
                list.append(ax1.add_patch(
                   patches.Rectangle(
                        (j, i),  # (x,y)
                    1,  # width
                    1,  # height
                        hatch='/',
                       alpha = food,
                        color="blue"
                    )))
            else:
                 list.append(ax1.add_patch(
                    patches.Rectangle(
                         (j, i),  # (x,y)
                         1,  # width
                         1,  # height
                         alpha=food,
                         color="yellow"
                     )))
    for i in FROGS:
        list.append(ax1.add_patch(
           patches.Rectangle(
               (i.getX() +.5, i.getY()+.5),  # (x,y)
               .25,  # width
               .25,  # height
               color="green"
           )))



    for i in list:
        ax1.add_patch(i)
        # fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')
    plt.show()

# StartBorder cells on the east, FinishBorder cells on the west,
# Border cells to the north and south, and Desert cells in the middle.
def initGrid():
    global numFrogs,GRID
    initFood(GRID)
    initFrogs(GRID)
    numFrogs = len(FROGS)
    initAWP(GRID)
    GRID = exGrid()

def initAWP(grid):
    test = n.random.uniform(0,1,(SIZE,SIZE))
    locs = n.where(test < PERCENT_AWPS)

    x_coor = locs[0]
    y_coor = locs[1]

    grid = setAWP(grid,x_coor,y_coor)
    for i in range(len(x_coor)):
        grid[y_coor[i], x_coor[i]].setWater(1.)
    return grid


def setAWP(grid, x_locs, y_locs):
    extendedGrid = n.empty((SIZE+6, SIZE+6), dtype=object)
    extendedGrid[:] = da.DesertAgent(-1,False, False, 0)
    extendedGrid[2:-2, 2:-2] = grid
    fenced = n.random.uniform(0,1,len(x_locs))
    fenced = n.where(fenced < PERCENT_AWPS_FENCED, True, False)
    for i in range(len(x_locs)):
        setAWPVals(1,.4,extendedGrid,x_locs[i],y_locs[i],fenced[i])
        setAWPVals(2,.2,extendedGrid,x_locs[i],y_locs[i],fenced[i])
    return extendedGrid[2:-2,2:-2]

def setAWPVals(level, water_val, grid, x,y, fenced):

    y1 = y + level
    y2 = y-level

    x1 = x + level
    x2 = x - level


    grid[y1+2,x+2].setWater(water_val)
    grid[y1+2,x+2].setFenced(fenced)

    grid[y2+2,x+2].setWater(water_val)
    grid[y2+2,x+2].setFenced(fenced)

    grid[y + 2, x1 + 2].setWater(water_val)
    grid[y + 2, x1 + 2].setFenced(fenced)
    grid[y + 2, x2 + 2].setWater(water_val)

    grid[y + 2, x2 + 2].setFenced(fenced)


    grid[y1 + 2, x1 + 2].setWater(water_val)
    grid[y2 + 2, x2 + 2].setWater(water_val)
    grid[y2 + 2, x1 + 2].setWater(water_val)
    grid[y1 + 2, x2 + 2].setWater(water_val)

    grid[y1 + 2, x1 + 2].setFenced(fenced)
    grid[y2 + 2, x2 + 2].setFenced(fenced)
    grid[y2 + 2, x1 + 2].setFenced(fenced)
    grid[y1 + 2, x2 + 2].setFenced(fenced)



    if level == 2:
        grid[y2+2, x + 3].setWater(water_val)
        grid[y1+2, x + 3].setWater(water_val)
        grid[y2 + 2, x + 1].setWater(water_val)
        grid[y1 + 2, x + 1].setWater(water_val)

        grid[y + 3, x2 + 2].setWater(water_val)
        grid[y + 3, x1 + 2].setWater(water_val)
        grid[y + 1, x2 + 2].setWater(water_val)
        grid[y + 1, x1 + 2].setWater(water_val)

        grid[y2 + 2, x + 3].setFenced(fenced)
        grid[y1 + 2, x + 3].setFenced(fenced)
        grid[y2 + 2, x + 1].setFenced(fenced)
        grid[y1 + 2, x + 1].setFenced(fenced)

        grid[y + 3, x2 + 2].setFenced(fenced)
        grid[y + 3, x1 + 2].setFenced(fenced)
        grid[y + 1, x2 + 2].setFenced(fenced)
        grid[y + 1, x1 + 2].setFenced(fenced)





def initFood(grid):
    # setup food and frogs
   # grid[1:-1,1:-1] = da.make_Desert(FOOD_CELL, f.Frog(-1, -1), False, 0)

    for y in range(1,SIZE+1):
        for x in range(1,SIZE+1):
            grid[y,x] = da.DesertAgent(FOOD_CELL, False, False, 0)



    #these are creating one DesertAgent that is shared for all elements rather than one for each

    for y in range(0,SIZE +2):
        grid[y, 0] = da.make_Desert(2., False, False, 0)

    for y in range(0,SIZE +2):
        grid[y, SIZE+1] = da.make_Desert(-1., False, False, 0)

    for x in range(1,SIZE +1):
        grid[0, x] = da.make_Desert(-1., False, False, 0)
    for x in range(1,SIZE+1 ):
        grid[SIZE+1, x] = da.make_Desert(-1., False, False, 0)
    return grid

def initFrogs(grid):
    rand_frogs = n.random.rand(SIZE)
    for i in range(len(rand_frogs)):
        if rand_frogs[i] < INIT_PERCENT_TOADS:
            global FROGS
            FROGS = n.append(FROGS, f.Frog(SIZE,i))

            grid[i, -1] = da.make_Desert(-1, True, False, 0)
        else:
            grid[i, -1] = da.make_Desert(-1., False, False, 0)
    return grid

def printFrogs():
    for i in FROGS:
        print i.__str__()
def printGrid(grid):
    for i in grid:
        for j in range(len(i)):
            print i[j].__str__(),
        print

    print "\n"






#Phase 1 of Simulation Driver Consumption phase of the simulation driver
#  Pre: The desert landscape has been initialized with AWPs and toads, and phase is 1.
#  Post: Toads have had the opportunity to eat and drink, and phase is 2.
# Algorithm:
def phase1():

    for i in FROGS:
        i_pos = i.getPos()
        i.toadMayEat(GRID[i_pos[1]+2, i_pos[0]+2])
        current_desert = GRID[i_pos[1]+2, i_pos[0]+2]
        current_desert.updateFood(i.getFood(), i.getWater())




#Phase 2 of Simulation Driver Movement phase of the simulation driver
# Pre: phase is 2. Post: All toads have had the opportunity to move, and phase is 3.
def phase2():
    #perform movement: All toads move.After each toad has moved or decided to remain in its current location,
    for i in FROGS:

        i.toadMove(GRID, 2)
    #request each toad agent to execute toadMove


def exGrid():
    extendedGrid = n.empty((SIZE + 6, SIZE + 6), dtype=object)
    extendedGrid[:] = da.DesertAgent(-1, True, False, 0)
    extendedGrid[2:-2, 2:-2] = GRID

    return extendedGrid


#Phase 3 of Simulation Driver Removal phase of the simulation driver
# Pre: phase is 3.
# Post: Migrated, desiccated, and starved toads are eliminated. If the simulation continues, phase is 1.
def phase3():
   # complete the cycle:
    #All dead and migrated toads are removed from the simulation.
    #The simulation may terminate because no toads remain. Otherwise, cycling back, phase changes to 1.
    toDelete = []


    global numFrogs, numCroaked, numMigrated, FROGS

    for i in range(len(FROGS)):
        currFrog = FROGS[i]
        curr_pos = currFrog.getPos()

        if currFrog.dead():

            GRID[curr_pos[1], curr_pos[0]].setFrog(False)
            numFrogs = numFrogs -1
            numCroaked = numCroaked + 1
            toDelete.append(i)
        elif currFrog.migrated():
            GRID[curr_pos[1], curr_pos[0]].setFrog(False)
            numFrogs = numFrogs - 1
            numMigrated = numMigrated + 1
            toDelete.append(i)

    FROGS = n.delete(FROGS,toDelete)

if __name__ == "__main__":
    dead = n.zeros(100)
    migrated =  n.zeros(100)
    for i in range(100):
        print str(i+1) + "/100"
        run_sim()
        dead[i] = numCroaked
        migrated[i] = numMigrated
    print "Mean Dead: " + str(n.mean(dead))
    print "Mean Migrated: " + str(n.mean(migrated))

