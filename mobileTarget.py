# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:56:11 2020

@author: HG19230
"""
import numpy as np
import math
import random
import ManhattenMobility
from MobilityPatterns.ManhattanMobilityMatlab import ManhattanMobileTarget


class mobileTarget (object):
    
    def __init__(self, ID, initiLocX, initialLocY, gridLowCorners, numCellsPerSide, cellSideSize, dimLimit, mobilityModel, randomLoc, testing, testFilesFolder, timeStepsScale, stepsLimit):
         
         self.resetToSameInitLoc= True
         self.followDiffPath= False
         self.testing= testing
         self.testingFolder= testFilesFolder
         
         self.ID= ID
         # if(ID==0):
         self.initialLocation= (initiLocX, initialLocY)# (10.0, 10.0) #(10.0, 10.0)#(initiLocX, initialLocY)
         # else:
         #     self.initialLocation= (2.0, 10.0)
         self.direction='u'
         self.MobilityModel=mobilityModel #'TM' 'StepsMatlab' 'ManhattanMatlab'#straight #Transition Matrix Manhatten
         #self.folderName=''
         
         self.gridLowCorners= gridLowCorners
         self.cellSideSize= cellSideSize
         self.areaDimLimit= dimLimit
         self.numCellsPerSide= numCellsPerSide

         self.episodeNum=1
         self.timeStepsScale= timeStepsScale

         print(self.MobilityModel)

         if(self.MobilityModel=='StepsMatlab'):
             #self.mobilityDatFile= open("TargetsStepsData_200K_24by24/Target"+str(self.ID)+".dat", "r")
             self.mobilityDatFile= open("TargetsStepsData_100K_12by12/Target"+str(self.ID)+".dat", "r")
             
         elif(self.MobilityModel=='ManhattanPython'):
            
             print('inside ManMatlab **')
             #self.mobilityDatFile= open( "TargetsManData_200K_24by24/Target"+str(self.ID)+".dat","r")
             
             minSpeed= 3/3.6
             maxSpeed= 5/3.6
             self.ManMobObject= ManhattanMobileTarget(self.areaDimLimit, self.areaDimLimit, self.cellSideSize, self.cellSideSize, minSpeed, maxSpeed, randomLoc, self.timeStepsScale)
             if(self.testing):
                 self.reset(self.testing, self.testingFolder)

             else:
                 self.realMobFile= open("RealMobTesting/ManRealMobility_N"+str(self.ID)+".dat", "w")

                 self.initialLocation=[self.ManMobObject.X, self.ManMobObject.Y]
                 self.initialDirection= self.ManMobObject.direction
                 self.initialLorC= self.ManMobObject.LorC
                 self.initialLinMan= self.ManMobObject.line_manhattan
                 self.initialColMan= self.ManMobObject.column_manhattan
                
         # if(self.MobilityModel == 'Manhatten'):
         #     self.initialLocation= ManhattenMobility.createManhattenLocation(gridLowCorners)
         #     self.createTransitionMatrix()
                

         elif (self.MobilityModel == 'TM'):
             self.speed= (4/3.6)*self.timeStepsScale
             self.initialLocation= gridLowCorners[random.randint(0, len(gridLowCorners)-1)]# ((initiLocX, initialLocY))
             print("************* Target Created Initi Loc")
             print(self.initialLocation)
         # #self.initialLocation= ((initiLocX, initialLocY))
             self.createTransitionMatrix()
            
             self.realMobFile= open("realMobility_N"+str(self.ID)+".dat", "w")
                 
         elif(self.MobilityModel == 'ShowUpPattern'):
            #self.createMobForTimeSteps(stepsLimit+1)
            cellIndicies= [i for i in range(len(self.gridLowCorners)-1)]

            self.subcells= random.sample(cellIndicies, int(len(gridLowCorners)/3))
            self.showUpPrs= self.createShowUpPrs(self.subcells)
            
            self.initialLocation= self.gridLowCorners[self.ShowUpMob()] #self.gridLowCorners[self.MobPerTimeStep[0]]

         # elif(self.MobilityModel == 'StepsMatlab'):
         #    self.mobilityDatFile.readline()
         #    self.reset()
         
         self.numCells= numCellsPerSide* numCellsPerSide
         self.currentLocation= self.initialLocation
         if(self.MobilityModel == 'TM' or self.MobilityModel == 'ShowUpPattern'):
             self.currentCell= self.currentLocation
         else:
             self.currentCell= self.findCell(gridLowCorners, numCellsPerSide, cellSideSize)
             
         self.initialCell= self.currentCell
         print('created target '+ str(self.ID) + 'loc '+ str(initiLocX) + ", "+ str(initialLocY))
         self.movementMode= 'uC'
         self.mobilityRate= 0
    
    def reset(self, testing, testingFolder):
        self.steps=0
        if(testing):
            self.mobilityDatFile= open(testingFolder+"/Node"+str(self.ID)+".dat","r")
            self.mobLines= self.mobilityDatFile.readlines()
            
            self.mobilityDatFile.readline()#skip title line
            del self.mobLines[0]
            
            mobilityLine= self.mobLines[0]
            values=mobilityLine.split('\t')
            x= float(values[1])
            y= float(values[2])
            self.initialLocation=(x,y)
            self.currentLocation= self.initialLocation
            
            if( self.MobilityModel ==  'TM'): 
                self.currentCell= self.currentLocation
                self.realMobFile.write(str(self.currentLocation[0])+'\t'+str(self.currentLocation[1])+'\n')
            elif (self.MobilityModel == 'ShowUpPattern'):
                self.currentCell= self.currentLocation
            else:
                self.currentCell= self.findCell(self.gridLowCorners, self.numCellsPerSide, self.cellSideSize)

            self.initialCell= self.currentCell
            self.episodeNum+=1
            
        else:
        
            if(not self.MobilityModel == 'StepsMatlab' and not self.MobilityModel == 'ManhattanPython'):
                #'ManhattanMatlab'
                self.currentLocation= self.initialLocation
                self.currentCell= self.initialCell
                print('reset target loc: ')
                print(self.currentLocation)
                
            elif('ManhattanPython'):
                self.currentLocation= self.initialLocation
                self.currentCell= self.initialCell
                self.ManMobObject.X= self.initialLocation[0]
                self.ManMobObject.Y= self.initialLocation[1]
                self.ManMobObject.direction= self.initialDirection
                self.ManMobObject.LorC= self.initialLorC
                self.ManMobObject.line_manhattan= self.initialLinMan
                self.ManMobObject.column_manhattan= self.initialColMan
                self.realMobFile.write(str(self.currentLocation[0])+'\t'+str(self.currentLocation[1])+'\n')

                
            else:
                if(self.resetToSameInitLoc):
                    self.mobilityDatFile.close()
                    
                    if(self.MobilityModel=='StepsMatlab'):
                        #self.mobilityDatFile= open("TargetsStepsData_200K_24by24/Target"+str(self.ID)+".dat", "r")
                        self.mobilityDatFile= open("TargetsStepsData_100K_12by12/Target"+str(self.ID)+".dat", "r")
                    elif(self.MobilityModel=='ManhattanMatlab'):
                        self.mobilityDatFile= open( "TargetsManData_200K_24by24/Target"+str(self.ID)+".dat","r")
                    
                    if(self.followDiffPath and self.episodeNum > 1):
                        self.mobilityDatFile.readline()
    
                        dataNum= random.randint(1,20)
                        counter=0
                        while counter < dataNum: 
                            mobilityLine= self.mobilityDatFile.readline()
                            values=mobilityLine.split('\t')
                            x= float(values[1])
                            y= float(values[2])
                            dataBelongToInitialCell= self.isDataPointInsideCell((x,y), self.initialCell, self.cellSideSize)
                            if(dataBelongToInitialCell):
                                counter+=1
                        
                    else:
                        self.mobilityDatFile.readline()
                                    
                mobilityLine= self.mobilityDatFile.readline()
                values=mobilityLine.split('\t')
                x= float(values[1])
                y= float(values[2])
                self.initialLocation=(x,y)
                self.currentLocation= self.initialLocation
                
                if(self.MobilityModel == 'TM'):
                    self.currentCell= self.currentLocation
                else:
                    self.currentCell= self.findCell(self.gridLowCorners, self.numCellsPerSide, self.cellSideSize)
                
                self.initialCell= self.currentCell
                
                self.episodeNum+=1

    def moveBasedOnDatFile(self):
        print('moving target: '+ str(self.ID)+ 'prevLoc'+ str(self.currentLocation[0])+ str(self.currentLocation[1]))
        print(self.steps)

        mobilityLine= self.mobLines[self.steps] #self.mobilityDatFile.readline()
        values=mobilityLine.split('\t')
        print(values)
        x= float(values[1])
        y= float(values[2])
        print(x)
        print(y)
        self.currentLocation=(x,y)
        print()
        
        if(self.MobilityModel == 'TM'):
            self.currentCell= self.currentLocation
        else:
            self.currentCell= self.findCell(self.gridLowCorners, self.numCellsPerSide, self.cellSideSize)

    def createTMwithMovementPattern(self, pattern):
        if pattern == 'straight':
            return 
        elif pattern == 'diagonal':
            return
        elif pattern == 'zigzag':
            return 
        
    def setTransitionMatrix(self, cellsNeighbors):
        self.M={}
        del cellsNeighbors[0] #del nodeID
        del cellsNeighbors[0] #del initLocX
        del cellsNeighbors[0] # del initLocY
        
        for s in cellsNeighbors:
            #cellID, numNeighbors, n1:pr1, n2:pr2
            sValues= cellsNeighbors.split(',')
            cID= float(sValues[0])
            numNeighbors= float(sValues[1])
            self.M[cID]={}
            for i in range(numNeighbors):
                neighborID_Pr= sValues[2+i].split(':')
                self.M[cID][neighborID_Pr[0]]= neighborID_Pr[1]
                 
        print('transitionMatrix')
        print(self.M)
         
    def definePrsGivenNumNeighborCells(self, numCells):
        Prs=[]
        
        print("defining Prs Given NumCells: "+str(numCells))
        
        if(numCells == 3):
            Prs=[0.6, 0.3, 0.1]
        elif(numCells == 5):
            Prs=[0.4, 0.3, 0.15, 0.1, 0.05]
        else: #
            Prs=[0.25,  0.21 ,  0.18, 0.14, 0.1, 0.07, 0.04, 0.01] 
        
        return Prs
        #1 ----------0.5 -----------0
    

    def createTransitionMatrix(self):
        oldApproach= False
        
        largePr=1.0
        numCells= len(self.gridLowCorners)
        self.M = {}
        #[[0]*self.numCells for _ in range(self.numCells)]

        path=[]
        path.append(0)
        for (i) in  range(numCells):
            self.M[i]={}
            surroundingCells=[]
            print('investigating cell ('+str(i)+'): '+ str(self.gridLowCorners[i]))
            for (j) in  range(numCells):
                if(not i==j):# and not j in path):
                    coordsI= self.gridLowCorners[i]
                    coordsJ= self.gridLowCorners[j]
                    
                    if(abs(coordsI[0]-coordsJ[0]) <=self.cellSideSize and abs(coordsI[1]-coordsJ[1])<=self.cellSideSize):
                        surroundingCells.append(j)
            
            print(surroundingCells)
            
            if(oldApproach):
                index= random.randint(0, len(surroundingCells)-1)
                selectedJ= surroundingCells[index]
                print('selected: '+ str(selectedJ))
                print(len(surroundingCells))
                numRemCells= len(surroundingCells)-1
                if(numRemCells>0):
                    PrPerCell= (1.0-largePr)/numRemCells
                else:
                    PrPerCell= 0.0
                    largePr=1.0
    
                for j in surroundingCells:
                    self.M[i][j]=PrPerCell
            
                print(len(self.M[i]))
                print(selectedJ)
            
                self.M[i][selectedJ]= largePr
                path.append(selectedJ)
                
            else:
                Prs= self.definePrsGivenNumNeighborCells(len(surroundingCells))
                random.shuffle(Prs)
                
                indx= 0
                for s in surroundingCells:
                    self.M[i][s]= Prs[indx]
                    indx+=1

        print('transition Matrix')
        print(self.M)
        print(path)

    def step(self, gridLowCorners, testing):

        self.steps+=1
        
        if(testing):
            # if (self.MobilityModel== 'TM'):
            #     #self.moveUsingTransitionMatrix(self.gridLowCorners)
            #     self.moveUsingProbabilisticTransitionMatrix(self.gridLowCorners)
            # else:
            self.moveBasedOnDatFile()
            if(self.MobilityModel== 'TM'):
                self.realMobFile.write(str(self.currentLocation[0])+'\t'+str(self.currentLocation[1])+'\n')

        else:
            if(self.MobilityModel=='Manhatten'):
                (nextCoord, nextDir)= ManhattenMobility.doManhattenStep(self.currentLocation, self.gridLowCorners, self.direction, self.cellSideSize, self.areaDimLimit)
                self.currentLocation= nextCoord
                self.currentCell= nextCoord
                self.direction= nextDir
            elif(self.MobilityModel == 'ManhattanPython'):
                self.ManMobObject.move()            
                self.currentLocation=(self.ManMobObject.X, self.ManMobObject.Y)

                self.realMobFile.write(str(self.currentLocation[0])+'\t'+str(self.currentLocation[1])+'\n')

            elif(self.MobilityModel== 'TM'):
                #self.moveUsingTransitionMatrix(self.gridLowCorners)
                self.moveUsingProbabilisticTransitionMatrix(self.gridLowCorners)
            elif(self.MobilityModel== 'ShowUpPattern'):
                #self.moveBasedOnMobPerTimeStep()
                self.currentLocation= gridLowCorners[self.ShowUpMob()]
            else:
                self.moveBasedOnDatFile()
            
            
    def moveUsingTransitionMatrix(self, gridLowCorners):
        i= gridLowCorners.index(self.currentCell)
        print(i)
        print(self.M[i])
        j= self.M[i].index(1.0)
        self.currentCell= gridLowCorners[j]
        self.currentLocation= self.currentCell
        
    def moveUsingProbabilisticTransitionMatrix(self, gridLowCorners):
        
         print(self.currentLocation)
         print(self.currentCell)
         prevLoc= self.currentLocation
         i= gridLowCorners.index(self.currentCell)
         neighbors= self.M[i]

         ListNextCells= []
         ListNextCellsPrs=[]
         
         for c in neighbors:
            ListNextCells.append(c)
            ListNextCellsPrs.append(neighbors[c])
         
         if( len(ListNextCells)==1):
             j = ListNextCells[0]
         else:
             j=  np.random.choice(
                 ListNextCells, 
                1,
                p=ListNextCellsPrs
                )
         self.currentCell= gridLowCorners[j[0]]
         self.currentLocation= self.currentCell
         
         #newLoc= gridLowCorners[j[0]]
         
         #distToTravelPerStep = self.speed
         
         #to mitigate time scale effect
         # dist= math.sqrt((newLoc[0]-prevLoc[0])**2 + (newLoc[1]-prevLoc[1])**2)
         # if(dist > 0):
         #     newDist= self.timeStepsScale * dist
         #     ratio= newDist/dist
         #     newX= (1-ratio)*prevLoc[0] + ratio * newLoc[0]
         #     newY= (1-ratio)*prevLoc[1] + ratio * newLoc[1]
         #self.currentLocation = (newX, newY)
        #     self.currentCell= self.findCell(self.gridLowCorners, self.numCellsPerSide, self.cellSideSize)

    def findSublistsOfGivenSize(size, l):

        sublists = [[]]
        for i in range(len(l) + 1):
            for j in range(i):
                sublist= l[j: i]
                if(len(sublist)):
                    sublists.append(sublist)
                    
        return sublists

    def createShowUpPrs(self, cells):
        showUpPrs= np.random.dirichlet(np.ones(len(cells)),size=1) # [ random.random()] * len(cells)
        print(showUpPrs[0])
    
        return showUpPrs[0]

    def ShowUpMob(self):
        
            print(self.subcells)
            if( len(self.subcells)==1):
                 j = self.subcells[0]
            else:
                 j=  np.random.choice(
                     self.subcells, 
                    1,
                    p=self.showUpPrs
                    )
            print('selected cell')
            print(j)
            return j[0]

    def createMobForTimeSteps(self, numTimeSteps):
        cells= [i for i in range(len(self.gridLowCorners))]
        Prs= self.createShowUpPrs(cells)
        mob=[-1]*numTimeSteps
        for t in range(numTimeSteps):
        
            if( len(cells)==1):
                 j = cells[0]
            else:
                 j=  np.random.choice(
                     cells, 
                    1,
                    p=Prs
                    )
            print(j)
            mob[t]= cells[j[0]]
    
        self.MobPerTimeStep=mob #index of gridLowCorner cells
        
        
    def moveBasedOnMobPerTimeStep(self):
        cellIndx= self.MobPerTimeStep[self.steps]
        
        self.currentCell= self.gridLowCorners[cellIndx]
        self.currentLocation= self.currentCell


    def mobiliyFunction(self, cellSideSize):
        ListNextCells=[]
       # if self.mobilityRate==0:
        X= self.initialLocation[0]
        Y= self.initialLocation[1]
        
        if self.mobilityRate==4:
            ListNextCells= ['uC', 'dC', 'rC', 'lC']
            ListNextLocations= []
            ListNextLocations.append((X, Y+cellSideSize)) #uc
            ListNextLocations.append((X, Y-cellSideSize)) #dC
            ListNextLocations.append((X+cellSideSize, Y)) #rc
            ListNextLocations.append((X-cellSideSize, Y)) #lc
            
        elif self.mobilityRate==8:
            ListNextCells= ['uC', 'dC', 'rC', 'lC', 'durC', 'dulC', 'ddrC', 'ddlC']
            ListNextLocations= []
            ListNextLocations.append((X, Y+cellSideSize)) #uc
            ListNextLocations.append((X, Y-cellSideSize)) #dC
            ListNextLocations.append((X+cellSideSize, Y)) #rc
            ListNextLocations.append((X-cellSideSize, Y)) #lc
            ListNextLocations.append((X+cellSideSize, Y+cellSideSize)) #durc
            ListNextLocations.append((X-cellSideSize, Y+cellSideSize)) #dulc
            ListNextLocations.append((X+cellSideSize, Y-cellSideSize)) #ddrc
            ListNextLocations.append((X-cellSideSize, Y-cellSideSize))            

    def getMDC(self, cellSideSize, dimLimit):
        
        #get number of surrounding cells
        X= self.currentCell[0]
        Y= self.currentCell[1]
        
        xL= self.currentLocation[0]
        yL= self.currentLocation[1]
      
        ListNextCells=[]
        ListNextCellsPrs=[]
        
            
        ListNextCells= ['uC', 'dC']#, 'rC', 'lC', 'durC', 'dulC', 'ddrC', 'ddlC']
        ListNextLocations= []
        ListNextLocations.append((X, Y+cellSideSize)) #uc
        ListNextLocations.append((X, Y-cellSideSize)) #dC
        # ListNextLocations.append((X+cellSideSize, Y)) #rc
        # ListNextLocations.append((X-cellSideSize, Y)) #lc
        # ListNextLocations.append((X+cellSideSize, Y+cellSideSize)) #durc
        # ListNextLocations.append((X-cellSideSize, Y+cellSideSize)) #dulc
        # ListNextLocations.append((X+cellSideSize, Y-cellSideSize)) #ddrc
        # ListNextLocations.append((X-cellSideSize, Y-cellSideSize))

        validCells=[]    

        up= ListNextLocations[0]
        down= ListNextLocations[1]
        
        if not self.isValidCell(up[0], up[1], dimLimit): 
            print("up not valid")
            self.movementMode== 'dC'

        elif not self.isValidCell(down[0], down[1], dimLimit):
            print("down not valid")
            self.movementMode== 'uC'
            
        
        if self.movementMode == 'uC' and up[1] < dimLimit:
            validCells.append('uC')
            ListNextCellsPrs.append(1.0)
            print("target "+ str(self.ID)+" up")
        else:
            #elif self.movementMode == 'dC' and down[1] >=0 :            
            validCells.append('dC')
            ListNextCellsPrs.append(1.0)
            print("target "+ str(self.ID)+" down")



        # for i in range(len(ListNextLocations)):
        #     cell= ListNextLocations[i]
        #     x= cell[0]
        #     y= cell[1]
            
        #     if self.isValidCell(x, y, dimLimit):
        #             validCells.append(ListNextCells[i])    
        
        # numSurroundingCells= len(validCells)
        # prPerCell= 1.0/numSurroundingCells
            
        # ListNextCellsPrs= []
        # for i in range(0, numSurroundingCells):
        #     ListNextCellsPrs.append(prPerCell)

            



        # elif action == 6: #dDwnL:  decrease y , decrease x
        #     cell= (agent.currentCell[0]-self.cellSideSize , agent.currentCell[1]-self.cellSideSize)
        # elif action == 7: #dDwnR:  decrease y , increase x
        #     cell= (agent.currentCell[0]+self.cellSideSize , agent.currentCell[1]-self.cellSideSize)

        return [validCells, ListNextCellsPrs]   
            
        #diagonal cells 
        
    def isValidCell(self, x, y, dimLimit):
     #    print('x,y,dim ' + str(x)+", "+ str(y)+", "+str(dimLimit))
        # print(y<dimLimit)
        # print(x<dimLimit)
        # print(x>=0)
       #  print(y>=0)
         if(y<dimLimit and x<dimLimit and x>=0 and y>=0):
           #  print("valid")
             return True
         
      #   print("InValid")
         return False
        
    def selectNextMove(self, cellSideSize, dimLimit):
        
         [ListNextCells, ListNextCellsPrs] = self.getMDC(cellSideSize, dimLimit)
         
         if( len(ListNextCells)==1):
             choice = ListNextCells[0]
         else:
             choice=  np.random.choice(
                 ListNextCells, 
                1,
                p=ListNextCellsPrs
                )
             
        
         X= self.currentCell[0]
         Y= self.currentCell[1]
        
         if choice == 'uC':
             return (X, Y+cellSideSize)
         elif choice == 'dC':
            return  (X, Y-cellSideSize)
         elif choice == 'rC':
            return (X+cellSideSize, Y)
         elif choice == 'lC':
            return (X-cellSideSize, Y)
         elif choice == 'durC':
            return (X+cellSideSize, Y+cellSideSize)
         elif choice == 'dulC':
            return (X-cellSideSize, Y+cellSideSize)
         elif choice == 'ddrC':
            return (X+cellSideSize, Y-cellSideSize)
         elif choice == 'ddlC':
            return (X-cellSideSize, Y-cellSideSize)
        
   
    def move(self, cellSideSize, dimLimit):

        nextCell= self.selectNextMove(cellSideSize, dimLimit)
        self.currentCell= nextCell
        self.currentLocation= (nextCell[0]+cellSideSize/2.0, nextCell[1]+ cellSideSize/2.0) 
      #  print("dimLim: "+ str(dimLimit))
        print('moved target '+ str(self.ID) + ' loc ('+ str(self.currentLocation[0]) + ", "+ str(self.currentLocation[1])+")")

        
        
    def findCell(self, gridLowCorners, numCellsPerSide, cellSideSize):
         for x in range (0, numCellsPerSide):
            for y in range (0, numCellsPerSide):
                print(x, y)
                cellX= x*cellSideSize
                cellY= y*cellSideSize
                isCell= self.isTargetInsideCell((cellX, cellY), cellSideSize)
                if(isCell): 
                    return (cellX, cellY)
                
    def isDataPointInsideCell(self, coordData, cellBottomLeft, cellSideSize):
        cellTopCorner= (cellBottomLeft[0]+cellSideSize, cellBottomLeft[1]+cellSideSize)

        # print("bottomLeft: ")
        # print(cellBottomLeft)
        if (coordData[0] >= cellBottomLeft[0] and coordData[0] <= cellTopCorner[0] and 
            coordData[1] >= cellBottomLeft[1] and coordData[1] <= cellTopCorner[1]) : 
           # print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY: "+ str(t[0]) +", "+ str(t[1]))
            return True
        else : 
          #  print("not covered -----------------------"+ str(t[0]) +", "+ str(t[1]))
            return False    
        
    def isTargetInsideCell(self, cellBottomLeft, cellSideSize):
        # print("isTargetInsideCell "+ str(t[0]) +", "+ str(t[1]))
        # print("topCOrner: ")
        # print(cellTopCorner)
        t= self.currentLocation
        cellTopCorner= (cellBottomLeft[0]+cellSideSize, cellBottomLeft[1]+cellSideSize)

        # print("bottomLeft: ")
        # print(cellBottomLeft)
        if (t[0] >= cellBottomLeft[0] and t[0] <= cellTopCorner[0] and 
            t[1] >= cellBottomLeft[1] and t[1] <= cellTopCorner[1]) : 
           # print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY: "+ str(t[0]) +", "+ str(t[1]))
            return True
        else : 
          #  print("not covered -----------------------"+ str(t[0]) +", "+ str(t[1]))
            return False    