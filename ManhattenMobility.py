# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:14:40 2021

@author: HG19230
"""
import random
import numpy as np
import OneDroneMobileTargetsEnv


def createManhattenLocation(GridLowCorners):
    return GridLowCorners[random.randint(0, len(GridLowCorners)-1)]


def doManhattenStep(coord, GridLowCorners, direction, cellSideSize, dimLimit):
    validSurroundingCells= returnValidSurroundingCells(coord,  dimLimit, cellSideSize)
    print('valid surrounding cells')
    print(validSurroundingCells)
    
    cellsProbabilities=[0]*len(GridLowCorners)
    
    
    if(direction == 'u'):
        upCell= (coord[0], coord[1]+cellSideSize)
        rightCell=(coord[0]+cellSideSize, coord[1])   #r
        leftCell= (coord[0]-cellSideSize, coord[1])   #l

    elif(direction == 'd'):
        upCell= (coord[0], coord[1]-cellSideSize)
        rightCell=(coord[0]-cellSideSize, coord[1])  #l
        leftCell= (coord[0]+cellSideSize, coord[1])  #r

    elif(direction == 'l'):
        upCell= (coord[0]-cellSideSize, coord[1])
        rightCell=(coord[0], coord[1]+cellSideSize)  #u
        leftCell= (coord[0], coord[1]-cellSideSize)  #d

    else: #r
        upCell= (coord[0]+cellSideSize, coord[1])
        rightCell=(coord[0], coord[1]-cellSideSize)  #d
        leftCell= (coord[0], coord[1]+cellSideSize)  #u

    print('upCell: ' + str(upCell))
    print('leftCell: '+ str(leftCell))
    print('rightCell: '+ str(rightCell))
    
    upValid=  upCell in validSurroundingCells
    print(upValid)
    rightValid= rightCell in validSurroundingCells
    print(rightValid)
    leftValid= leftCell in validSurroundingCells
    print(leftValid)
    if(upValid and rightValid and leftValid):
        print('all valid')
        cellsProbabilities[GridLowCorners.index(upCell)]= 0.5
        cellsProbabilities[GridLowCorners.index(rightCell)]= 0.25
        cellsProbabilities[GridLowCorners.index(leftCell)]= 0.25
        
    elif(not upValid and rightValid and leftValid):
        print('up NV .. Left V... Right V')

        cellsProbabilities[GridLowCorners.index(rightCell)]= 0.5
        cellsProbabilities[GridLowCorners.index(leftCell)]= 0.5
    
    elif( upValid and not rightValid and leftValid):
        print('up V .. Left V... Right NV')

        cellsProbabilities[GridLowCorners.index(upCell)]= 0.75
        cellsProbabilities[GridLowCorners.index(leftCell)]= 0.25
        
    elif( upValid and rightValid and not leftValid):
        print('up V .. Left NV... Right V')
        cellsProbabilities[GridLowCorners.index(upCell)]= 0.75
        cellsProbabilities[GridLowCorners.index(rightCell)]= 0.25
        
    elif(not upValid and rightValid and not leftValid):
        print('up NV .. Left NV... Right V')
        cellsProbabilities[GridLowCorners.index(rightCell)]= 1.0

    elif(not upValid and not rightValid and leftValid):
        print('up NV .. Left V... Right NV')
        cellsProbabilities[GridLowCorners.index(leftCell)]= 1.0
    
    elif(upValid and not rightValid and not leftValid):
        print('up V .. Left NV... Right NV')
        cellsProbabilities[GridLowCorners.index(upCell)]= 1.0



    cells= [*range(0, len(GridLowCorners), 1)] 
    print(coord)
    print(cells)
    print(cellsProbabilities)
    
    if( len(cells)==1):
             j = cells[0]
    else:
             j=  np.random.choice(
                 cells, 
                1,
                p=cellsProbabilities
                )
    print(GridLowCorners[2])
    print(j[0])
    nextCoord= GridLowCorners[j[0]]
    if(nextCoord==rightCell):
        if(direction == 'u'):
            direction='r'
        elif(direction == 'd'):
            direction='l'
        elif(direction == 'l'):
            direction='u'
        else:
            direction='d'

                
    elif(nextCoord==leftCell):
        if(direction == 'u'):
            direction='l'
        elif(direction == 'd'):
            direction='r'
        elif(direction == 'l'):
            direction='d'
        else:
            direction='u'

    return(nextCoord, direction)

def returnValidSurroundingCells(cell, dimLimit, cellSideSize):
    validCells=[]

    newCell= (cell[0], cell[1]+cellSideSize)
    if(isValid(newCell, dimLimit, cellSideSize)):
        validCells.append(newCell)
        
    newCell= (cell[0], cell[1]-cellSideSize)
    if(isValid(newCell, dimLimit, cellSideSize)):
        validCells.append(newCell)
    
    newCell= (cell[0]+cellSideSize, cell[1])
    if(isValid(newCell, dimLimit, cellSideSize)):
        validCells.append(newCell)
    
    newCell= (cell[0]-cellSideSize, cell[1])
    if(isValid(newCell, dimLimit, cellSideSize)):
        validCells.append(newCell)
        
    return validCells

def isValid(cell, dimLimit, cellSideSize):
    if(cell[0]>=0 and cell[0]<=(dimLimit-cellSideSize) and cell[1]>=0 and cell[1]<= (dimLimit-cellSideSize)):
        return True
    else:
        return False

##################################################################################
##################################################################################

# areaSize= np.power(12, 2) # keep area size as multiple of 5
# numTargets= 10
# coverageMajorSemiAxis= 3.5355339059327
# coverageMainorSemiAxis= 2.83 #2.53553390593275
# droneCoverageDiameter=  coverageMainorSemiAxis*2
# areaDimLimit= np.sqrt(areaSize)

# env = OneDroneMobileTargetsEnv.OneDroneMobileTargetsEnv(areaSize, numTargets, coverageMainorSemiAxis*2) 

# coord= createManhattenLocation(env.gridlowCorners)
# direction='u'

# for i in range(0, 20):
#     (nextCoord, nextDir)= doManhattenStep(coord, env.gridlowCorners, direction, env.cellSideSize, areaDimLimit)
#     coord= nextCoord
#     direction= nextDir
#     print('nextCoord: '+ str(coord))
#     print('nextDir: '+ str(direction))