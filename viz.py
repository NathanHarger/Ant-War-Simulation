import Tkinter as tk
import numpy as n

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
        self.testCircle = self.canvas.create_oval(4,4,12,12)
        self.delay = delay

    # function that is called by the tkinter canvas that updates ojects in sim every frame
    def draw_frame(self):
        self.canvas.move(self.testCircle, 5, 5)
        self.draw_colors_test()
        self.canvas.after( self.delay, self.draw_frame)


    def __setup_grid__(self):
        size_ration = self.wWidth / self.dim
        for i in range(self.dim):
            for j in range(self.dim):
                self.cell[i, j] = self.canvas.create_rectangle(self.dim, self.dim, size_ration * i
                                                               + size_ration, size_ration * j + size_ration)

    # test that shows animation of object moving and changing color
    def draw_colors_test(self):

        # color changing from
        # http://stackoverflow.com/questions/11340765/default-window-colour-tkinter-and-hex-colour-codes
        rgb = tuple(n.random.randint(0,256, (3)))
        mycolor = '#%02x%02x%02x' % rgb
        self.canvas.itemconfig(self.testCircle, fill=mycolor)
    def dispViz(self):

        self.root.mainloop()


# viz class demo
if __name__ == '__main__':
    vizTest = viz(2,300,300, 100)
    vizTest.draw_frame()
    vizTest.dispViz()
