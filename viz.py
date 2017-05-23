import Tkinter as tk
import numpy as n
import Desert as des
from DesertAgent import State as state
import random as r
import Ant as a
import HiveClass as hive

SIM_LENGTH = 1         #How many ticks in a simulation
DESSICATION_LEVEL = 1  #Level an ant dies of thirst
STARVATION_LEVEL = 1   #Level an ant dies of starvation
MAX_FOOD_WHATER = 1    #Maximum level of food and water an ant can carry
MOISTURE_FROM_FOOD = 1 #Moisture gained from eating

# Controls the simulation. Allows you to run sims and change various variables.
class viz:

    def __init__(self, dim, window_width, window_height, delay):
        self.wWidth = window_width
        self.dim = dim

        self.root=tk.Tk()
        self.canvas= tk.Canvas(self.root,width=window_width,height=window_height)
        self.canvas.pack()
        self.size_ratio = self.wWidth / self.dim

        self.wHeight = window_height
        self.cell = n.empty((self.dim, self.dim), dtype=object)
        self.__setup_grid__()
        self.delay = delay
        self.running = True

    # the enviorment is a grid of DesertAgent
    # 0: desert
    # 1: food
    # 2: water
    # 3: hive
    # function that is called by the tkinter canvas that updates ojects in sim every frame
    def update_frame(self,enviornment):
        for i in range(self.dim):
            for j in range(self.dim):
                enviornment_type = enviornment.getItem(j,i).getState()
                #print enviornment_type
                if enviornment_type == state.DESERT:
                    self.canvas.itemconfig(self.cell[i,j], fill="yellow")
                elif enviornment_type ==  state.FOOD:
                    self.canvas.itemconfig(self.cell[i,j], fill="green")
                elif enviornment_type==  state.WATER:
                    self.canvas.itemconfig(self.cell[i,j], fill="blue")
                else:
                    self.canvas.itemconfig(self.cell[i,j], fill="brown")

                    # self.canvas.move(self.testCircle, 5, 5)
        # self.draw_colors_test()


    def __setup_grid__(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.cell[i, j] = self.canvas.create_rectangle(self.size_ratio * i, self.size_ratio * j,
                                                               self.size_ratio * i+ self.size_ratio, self.size_ratio * j + self.size_ratio)

    # test that shows animation of object moving and changing color
    #def draw_colors_test(self):

        # color changing from
        # http://stackoverflow.com/questions/11340765/default-window-colour-tkinter-and-hex-colour-codes
       # rgb = tuple(n.random.randint(0,256, (3)))
      #  mycolor = '#%02x%02x%02x' % rgb
      #  self.canvas.itemconfig(self.testCircle, fill=mycolor)
    def dispViz(self):
        self.root.mainloop()

    def draw_frame(self,enviorment, Ants):

        self.update_frame(enviorment)

        if self.running:
            self.canvas.after(self.delay,self.Run_Sim, enviorment, Ants)
        else:
            self.dispViz()

    # Runs a simulation. Initialize all values based on keywords if passed in.
    # For each time tick, run phase 1-3. When the simulation runs to the
    # variable sim_length, end it.
    def Run_Sim(self, enviornment):
        self.Phase_One()
        for i in enviornment.getHives():
            ants = i.getAnts()
            self.Phase_Two(ants)
            self.draw_frame(enviornment, ants)
        #self.Phase_Three(enviornment)
        # TODO
        return

    def ant_movement(self, ants):
        for i in range(len(ants)):
            [x,y] = ants[i].move()
            self.canvas.move(ants[i].getShape(), self.size_ratio*x, self.size_ratio*y)

    # Ants eat and drink. Eggs turn into pupae. Pupae grow up.
    # The queen lays eggs based on amount of food in nest.
    def Phase_One(self):

        # TODO
        return

    # First - execute combat for the entire desert. Remove all ants destroyed.
    # Second - move all ants based on caste, current job,
    # and pheromones of neighbor cells.
    def Phase_Two(self,ants):
        self.ant_movement(ants)
        # TODO
        return

    # Kill all dessicated and starving ants. Update desert (add/remove food
    # and moisture based on season, remove hives with no ants, and update season)
    def Phase_Three(self,enviornment):
        enviornment.update_seasons()
        rand = r.random()
        #if rand < .01:
        # self.running = False
        # TODO
        return

    def create_ants(self, testAnts, loc):
        for j in n.arange(n.alen(testAnts)):
            testAnts[j] = a.ANT(loc[0], loc[1],
                                self.canvas.create_oval(j*self.size_ratio ,0 ,(j*self.size_ratio)+self.size_ratio,self.size_ratio,
                                                                                fill = "black"))
                                                                                
    def create_hive(self, myHive, location):
        myHive = hive.Hive(location[0], location[1], 
                                self.canvas.create_oval(location[0]*self.size_ratio ,location[1]*self.size_ratio ,(i*self.size_ratio)
                                +self.size_ratio,self.size_ratio, fill = "brown"))
        return myHive

# viz class demo
if __name__ == '__main__':
    dim = 50
    vizTest = viz(dim,500,500, 900) 
    testEnviorment = des.Desert(dim,1)
    hives = testEnviorment.getHives()
    
    for i in hives:
        myAnts = n.empty(5, dtype=object)
        print(i)
        vizTest.create_ants(myAnts, i.getLocation())
        i.setAnts(myAnts)  
    
    #print testAnts
    vizTest.Run_Sim(testEnviorment)

    vizTest.dispViz()


