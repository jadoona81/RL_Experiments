# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:36:06 2021

@author: HG19230
"""
import random
import numpy as np, numpy.random

cells=[i for i in range(10)]
cellsLastVisit=[-1]*len(cells)

    
    
def moveBasedOnShowUpPattern(timeStep):
    for cellID in cells:

        if(timeStep== cellID or timeStep-cellsLastVisit[cellID]==len(cells)):
            cellsLastVisit[cellID]= timeStep
            return cellID
        

print(cells)

for i in range(20):
    cell= moveBasedOnShowUpPattern(i)
    print(cell)
    
    
def createShowUpPrs():
    showUpPrs= np.random.dirichlet(np.ones(len(cells)),size=1) # [ random.random()] * len(cells)
    print(showUpPrs[0])
    
    return showUpPrs[0]


def createMobForTimeSteps(numTimeSteps, Prs):
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
    
    return mob

Prs= createShowUpPrs()
createMobForTimeSteps(10, Prs)



