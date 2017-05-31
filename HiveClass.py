# -*- coding: utf-8 -*-
import random as r
import numpy as n
from enum import Enum
import Desert as ds
import DesertAgent as ANT_agent
import math

class HiveState(Enum):
    HEALTHY = 0
    QUEENLESS = 1
    DEAD = 2
    MILDAGRESSION = 3
    SEVEREAGRESSION = 4


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
    total_number_ants = 0  #Keeps track of total ants in colony
    color = 0 #Color of ants emerging from the Hive 

    #Initialize the hive with a certain amount of starting ants.
    def __init__(self, location, initialFoodLevel):
        self.list_ants = n.array([])
        self.my_location = location
        self.foodLevel = initialFoodLevel
        self.initialFoodLevel = initialFoodLevel
        self.scouted_food_locations = []

    def setFoodLoc(self, x_loc, y_loc):
        if ( (x_loc, y_loc) not in self.scouted_food_locations):
            self.scouted_food_locations.append((x_loc, y_loc))

    def getAllFoodLoc(self):
        return self.scouted_food_locations

    def getFoodLoc(self):
        if (len(self.scouted_food_locations) != 0 ):
            return self.scouted_food_locations.pop()
        else:
            return (self.my_location[0], self.my_location[1])
    
    def getAnts(self):
        return self.list_ants

    def get_ant_count(self):
        return len(self.list_ants)

    def setAnts(self, ants):
        self.list_ants = n.append(self.list_ants, ants)
        self.total_number_ants = len(self.list_ants)
        
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

    def get_number_of_ants(self):
       return self.total_number_ants
    
    def update_hive_food_store(self):
        if(self.foodLevel > 0):
            self.foodLevel =  self.foodLevel - (len(self.list_ants) * self.desication_level)


    def queen_lays_eggs(self):
        if len(self.list_ants) == 0:
            return
        if(self.foodLevel / len(self.list_ants)) > (self.desication_level * len(self.list_ants)):
            self.num_eggs+=5

    def eggs_turn_into_pupae(self):
        if(self.num_eggs > 0):
            number_of_eggs_into_pupae = r.randint(0,self.num_eggs)
            self.num_eggs-=number_of_eggs_into_pupae
            self.num_pupae+=number_of_eggs_into_pupae

    def setListAnts(self, a):
        self.list_ants = a

    def evolution_of_pupae(self): 
        if(r.randint(0,10) > 5):
            self.num_workers_nest+=1
            self.total_number_ants+=1
        else:
            self.num_soldiers_nest+=1
            self.total_number_ants+=1

    def update_aggression_level(self):
        if(self.foodLevel / len(self.list_ants)< self.desication_level or self.num_queens_nest < 1): 
            self.state = HiveState.SEVEREAGRESSION
            print("Aggression level of Hive is severe")
        if (self.foodLevel / len(self.list_ants)< (self.desication_level  + 2)):
            self.state = HiveState.MILDAGRESSION
            print("Aggression level of Hive is Mild")
        else:
             self.state = HiveState.HEALTHY
             #print("Hive is healthy")

    def if_hive_needs_to_replenish_food(self):
        return (self.foodLevel < self.initialFoodLevel)

    def set_color(self, color):
        self.color = color
    def get_color(self):
        return self.color

    def dispatch_number_gathers(self):
        number_of_gathers = 0
        if(self.if_hive_needs_to_replenish_food()):
         if(self.total_number_ants>=1):
            if(self.state == HiveState.MILDAGRESSION):
                number_of_gathers = int(math.floor(len(self.list_ants) * .01))
                self.num_workers_nest -= number_of_gathers
                self.total_number_ants -= number_of_gathers
                number_of_gathers = n.empty(number_of_gathers, dtype=object)
                return number_of_gathers
            if(self.state == HiveState.SEVEREAGRESSION):
                number_of_gathers = int(math.floor(len(self.list_ants) * .02))
                self.num_workers_nest -= number_of_gathers
                self.total_number_ants -= number_of_gathers
                number_of_gathers = n.empty(number_of_gathers, dtype=object)
                return number_of_gathers
            else:
                if(self.total_number_ants>=1):
                   
                    number_of_gathers = int(math.floor(len(self.list_ants) * .001))
                    #Send the last ant out to find food
                    if(number_of_gathers == 0):
                        number_of_gathers = 1
                    self.num_workers_nest -= number_of_gathers
                    self.total_number_ants -= number_of_gathers
                    number_of_gathers = n.empty(number_of_gathers, dtype=object)
                    return number_of_gathers
   
    def dispatch_number_of_soliders(self):
        if(self.state == HiveState.MILDAGRESSION):
            number_solider_ants_to_create = int(math.floor(len(self.list_ants) * .01))
            self.total_number_ants -= number_solider_ants_to_create
            return n.empty(number_solider_ants_to_create, dtype=object)
        if((self.state == HiveState.SEVEREAGRESSION)):
            number_solider_ants_to_create = int(math.floor(len(self.list_ants) * .02))
            self.total_number_ants -= number_solider_ants_to_create
            return n.empty(number_solider_ants_to_create, dtype=object)

    #Add/remove food based on season. (If it is a rainy season, add food, 
    #otherwise remove it). Then, if the current season length is equal to 
    #that season’s length, change seasons and set season length to zero.
    def update_nest(self):
        if (len(self.list_ants) > 0):
            #1. Food/Water stores depleted by all ants in nest multiplied by starvation/desiccation value
            #self.update_hive_food_store()
            #2. Queen lays eggs for if there is food for that egg
            self.queen_lays_eggs()
            #3. Eggs morph into pupae
            self.eggs_turn_into_pupae()
            #4. Pupae morphs into ant with random caste (keeping right percentages) if there is food and a nursing worker ant, or dies if either is not true. If there is no queen, it becomes a new queen.
            self.evolution_of_pupae()
            #5. Update agression level to manipulate how to dispatch ants from Hive
            self.update_aggression_level()
        
        return 
