# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:32:12 2020
REF: https://github.com/sichkar-valentyn/Reinforcement_Learning_in_Python/blob/master/RL_Q-Learning_E1/env.py
@author: HG19230
"""

import numpy as np  # To deal with data in form of matrices
import math
import random
#import tkinter as tk  # To build GUI
import gym
from gym import spaces
from drone import drone
from mobileTarget import mobileTarget
from MobilityPatterns.RPGM_Mobility import RPGM_Mobility

route = {}

class OneDroneMobileTargetsEnv (gym.Env):
    metadata = {'render.modes': ['human']}

        
    class cell(object):
        def __init__(self, ID, x, y, numTs):
            self.cell= (x,y)
            self.cellID= ID
            self.numTargets=numTs
            self.numUnCoveredTargets= 0
            self.TargetsIndicators=[0]*numTs
            self.TargetsCoverageIndicators=[0]*numTs
            
        def addTarget(self, tID):
            self.numUnCoveredTargets+=1
            self.TargetsIndicators[tID]=1
            print("cell "+ str(self.cell[0])+", "+str(self.cell[1])+": "+ str(self.numUnCoveredTargets))
        
        def removeTarget(self, tID):
            self.TargetsIndicators[tID]=1
            self.TargetsCoverageIndicators=[0]*self.numTargets

        def cellCovered(self):
            self.numUnCoveredTargets= 0
            print("cell covered "+ str(self.numUnCoveredTargets))
        
        def setTargetCovered(self, tID):
            self.TargetsCoverageIndicators[tID]=1
            
        def resetTargetsIndicators(self):
            self.TargetsIndicators=[0]*self.numTargets
            self.TargetsCoverageIndicators=[0]*self.numTargets


    def __init__(self, stepsLimitPerEpisode, areaSize, numTargets, droneCoverageDiameter, numCells, cellSideSize,  mobilityModel, reward_scale, testing, testDatFolder, stateRep):
        self.testing= testing
        self.testFilesFolder= testDatFolder
        self.MobilityModel= mobilityModel
        super(OneDroneMobileTargetsEnv, self).__init__()
        self.trainingStarted= False
        self.areaDimLimit= np.sqrt(areaSize)
        
        self.stateRep= stateRep
        print("areaDimLimit: "+ str(self.areaDimLimit))
        self.targets= []

        self.route=[]
        #self.targetsVelocity= 1.4 #m/s
        self.gridlowCorners=[]

        self.reward_scale= reward_scale
        
        self.cells={}
        
        self.numTargets= numTargets

        self.cellSideSize=  cellSideSize #self.calculateGridCellSize(droneCoverageDiameter)
        self.numCells= numCells
        print("side:"+ str(self.cellSideSize))

        self.buildGrid(areaSize)    

        self.n_actions = 9#9

        self.action_space= spaces.Discrete(self.n_actions)
        self.state_size= numTargets+2
        self.observation_space= spaces.Box(low=0, high= 200000, shape=(1,(self.numTargets+2)))#shape=(1,(2))) # 
 #shape=(1,(2))) #shape=(1,(self.numTargets+2)))
        self.timeStep=0
        self.totalSteps=0
        self.TargetsCoverageIndicators=[0]*self.numTargets

        print(self.cells)
       
        #self.createTargets()
            
        self.epReward=0
        self.numEpisodes=0
        
        print(self.targets)
        
        
        if(testing):
            self.stepsLimit= stepsLimitPerEpisode
        else:
            self.stepsLimit= stepsLimitPerEpisode #math.ceil(len(self.cells)+0.5*(len(self.cells))) #len(self.cells)# math.ceil(len(self.cells)+0.5*(len(self.cells))) #math.ceil(len(self.cells)+0.5*(len(self.cells))) #len(self.cells) # math.ceil(len(self.cells)+0.5*(len(self.cells)))

            self.trainingFileName= "TrainingFiles/Training_A"+str(int(self.areaDimLimit))+"_T"+str(numTargets)+"_"+self.MobilityModel +"_"+str(self.stepsLimit)+".dat"
            with open(self.trainingFileName, "w") as statsfile:
                statsfile.write('EpNum'+'\t'+'EpSteps'+'\t'+'Reward'+'\t'+'ener'+'\t'+'dist'+'\t'+'NumCovTargets'+'\n')
    
        #add hovering later
        #self.action_space = ['up', 'down', 'left', 'right', 'dUpL', 'dUpR', 'dDwnL', 'dDwnR','hover']
        
        #for i in range(len(self.gridlowCorners)):
         #   self.action_space.append(''+str(i))
        
        print(self.action_space)
        
        self.n_actions =9#9#len(self.action_space)
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

            # with open("RPGM_Locs.dat", "w") as rpgm:
            #     rpgm.write('EpNum'+'\t'+'EpSteps'+'\t'+'NodeLocs'+'\n')
            
            
    def findCellForPoint(self, xp, yp):
        
        xCell= math.floor(xp/self.cellSideSize)
        yCell= math.floor(yp/self.cellSideSize)
        
        xCell*=self.cellSideSize
        yCell*=self.cellSideSize
        
        return(xCell, yCell)
        
    def createTargets(self, randomLoc):
         for i in range(0, self.numTargets):
            #(self, initiLocX, initialLocY, gridLowCorners, numCellsPerSide, cellSideSize, dimLimit):
            t= mobileTarget(i, random.random()*self.areaDimLimit, random.random()*self.areaDimLimit, self.gridlowCorners, self.numCellsPerSide, self.cellSideSize, self.areaDimLimit, self.MobilityModel, randomLoc, self.testing, self.testFilesFolder, self.timeStepsScale, self.stepsLimit)
            print(t.currentLocation)
            
            if(self.MobilityModel=='RPGM'):
                t.realMobFile= open("RealMobTesting/RPGMRealMobility_N"+str(t.ID)+".dat", "w")

                t.currentLocation= self.RPGM.moveNode(t.ID, self.timeStep)
                t.currentCell= t.findCell(self.gridlowCorners, self.numCellsPerSide, self.cellSideSize)

            tCell= self.findCellForPoint(t.currentLocation[0], t.currentLocation[1])
            print('finding cell for target'+ str(t.currentLocation))            
            print(tCell)
            cell= self.cells[tCell]
            cell.addTarget(i)
            self.targets.append(t)
            
    def placeDrone(self, drone):
        drone.setRandomInitialLocation(self.gridlowCorners, self.cellSideSize, self.targets)
        [covTPerc, covTsIDs, oldCovTsIDs]= drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
        drone.numTargetsCoveredInitially= len(drone.coveredTargets)
        self.drone=drone
        
        self.timeStepsScale= self.cellSideSize/ self.drone.speed
        
        if(self.MobilityModel=='RPGM'):
            self.maxStepsPerEpisode= self.stepsLimit+1
            maxTargetsPerGroup= 2
            numGroups= math.ceil(int(self.numTargets/maxTargetsPerGroup))
            print(numGroups)
            self.RPGM= RPGM_Mobility(self.areaDimLimit, self.areaDimLimit, numGroups, self.numTargets, self.maxStepsPerEpisode, self.timeStepsScale)
            self.RPGM.generateMobility()

    def buildGrid(self, areaSize):

        # self.areaNumCells= int(round(areaSize / np.power(self.cellSideSize, 2)))
        print(self.numCells)

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
                currState= self.cell( self.gridlowCorners.index(cell), x*self.cellSideSize,y*self.cellSideSize, self.numTargets)
                self.cells[(x*self.cellSideSize,y*self.cellSideSize)]=currState

                
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
    def getState(self, state, newCovTsIDs, oldCovTsIDs):
        
        print('getting STATE INFO ===== '+ str(state.cellID))
        currentSeenTs= [0]*self.numTargets
        
        for t in self.targets:
            if(t.ID in newCovTsIDs or t.ID in oldCovTsIDs):
                currentSeenTs[t.ID]=1
        if(self.stateRep=='TargetCov'):
            stateInfo = [state.cellID, self.timeStep] + self.TargetsCoverageIndicators #+ list(self.drone.coveredTargets.keys())+[-1]*remTs
        else:
            stateInfo = [state.cellID, self.timeStep] + currentSeenTs #+ list(self.drone.coveredTargets.keys())+[-1]*remTs

        reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
        print('((((((((((((((( State ))))))))'+ str(reshapedStateInfo))
        return reshapedStateInfo

        
    def reset(self):
        #self.update()
        #time.sleep(0.1)

        print('ENV RESET ================')
        self.route=[]
        if(self.timeStep> 0 and self.trainingStarted and not self.testing):
            self.numEpisodes+=1
            with open(self.trainingFileName, "a") as statsfile:
                statsfile.write(str(self.numEpisodes)+'\t'+str(self.timeStep)+'\t'+str(self.epReward)+'\t'+str(self.drone.totalEnergy)+'\t'+str(self.drone.totalTravelledDistance)+'\t'+str(len(self.drone.coveredTargets))+'\t'+str(self.drone.route)+'\n')


        self.drone.reset(self.gridlowCorners, self.cellSideSize, self.targets)
        self.drone.resetLocation()
        
        self.timeStep=0
        self.epReward=0

        for s in self.cells:
            self.cells[s].cellCovered()
            self.cells[s].resetTargetsIndicators()
            
            
        for t in self.targets:
            t.reset(self.testing, self.testFilesFolder)
            cell= t.initialCell
            self.cells[cell].addTarget(t.ID)
            
            
        self.TargetsCoverageIndicators=[0]*self.numTargets

        #
        # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        if(self.MobilityModel=='RPGM'):
            self.RPGM.generateMobility()
            # with open("RPGM_Locs.dat", "w") as rpgm:
            #     rpgm.write('EpNum'+'\t'+'EpSteps'+'\t'+'NodeLocs'+'\n')
            
            
        currState= self.cells[self.drone.currCell]


        # stateInfo = [currState.cellID, self.timeStep] + self.TargetsCoverageIndicators #+ list(self.drone.coveredTargets.keys())+[-1]*remTs
        # reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])

        reshapedStateInfo= self.getState(currState, [], [])

        #return [currState.cellID, currState.numUnCoveredTargets, len(self.drone.coveredTargets)]#[currState.cellID, self.timeStep]
        return reshapedStateInfo#[currState.cellID, self.timeStep]

        #return drone.currentCell


    # Function to get the next observation and reward by doing next step
    def step(self, action):
        if(self.timeStep == 0):
            [covTPerc, newCovTsIDs, oldCovTsIDs]= self.drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
            self.drone.numTargetsCoveredInitially= len(self.drone.coveredTargets)
            for t in newCovTsIDs:
                self.TargetsCoverageIndicators[t]= 1
            print("numTargets covered initially:  "+ str(self.drone.numTargetsCoveredInitially))
            initReward= self.drone.numTargetsCoveredInitially * self.reward_scale
            
            if(self.drone.numTargetsCoveredInitially == len(self.targets)):
                done=True
                reward= initReward
                currState= self.cells[self.drone.currCell]
                newState= self.cell(currState.cellID, currState.cell[0], currState.cell[1], self.timeStep)    
            
                reshapedStateInfo= self.getState(newState, newCovTsIDs, oldCovTsIDs)
                self.epReward+=reward
                return [reshapedStateInfo, reward, done, {}]
        
        else:
            initReward=0
            
        self.timeStep+=1 ############# increment before stepping 
        currState= self.cells[self.drone.currCell]
        self.route.append(self.drone.currCell)

        print("env step "+str(self.timeStep)+" / "+ str(self.stepsLimit)+" function +++++++++++++State: ("+str(self.drone.currLocation[0])+","+str(self.drone.currLocation[1])+","+str(len(self.drone.coveredTargets))+") >>> Action: "+ str(action)+" +++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        
        for cell in self.cells:
            self.cells[cell].resetTargetsIndicators()
            
        for t in self.targets:           
            #t.move(self.cellSideSize, self.areaDimLimit)
            # with open("RPGM_Locs.dat", "a") as rpgm:
            #     rpgm.write(self.timeStep)

                tPrevLoc= t.currentLocation
                
                if(self.MobilityModel== 'RPGM'):
                    t.currentLocation= self.RPGM.moveNode(t.ID, self.timeStep)
                    t.currentCell= t.findCell(self.gridlowCorners, self.numCellsPerSide, self.cellSideSize)
                    t.realMobFile.write(str(t.currentLocation[0])+'\t'+str(t.currentLocation[1])+'\n')

                                
                  #  rpgm.write('\t'+t.currentCell)
                else:
                    t.step(self.gridlowCorners, self.testing)
                    print('=================== MOVED TARGET '+ str(t.ID)+" >> "+ str(t.currentLocation))


                    # mitigate time Scale effect ###################################################
                    #distance betwen the two points
                    # dist= math.sqrt((t.currentLocation[0]-tPrevLoc[0])**2 + (t.currentLocation[1]-tPrevLoc[1])**2)
                    # if(dist > 0):
                    #     newDist= self.timeStepsScale * dist
                    #     ratio= newDist/dist
                    #     newX= (1-ratio)*tPrevLoc[0] + ratio * t.currentLocation[0]
                    #     newY= (1-ratio)*tPrevLoc[1] + ratio * t.currentLocation[1]
                    #     t.currentLocation = (newX, newY)
                    #     t.currentCell= t.findCell(self.gridlowCorners, self.numCellsPerSide, self.cellSideSize)

                    
               # rpgm.write('\n')

            
        
            #self.cells[t.currentCell].addTarget(t.ID)
            
            
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
        
        
        #[0'up', 1'down', 2'left', 3'right', 4'dUpL', 5'dUpR', 6'dDwnL', 7'dDwnR', 8'hover']

        if action == 0: #up: increase y 
            cell= (self.drone.currCell[0], self.drone.currCell[1]+ self.cellSideSize)
        elif action == 1: #down: decrease y
            cell= (self.drone.currCell[0], self.drone.currCell[1]- self.cellSideSize)
        elif action == 2: #left: decrease x
            cell= (self.drone.currCell[0]-self.cellSideSize , self.drone.currCell[1])
        elif action == 3: #right: increase x
            cell= (self.drone.currCell[0]+self.cellSideSize , self.drone.currCell[1])
        elif action == 4: #dUpL:  increase y , decrease x
            cell= (self.drone.currCell[0]-self.cellSideSize , self.drone.currCell[1]+self.cellSideSize)
        elif action == 5: #dUpR:  increase y , icrease x
            cell= (self.drone.currCell[0]+self.cellSideSize , self.drone.currCell[1]+self.cellSideSize)
        elif action == 6: #dDwnL:  decrease y , decrease x
            cell= (self.drone.currCell[0]-self.cellSideSize , self.drone.currCell[1]-self.cellSideSize)
        elif action == 7: #dDwnR:  decrease y , increase x
            cell= (self.drone.currCell[0]+self.cellSideSize , self.drone.currCell[1]-self.cellSideSize)
        else: # hovering
            cell= self.drone.currCell

            #targetsCoveredBefore= drone.coveredTargets
            [reward, newCovTsIDs, oldCovTsIDs]= self.drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
            #reward= reward/self.numTargets
            #targetsCoveredAfter= drone.coveredTargets
            for t in newCovTsIDs:
                self.TargetsCoverageIndicators[t]= 1
                
            time= self.cellSideSize/self.drone.speed
            ener=  (time * self.drone.hoveringEnergyPerSec_J)
            self.drone.totalEnergy+= ener
        
            if(reward==0):
                reward = -1
            else:
                reward*=self.reward_scale

            
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))
#(self.drone.totalEnergy > self.drone.energyCapacity) or 
            if(len(self.drone.coveredTargets) == len(self.targets) or self.timeStep >= self.stepsLimit):
            #    reward= -100
                    done= True
                    print("done at hovering")
            else:
                done= False
                
                
            #self.timeStep+=1
            currState= self.cells[cell]
            newState= self.cell(currState.cellID, currState.cell[0], currState.cell[1], self.timeStep)    
            self.epReward+=(reward+initReward)


            # stateInfo = [newState.cellID, self.timeStep] + self.TargetsCoverageIndicators #list(self.drone.coveredTargets.keys())+[-1]*remTs
            # reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
            reshapedStateInfo= self.getState(newState, newCovTsIDs, oldCovTsIDs)

            print("nextStateInfo "+str(currState.cell))
            print(reshapedStateInfo)         
            print("action: "+str(action)+"...reward: "+ str(reward)+'-----------------------------------')
             
            return [reshapedStateInfo, initReward+reward, done, {}]

            #return [cell, reward, done]
        
        ########## finished hovering action ###############
        
        #if action is not hovering
        nextX= cell[0]
        nextY= cell[1]
    
        if(nextY >= self.areaDimLimit or nextX>=self.areaDimLimit or nextX<0 or nextY<0):
            
            print('Invalid Action ---------------------------')
            
            cell= self.drone.currCell
            currState= self.cells[cell]       
            print('nextCell: ('+ str(nextX)+", "+ str(nextY)+')'+ str(currState.numUnCoveredTargets))    

            [reward, newCovTsIDs, oldCovTsIDs]= self.drone.filterCoveredTargets(self.targets, False, self.cellSideSize)
            #reward=reward/self.numTargets
            print(newCovTsIDs)
            for t in newCovTsIDs:
                print(t)
                print(self.TargetsCoverageIndicators[t])
                self.TargetsCoverageIndicators[t]=1
                
            time= self.cellSideSize/self.drone.speed
            ener=0
            ener=  (time * self.drone.hoveringEnergyPerSec_J)
            self.drone.totalEnergy+= ener
        
            if(reward==0):
                reward = -1
            else:
                reward*=self.reward_scale
                # currState= self.states[cell]
                # currState.cellCovered()
                
            #reward -=10 #adding extra punishment for invalid action
            
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))
#self.drone.totalEnergy > self.drone.energyCapacity) or

            if (len(self.drone.coveredTargets) == len(self.targets) or self.timeStep >= self.stepsLimit):
            #    reward= -100
                    done= True
                    print("done at invalid action")
            else:
                done= False
                
            currState= self.cells[cell]
            newState= self.cell(currState.cellID, currState.cell[0], currState.cell[1], self.timeStep)
            self.epReward+=(reward+initReward)
            
            # stateInfo = [newState.cellID, self.timeStep] +  self.TargetsCoverageIndicators #list(self.drone.coveredTargets.keys())+[-1]*remTs
            # reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
            reshapedStateInfo= self.getState(newState, newCovTsIDs, oldCovTsIDs)

            print("nextStateInfo "+str(newState.cell))
            print(reshapedStateInfo)         
            print("action: "+str(action)+"...reward: "+ str(reward)+'-----------------------')

            return [reshapedStateInfo, initReward+reward, done, {}]
            #return [cell, reward, done]

        else: ########### valid transition ####################
            currState= self.cells[cell]       
            print('valid action ++++ nextCell: ('+ str(nextX)+", "+ str(nextY)+')'+ str(currState.numUnCoveredTargets))    

            actionValid= True            
            
            [cov,  newCovTsIDs, oldCovTsIDs, ener]= self.drone.move(cell, self.cellSideSize, self.targets )
            print(newCovTsIDs)
            for t in newCovTsIDs:
                print(t)
                print(self.TargetsCoverageIndicators[t])
                self.TargetsCoverageIndicators[t]=1
           # Calculating the reward for the agent
           #self.drone.totalEnergy > self.drone.energyCapacity) or 
            if(len(self.drone.coveredTargets) == len(self.targets) or self.timeStep >= self.stepsLimit):
            #    reward= -100
                    done= True
                    print("done at other actions totalEner: "+ str(self.drone.totalEnergy> self.drone.energyCapacity)+ ", "+ str((len(self.drone.coveredTargets) == len(self.targets))))

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
               reward = cov*self.reward_scale#*len(self.targets)
               # currState= self.states[cell]
               # currState.cellCovered()
              # done = False
       
            print("Calculating Reward ++++ ("+str(reward)+") +++ "+str(ener)+ " ++++ "+ str(self.drone.totalEnergy))

        next_state = self.drone.currCell
        print("done?????????????"+ str(done))
        print(self.drone.totalEnergy > self.drone.energyCapacity)
        print("num covered targets: "+ str(len(self.drone.coveredTargets)))
        print(len(self.drone.coveredTargets) == len(self.targets))
        
        currState= self.cells[next_state]
        newState= self.cell(currState.cellID, currState.cell[0], currState.cell[1], self.timeStep)
        self.epReward+=(reward+initReward)
        
        #return [[newState.cellID, self.timeStep], reward, done, {}]
        #return [[newState.cellID, reward, len(self.drone.coveredTargets)], reward, done, {}]
        
        remTs=  self.numTargets - len(self.drone.coveredTargets)
        # stateInfo = [newState.cellID, self.timeStep] +  self.TargetsCoverageIndicators #list(self.drone.coveredTargets.keys())+[-1]*remTs
        # reshapedStateInfo= np.reshape(stateInfo, [1, self.state_size])
        
        reshapedStateInfo= self.getState(newState, newCovTsIDs, oldCovTsIDs)
        
        print("nextStateInfo "+str(newState.cell))
        print(reshapedStateInfo)         
        print("action: "+str(action)+"...reward: "+ str(reward)+'-----------------------------')

        return [reshapedStateInfo, initReward+reward, done, {}]


        #return [next_state, reward, done]


    def final(self, drone):
        # for cell in agent.route:
        #     print(str(self.gridTopCorners.index(cell)) + " >> ")
        print(drone.route)
        
        
    def final_states(self, drone):
        return drone.route    