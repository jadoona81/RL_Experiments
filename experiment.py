# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 08:12:17 2021

@author: HG19230
"
"""""

import numpy as np
from gym import spaces

observation_space = spaces.Box(
                low=0, high=1.0, shape=(1,30), dtype=np.float32) 

print(observation_space)
print(observation_space.shape)

assignedSF=np.ones((5,6))
print(assignedSF)

cur_state=np.expand_dims(np.concatenate(assignedSF, axis=None),0) 
print(cur_state)

observation_space = spaces.Box(
                low=0, high=1.0, shape=(1,2), dtype=np.float32) 
print(observation_space.shape)

cur_state= [0,1]