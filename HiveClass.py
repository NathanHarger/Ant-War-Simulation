# -*- coding: utf-8 -*-
import random as r
import numpy as n
from enum import Enum

class HiveState(Enum):
    HEALTHY = 0
    QUEENLESS = 1
    DEAD = 2

class JOB(Enum):
    GATHERER = 0        # go out find food and bring it home
    WARRIOR = 1         # go out find enemy and kill it
    QUEEN = 2           # stay home reproduce
    OTHER = 3           # NOTE: if you have another job add here and explain

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
    kill_count = 1 #How many opposing ants have been killed by this hive
    amount_dead = 1 #How many ants of this hive have died
    peak_population = 1#The most population this hive has had
    desication_level = .01 #Picking random number to start of the hive adaptation
    
    #Initialize the hive with a certain amount of starting ants.
    def __init__(self, location):
        self.list_ants = n.array([])
        self.my_location = location
        self.foodLevel = 50
        #TODO 

    def getAnts(self):
        return self.list_ants
        
    def setAnts(self, ants):
        self.list_ants = n.append(self.list_ants, ants)
        
    def getLocation(self):
        return self.my_location
       
    def eatFood(self, howMuchRequested):
        if(self.foodLevel > 0):
            self.foodLevel -= howMuchRequested

            if self.foodLevel < 0:
                self.foodLevel = 0
            return howMuchRequested
        else:
            return 0   

    def getFoodLevel(self):
        return self.foodLevel

    def setFoodLevel(self, food):
        self.foodLevel = food

    def add_food(self, amt):
        self.foodLevel += amt
    
    def update_hive_food_store(self):
        self.foodLevel =  self.foodLevel - (len(self.list_ants) * self.desication_level)


    def queen_lays_eggs(self):
        if len(self.list_ants) == 0:
            return
        if(self.foodLevel / len(self.list_ants)) > (self.desication_level * len(self.list_ants)):
            self.num_eggs+=5

    def eggs_turn_into_pupae(self):
        number_of_eggs_into_pupae = r.randint(0,3)
        self.num_eggs-=number_of_eggs_into_pupae
        self.num_pupae+=number_of_eggs_into_pupae

    def evolution_of_pupae(self): 
        if(r.randint(0,10) > 5):
            self.num_workers_nest+=1
        else:
            self.num_soldiers_nest+=1

    #Add/remove food based on season. (If it is a rainy season, add food, 
    #otherwise remove it). Then, if the current season length is equal to 
    #that season’s length, change seasons and set season length to zero.
    def update_nest(self):
        # TODO
        #1. Food/Water stores depleted by all ants in nest multiplied by starvation/desiccation value
        self.update_hive_food_store()
        #2. Queen lays eggs for if there is food for that egg
        self.queen_lays_eggs()
        #3. Eggs morph into pupae
        self.eggs_turn_into_pupae()
        #4. Pupae morphs into ant with random caste (keeping right percentages) if there is food and a nursing worker ant, or dies if either is not true. If there is no queen, it becomes a new queen.
        self.evolution_of_pupae()
        #5. Create new ant agents based on rules from the Ant behavior section. Up to 8 can be created, one for each neighboring cell.
        return 
