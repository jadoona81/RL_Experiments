# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:02:43 2021

@author: HG19230
"""
import random
from MobilityPatterns.ManhattanMobilityMatlab import ManhattanMobileTarget
from MobilityPatterns.RPGM_Mobility import RPGM_Mobility
#from GenerateMobilityData import generateMobilityData
import numpy as np

tsScale= 333/5


def testManhattan():
    manMob= ManhattanMobileTarget(999, 999, 333, 333, 3/3.6, 5/3.6, True, tsScale)
    print(manMob.speed)
    print(manMob.X)
    print(manMob.Y)
    
    coords=[]
    
    for i in range(10):
        manMob.move()
        coords.append((manMob.X, manMob.Y))
        print(manMob.X)
        print(manMob.Y)
#        print(manMob.currCell)
        print('*************************************************************')
        
    
    print(tsScale)
    movePerTimeStep= manMob.speed * tsScale
    print(movePerTimeStep)
    
    print(coords)
    
def generateManhattan():
    numTimeSteps=20
    numNodes=5
    xDim= 4998
    yDim= 4998
    cellSideSize= 833
    mobilityModel= 'ManhattanPython'
 #   numCellsPerSide= 
    
   # generateMobilityData(gridLowCorners, numTimeSteps, numNodes, xDim, yDim, cellSideSize, mobilityModel, modelName, randomLoc, timeStepScale, numCellsPerSide)


# mixVals={'k1': 45, 'k2':[1,2,3], 'k3':{'a','c'}}
# print(mixVals['k1'])

# arr=np.array([[1,2,3,4]])

# r,c= len(arr), len(arr[0])
# print(r)
# print(c)
# print(np.shape(arr))
# arr.resize(r+1, c)
# arr[r][0]= 9
# print(np.shape(arr))
# print(arr)
        

# (xDim, yDim, numGroups, radiusGroup, min_speed, max_speed, numTargets, maxTime):

def testRPGM():
    print(tsScale)

    #xDim, yDim, numGroups, numNodes, maxTime, timeStepsScale
    mob= RPGM_Mobility(999, 999, 1, 2, 7, tsScale)
    mob.generateMobility()
    #mob.moveNodes()


#testRPGM()
testManhattan()

# def randomlyAssignTargetsToGroups():
#         number_targets= 10
#         number_groups= 3
#         targets= list(range(0, number_targets))
        
#         while number_targets > 0 and number_groups > 0:
#             team = random.sample(targets, int(number_targets/number_groups))

            
#             for x in team:
#                 targets.remove(x)
            
#             number_targets -= int(number_targets/number_groups)
#             number_groups -= 1
#             print(team)
            
#randomlyAssignTargetsToGroups()