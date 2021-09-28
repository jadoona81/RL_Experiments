# -*- coding: utf-8 -*-

import sys
sys.path.append("..\..\DQNLibrary") 

from Benchmark.gridAStar import AStarGridPathPlanning
import numpy as np

class TSP_greedy:
    
    class gridCellRoutes:
        
        def __init__(self, coord, glc, aStar, cellSideSize):
            self.gridLowCorners= glc
            self.coords= coord
            self.aStar= aStar
            self.cellRoutes={} # cellCoord, route
            self.cellsByHops= {} # numHops, listCells 
            self.maxHops= 0
            self.cellSideSize= cellSideSize
            
        def claculateRoutesToOtherCells(self):
            
            print('creating routes for cell: '+ str(self.coords))
            
            for cell in self.gridLowCorners:
                if cell == self.coords:
                    continue
                
                start= (int(self.coords[0]/self.cellSideSize), int(self.coords[1]/self.cellSideSize)) #4
                goal= (int(cell[0]/self.cellSideSize), int(cell[1]/self.cellSideSize)) #4
                
                print(start)
                print(goal)
                
                route= self.aStar.search(start, goal)
                self.cellRoutes[cell]= route
                hops= len(route)-1
                
                if not hops in  self.cellsByHops:
                    self.cellsByHops[hops]=[]

                self.cellsByHops[hops].append(cell)
                if(hops> self.maxHops):
                    self.maxHops= hops
        
            print(self.cellsByHops)
            print(self.cellRoutes)
        
        
    class Target_Node:
        
        def __init__(self, ID, glc, ncps, css, maxTimeSteps, targetsDatFolder, MobilityModel):
            self.ID= ID
            self.gridLowCorners= glc
            self.numCellsPerSide= ncps
            self.cellSideSize= css            
            
            self.mobilityRoute={}
            self.mobilityCells={}
            self.cellsVisitation={}
            
            print('TARGET '+ str(self.ID)+' reading mobility file')
            
            self.mobilityDatFile= open(targetsDatFolder+"/Node"+str(self.ID)+".dat", "r")
            
            print(targetsDatFolder+"/Node"+str(self.ID))

            self.mobilityDatFile.readline()
            
            lines= self.mobilityDatFile.readlines()

            timeStep=0
            for line in lines:
                values=line.split('\t')
                print(values)
                
                if(len(values)>0):
                    x= float(values[1])
                    y= float(values[2])
                    self.mobilityRoute[timeStep]= (x, y)
                    # if(MobilityModel == 'TM'):
                    #     currentCell= (int(values[1]), int(values[2]))
                    # else:
                    currentCell= TSP_greedy.findCell((x,y), self.gridLowCorners, self.numCellsPerSide, self.cellSideSize)

                    self.mobilityCells[timeStep]=currentCell
                    if(not currentCell in self.cellsVisitation.keys()):
                        self.cellsVisitation[currentCell]=[]
                    self.cellsVisitation[currentCell].append(timeStep)
                    timeStep+=1
                    
                    if(timeStep== maxTimeSteps):
                        break

            print('mobility for target: '+ str(self.ID))
            print(self.mobilityRoute)
            print(self.mobilityCells)


    def  __init__(self, numNodes, maxTimeSteps, numGridCells, numCellsPerSide, gridLowCorners, cellSideSize, targetsDataFolder, reward_scale, MobilityModel, horizontalEnergy):
        
        self.numTargets= numNodes
        self.nodes={}
        self.totalSteps=0
        self.reward= 0
        self.currLoc= (0,0)
        self.currCell=(0,0)
        self.totalDist=0
        self.totalEnergy=0
        self.reward=0
        self.route=[]
        self.route.append(self.currCell)
        self.coveredTargets={}
        self.reward=0
        self.reward_scale= reward_scale
        
        self.MobilityModel= MobilityModel
        self.numCovTargets=0
        self.maxTimeSteps=maxTimeSteps
        self.numCellsPerSide= numCellsPerSide
        self.cellSideSize= cellSideSize
        self.gridLowCorners= gridLowCorners
        
        self.cellsRoutes={}
        aStar=  AStarGridPathPlanning(self.numCellsPerSide, self.cellSideSize)
        for cell in self.gridLowCorners:
            cellRoutes= self.gridCellRoutes(cell, self.gridLowCorners, aStar, self.cellSideSize)
            cellRoutes.claculateRoutesToOtherCells()
            self.cellsRoutes[cell]= cellRoutes
        
        c, r = numGridCells, maxTimeSteps
        self.cellsMatrix = {} #[[[] for x in range(c)] for y in range(r)]  # [timeStep][cellID]

        for i in range(numNodes):
            self.nodes[i]= self.Target_Node(i, self.gridLowCorners, self.numCellsPerSide, self.cellSideSize, self.maxTimeSteps, targetsDataFolder, MobilityModel)
        
        print('matrix shape')
        print(np.shape(self.cellsMatrix))

        #cellsMatrix={time, listCells }
            #listCells={cellID, listTargets}
        for t in range(self.maxTimeSteps):
            self.cellsMatrix[t]=[-1]*numGridCells
            for c in range(numGridCells):
                self.cellsMatrix[t][c]=[]
            for n in range(numNodes):
                print('iteration time '+ str(t)+' node '+ str(n))
                node= self.nodes[n]
                ncell= node.mobilityCells[t]
                print('node.mobility cells ')
                print(node.mobilityCells)
                print('node.mobility route ')
                print(node.mobilityRoute)
                print('node cell at time t')
                print(ncell)
                cellIndex= self.gridLowCorners.index(ncell)
                print('cell index')
                print(cellIndex)
                self.cellsMatrix[t][cellIndex].append(n)
        
        #cover nodes at curr cell
        cellIndex= self.gridLowCorners.index(self.currCell)
        targets= self.cellsMatrix[0][cellIndex]
        print('targets exist at initial Step')
        for t in targets:
            self.coveredTargets[t]=0
            self.numCovTargets+=1
            self.reward+=(self.reward_scale)
        
            
    
    def runOptimization(self):
        
        currTS=0
        locationsAtNextTS={}
        done=False
        
        while not done :
            
            if(len(self.coveredTargets) >= self.numTargets or currTS >= self.maxTimeSteps-1):
                done= True
                break
                
            currTS+=1
            for nodeID in self.nodes:
                node= self.nodes[nodeID]
                print(node.mobilityCells)
                print(len(node.mobilityCells))
                locationsAtNextTS[nodeID]= node.mobilityCells[currTS]
                
            #print(locationsAtNextTS)
            [maxCovCell,  maxCovTs, route]= self.findClosestMostOccupiedCell(locationsAtNextTS)
            
            
            self.coverNodesAtCell(maxCovCell, maxCovTs, route)
            locationsAtNextTS.clear()
            
            print('NEW ITER Num COV TARGETS '+ str(self.numCovTargets))
            print(self.numCovTargets)
            print(len(self.coveredTargets))
            print(self.route)
            print(self.coveredTargets)
                

    
    def findClosestMostOccupiedCell(self, locationsAtNextTS):
        print(self.gridLowCorners)
        print(self.cellsMatrix)
        
        cellRoutesObject= self.cellsRoutes[self.currCell]
        for z in range(1, cellRoutesObject.maxHops+1): #iterate over zones
            if(self.totalSteps+z >= self.maxTimeSteps):
                break
            print('considering ZONE W/' +str(z)+ ' Steps AWAY')
            cellsInZoneWithNewTargets={}
            timeStepToBeThere= self.totalSteps+z 

            for cell in cellRoutesObject.cellsByHops[z]:
                print(cell)
                print(timeStepToBeThere)
                cellIndex= self.gridLowCorners.index(cell)
                print('cellIndex'+ str(cellIndex))
                print('targetIDsListThere')
                print(self.cellsMatrix[timeStepToBeThere])
                targetIDsListThere= self.cellsMatrix[timeStepToBeThere][cellIndex]
                print('targets to be there' )
                print(targetIDsListThere)
                
                for t in targetIDsListThere:
                    if(not t in self.coveredTargets):
                        if(not cell in cellsInZoneWithNewTargets):
                            cellsInZoneWithNewTargets[cell]=[]
                        cellsInZoneWithNewTargets[cell].append(t)
                print('cellsInZoneWithNewTargets')
                print(cellsInZoneWithNewTargets)

            if(len(cellsInZoneWithNewTargets)>0):
                print('new Targets at next Zones +++++++++++++++++++++++++++')
                maxCovCell= next(iter(cellsInZoneWithNewTargets))
                maxCovTs= cellsInZoneWithNewTargets[maxCovCell]
                for k in cellsInZoneWithNewTargets:
                    if(not k == maxCovCell and len(cellsInZoneWithNewTargets[k]) > len(maxCovTs)):
                        maxCovTs=  cellsInZoneWithNewTargets[k]
                        maxCovCell= k
                        
                        #print('cellroutes: ')
                       # print(cellRoutesObject)
                route= cellRoutesObject.cellRoutes[maxCovCell]
                return [maxCovCell,  maxCovTs, route]

                       
        print('no more targets to be in other cells --------------')
        print(self.currCell)
        maxCovCell= self.gridLowCorners.index(self.currCell)
        print(self.cellsMatrix[self.totalSteps+1])
            
        maxCovTs= self.cellsMatrix[self.totalSteps+1][maxCovCell]

        ts=[]
        for t in maxCovTs:
            if not t in self.coveredTargets:
                ts.append(t)
                    
        maxCovTs=ts
        route=[self.currCell]
        return [maxCovCell,  maxCovTs, route]

                
                    
            
    def coverNodesAtCell(self, maxCovCell, maxCovTs, route): 
        print('step '+str(self.totalSteps)+' covering cell '+ str(maxCovCell))
        
        if(len(route) == 1):
            self.totalSteps+=1
            self.route.append(self.currCell)
            
        elif(len(route) > 1):
            print('currCell')
            print(self.currCell)
            print('moving to cell ..steps= '+ str(len(route)))
            print(route)
            
            for i in range(1, len(route)):
                self.totalSteps+=1
                self.currCell= route[i]
                self.route.append(self.currCell)
                self.totalDist+=self.cellSideSize
                
            
        if( len(route)> 2):
            print('adding negatives for unfruitful steps')
            self.reward+=(len(route)-2) * -1 #give -1 for all unfruitful steps excluding initialcell and last cell in the route 

        for t in maxCovTs:
            if(not t in self.coveredTargets):
                self.coveredTargets[t]=self.totalSteps
                self.numCovTargets+=1
                self.reward+= 1*self.reward_scale
        
        print ('reward '+ str(self.reward))


    def euclideanDistance(self, a,b):
        a= np.array(a)
        b=np.array(b)
        dist = np.linalg.norm(a-b)
        return dist
    
    @staticmethod
    def findCell(coord, gridLowCorners, numCellsPerSide, cellSS):
         for x in range (0, numCellsPerSide):
            for y in range (0, numCellsPerSide):
               # print(x, y)
                cellX= x*cellSS
                cellY= y*cellSS
                isCell= TSP_greedy.isTargetInsideCell(coord, (cellX, cellY), cellSS)
                if(isCell): 
                    return (cellX, cellY)
                
                
    @staticmethod
    def isTargetInsideCell( loc, cellBottomLeft, cellSideSize):
        # print("isTargetInsideCell "+ str(t[0]) +", "+ str(t[1]))
        # print("topCOrner: ")
        # print(cellTopCorner)
        t= loc
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
                