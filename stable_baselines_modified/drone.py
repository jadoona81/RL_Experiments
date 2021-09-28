# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:34:26 2020

@author: HG19230
"""

import numpy as np
import random
import math
#import pandas as pd
#from env import final_states

from random import randrange

class drone (object):
  
    def __init__(self, areaSize, learning_rate, reward_decay, gridLowCorners, cellSideSize, targets, actions):
        
         self.altitude= 20#2.5, 5, 10, 20
         self.areaSize= areaSize
         #self.coordinates=(random.random()*self.areaSize, random.random()*self.areaSize, self.altitude)
         
         self.angle= 0 #radiant
         self.speed=5 #m/s
         
         self.cameraAngle= 30
         self.AOV= 64 #degrees
         
         self.UpwardsPC_W = 70.09 
         self.UpwardsEnergyPerMeter_J = 15.62
         self.DownwardsPC_W = 63.74
         self.DownwardsEnergyPerMeter_J= 12.75
         self.HorizontalPC_W = 65.94        
         self.horizontalEnergyPerMeter_J = 13# 13 #19 #13.19
         self.energyCapacity= 117000 #68400 for 12 mins @ 13 J #300000 #J
         self.hoveringEnergyPerSec_J= 12# 12;

        # (2.2, 3.9): https://www.sciencedirect.com/science/article/pii/S0380133019300619#t0005
         self.coverageMajorSemiAxis=  3.53553390593275 #4 #3.9
         self.coverageMinorSemiAxis=  2.53553390593275 #2.2

         self.rotationSpeed= 250 #radiants per sec
         self.rotationEnergyPerRadiant = 0.048 #Joules/radiant
         
         self.reset(gridLowCorners, cellSideSize, targets)
         
        # List of actions
         self.actions = actions
        # Learning rate
         self.lr = learning_rate
        # Value of gamma
         self.gamma = reward_decay
        # Value of epsilon
        # self.calculateEpsilon()
        # Creating full Q-table for all cells
     #    self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # Creating Q-table for cells of the final route
     #    self.q_table_final = pd.DataFrame(columns=self.actions, dtype=np.float64)
         self.epsilon=1.0
         self.initialLocation= (2,2)
         self.initialCoordinates=(0,0)
        
         
    # def calculateEpsilon(self):
    #     # if self.totalEnergy < (self.energyCapacity/4.0):
    #     #     self.epsilon= 0.8
    #     # elif  self.totalEnergy >= (self.energyCapacity/4.0) and self.totalEnergy < (self.energyCapacity/2.0):
    #     #     self.epsilon= 0.4
    #     # else:
    #     #     self.epsilon= 0
    #     self.epsilon = self.epsilon*0.999
        
        
    #  # Function for choosing the action for the agent
    # def choose_action(self, observation):
        
    #     # Checking if the state exists in the table
    #     self.check_state_exist(observation)
    #     if np.random.uniform() < self.epsilon:  # Explore: Choosing random action

    #         action = np.random.choice(self.actions)
    #         print(" EXPLORINGGGGGGG  ^^^^^^^^^^^^")


    #     else: # Exploit: Choosing the best action

    #         state_action = self.q_table.loc[observation, :]
    #         state_action = state_action.reindex(np.random.permutation(state_action.index))
    #         action = state_action.idxmax()
    #         print(" EXPLOITING  VVVVVVVVVVVV")

            
    #     print("Chosen Action: "+ str(action))    
    #     return action
    
    # # Function for learning and updating Q-table with new knowledge
    # def learn(self, state, action, reward, next_state, done):
    #     # Checking if the next step exists in the Q-table
    #     self.check_state_exist(next_state)

    #     # Current state in the current position
    #     q_predict = self.q_table.loc[state, action]

    #     # Checking if the next state is free or it is obstacle or goal
    #     if not done: #if next_state != 'goal' or next_state != 'obstacle':
    #         q_target = reward + self.gamma * self.q_table.loc[next_state, :].max()
    #     else:
    #         q_target = reward

    #     # Updating Q-table with new knowledge
    #     self.q_table.loc[state, action] += self.lr * (q_target - q_predict)

    #     print("Learning: "+ str(state )+ "- "+ str(action)+" >>> "+ str(self.q_table.loc[state, action]))    

    #     return self.q_table.loc[state, action]

    #     # Adding to the Q-table new states
    # def check_state_exist(self, state):
    #     if state not in self.q_table.index:
    #         self.q_table = self.q_table.append(
    #             pd.Series(
    #                 [0]*len(self.actions),
    #                 index=self.q_table.columns,
    #                 name=state,
    #             )
    #         )

    # # Printing the Q-table with states
    # def print_q_table(self, final_states):
    #     # Getting the coordinates of final route from env.py
    #     e = final_states

    #     # Comparing the indexes with coordinates and writing in the new Q-table values
    #     #for i in range(len(e)):
    #      #   state = str(e[i])  # state = '[5.0, 40.0]'
    #         # Going through all indexes and checking
    #     for state in e:  
    #         for j in range(len(self.q_table.index)):
    #             if self.q_table.index[j] == state:
    #                 self.q_table_final.loc[state, :] = self.q_table.loc[state, :]

    #     print()
    #     print('Length of final Q-table =', len(self.q_table_final.index))
    #     print('Final Q-table with values from the final route:')
    #     print(self.q_table_final)

    #     print()
    #     print('Length of full Q-table =', len(self.q_table.index))
    #     print('Full Q-table:')
    #     print(self.q_table)
        
        
        

    def reset(self, gridLowCorners, cellSideSize, targets):
         print("resetting=============")
         self.totalEnergy= 0.0
         self.totalTravelledDistance=0.0
         self.totalRotations=0.0
         self.missionTime=0.0         
         self.numStops=0 
         self.numTargetsCoveredInitially=0
         self.coveredTargets={}
         self.route=[]
        
    def resetLocation(self):
        self.currentCell= self.initialLocation
        self.coordinates= self.initialCoordinates
        print('reset drone location: ')
        print(self.currentCell)

    def setRandomInitialLocation(self, gridCells, cellSideSize, targets):
        self.currentCell= (0,0) #gridCells[randrange(len(gridCells))] #(0,0) #
        x= self.currentCell[0]+(cellSideSize/2)
        y= self.currentCell[1]+(cellSideSize/2)
        #x=2.0
        #y=2.0
        self.coordinates= (x,y,self.altitude)
        self.route.append(self.currentCell)
        print("selected start location: "+ str(self.currentCell[0])+ ', ' +str(self.currentCell[1]))
        self.initialLocation=self.currentCell
        self.initialCoordinates= self.coordinates
        

    def hover(self, targetsVelocity, cellArea, targets, cellSideSize):
        print("hovering============="+ str(self.currentCell[0])+ str(self.currentCell[1]))

        time= cellArea/ targetsVelocity
        ener=  (time * self.hoveringEnergyPerSec_J)
        self.totalEnergy+= ener
        
        covTPerc= self.filterCoveredTargets(targets, False, cellSideSize)
        enerConsPerc= ener/self.energyCapacity
        
        return [covTPerc, enerConsPerc]
    
    def rotate(self, targets, cellSideSize):
        
        print("rotating============="+ str(self.currentCell[0])+ str(self.currentCell[1]))
        angle= math.radians(180)
        ener= angle * self.rotationEnergyPerRadiant
        self.totalEnergy+= ener
        
        covTPerc= self.filterCoveredTargets(targets, True, cellSideSize)
        enerConsPerc= ener/self.energyCapacity
        
        return [covTPerc, enerConsPerc]
        
        
    def move(self, cellLowCorner, cellSideSize, targets):
            
         print("agent move function == before moving target cell low corner:")
         print(cellLowCorner)
         cellCenterX= cellLowCorner[0] + (cellSideSize/2)
         cellCenterY= cellLowCorner[1] + (cellSideSize/2)
         
         a= (self.coordinates[0], self.coordinates[1])
         b=  (cellCenterX, cellCenterY)
         travelDist= self.euclideanDistance(a,b)
          
        # print("dist: "+str(travelDist))
         ener= travelDist*self.horizontalEnergyPerMeter_J
         
         self.currentCell= cellLowCorner

         x= self.currentCell[0]+(cellSideSize/2)
         y= self.currentCell[1]+(cellSideSize/2)
         self.coordinates= (x,y,self.altitude)
        
         print("moved============= ("+ str(self.currentCell[0])+ ", "+str(self.currentCell[1])+")")
         print("moved=============coords: ("+ str(self.coordinates[0])+ ", "+ str(self.coordinates[1])+")")

         self.route.append(self.currentCell)

         self.totalEnergy+= ener
        
        # covTPerc= self.filterCoveredTargets(targets, False, cellSideSize)
         numCovered= self.filterCoveredTargets(targets, False, cellSideSize)
         enerConsPerc= ener/self.energyCapacity
        
         return [numCovered, enerConsPerc]
        
    def filterCoveredTargets(self, targets, isRotate, cellSideSize):
        numNewTargets= 0
        
       # print("filter covered targets ")
        if isRotate:
            
            for t in targets:
                if not t.ID in self.coveredTargets:
                    if self.isTargetInsideCell(t, self.currentCell, cellSideSize):
                        numNewTargets+=1
                        self.coveredTargets[t.ID]=t
                
        else:
                
            for target in targets:
                if not target.ID in self.coveredTargets:
                    
                    t= target.currentLocation
                    a= (self.coordinates[0], self.coordinates[1])
                    b= (t[0], t[1])
                   # print(a)
                   # print(b)
                   # print(t) 
                    print("dist to t "+ str(target.ID)+" -- " +str(self.euclideanDistance(a, b)))
                    if self.euclideanDistance(a, b) > self.coverageMajorSemiAxis:
                        continue
                    elif self.isTargetInsideCell(t, self.currentCell, cellSideSize):
                        numNewTargets+=1
                        self.coveredTargets[target.ID]=target
                        
                    elif self.pointInEllipse(t[0], t[1]):
                        numNewTargets+=1
                        self.coveredTargets[target.ID]=target


       # numtargets= len(targets)- self.numTargetsCoveredInitially    
       # return (numNewTargets/numtargets)
        return numNewTargets
        
    def isTargetInsideCell(self, t, cellBottomLeft, cellSideSize):
        print("isTargetInsideCell "+ str(t[0]) +", "+ str(t[1]))
        print("topCOrner: ")
        cellTopCorner= (cellBottomLeft[0]+cellSideSize, cellBottomLeft[1]+cellSideSize)
        print(cellTopCorner)

        print("bottomLeft: ")
        print(cellBottomLeft)
        if (t[0] >= cellBottomLeft[0] and t[0] <= cellTopCorner[0] and 
            t[1] >= cellBottomLeft[1] and t[1] <= cellTopCorner[1]) : 
            print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY Inside Cell: "+ str(t[0]) +", "+ str(t[1]))
            return True
        else : 
            print("not covered -----------------------"+ str(t[0]) +", "+ str(t[1]))
            return False
   
    def euclideanDistance(self, a,b):
        a= np.array(a)
        b=np.array(b)
        dist = np.linalg.norm(a-b)
        return dist
        
    
    def pointInEllipse(self, xp,yp):
        #tests if a point[xp,yp] is within
        #boundaries defined by the ellipse
        #of center[x,y], diameter d D, and tilted at angle
        x= self.coordinates[0]
        y= self.coordinates[1]
        cosa=math.cos(self.angle)
        sina=math.sin(self.angle)
        dd=self.coverageMinorSemiAxis/2*self.coverageMinorSemiAxis/2
        DD=self.coverageMajorSemiAxis/2*self.coverageMajorSemiAxis/2
    
        a =math.pow(cosa*(xp-x)+sina*(yp-y),2)
        b =math.pow(sina*(xp-x)-cosa*(yp-y),2)
        ellipse=(a/dd)+(b/DD)
    
      #  print("pointInEllipse "+ str(xp)+ ", "+ str(yp) +" ellipse: "+ str( ellipse))

        if ellipse <= 1:
            print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY Inside Ellipse"+ str(xp) +", "+ str(yp))
            return True
        else:
          #  print("not covered -----------------------"+ str(xp) +", "+ str(yp))
            return False