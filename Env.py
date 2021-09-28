# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 11:02:40 2020

@author: ebaccourepbesaid
"""

import random
import math
import cmath
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import csv
from utility import * 
from random import seed
from random import randint
import control

class NetworkEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(NetworkEnv, self).__init__()
        print("init")
        self.M=5
        self.L=300000
        self.SFs=6
        self.K=self.SFs*self.M
        self.sp=10
        self.dmax=500
        self.N0=1.6*10**(-12)
        self.siDB=0 #-10 
        fc=2.5*10**9
        d0=1
        alphaa=3.7
        g0=(3*10**8/(4*np.pi*d0*fc))**2
        self.Tout=10**-3
        self.SI0=control.db2mag(self.siDB)
        self.H=math.sqrt(1/2)*(np.random.randn(self.K,self.M,self.L)+np.random.randn(self.K,self.M,self.L)*1j)
        #math.sqrt(1/2)*complex(np.random.randn(self.K,self.M,self.L),np.random.randn(self.K,self.M,self.L))
        self.d=np.random.randint(self.dmax/10,self.dmax,size=self.K)
        self.d=g0*self.d**(-alphaa)
        self.d=self.d**(1/2)
        self.D=np.diag(self.d)        
        self.action_space = spaces.Discrete(self.SFs)#MultiDiscrete([self.M,self.SFs]) 
        self.observation_space = spaces.Box(
                low=0, high=1.0, shape=(1,30), dtype=np.float32) 
        self.current_step = 0 #steps in the episode
        self.episode_reward=0 # episode reward
        self.episode=0 # epised
        self.totalEnergy=0
        self.resultsCsv=[] 
        #self.data = getDataList() # Get the created data
        self.rewards=0
        self.assignedLD=np.zeros(self.M)
        self.assignedSF=np.ones((self.M,self.SFs))
        self.maxLdPerChannel=6 # should be equal to SFs => check
        #self.states=
    def _next_observation(self): 
        self.cur_state=np.expand_dims(np.concatenate(self.assignedSF, axis=None),0) 
        #print(self.assignedSF)
        return self.cur_state     

    def _take_action(self, action):
        phy=1 # reset the reward in the time  step
        self.assignedLD[action[0]]=self.assignedLD[action[0]]+1           
        if self.assignedLD[action[0]]>self.maxLdPerChannel:
            phy=phy*0
        if self.assignedSF[action[0]][action[1]]==0: 
            phy=phy*0
        else:
            self.assignedSF[action[0]][action[1]]=0
        self.stepRewards= phy 
        self.stepEnergy=-getEnergy(self.current_step,action[0],action[1],self.episode,self.H,self.D,self.N0,self.SI0,self.Tout)*0.1


    def step(self, predictedAction):
        self._take_action(predictedAction)
        print(str(self.episode)+': '+str(self.current_step)+': '+str(predictedAction)+ ':'+ str(self.stepRewards))
        self.totalEnergy=self.totalEnergy+(self.stepEnergy) #penalty of the episode
        reward=self.stepEnergy+self.stepRewards #Reward of the episode: rewards + penalty
        self.episode_reward=self.episode_reward+self.stepRewards #only rewards are counted
        self.current_step=self.current_step+1 #increment for the next step
        done=False
        self.render("human")
        if(self.current_step % self.K ==0):
            self.current_step=0
            obs=self.reset()
        # if(self.episode>=len(self.data)-1):
        #     self.reset()
        #     done=True
        obs = self._next_observation()

        return obs, reward, done, {}

    def reset(self):
        self.resultsCsv.append([self.episode,self.episode_reward,self.totalEnergy,self.episode_reward+self.totalEnergy]) 
        with open("PPO_sigma_0.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.resultsCsv)
        self.episode_reward=0 # reset reawrds
        self.episode=self.episode+1 # pass to the nex episode
        self.current_step=0 # reset step
        self.totalEnergy=0
        self.assignedLD=np.zeros(self.M)
        self.assignedSF=np.ones((self.M,self.SFs))
        return self._next_observation()

    def render(self, mode='human'):
        if(self.current_step % self.K ==0):
            print("Episode: "+ str(self.episode)+ ", constraints respect: "+ str(self.episode_reward)+", Total energy (penalties): "+str(self.totalEnergy) + ", Total Rewards: "+str(self.episode_reward+self.totalEnergy))
            print("------------")


