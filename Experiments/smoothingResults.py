# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:15:05 2020

@author: HG19230
"""
from statistics import mean
from itertools import chain
import pandas as pd
import numpy as np


def getSmoothedListSimpleAvg(listVals, window_size):
    list= list(chain.from_iterable([mean(listVals[i:i+window_size])]*window_size for i in range(0,len(listVals),window_size)))
    
    
def getSmoothedListRollingAvg(listVals, window_size):    
    numbers_series = pd.Series(listVals)

    windows = numbers_series.rolling(window_size)

    moving_averages = windows.mean()

    moving_averages_list = moving_averages.tolist()

    without_nans = moving_averages_list[window_size - 1:]
    
    return without_nans     

def smoothResults(folder, filename):

    stepsList= []
    enerList=[]
    rewardList=[]
    window_size=50
    file= folder+filename+'.dat'
    with open(file, 'r') as original:
        
        lines= original.readlines()
        first=True
        for line in lines:
            if(first):
                first=False
                continue
            values= line.split('\t')
            stepsList.append(float(values[1]))
            rewardList.append(float(values[2]))
            enerList.append(float(values[3]))
              
    
    #stepsSmoothed= list(chain.from_iterable([mean(stepsList[i:i+n])]*n for i in range(0,len(stepsList),n)))
    # print(stepsSmoothed)
    #stepsSmoothed= [sum(stepsList[i:i+n])//n for i in range(0,len(stepsList),n)]
    #print(stepsSmoothed)
    
    stepsSmoothed= getSmoothedListRollingAvg(stepsList, window_size) # [sum(stepsList[i:i+n])//n for i in range(0,len(stepsList),n)]
    
    enerSmoothed=  getSmoothedListRollingAvg(enerList, window_size) 
    #enerSmoothed= [sum(enerList[i:i+n])//n for i in range(0,len(enerList),n)]
    #enerSmoothed= list(chain.from_iterable([mean(enerList[i:i+n])]*n for i in range(0,len(enerList),n)))
    
    rewardSmoothed= getSmoothedListRollingAvg(rewardList, window_size) #
    #rewardSmoothed= [sum(rewardList[i:i+n])//n for i in range(0,len(rewardList),n)]
    #rewardSmoothed= list(chain.from_iterable([mean(rewardList[i:i+n])]*n for i in range(0,len(rewardList),n)))
    
    
    print(len(stepsSmoothed))
    
    i=0
    with open(file+'_smoothed.dat', 'w') as smoothed:
        smoothed.write('Episode_Group'+'\t'+ 'numSteps'+'\t'+'Reward'+'\t'+'Energy'+'\n')

        while(i < len(stepsSmoothed)):
            smoothed.write(str(i+1)+'\t'+ str(stepsSmoothed[i])+'\t'+str(rewardSmoothed[i])+'\t'+str(enerSmoothed[i])+'\n')
            i+=1
            
                        
folder= 'pyMan\\'#'RPGM_12A_10T'#pyMan' 'RPGM_20A_10T'#'Steps_2T_12A_ResetDiffPath'#'Steps_10T_52A_Step_Reset' #'Steps12A_10T_NOT_Step_RS10'#'Man_10T_24A_NOT_Step'#'ManMob_10T_24A2'
filename='Training_A4998_T30_ManhattanPython_54'
smoothResults(folder, filename)

          