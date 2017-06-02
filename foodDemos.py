import unittest
from Ant import *
from Desert import *
from viz import *
import matplotlib.pyplot as plt






if __name__ == '__main__':


    # ==========User Adjusatable===================
    SIM_LENGTH = 200   # How many ticks in a simulation
    DESERT_SIZE = 10  # Size of desert
    NUM_HIVES = 2  # How many hives
    AMT_ANTS_PER_HIVE = 10  # How many ants start in each hive
    # ============================================

    b1 = n.array([])
    b2 = n.array([])
    for i in range(10):
        dim = DESERT_SIZE
        num_ants_per_hive = AMT_ANTS_PER_HIVE
        vizTest = viz(dim,500,500, 100, SIM_LENGTH)
        amt_hives = NUM_HIVES
        testEnviorment = des.Desert(dim,amt_hives)
        #print testEnviorment.__str__()
        hives = testEnviorment.getHives()
        vizTest.create_stat_labels(testEnviorment)
        #print vizTest.canvas
        for i in hives:
            myAnts = n.empty(num_ants_per_hive, dtype=object)
            i.set_color(vizTest.get_random_color())
            vizTest.create_ants(myAnts, i.getLocation(), i, testEnviorment, a.JOB.GENERICINITIAL)
            i.setAnts(myAnts)

        vizTest.Run_Sim(testEnviorment)

        b  =  vizTest.dispViz()
        b1 = n.append(b1, b[0])
        b2 = n.append(b2,b [1])

    #b1 = n.reshape(b1, (10,SIM_LENGTH + 1))
    #b2 =  n.reshape(b2, (10,SIM_LENGTH + 1))

#    b1 =  n.mean(b1,axis = 0)
 #   b2 = n.mean(b2, axis = 0)
    plt.scatter(b2, b1)
    #plt.plot(range(len(b2)), b1)

    plt.xlabel("Food")
    plt.ylabel("Number of Fights")
    plt.title("Food vs Fights")
    plt.show()
    #print b

