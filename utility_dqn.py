# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:04:56 2020

@author: ebaccourepbesaid
"""
import numpy as np
import math
import cmath 
import h5py
import pickle
import scipy.io
from scipy.spatial import distance
from scipy.spatial.distance import squareform
import pandas as pd
from scipy.io import loadmat
import pandas


def getEnergy(k,m,alpha,i,H,D,N0,SI0,Tout):

    Hl=H[:,:,i]
    G=np.dot(D,Hl)
    # alpha=0:6 => 0 1 2 3 4 5 6
    E=(N0*SI0/abs(G[k,m])**2)*(2.0**(alpha+7-12))*Tout

    return E


def markov_EA(N,L,x,pi0,P):
    T=L #number of periods to simulate
    n = len(x) #number of state
    E =np.random.rand(1,T) # T-vector of draws from independent uniform [0,1]  #[0.9828,0.4022,0.6207,0.1544,0.3813] #
    #chain = sequence of realizations from the simulation
    E1=[]
    P=np.array(P)
    for n1 in range(1,N+1):
        cumsumP = P.dot(np.triu(np.ones(np.shape(P))))
        E0   =  np.random.rand(1,1) #0.5250 #
        ppi0 = np.append (0, np.cumsum(pi0))
        s0   = np.transpose((E0<=ppi0[1:n+1])*(E0>ppi0[0:n]))
        ss    = s0
        state=np.empty((5,1))
        #ss = np.expand_dims(ss,1)
        for t in range(0,T):
            state=np.hstack((state,ss))
            temp=np.transpose(ss)
            ppi= np.append (0,temp.dot(cumsumP))
            ss= np.transpose((E[0][t]<=ppi[1:n+1])*(E[0][t]>ppi[0:n]))
            ss = np.expand_dims(ss,1)
        state=state[:,1:]
        temp=np.transpose(x) 
        chain = temp.dot(state)
        E1.append(chain)
    return E1

def loadData(filename,column):
    excel_data_df = pandas.read_csv(filename)
    data=excel_data_df[column]
    d=data.append(data,ignore_index=True)
    #d=data.append(data,ignore_index=True)
    return d.append(data,ignore_index=True)
#loadData('PPO_more.csv','0.2')