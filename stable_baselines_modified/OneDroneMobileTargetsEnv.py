# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:32:12 2020
REF: https://github.com/sichkar-valentyn/Reinforcement_Learning_in_Python/blob/master/RL_Q-Learning_E1/env.py
@author: HG19230
"""

import numpy as np  # To deal with data in form of matrices
import random
#import tkinter as tk  # To build GUI
from mobileTarget import mobileTarget
import gym
from gym import spaces
from drone import drone
import math
import time
route = {}

class OneDroneMobileTargetsEnv (gym.Env):
    metadata = {'render.modes': ['human']}

    class state(object):
        def __init__(self, ID, x, y, t):
            self.cell= (x,y)
            self.stateID= ID

            self.numUnCoveredTargets= 0
            self.timeStep=t
            
        def addTarget(self):
            self.numUnCoveredTargets+=1
            print("cell "+ str(self.cell[0])+", "+str(self.cell[1])+": "+ str(self.numUnCoveredTargets))
        
        def cellCovered(self):
            self.numUnCoveredTargets= 0
            print("cell covered "+ str(self.numUnCoveredTargets))

            
        
    def __init__(self, areaSize, numTargets, droneCoverageDiameter):
        
        super(OneDroneMobileTargetsEnv, self).__init__()
        
        self.areaDimLimit= np.sqrt(areaSize)
        print("areaDimLimit: "+ str(self.areaDimLimit))
        self.targets= []
        
        self.targetsVelocity= 1.4 #m/s
        self.gridlowCorners=[]

        self.states={}

        self.state_size= numTargets+1

        self.buildGrid(areaSize, droneCoverageDiameter)    
        
        self.numTargets= numTargets
        self.n_actions = 9

        self.action_space= spaces.Discrete(self.n_actions)
        self.observation_space= spaces.Box(low=0, high= 1000, shape=(1,(self.numTargets+1)))
        self.timeStep=0
        
        print(self.states)
        for i in range(0, numTargets):
            #(self, initiLocX, initialLocY, gridLowCorners, numCellsPerSide, cellSideSize, dimLimit):

            t= mobileTarget(i, random.random()*self.areaDimLimit, random.random()*self.areaDimLimit, self.gridlowCorners, self.numCellsPerSide, self.cellSideSize, self.areaDimLimit)
            tCell= self.findCellForPoint(t.currentLocation[0], t.currentLocation[1])            
            state= self.states[tCell]
            state.addTarget()
            self.targets.append(t)
            
        self.epReward=0
        self.numEpisodes=0
        print(self.targets)

        with open("stats.dat", "w") as statsfile:
            statsfile.write('EpNum'+'\t'+'EpSteps'+'\t'+'Reward'+'\t'+'ener'+'\t'+'dist'+'\n')
        
        
        #add hovering later
        #self.action_space = ['up', 'down', 'left', 'right', 'dUpL', 'dUpR', 'dDwnL', 'dDwnR','hover']
        
        #for i in range(len(self.gridlowCorners)):
         #   self.action_space.append(''+str(i))
        
        print(self.action_space)
        
        print(self.n_actions)
        
        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.i = 0

        # Writing the final dictionary first time
        self.c = True

        # Showing the steps for longest found route
        self.longest = 0

        # Showing the steps for the shortest route
        self.shortest = 0
       
        
    def findCellForPoint(self, xp, yp):
        
        xCell= math.floor(xp/4.0)
        yCell= math.floor(yp/4.0)
        
        xCell*=4
        yCell*=4
        
        return(xCell, yCell)
        
        
        
        
    def placeDrone(self, drone):
        drone.setRandomInitialLocation(self.gridlowCorners, self.cellSideSize, self.targets)
        covTPerc= drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
        drone.numTargetsCoveredInitially= len(drone.coveredTargets)
        self.drone=drone
        
    def buildGrid(self, areaSize, droneCoverageDiameter):
        
        self.cellSideSize=  self.calculateGridCellSize(droneCoverageDiameter)
        print("side:"+ str(self.cellSideSize))

        self.areaNumCells= int(round(areaSize / np.power(self.cellSideSize, 2)))
        print(self.areaNumCells)

        areaDimMax= np.sqrt(areaSize)
        print(areaDimMax)
        
        self.maxLowerDim= self.areaDimLimit-self.cellSideSize
        self.cornerCells= [(0,0), (0, self.maxLowerDim), (self.maxLowerDim, 0), (self.maxLowerDim, self.maxLowerDim)]

        self.OtherSideCells= []

        self.numCellsPerSide= int(areaDimMax/self.cellSideSize)
        indx=0
        for x in range (0, self.numCellsPerSide):
            for y in range (0, self.numCellsPerSide):
                print(x, y)
                cell= (x*self.cellSideSize,y*self.cellSideSize)
                self.gridlowCorners.append(cell)
                currState= self.state( self.gridlowCorners.index(cell), x*self.cellSideSize,y*self.cellSideSize, 0)
                self.states[(x*self.cellSideSize,y*self.cellSideSize)]=currState

                
                indx+=1
                if(x ==0  or y==0 or x==self.numCellsPerSide or y==self.numCellsPerSide):
                     self.OtherSideCells.append(cell)     

        self.OtherSideCells  = list(set(self.OtherSideCells) - set(self.cornerCells))

        # xlin = np.linspace(0+self.cellSideSize, areaDimMax, self.areaNumCells);
        # [X,Y] = np.meshgrid(xlin, xlin,  sparse=True)

        # #print(X)
        # Y= np.rollaxis(Y, 0, Y.ndim)
        # #print(Y)
        # self.gridTopCorners= list(zip(X[0], Y[0]))

        # gridCenters = np.mgrid[self.cellSideSize/2:self.areaNumCells*self.cellSideSize:self.cellSideSize, 
        #                        self.cellSideSize/2:self.areaNumCells*self.cellSideSize:self.cellSideSize]
        # gridCenters = np.rollaxis(gridCenters, 0, gridCenters.ndim)
         
        # print(gridCenters)

        print(self.gridlowCorners)
        
    def calculateGridCellSize(self, droneCoverageDiameter):
        squareDiagonal= droneCoverageDiameter
        squareSide= squareDiagonal / np.sqrt(2)
        return int(round(squareSide))
    
    # Function to refresh the environment
    def render(self):
        #time.sleep(0.03)
        self.update()


     # Function to reset the environment and start new Episode
    
    def reset(self):
        
        if(self.timeStep> 0):
            self.numEpisodes+=1
            with open("stats.dat", "a") as statsfile:
                statsfile.write(str(self.numEpisodes)+'\t'+str(self.timeStep)+'\t'+str(self.epReward)+'\t'+str(self.drone.totalEnergy)+'\t'+str(self.drone.totalTravelledDistance)+'\n')


        #self.update()
        #time.sleep(0.1)
        self.timeStep=0
        self.epReward=0
        self.drone.reset(self.gridlowCorners, self.cellSideSize, self.targets)
        self.drone.resetLocation()
        
        for s in self.states:
            self.states[s].cellCovered()
            
        for t in self.targets:
            t.reset()
            cell= t.initialCell
            self.states[cell].addTarget()
            
        
        [covTPerc, newCovTsIDs]= drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
        drone.numTargetsCoveredInitially= len(drone.coveredTargets)
        for t in newCovTsIDs:
            self.TargetsCoverageIndicators[t]= 1

        print("numTargets covered initially:  "+ str(self.drone.numTargetsCoveredInitially))
        #
        # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        currState= self.states[self.drone.currentCell]
        remTs=  self.numTargets - len(self.drone.coveredTargets)
        stateInfo = [currState.stateID] + list(self.drone.coveredTargets.keys())+[-1]*remTs
        reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])

        #return [currState.stateID, currState.numUnCoveredTargets, len(self.drone.coveredTargets)]#[currState.stateID, self.timeStep]
        return reshapedStateInfo#[currState.stateID, self.timeStep]

    # Function to get the next observation and reward by doing next step
    def step(self, action):
        currState= self.states[self.drone.currentCell]
         
        print("env step function +++++++++++++State: ("+str(self.drone.coordinates[0])+","+str(self.drone.coordinates[1])+","+str(currState.numUnCoveredTargets)+") >>> Action: "+ str(action)+" +++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        reward_scale= 50
        
        # for t in self.targets:           
        #     t.move(self.cellSideSize, self.areaDimLimit)
        
        # Current state of the drone
        base_action = np.array([0, 0])
        
         # Updating next state according to the action

        # Action 'up'
        #if action == 0:
        #   [cov, ener]= drone.rotate(self.targets, self.cellSideSize)
        # Action 'hover'
        # elif action == 1:
        #    [cov, ener]= drone.hover(self.targetsVelocity, self.cellSideSize*2, self.targets,  self.cellSideSize)
        # # Action 'goToCell action-2'
       # else:
        #    cell= self.gridlowCorners[action-1] #[action-2]
        
        
        #['up', 'down', 'left', 'right', 'dUpL', 'dUpR', 'dDwnL', 'dDwnR','hover']

        if action == 0: #up: increase y 
            cell= (self.drone.currentCell[0], self.drone.currentCell[1]+ self.cellSideSize)
        elif action == 1: #down: decrease y
            cell= (self.drone.currentCell[0], self.drone.currentCell[1]- self.cellSideSize)
        elif action == 2: #left: decrease x
            cell= (self.drone.currentCell[0]-self.cellSideSize , self.drone.currentCell[1])
        elif action == 3: #right: increase x
            cell= (self.drone.currentCell[0]+self.cellSideSize , self.drone.currentCell[1])
        elif action == 4: #dUpL:  increase y , decrease x
            cell= (self.drone.currentCell[0]-self.cellSideSize , self.drone.currentCell[1]+self.cellSideSize)
        elif action == 5: #dUpR:  increase y , icrease x
            cell= (self.drone.currentCell[0]+self.cellSideSize , self.drone.currentCell[1]+self.cellSideSize)
        elif action == 6: #dDwnL:  decrease y , decrease x
            cell= (self.drone.currentCell[0]-self.cellSideSize , self.drone.currentCell[1]-self.cellSideSize)
        elif action == 7: #dDwnR:  decrease y , increase x
            cell= (self.drone.currentCell[0]+self.cellSideSize , self.drone.currentCell[1]-self.cellSideSize)
        else:
            cell= self.drone.currentCell
            [reward, newCovTsIDs]= self.drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
            hovT= self.cellSideSize/self.drone.speed
            ener=  (hovT * self.drone.hoveringEnergyPerSec_J)
            self.drone.totalEnergy+= ener
        
            reward= reward/self.numTargets
            #targetsCoveredAfter= drone.coveredTargets
            for t in newCovTsIDs:
                self.TargetsCoverageIndicators[t]= 1

            if(reward==0):
                reward = -1
            else:
                reward*=reward_scale

            
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))

            if(self.drone.totalEnergy > self.drone.energyCapacity) or (len(self.drone.coveredTargets) == len(self.targets)):
            #    reward= -100
                    done= True
                    print(str(self.timeStep)+"--DONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNE")
                    #time.sleep(60000)

                    print("done at hovering")
            else:
                done= False
                
            self.timeStep+=1
            
            currState= self.states[cell]
            newState= self.state(currState.stateID, currState.cell[0], currState.cell[1], self.timeStep)
            self.epReward+=reward
            #return [[newState.stateID, self.timeStep], reward, done, {}]
#            return [[newState.stateID, reward, len(self.drone.coveredTargets)], reward, done, {}]
            remTs=  self.numTargets - len(self.drone.coveredTargets)
            stateInfo = [newState.stateID] + list(self.drone.coveredTargets.keys())+[-1]*remTs
            reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
            return [reshapedStateInfo, reward, done, {}]
       
        #if action is not hovering
        nextX= cell[0]
        nextY= cell[1]
    
        if(nextY >= self.areaDimLimit or nextX>=self.areaDimLimit or nextX<0 or nextY<0):
            cell= self.drone.currentCell
            currState= self.states[cell]       
            print('nextCell: ('+ str(nextX)+", "+ str(nextY)+')'+ str(currState.numUnCoveredTargets))    

            [reward, newCovTsIDs]= drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
            reward=reward/self.numTargets
            print(newCovTsIDs)
            for t in newCovTsIDs:
                print(t)
                print(self.TargetsCoverageIndicators[t])
                self.TargetsCoverageIndicators[t]=1
                
            hovt= self.cellSideSize/self.drone.speed
            ener=0
            ener=  (hovt * self.drone.hoveringEnergyPerSec_J)
            self.drone.totalEnergy+= ener
        
            if(reward==0):
                reward = -1
            else:
                reward*=reward_scale
                # currState= self.states[cell]
                # currState.cellCovered()
            
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))

            if(self.drone.totalEnergy > self.drone.energyCapacity) or (len(self.drone.coveredTargets) == len(self.targets)):
            #    reward= -100
                    done= True
                    print(str(self.timeStep)+"--DONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNE")
                    #time.sleep(60000)

                    print("done at hovering")
            else:
                done= False
                
            self.timeStep+=1
            currState= self.states[cell]
            newState= self.state(currState.stateID, currState.cell[0], currState.cell[1], self.timeStep)
            self.epReward+=reward
            #return [[newState.stateID, self.timeStep], reward, done, {}]
            #return [[newState.stateID, reward, len(self.drone.coveredTargets)], reward, done, {}]
            
            remTs=  self.numTargets - len(self.drone.coveredTargets)
            stateInfo = [newState.stateID] + list(self.drone.coveredTargets.keys())+[-1]*remTs
            reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
            return [reshapedStateInfo, reward, done, {}]

        else:
            currState= self.states[cell]       
            print('nextCell: ('+ str(nextX)+", "+ str(nextY)+')'+ str(currState.numUnCoveredTargets))    


            actionValid= True            
            
            [cov, ener]= self.drone.move(cell, self.cellSideSize, self.targets )
                            
           # Calculating the reward for the agent
           
            if(self.drone.totalEnergy > self.drone.energyCapacity) or (len(self.drone.coveredTargets) == len(self.targets)):
            #    reward= -100
                    done= True
                    print(str(self.timeStep)+"--DONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNE")
                    #time.sleep(60000)
                    print("done at other actions totalEner: "+ str(self.drone.totalEnergy>self.drone.energyCapacity)+ ", "+ str((len(self.drone.coveredTargets) == len(self.targets))))

            else:
                done= False
                
             #elif len(agent.coveredTargets) == len(self.targets):
            #    reward= +100
            #    done= True
            # elif cov==0:
            if cov==0:    
             #  reward= -0.1   
                 reward= -1
                # done= False
            else:
               #reward = (cov/ener)
               reward = cov*reward_scale#*len(self.targets)
               # currState= self.states[cell]
               # currState.cellCovered()
              # done = False
       
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))

       
        next_state = self.drone.currentCell
        print("done??"+ str(done))
        print(self.drone.totalEnergy > self.drone.energyCapacity)
        print("num covered targets: "+ str(len(self.drone.coveredTargets)))
        print(len(self.drone.coveredTargets) == len(self.targets))
        
        self.timeStep+=1
        currState= self.states[next_state]
        newState= self.state(currState.stateID, currState.cell[0], currState.cell[1], self.timeStep)
        self.epReward+=reward
        #return [[newState.stateID, self.timeStep], reward, done, {}]
        #return [[newState.stateID, reward, len(self.drone.coveredTargets)], reward, done, {}]
        remTs=  self.numTargets - len(self.drone.coveredTargets)
        stateInfo = [newState.stateID] + list(self.drone.coveredTargets.keys())+[-1]*remTs
        reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
        return [reshapedStateInfo, reward, done, {}]



    def final(self):
        # for cell in agent.route:
        #     print(str(self.gridTopCorners.index(cell)) + " >> ")
        print(self.drone.route)
        
    def final_states(self):
        return self.drone.route    