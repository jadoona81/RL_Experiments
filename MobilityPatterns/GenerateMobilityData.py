# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:49:16 2021

@author: HG19230
"""
import math
import numpy as np
from MobilityPatterns.ManhattanMobilityMatlab import ManhattanMobileTarget
from MobilityPatterns.RPGM_Mobility import RPGM_Mobility

def createNodeFile(mobilityModel, folderName, nodeID, values):
    
    if mobilityModel == 'ManhattanPython':
        with open(folderName+"/Node"+str(nodeID)+".dat", "w") as targetfile:
            targetfile.write('TS'+'\t'+'X'+'\t'+'Y'+'\t'+'Direction'+'\t'+'Line_Man'+'\t'+'Column_Man'+'\n')
            targetfile.write(str(0)+'\t'+str(values[1])+'\t'+str(values[2])+'\t'+str(values[3])+'\t'+str(values[4])+'\t'+str(values[5])+'\n')

    elif mobilityModel == 'TM' or mobilityModel == 'ShowUpPattern':
        with open(folderName+"/Node"+str(nodeID)+".dat", "w") as targetfile:
            targetfile.write('TS'+'\t'+'X'+'\t'+'Y'+'\n')
            targetfile.write(str(0)+'\t'+str(values[1])+'\t'+str(values[2])+'\n')
        
    elif mobilityModel == 'RPGM':
        with open(folderName+"/Node"+str(nodeID)+".dat", "w") as targetfile:
            targetfile.write('TS'+'\t'+'X'+'\t'+'Y'+'\n')
            

def isTargetInsideCell(currentLocation, cellBottomLeft, cellSideSize):
         print("isTargetInsideCell "+ str(currentLocation[0]) +", "+ str(currentLocation[1]))
         print("topCOrner: ")
        # print(cellTopCorner)
         t= currentLocation
         cellTopCorner= (cellBottomLeft[0]+cellSideSize, cellBottomLeft[1]+cellSideSize)
         print(cellTopCorner)

         print("bottomLeft: ")
         print(cellBottomLeft)
         if (t[0] >= cellBottomLeft[0] and t[0] <= cellTopCorner[0] and 
            t[1] >= cellBottomLeft[1] and t[1] <= cellTopCorner[1]) : 
           # print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY: "+ str(t[0]) +", "+ str(t[1]))
            return True
         else : 
          #  print("not covered -----------------------"+ str(t[0]) +", "+ str(t[1]))
            return False    
        

def findCell(currLoc, gridLowCorners, numCellsPerSide, cellSideSize):
    #gridLowCorners.index(currLoc)
    
    for x in range (0, numCellsPerSide):
        for y in range (0, numCellsPerSide):
            print('find cell')
            print(x, y)
            cellX= x*cellSideSize
            cellY= y*cellSideSize
            isCell= isTargetInsideCell(currLoc, (cellX, cellY), cellSideSize)
            if(isCell): 
                return (cellX, cellY)

def  ShowUpMob(subcells, showUpPrs, gridLowCorners):
        
            print(subcells)
            if( len(subcells)==1):
                 j = subcells[0]
            else:
                 j=  np.random.choice(
                    subcells, 
                    1,
                    p=showUpPrs
                    )
            print('selected cell')
            print(j)
            return gridLowCorners[j[0]]

def moveTM(TM, prevLoc, gridLowCorners, timeStepScale, cellSideSize, numCellsPerSide):
    
    currentCell= prevLoc#findCell(prevLoc, gridLowCorners, numCellsPerSide, cellSideSize)

    print('Move TM current cell:' + str(currentCell))
    print(gridLowCorners)
    
    i= gridLowCorners.index(currentCell)
    neighbors= TM[i]

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
             
    currentCell= gridLowCorners[j[0]]
    newLoc= currentCell
    
    # dist= math.sqrt((newLoc[0]-prevLoc[0])**2 + (newLoc[1]-prevLoc[1])**2)
    # if(dist > 0):
    #     newDist= timeStepScale * dist
    #     ratio= newDist/dist
    #     newX= (1-ratio)*prevLoc[0] + ratio * newLoc[0]
    #     newY= (1-ratio)*prevLoc[1] + ratio * newLoc[1]
    #     currentLocation = (newX, newY)



    return newLoc
     
def createTM(cellsNeighbors):
    print('generate Mobility ----------------------------')
    M={}
    del cellsNeighbors[0] #del nodeID
    del cellsNeighbors[0] #del initLocX
    del cellsNeighbors[0] # del initLocY
        
    for s in cellsNeighbors:
            #cellID, numNeighbors, n1:pr1, n2:pr2
        sValues= s.split(',')
        cID= int(sValues[0])
        numNeighbors= int(sValues[1])
        M[cID]={}
        for i in range(numNeighbors):
            neighborID_Pr= sValues[2+i].split(':')
            M[cID][int(neighborID_Pr[0])]= neighborID_Pr[1]
    print(M)
    return M



def generateMobilityData(gridLowCorners, numTimeSteps, numNodes, xDim, yDim, cellSideSize, mobilityModel, modelName, randomLoc, timeStepScale, numCellsPerSide):

    minSpeed= 3/3.6
    maxSpeed= 5/3.6
    
    folderName= 'MobilityPatterns/'+mobilityModel+'/A'+str(xDim)+'_N'+str(numNodes)
    
    if mobilityModel == 'TM':
        #str(numTimeSteps)+
        with open("TargetsInitLocFiles/TargetsIniLocs_"+modelName+"_"+str(numTimeSteps)+".dat", "r") as expfile:
            for i in range(numNodes):
                tm={}
                nodeLine= expfile.readline()
                lineValues= nodeLine.split('\t')
                
                nodeID= lineValues[0]
                xLoc= int(lineValues[1])
                yLoc= int(lineValues[2])
                
                createNodeFile(mobilityModel, folderName, nodeID, lineValues)
                M= createTM(lineValues)
                
                numDataPoints= numTimeSteps*2

                with open(folderName+"/Node"+str(nodeID)+".dat", "a") as targetfile:
                    currLoc=(xLoc, yLoc)
                    for t in range(1, numDataPoints):
                        newLoc= moveTM(M, currLoc, gridLowCorners, timeStepScale, cellSideSize, numCellsPerSide)
                        targetfile.write(str(t)+'\t'+str(newLoc[0])+'\t'+str(newLoc[1])+'\n')
                        currLoc= newLoc
            
    elif mobilityModel == 'ShowUpPattern':
        
        print('generating mobility show up pattern')
        
        with open("TargetsInitLocFiles/TargetsIniLocs_"+modelName+"_"+str(numTimeSteps)+".dat", "r") as expfile:
            for i in range(numNodes):
                cells=[]
                prs=[]
                
                nodeLine= expfile.readline()
                lineValues= nodeLine.split('\t')
                
                nodeID= lineValues[0]
                print(nodeID)
                xLoc= int(lineValues[1])
                yLoc= int(lineValues[2])
                print(xLoc, yLoc)
                
                createNodeFile(mobilityModel, folderName, nodeID, lineValues)
                
                numDataPoints= numTimeSteps*2

                numCells= int(lineValues[3])
                print('numCells: '+ str(numCells))
                
                print(lineValues)
                print(len(lineValues))
                
                for i in range(numCells):
                    print(i)
                    cell,pr= lineValues[4+i].split(',')
                    cells.append(int(cell))
                    prs.append(float(pr))
                print('cells: ')
                print(cells)
                print('probs: ')
                print(prs)
                
                with open(folderName+"/Node"+str(nodeID)+".dat", "a") as targetfile:
                    currLoc=(xLoc, yLoc)
                    for t in range(1, numDataPoints):
                        newLoc= ShowUpMob(cells, prs, gridLowCorners)
                        targetfile.write(str(t)+'\t'+str(newLoc[0])+'\t'+str(newLoc[1])+'\n')
                        currLoc= newLoc
                        
                        
    elif mobilityModel == 'ManhattanPython':
        
        with open("TargetsInitLocFiles/TargetsIniLocs_"+modelName+"_"+str(numTimeSteps)+".dat", "r") as expfile:

           # expfile.readline()#skip title line
            for i in range(numNodes):
                
                locLine= expfile.readline()
                values=locLine.split('\t')
                
                manMobTarget= ManhattanMobileTarget(xDim, yDim, cellSideSize, cellSideSize, minSpeed, maxSpeed, randomLoc, timeStepScale)
                print('init Loc Values')
                print(values)
                
                if('\n' in values[-1]):
                        values[-1]= values[-1].rstrip("\n")
                        
                manMobTarget.setTargetLoc(values)
                createNodeFile(mobilityModel, folderName, i, values)
                
                numDataPoints= numTimeSteps*2

                with open(folderName+"/Node"+str(i)+".dat", "a") as targetfile:
                    for t in range(1, numTimeSteps+1):
                        manMobTarget.move()
                        print('GENERATED MOB DATA FOR TARGET >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+ str(i))
                        targetfile.write(str(t)+'\t'+str(manMobTarget.X)+'\t'+str(manMobTarget.Y)+'\t'+str(manMobTarget.direction)+'\t'+str(manMobTarget.line_manhattan)+'\t'+str(manMobTarget.column_manhattan)+'\n')
                        # if(manMobTarget.Y < 0):
                        #     print(' POINT Y  <  0 '+str(manMobTarget.Y)+'-----------------------------------------------------------')
                        #     return

    elif mobilityModel == 'RPGM':
        
            maxTargetsPerGroup= 2
            numGroups= int(numNodes/maxTargetsPerGroup)

            
            #get targets initial locations and groups
            with open("TargetsInitLocFiles/TargetsIniLocs_"+modelName+"_"+str(numTimeSteps)+".dat", "r") as expfile:
                groupsLine= expfile.readline()
                print(groupsLine)
                nodeGroups=[]
                values= groupsLine.split('\t')
                
                for val in values:
                    if('\n' in val):
                        val= val.rstrip("\n")
                    if(not val==''):
                        nodeGroups.append(int(val))
                    
                groupsXLoc={}
                groupsYLoc={}
                for i in range(numGroups):
                    locLine= expfile.readline()

                    values= locLine.split('\t')

                    if('\n' in values[1]):
                        values[1]= values[1].rstrip("\n")
                    
                    groupsXLoc[i]= float(values[1])
                    
                    
                    if( '\n' in values[2]):
                        values[2]= values[2].rstrip("\n")
                        
                    groupsYLoc[i]= float(values[2])
                    
            #generate the data 

            numDataPoints= numTimeSteps*2

            RPGM= RPGM_Mobility(xDim, yDim, numGroups, numNodes, numDataPoints, timeStepScale)
            RPGM.setGroupsAndLocs(nodeGroups, groupsXLoc, groupsYLoc)
            RPGM.generateMobility()
            
            for n in range(numNodes):
                createNodeFile(mobilityModel, folderName, n, [])

                with open(folderName+"/Node"+str(n)+".dat", "a") as targetfile:
                    for t in range(numDataPoints):
                        loc= RPGM.moveNode(n, t)
                        targetfile.write(str(t)+'\t'+str(loc[0])+'\t'+str(loc[1])+'\n')

                