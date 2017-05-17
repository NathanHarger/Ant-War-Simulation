import Tkinter as tk
import numpy as n

class viz:

    def __init__(self, dim, window_width, window_height):
        self.root=tk.Tk()
        self.canvas= tk.Canvas(self.root,width=window_width,height=window_height)
        self.canvas.pack()
        self.dim = dim
        self.wHeight = window_height
        self.wWidth = window_width
        self.cell = n.empty((self.dim, self.dim), dtype=object)
        self.__setup_grid__()

    def draw_frame(self):


    def __setup_grid__(self):
        size_ration = self.wWidth / self.dim
        for i in range(self.dim):
            for j in range(self.dim):
                self.cell[i, j] = self.canvas.create_rectangle(self.dim, self.dim, size_ration * i
                                                               + size_ration, size_ration * j + size_ration)

    def dispViz(self):
        self.root.mainloop()


# viz class demo
if __name__ == '__main__':
    vizTest = viz(2,300,300)
    vizTest.dispViz()
