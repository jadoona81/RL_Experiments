# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:46:17 2021

@author: HG19230
"""
import sys
sys.path.append("..\..\DQNLibrary") 
sys.path.append("..\..\DQNLibrary\MobilityPatterns") 
import numpy as np
from gridAStar import AStarGridPathPlanning
from TSP_greedy import TSP_greedy
import math 
import random

def manhattanData(xDim, yDim, block_width, street_width):

        line_manhattan =0
        column_manhattan =0
        speed= 0
        direction=0
        
        line_count = math.ceil(yDim / block_width) #number of lines (#rows)
        print(line_count)
        line_manhattan = random.randrange(1, line_count+1) #random integer between 1 and line_count.
        print(line_manhattan)
        column_count = math.ceil(xDim / block_width) #number of lines (#columns)
        print(column_count)
        column_manhattan = random.randrange(1, column_count+1) #random integer between 1 and column_count.
        print(column_manhattan)
        

        
        for i in range (20):
                    #initialize location
            k= random.random()
            if(k < 0.5):
                rand = random.random()
                X= rand * xDim
                Y = (line_manhattan)* block_width + 1
                delta = street_width*rand - (street_width/2)
                Y = Y + delta
            else:
                X = (column_manhattan)* block_width + 1
                rand= random.random()
                delta = street_width*rand - (street_width/2)
                X = X + delta
                rand = random.random()
                Y = rand * yDim
        
            print('created X and Y==========='+ str(X)+", "+ str(Y))
        
    
    
def euclideanDistance(a,b):
    a= np.array(a)
    
    b=np.array(b)
    dist = np.linalg.norm(a-b)
    return dist
    
def numHops(dist):
    
    return dist%4
    
# dist= euclideanDistance((8,8), (16,16))
# print(dist)
# print(numHops(dist))

# print(dist/4)
# print(int(dist/4))


# print(int(dist/4) -1)


# print(dist/5.657)
# print(int(dist/5.657))

# aStar= AStarGridPathPlanning(4, 4)
# path = aStar.search((0,1), (3,3))
# for i in range(len(path)):
#     print(path[i]) 
# print(path[3][0])
# print(len(path))



# total_timesteps= 20
# areaSize= np.power(48, 2) # keep area size as multiple of 4
# numTargets= 10
# coverageMajorSemiAxis= 3.5355339059327
# coverageMainorSemiAxis= 2.83 #2.53553390593275
    
    
# gridLowCorners= {(0,0), (4,0), (8,0), (12, 0), (0,4),  (4,4), (8,4), (12,4), (0,8), (4,8), (8, 8), (12, 8), (0,12), (4,12), (8,12), (12,12)}

# tsp= TSP_greedy(2, 100, 16, 4, gridLowCorners, 4)
    

manhattanData(20, 20, 4, 4)