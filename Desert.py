# -*- coding: utf-8 -*-
import random as r
import numpy as n
from enum import Enum

# this class in in charge of controlling seasons and its effect on the desert agents
class Season(Enum):
    SPRING = 0
    SUMMER = 1
    FALL = 2
    WINTER = 3
    
    # return the effect of a season. Like level of rainfal or food
    def getSeasonResults(season):
        #TODO 
        return 

SIZE = (50,50)          #A tuple of the x,y coordinates
SEASON = Season.SPRING  #Either rainy or dry

season_length_rainy = 1    #Number of time ticks the rainy season lasts
season_length_dry = 1      #Number of ticks the dry season lasts
current_season_length = 1  #How many ticks the current season has lasted. 


#The desert class will have an m x n sized grid of desert cells. 
#We will simulate two seasons, rainy and dry, with user adjustable 
#variables to change the length of either, or give them a random length. 
#The desert class will keep track of the season
class Desert:
    
    #Initialize a new desert using desert agents. Allows keywords to change variables.
    def __init__():
        #TODO 
        return 
        
    #Add/remove food based on season. (If it is a rainy season, add food, 
    #otherwise remove it). Then, if the current season length is equal to 
    #that season’s length, change seasons and set season length to zero.
    def update_seasons():
        #TODO 
        return 

    #create a custom desert from an existing food and moisture grid
    def custom_desert_init(hive_locations, food_location, moisture_locations):
        #TODO 
        return 
        
    #create a random desert 
    def random_desert_init(num_hives):
        #TODO 
        return    
    
