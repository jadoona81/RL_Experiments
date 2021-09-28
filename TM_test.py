# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:12:57 2021

@author: HG19230
"""
import random
import numpy as np

numCellsPerSide=6
cellSideSize= 833


def buildGrid():
            gridLowCorners=[]
            for x in range (0, numCellsPerSide):
                for y in range (0, numCellsPerSide):
                    print(x, y)
                    cell= (x*cellSideSize,y*cellSideSize)
                    gridLowCorners.append(cell)
            return gridLowCorners

def moveUsingProbabilisticTransitionMatrix(gridLowCorners, currentCell, M):

         i= gridLowCorners.index(currentCell)
         neighbors= M[i]
         numCells=  len(neighbors)

         ListNextCells= []
         ListNextCellsPrs=[]
         
         
         for c in neighbors:
            ListNextCells.append(c)
            ListNextCellsPrs.append(neighbors[c])
        
         print(ListNextCells)

         print(ListNextCellsPrs)

         
         if( len(ListNextCells)==1):
             j = ListNextCells[0]
         else:
             j=  np.random.choice(
                 ListNextCells, 
                1,
                p=ListNextCellsPrs
                )
         print(j)
         currentCell= gridLowCorners[j[0]]
         print(currentCell)
         return currentCell
         
def createTransitionMatrix():
        gridLowCorners= buildGrid()
        largePr=1.0
        numCells= len(gridLowCorners)
        M = {}
        #[[0]*self.numCells for _ in range(self.numCells)]

        path=[]
        path.append(0)
        for (i) in  range(numCells):
            M[i]={}
            surroundingCells=[]
            print('investigating cell ('+str(i)+'): '+ str(gridLowCorners[i]))
            for (j) in  range(numCells):
                print(j)
                if(not i==j):# and not j in path):
                    coordsI= gridLowCorners[i]
                    coordsJ= gridLowCorners[j]
                    
                    if(abs(coordsI[0]-coordsJ[0]) <=4 and abs(coordsI[1]-coordsJ[1])<=4):
                        surroundingCells.append(j)
            
            print(surroundingCells)
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
                M[i][j]=PrPerCell
            
            print(len(M[i]))
            print(selectedJ)
            
            M[i][selectedJ]= largePr
            path.append(selectedJ)
            print(path)

        print('transition Matrix')
        print(M)
        print(path)
        return M
    
def currCreateTranisitionMatrix():
        gridLowCorners= buildGrid()
        
        largePr=1.0
        numCells= len(gridLowCorners)
        M = {}
        #[[0]*self.numCells for _ in range(self.numCells)]

        path=[]
        path.append(0)
        for (i) in  range(numCells):
            M[i]={}
            surroundingCells=[]
            print('investigating cell ('+str(i)+'): '+ str(gridLowCorners[i]))
            for (j) in  range(numCells):
                if(not i==j):# and not j in path):
                    coordsI= gridLowCorners[i]
                    coordsJ= gridLowCorners[j]
                    
                    if(abs(coordsI[0]-coordsJ[0]) <=cellSideSize and abs(coordsI[1]-coordsJ[1])<=cellSideSize):
                        surroundingCells.append(j)
            
            print(surroundingCells)
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
                M[i][j]=PrPerCell
            
            print(len(M[i]))
            print(selectedJ)
            
            M[i][selectedJ]= largePr
            path.append(selectedJ)
        
        print(M)
        return M
            
        
M= currCreateTranisitionMatrix()
cell=  moveUsingProbabilisticTransitionMatrix((4,0), M)

string= str(0)
                    
for c in M:
    neighbors= M[c]
    string+=('\t'+str(c)+','+str(len(neighbors)))
    for n in neighbors:
        string+=(','+str(n)+':'+str(neighbors[n]))
string+=('\n')
                  
print(string)  
                    