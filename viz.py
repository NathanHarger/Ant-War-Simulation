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
        self.canvas= tk.Canvas(self.root,width=window_width * 1.2,height=window_height * 1.2)
        self.canvas.pack()
        self.size_ratio = (self.wWidth / self.dim) * .8
        self.text_width = window_width * 1.2
        self.text_height = window_height * 1.2

        self.wHeight = window_height
        self.cell = n.empty((self.dim, self.dim), dtype=object)
        self.text_cells = n.empty((self.dim + 10, self.dim + 10), dtype=object)
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
                curr_agent = enviornment.getItem(j,i)
                enviornment_type = curr_agent.getState()
                #print enviornment_type
                if enviornment_type is state.DESERT:
                    self.canvas.itemconfig(self.cell[i,j], fill="yellow")
                elif enviornment_type is  state.FOOD:
                    color = self.get_food_color_intensity(curr_agent.getFood())
                    self.canvas.itemconfig(self.cell[i,j], fill= color)
                elif enviornment_type is  state.WATER:
                    self.canvas.itemconfig(self.cell[i,j], fill="blue")

                elif enviornment_type is  state.HIVE:
                    self.canvas.itemconfig(self.cell[i,j], fill="brown")
                else:
                    self.canvas.itemconfig(self.cell[i,j], fill="green")

        for i in range(len(enviornment.getHives())):
            canvas_id = self.canvas.create_text(500, 500 + 15 * i, anchor="s")
            label_string = "Number of ants in Hive "  + str(i) + " " + str(len(enviornment.getHives()[0].getAnts()))
            self.canvas.itemconfig(canvas_id, text=label_string)


    def get_food_color_intensity(self, greenVal):
        rgb = (0,255-greenVal*100,0)
        return '#%02x%02x%02x' % rgb

    def __setup_grid__(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.cell[i, j] = self.canvas.create_rectangle(self.size_ratio * j, self.size_ratio * i,
                                                               self.size_ratio * j+ self.size_ratio, self.size_ratio * i + self.size_ratio, outline="")
        for i in range(self.dim + 10):
            for j in range(self.dim + 10):
                self.text_cells[i,j] = self.canvas.create_rectangle(0, self.text_width, 0, self.text_height, outline="")    

    def dispViz(self):
        self.root.mainloop()

    def draw_frame(self,enviorment):

        self.update_frame(enviorment)

        if self.running:
            self.canvas.after(self.delay,self.Run_Sim, enviorment)

            #stats_text = """
            #-------------------
            #|   ------     line1    |
            #|   ------     line2    |
            #|   ------     line3    |
            #-------------------"""

            #legend_frame = tk.LabelFrame(self.canvas,text=stats_text,padx=5, pady=5)
            #legend_label = tk.Label(legend_frame,text=stats_text)
            #legend_label.pack()

            #self.canvas.create_window(500,500,window=legend_frame,anchor="se")

            #for i in enviorment.getHives():
            #    location = i.getLocation()
            #    ants = i.getAnts()
            #    canvas_id = self.canvas.create_text(location[0] * 10, location[1] * 10)
            #    self.canvas.itemconfig(canvas_id, text="Number of in this Hive" + str(len(ants)))
            #    self.canvas.insert(canvas_id, 6, "new ")

        else :
            self.dispViz()

    # Runs a simulation. Initialize all values based on keywords if passed in.
    # For each time tick, run phase 1-3. When the simulation runs to the
    # variable sim_length, end it.
    def Run_Sim(self, enviornment):

        self.Phase_One()
        #print enviornment.getHives()
        for i in enviornment.getHives():
            print i.getFoodLevel()
            ants = i.getAnts()
            i.update_nest()
           # print ants
            self.Phase_Two(ants,enviornment)
        self.draw_frame(enviornment)
        self.Phase_Three(enviornment)
        # TODO
        return

    def ant_movement(self, ants,env):
        #print ants[1]

        for i in range(len(ants)):
            [x,y] = ants[i].move( self.dim, env)
            #print str(x) + " " + str(y)
            self.canvas.move(ants[i].getShape(), self.size_ratio* x, self.size_ratio* y)

    # Ants eat and drink. Eggs turn into pupae. Pupae grow up.
    # The queen lays eggs based on amount of food in nest.
    def Phase_One(self):

        # TODO
        return

    # First - execute combat for the entire desert. Remove all ants destroyed.
    # Second - move all ants based on caste, current job,
    # and pheromones of neighbor cells.
    def Phase_Two(self,ants,enviornment):
        self.ant_movement(ants,enviornment)
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
      
    def get_random_color(self):
        # color changing from
       # http://stackoverflow.com/questions/11340765/default-window-colour-tkinter-and-hex-colour-codes
        rgb = tuple(n.random.randint(0,255, (3)))
        return '#%02x%02x%02x' % rgb



    def create_ants(self, testAnts, loc,myHive, myEnv):
        color = self.get_random_color()
        #print color
        for i in n.arange(n.alen(testAnts)):

            #print loc

            testAnts[i] = a.ANT(loc[0],loc[1],0,0, self.canvas.create_rectangle(loc[0]*self.size_ratio ,loc[1] *self.size_ratio + self.size_ratio,(loc[0]*self.size_ratio),loc[1]*self.size_ratio,
                                                                                outline = color), myHive, myEnv)
                                                                                

    def create_hive(self, myHive, location):
        myHive = hive.Hive((location[0], location[1]))
        return myHive


if __name__ == '__main__':

    dim = 50
    num_ants_per_hive = 20
    vizTest = viz(dim,500,500, 1)
    testEnviorment = des.Desert(dim,1)
    #print testEnviorment.__str__()
    hives = testEnviorment.getHives()
    
    for i in hives:
        myAnts = n.empty(num_ants_per_hive, dtype=object)
        vizTest.create_ants(myAnts, i.getLocation(), i, testEnviorment)
        i.setAnts(myAnts)
        #print i.getAnts()

    #print testEnviorment.getHives()
    #print testAnts
    vizTest.Run_Sim(testEnviorment)

    vizTest.dispViz()


