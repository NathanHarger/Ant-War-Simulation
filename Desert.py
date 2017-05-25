# -*- coding: utf-8 -*-
import random as r
import numpy as n
from enum import Enum
from DesertAgent import DesertAgent, State
from HiveClass import Hive
# this class in in charge of controlling seasons and its effect on the desert agents
class Season(Enum):
    SPRING = 0
    SUMMER = 1
    FALL = 2
    WINTER = 3
    
    # static method that determines if a season is a rainy season
    #  returns if  season == FALL or WINTER
    @staticmethod
    def getSeasonResults(season):
        if ( season == Season.WINTER):
            return season == 2 or season == 3
        
    @staticmethod
    def getNextSeason(season):
        if season is Season.WINTER:
            return Season.SPRING
        else:
            season = Season(season.value + 1)

#SIZE = (50,50)          #A tuple of the x,y coordinates
#SEASON = Season.SPRING  #Either rainy or dry

season_length_rainy = 1    #Number of time ticks the rainy season lasts
season_length_dry = 1      #Number of ticks the dry season lasts
current_season_length = 1  #How many ticks the current season has lasted.


#The desert class will have an n x n sized grid of desert cells.
#We will simulate two seasons, rainy and dry, with user adjustable 
#variables to change the length of either, or give them a random length. 
#The desert class will keep track of the season
class Desert:

    #SIZE = (50,50)          #A tuple of the x,y coordinates
    #SEASON = Season.SPRING  #Either rainy or dry
    #Initialize a new desert using desert agents. Allows keywords to change variables.
    def __init__(self, size, num_hives):
        self.season = Season.SPRING  #Either rainy or dry
        self.size = size
        self.hives = []
        self.grid = self.random_desert_init(num_hives)
        
    def setHive(self, hive):
        self.hives.append(hive)

    def getHives(self):
        return self.hives  
    
    #Add/remove food based on season. (If it is a rainy season, add food, 
    #otherwise remove it). Then, if the current season length is equal to 
    #that season’s length, change seasons and set season length to zero.
    def update_seasons(self):
        #global SEASON, 
        current_season_length = 0
        rainy = Season.getSeasonResults(self.season)

        delta_leaf = r.randint(0, 50)

        #print SEASON
        self.season = Season.getNextSeason(self.season)


        if rainy:
            if current_season_length == season_length_rainy:
                self.add_leaves(delta_leaf)
        else:
            if current_season_length == season_length_dry:
                self.remove_leaves(delta_leaf)
        current_season_length = 1

    def add_leaves(self, delta_leaf):
        while delta_leaf != 0:
            rand_x = r.randint(0, self.size - 1)
            rand_y = r.randint(0, self.size - 1)

            # a hive cannot be placed in water, or ontop an existing hive
            if self.grid[rand_y, rand_x].getState() == State.DESERT or self.grid[rand_y, rand_x].getState() == State.FOOD:
                self.grid[rand_y, rand_x].setState(State.FOOD)
                delta_leaf = delta_leaf - 1

    # remove leafs using the random picking of grids method since
    # which cannot be performed on a numpy array of objects
    def remove_leaves(self, delta_leaf):
        while delta_leaf != 0:
            rand_x = r.randint(0, self.size - 1)
            rand_y = r.randint(0, self.size - 1)

            # a hive cannot be placed in water, or ontop an existing hive
            if self.grid[rand_y, rand_x].getState() == State.FOOD or self.grid[rand_y, rand_x].getState() == State.DESERT:
                self.grid[rand_y, rand_x].setState(State.DESERT)
                delta_leaf = delta_leaf - 1

    #create a custom desert from an existing food and moisture grid
    # hive_locations, food_location and moisture_locations are boolean
    # size x size arrays of values indicating if the grid[i,j] is a hive,
    # food or water grid
    def custom_desert_init(self, hive_locations, food_location, moisture_locations):
        desert = n.empty((self.dim, self.dim), dtype=object)
        for i in range(self.size):
            for j in range(self.size):
                water = moisture_locations[i, j]
                food = food_location[i,j]
                hive_locations = hive_locations[i, j]
                desert[j, i] = DesertAgent(0, None, 0)
                state = 0
                if water:
                    state = State.WATER
                elif hive_locations:
                    state = State.HIVE
                elif food:
                    state = State.FOOD
                desert[i, j].setState(state)
                return desert
        
    #create a random desert 
    def random_desert_init(self, num_hives):
        desert = n.empty((self.size, self.size), dtype=object)
        for i in range(self.size):
            for j in range(self.size):

                desert[j, i] = DesertAgent(0, None, 0)
                # print test_env
        self.place_food(desert)
        self.place_anthills(desert, num_hives)
        return desert
    def __str__(self):
        r=""
        for j in range(10):
            for i in range(10):
                r= r +  str(self.grid[j,i])
            r = r + "\n"
        return r

    def get_size(self):
        return self.size
    def place_food(self,env):
        count = r.randint(25,35)
        for i in range(count):
            rand_x = r.randint(0, self.size - 1)
            rand_y = r.randint(0, self.size - 1)
            self.set_leaves(env, rand_x,rand_y)


    def set_leaves(self, env, x,y):
        if x + 2 >= self.size or y+2 >= self.size:
            return
        env[y, x].setState(State.FOOD)
        env[y-1, x].setState(State.FOOD)
        env[y+1, x].setState(State.FOOD)

        env[y, x-1].setState(State.FOOD)
        env[y , x+1].setState(State.FOOD)
        env[y - 1, x-1].setState(State.FOOD)
        env[y + 1, x+1].setState(State.FOOD)
        env[y -1, x+1].setState(State.FOOD)
        env[y +1, x - 1].setState(State.FOOD)

        env[y - 2, x].setState(State.FOOD)
        env[y + 2, x].setState(State.FOOD)

        env[y - 2, x-1].setState(State.FOOD)
        env[y - 2, x+1].setState(State.FOOD)
    def place_anthills(self, test_env, num_hives):
        while num_hives != 0:
            rand_x = r.randint(0, self.size - 1)
            rand_y = r.randint(0, self.size - 1)

            # a hive cannot be placed in water, or ontop an existing hive
            if not test_env[rand_y, rand_x].getState() is 2 and not test_env[rand_y, rand_x].getState() is 3:
                test_env[rand_y, rand_x].setState(State.HIVE)
                self.setHive(Hive((rand_x, rand_y)))
                num_hives = num_hives - 1
                
    def getItem(self, x , y):
        if (y>=len(self.grid) or x >= len(self.grid)):
            return None
        return self.grid[y,x]