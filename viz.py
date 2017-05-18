import Tkinter as tk
import numpy as n
import DesertAgent as da
import random as r
class viz:

    def __init__(self, dim, window_width, window_height, delay):
        self.root=tk.Tk()
        self.canvas= tk.Canvas(self.root,width=window_width,height=window_height)
        self.canvas.pack()
        self.dim = dim
        self.wHeight = window_height
        self.wWidth = window_width
        self.cell = n.empty((self.dim, self.dim), dtype=object)
        self.__setup_grid__()
        self.delay = delay

    # the enviorment is a grid of DesertAgent
    # 0: desert
    # 1: food
    # 2: water
    # 3: hive
    # function that is called by the tkinter canvas that updates ojects in sim every frame
    def draw_frame(self,enviornment):
        for i in range(self.dim):
            for j in range(self.dim):
                enviornment_type = enviornment[i,j].getType()
                #print enviornment_type
                if enviornment_type == 0:
                    self.canvas.itemconfig(self.cell[i,j], fill="yellow")
                elif enviornment_type == 1:
                    self.canvas.itemconfig(self.cell[i,j], fill="green")
                elif enviornment_type== 2:
                    self.canvas.itemconfig(self.cell[i,j], fill="blue")
                else:
                    self.canvas.itemconfig(self.cell[i,j], fill="brown")


       # self.canvas.move(self.testCircle, 5, 5)
        # self.draw_colors_test()
        self.canvas.after( self.delay, self.draw_frame, enviornment)


    def __setup_grid__(self):
        size_ration = self.wWidth / self.dim
        for i in range(self.dim):
            for j in range(self.dim):
                self.cell[i, j] = self.canvas.create_rectangle(size_ration * i, size_ration * j,
                                                               size_ration * i+ size_ration, size_ration * j + size_ration)

    # test that shows animation of object moving and changing color
    #def draw_colors_test(self):

        # color changing from
        # http://stackoverflow.com/questions/11340765/default-window-colour-tkinter-and-hex-colour-codes
       # rgb = tuple(n.random.randint(0,256, (3)))
      #  mycolor = '#%02x%02x%02x' % rgb
      #  self.canvas.itemconfig(self.testCircle, fill=mycolor)
    def dispViz(self):
        self.root.mainloop()

def make_test_enviorment(size):
    test_env = n.empty((size,size), dtype=object)
    for i in range(size):
        for j in range(size):
            test_env[i,j] = da.DesertAgent(0,0, 0, 0)
   # print test_env
    place_anthills(test_env, 2, size)
    return test_env
def place_anthills(test_env, num_hives, size):
    while num_hives != 0:
        rand_x = r.randint(0, size-1)
        rand_y =  r.randint(0, size-1)

        # a hive cannot be placed in water, or ontop an existing hive
        if test_env[rand_y,rand_x].getState() != 2 and test_env[rand_y,rand_x].getState() != 3:
            test_env[rand_y,rand_x].setState(3)
            num_hives = num_hives -1
# viz class demo
if __name__ == '__main__':
    dim = 50
    testEnviorment = make_test_enviorment(dim)
    #print testEnviorment.__str__()
    vizTest = viz(dim,900,900, 100)
    vizTest.draw_frame(testEnviorment)
    vizTest.dispViz()