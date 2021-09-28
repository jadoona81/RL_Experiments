# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 22:32:27 2021

@author: HG19230
"""
import math


prev= (0,0)
new= (10, 0)

timeStepsScale= 2

        

dist= math.sqrt((new[0]-prev[0])**2 + (new[1]-prev[1])**2)
if(dist > 0):
    newDist= timeStepsScale * dist
    ratio= newDist/dist
    newX= (1-ratio)*prev[0] + ratio * new[0]
    newY= (1-ratio)*prev[1] + ratio * new[1]
    currentLocation = (newX, newY)

print(currentLocation)
