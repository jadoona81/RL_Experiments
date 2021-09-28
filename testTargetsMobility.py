# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 08:55:27 2021

@author: HG19230
"""
from OneDroneMobileTargetsEnv import OneDroneMobileTargetsEnv
import numpy as np



areaSize= np.power(12, 2) # keep area size as multiple of 4
numTargets= 2
coverageMajorSemiAxis= 3.5355339059327
coverageMainorSemiAxis= 2.83 #2.53553390593275



env= OneDroneMobileTargetsEnv(areaSize, numTargets, coverageMainorSemiAxis*2) 


target= env.targets[0]
for i in range(10):
    target.step(env.gridlowCorners)
    print(target.currentLocation)    
    print(target.currentCell)