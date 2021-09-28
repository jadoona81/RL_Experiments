# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:21:30 2021

@author: HG19230
"""

from OneDroneMobileTargetsEnv import OneDroneMobileTargetsEnv
import numpy as np

areaSize= np.power(24, 2) # keep area size as multiple of 5
numTargets= 10
coverageMajorSemiAxis= 3.5355339059327
coverageMainorSemiAxis= 2.83 #2.53553390593275
gamma = 0.95    # discount rate
learning_rate = 0.001


env = OneDroneMobileTargetsEnv(areaSize, numTargets, coverageMainorSemiAxis*2) 


for t in env.targets:
    print(t.ID)
    print(t.currentLocation)
    print(t.currentCell)
