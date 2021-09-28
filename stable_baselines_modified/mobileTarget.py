# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:56:11 2020

@author: HG19230
"""
import numpy as np

class mobileTarget (object):
    
    def __init__(self, ID, initiLocX, initialLocY, gridLowCorners, numCellsPerSide, cellSideSize, dimLimit):
         self.ID= ID
         # if(ID==0):
         #     self.initialLocation= (10.0, 10.0) #(10.0, 10.0)#(initiLocX, initialLocY)
         
         # else:
         #     self.initialLocation= (2.0, 10.0)
         
         self.initialLocation= ((initiLocX, initialLocY))
             
         self.currentLocation= self.initialLocation
         self.currentCell= self.findCell(gridLowCorners, numCellsPerSide, cellSideSize)
         self.initialCell= self.currentCell
         print('created target '+ str(self.ID) + 'loc '+ str(initiLocX) + ", "+ str(initialLocY))
         self.movementMode= 'uC'
         self.mobilityRate= 0
    
    def reset(self):
        self.currentLocation= self.initialLocation
        self.currentCell= self.initialCell
        print('reset target loc: ')
        print(self.currentLocation)

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