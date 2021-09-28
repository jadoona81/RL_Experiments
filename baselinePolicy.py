# -*- coding: utf-8 -*-

import numpy as np
import OneDroneMobileTargetsEnv

#up=0, down=1, r= 3, left=2, 
def nextScanAction(scan, currCell, cellSideSize, areaOneDimSize):
    action=-1
    
    if(scan=='RU'):
        if(currCell[0] < (areaOneDimSize-cellSideSize)):
            print('case 1')
            action=3
        else:
            if(currCell[1] < (areaOneDimSize-cellSideSize)):
                print('case 2')
                action=0
                scan='LU'
            else:
                print('case 3')
                action=2
                scan='LD'
                
    elif(scan=='RD'):
         if(currCell[0] < (areaOneDimSize-cellSideSize)):
            print('case 4')
            action=3
         else:
            if(currCell[1] > 0):
                print('case 5')
                action=1
                scan='LD'
            else:
                print('case 6')
                action=2
                scan='RU'
        
    elif(scan=='LU'):
        
        if(currCell[0] > 0):
                print('case 7')
                action=2
        else:
            if(currCell[1] < (areaOneDimSize-cellSideSize)):
                print('case 8')
                action=0
                scan='RU'
            else:
                print('case 9')
                
    elif(scan=='LD'):
        
        if(currCell[0] > 0):
            print('case 10')
            action=2
        else:
            if(currCell[1] > 0):
                print('case 11')
                action=1
                scan='RD'
            else:
                print('case 12')
                action= 3
                scan='RU'
    
    return [scan, action]




def runBaselinePolicy(env, drone):
    
    finalReward=0
    scan = 'RU'
    steps=0
    actions=[]

    while len(drone.coveredTargets) < env.numTargets and steps < env.stepsLimit:
            print(drone.coveredTargets.keys())
            [scanOut, action]= nextScanAction(scan, drone.currCell, env.cellSideSize, env.areaDimLimit)
            scan= scanOut
            [next_state, reward, done, _]= env.step(action)
            print(env.TargetsCoverageIndicators)
            print(reward)
            finalReward+=reward
            
            steps+=1
            actions.append(action)
            print(len(env.targets))
            print( len(drone.coveredTargets))
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            
    return[steps-1, finalReward, drone.totalEnergy,  len(drone.coveredTargets)]       

