# -*- coding: utf-8 -*-
import random as r
import numpy as n
from enum import Enum

class HiveState(Enum):
    HEALTHY = 0
    QUEENLESS = 1
    DEAD = 2

#The hive class keeps track of the ants belonging to a single hive. 
#It has a list of ants belonging to the hive,the location of the mouth of the nest, 
#and a mask grid of pheromones belonging to the hive.
class Hive:
    
    env = 1    #The current desert the hive is located in.
    list_ants = 1 #A list of ants in the hive.
    pheremone_total = 1 #holds the pheromone values belonging to the hive.
    whater_total = 1 #shows total moisture supply for hive.
    food_total = 1 #shows total food supply for hive.
    loc_nest = (0,0) #A tuple containing the xy coordinates of the hive’s nest. 
    num_eggs = 1 #How many eggs are in the nest.
    num_pupae = 1 #How many pupae are in the nest
    num_workers_nest = 1 # How many workers are in the nest
    num_soldiers_nest = 1 #How many soldiers are in the nest.
    num_queens_nest = 1 #Number of queens in nest. Will only be 0 or 1.
    state = HiveState.HEALTHY # state of the hive
    kill_count = 0 #How many opposing ants have been killed by this hive
    amount_dead = 0 #How many ants of this hive have died
    peak_population = 0#The most population this hive has had

    
    #Initialize the hive with a certain amount of starting ants.
    def __init__(size):
        #TODO 
        return 
        
    #Add/remove food based on season. (If it is a rainy season, add food, 
    #otherwise remove it). Then, if the current season length is equal to 
    #that season’s length, change seasons and set season length to zero.
    def update_nest():
        # TODO
        #1. Food/Water stores depleted by all ants in nest multiplied by starvation/desiccation value
        #2. Queen lays eggs for if there is food for that egg
        #3. Eggs morph into pupae
        #4. Pupae morphs into ant with random caste (keeping right percentages) if there is food and a nursing worker ant, or dies if either is not true. If there is no queen, it becomes a new queen.
        #5. Create new ant agents based on rules from the Ant behavior section. Up to 8 can be created, one for each neighboring cell.
        return 

