# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:15:19 2020

@author: ebaccourepbesaid
"""

import sys

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import DQN

#from Env import NetworkEnv
from OneDroneMobileTargetsEnv import OneDroneMobileTargetsEnv
import pandas as pd
import numpy as np
import gym
import drone
import baselinePolicy
import math
from Benchmark.TSP_greedy import TSP_greedy
from MobilityPatterns.GenerateMobilityData import generateMobilityData

def runTrainedModel(env, modelName, targetsDatFolder, mobilityModel):

    tRandomLocs= False
    
    if(len(env.targets)==0):
        env.createTargets(False)

    
    model = DQN.load("PKL_Files/"+modelName+"_"+str(env.stepsLimit)+".pkl")
    model.exploration_fraction=0
    env.testing=True
    env.testFilesFolder=targetsDatFolder
   # env.stepsLimit= 5*env.stepsLimit
    obs = env.reset()
    print('done reset')
    done= False
    totalReward=0
    states=[]
    
    while not done:
        print('obs'+str(obs))
        states.append(obs)
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        totalReward+=rewards
        print('action'+ str(action))

        #env.render()
    print(env.route)
    print(totalReward)
    print(env.timeStep)
    
    return[totalReward, env.timeStep]

    
def runDRL(total_timesteps, env, droneAgent, modelName, mobilityModel, stateRep):
    env.testing=False
    env.trainingStarted=True
    tRandomLocs= True
    env.createTargets(True)

    with open("TargetsInitLocFiles/TargetsIniLocs_"+modelName+"_"+str(env.stepsLimit)+".dat", "w") as expfile:

        if(mobilityModel == "RPGM"):
            for i in range(env.numTargets):
                expfile.write(str(env.RPGM.NodeGroups[i]) +'\t')
            expfile.write('\n')
                
            for g in range(env.RPGM.numGroups):
                expfile.write(str(g)+'\t'+str(env.RPGM.GroupsInitLocX[g])+'\t'+str(env.RPGM.GroupsInitLocY[g])+'\n')
            
        else:
            
            for t in env.targets:
                if(mobilityModel == "ManhattanPython"):
                    mnObj= t.ManMobObject
                    expfile.write(str(t.ID)+'\t'+str(t.initialLocation[0])+'\t'+str(t.initialLocation[1])+'\t'+str(mnObj.direction)+'\t'+str(mnObj.line_manhattan)+'\t'+str(mnObj.column_manhattan)+'\t'+str(mnObj.speed)+'\n')
    
                elif(mobilityModel == "TM"):
                    transitionMatrix= t.M
                    expfile.write(str(t.ID)+'\t'+str(t.initialLocation[0])+'\t'+str(t.initialLocation[1]))
                    
                    for c in transitionMatrix:
                        neighbors= transitionMatrix[c]
                        expfile.write('\t'+str(c)+','+str(len(neighbors)))
                        for n in neighbors:
                            expfile.write(','+str(n)+':'+str(neighbors[n]))
                    expfile.write('\n')
                            
                elif(mobilityModel == "ShowUpPattern"):

                    expfile.write(str(t.ID)+'\t'+str(t.initialLocation[0])+'\t'+str(t.initialLocation[1]))
                    cells= t.subcells
                    prs= t.showUpPrs
                    
                    expfile.write('\t'+str(len(cells)))
                    for i in range(len(cells)):
                        expfile.write('\t'+str(cells[i])+','+str(prs[i]))
                        
                    expfile.write('\n')

                    #folderName= 'MobilityPatterns/'+mobilityModel+'/A'+str(int(env.areaDimLimit))+'_N'+str(env.numTargets)
                    
                    # with open(folderName+"/Node"+str(t.ID)+".dat", "w") as targetfile:
                    #     targetfile.write('TS'+'\t'+'X'+'\t'+'Y'+'\n')
                            
                    #     for i in range(env.stepsLimit+1):
                    #         cellID= t.MobPerTimeStep[i]
                    #         currentCell= env.gridlowCorners[cellID]
                    #         targetfile.write(str(i)+'\t'+str(currentCell[0])+'\t'+str(currentCell[1])+'\n')

                
                else:
                    expfile.write(str(t.ID)+'\t'+str(t.initialLocation[0])+'\t'+str(t.initialLocation[1])+'\n')
                
        ###################### DQL #########################
	#env = SubprocVecEnv([lambda:  NetworkEnv() for i in range(1)])
    model = DQN(MlpPolicy, env, verbose=0)#, exploration_fraction=0.005)#,cliprange_vf=-1)
    print(model.exploration_fraction)
    model.learn(total_timesteps) #2261475#3000000
    model.save("PKL_Files/"+modelName+"_"+str(env.stepsLimit)+".pkl")
    
            
    
def runBaseline(env, droneAgent, targetsDatFolder):
    tRandomLocs=False
    if(len(env.targets)==0):
        env.createTargets(tRandomLocs)

    env.testing=True
    env.testFilesFolder=targetsDatFolder

   # env.stepsLimit= 5*env.stepsLimit
    env.reset()

    [steps, finalReward, energy, numTargets]=baselinePolicy.runBaselinePolicy(env, droneAgent)

    print(finalReward)
    print(steps)
    print(numTargets)
    
    return[finalReward, steps, energy, numTargets]

    
def runBenchmark(env, targetsDatFolder, reward_scale, MobilityModel, horizontalEnergyPerMeter_J):
    
    env.reset()
    
    maxTimeSteps= env.stepsLimit
    
    print(env.numTargets)
    
    tsp= TSP_greedy(env.numTargets, maxTimeSteps, len(env.gridlowCorners), env.numCellsPerSide, env.gridlowCorners, env.cellSideSize, targetsDatFolder, reward_scale, MobilityModel, horizontalEnergyPerMeter_J)
    tsp.runOptimization()

    # for t in tsp.nodes:
    #     print(tsp.nodes[t].mobilityCells)
    #     print(tsp.nodes[t].mobilityRoute)
    energy= tsp.totalDist * horizontalEnergyPerMeter_J

    print(tsp.route)
    print(tsp.reward)
    print(tsp.totalSteps)
    
    return [tsp.reward, tsp.totalSteps, energy, len(tsp.coveredTargets)]

        

def train(minEpisodes, stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis,  coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, stateRep):
    
    testing= False
    env = OneDroneMobileTargetsEnv(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize,  MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 

    total_timesteps= minEpisodes*env.stepsLimit
    
    startLocsForTargets={}
    for t in env.targets:
        startLocsForTargets[t]= t.initialLocation()

    droneAgent= drone.drone(MobilityModel, areaSize, coverageMinorSemiAxis,  coverageMajorSemiAxis, altitude, cameraAngle, learning_rate, gamma, env.gridlowCorners, 
               env.cellSideSize, env.targets, 
               actions=list(range(env.n_actions)))
    
    env.placeDrone(droneAgent)

    #######################################
    runDRL(total_timesteps, env, droneAgent, modelName, MobilityModel, stateRep) #set Testing False
    
    
def test(areaSize, numTargets, coverageMinorSemiAxis,  coverageMajorSemiAxis, numCells, cellSideSize, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, squareSideLen, stateRep):

    testing= True
    env = OneDroneMobileTargetsEnv(areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize, MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 

    startLocsForTargets={}
    for t in env.targets:
        startLocsForTargets[t]= t.initialLocation()

    droneAgent= drone.drone(areaSize, learning_rate, gamma, env.gridlowCorners, 
               env.cellSideSize, env.targets, 
               actions=list(range(env.n_actions)))
    
    env.placeDrone(droneAgent)

    #generateMobilityData(env.stepsLimit*5, numTargets, squareSideLen, squareSideLen, env.cellSideSize, MobilityModel, modelName, False)
    #runBaseline(env, droneAgent, targetsDatFolder)

    runTrainedModel(env, modelName, targetsDatFolder, MobilityModel)

    #runBenchmark(env, targetsDatFolder, reward_scale)



def runExperiment(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, areaSquareSideLen, stateRep):

    numRuns= 50
    DRL= True
    Bench= True
    Base= True

    testing= True

    rBM_List=[]
    rDRL_List=[]
    rBL_List=[]
    
    sBM_List=[]
    sDRL_List=[]
    sBL_List=[]
    
    eBM_List=[]
    eDRL_List=[]
    eBL_List=[]
    
    tBM_List=[]
    tDRL_List=[]
    tBL_List=[]
    
    with open("ExperimentsFiles/Experiment_"+modelName+"_.dat", "w") as expfile:
        expfile.write('Steps_BM'+'\t'+'Steps_DRL'+'\t'+'Steps_BL'+'\t'+
                      'Reward_BM'+'\t'+'Reward_DRL'+'\t'+'Reward_BL'+'\t'+
                      'Energy_BM'+'\t'+'Energy_DRL'+'\t'+'Energy_BL'+'\t'+
                      'Targets_BM'+'\t'+'Targets_DRL'+'\t'+'Targets_BL'+'\n')
    
    #        expfile.write('Steps_BM'+'\t'+'Reward_BM'+'\t'+#'ener_BM'+'\t'+'NumCovTargets_BL'+'\t'+
    #                      'Steps_DRL'+'\t'+'Reward_DRL'+'\t'+#'ener_DRL'+'\t'+'NumCovTargets_DRL'+'\t'+
    #                      'Steps_BL'+'\t'+'Reward_BL'+'\n') #'\t'+'ener_BL'+'\t'+'NumCovTargets_BL'+'\n')

    for i in range(numRuns):

        with open("ExperimentsFiles/Experiment_"+modelName+"_.dat", "a") as expfile:

            env = OneDroneMobileTargetsEnv(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize,  MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 

            startLocsForTargets={}
            for t in env.targets:
                startLocsForTargets[t]= t.initialLocation()

            droneAgent= drone.drone(MobilityModel, areaSize, coverageMinorSemiAxis,  coverageMajorSemiAxis, altitude, cameraAngle, learning_rate, gamma, env.gridlowCorners, 
                           env.cellSideSize, env.targets, 
                           actions=list(range(env.n_actions)))

            env.placeDrone(droneAgent)
                
#################
            #if(not MobilityModel=='ShowUpPattern'):
            generateMobilityData(env.gridlowCorners, env.stepsLimit, numTargets, areaSquareSideLen, areaSquareSideLen, env.cellSideSize, MobilityModel, modelName, False, env.timeStepsScale, env.numCellsPerSide)
                
            if(Bench):
                [rBM, sBM, eBM, tBM]= runBenchmark(env, targetsDatFolder, reward_scale, MobilityModel, droneAgent.horizontalEnergyPerMeter_J)
            else:
                [rBM, sBM, eBM, tBM] = [0,0,0,0]
                
            rBM_List.append(rBM)
            sBM_List.append(sBM)
            eBM_List.append(eBM)
            tBM_List.append(tBM)

##############
            
            if(not Bench and DRL):
                env = OneDroneMobileTargetsEnv(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize,  MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 
    
                startLocsForTargets={}
                for t in env.targets:
                    startLocsForTargets[t]= t.initialLocation()
                
                droneAgent= drone.drone(MobilityModel, areaSize,coverageMinorSemiAxis,  coverageMajorSemiAxis, altitude, cameraAngle, learning_rate, gamma, env.gridlowCorners, 
                                env.cellSideSize, env.targets, 
                                actions=list(range(env.n_actions)))
                    
                env.placeDrone(droneAgent)
            
            if(DRL):
                [rDRL, sDRL]= runTrainedModel(env, modelName, targetsDatFolder, MobilityModel)
                eDRL= droneAgent.totalEnergy
                tDRL= len(droneAgent.coveredTargets)
            else:
                [rDRL, sDRL, eDRL, rDRL]= [0,0, 0,0]
            
            rDRL_List.append(rDRL)
            sDRL_List.append(sDRL)
            eDRL_List.append(eDRL)
            tDRL_List.append(tDRL)

# ##############

            if(not Bench and Base):
                env = OneDroneMobileTargetsEnv(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize,  MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 
    
                startLocsForTargets={}
                for t in env.targets:
                    startLocsForTargets[t]= t.initialLocation()
                
                droneAgent= drone.drone(MobilityModel, areaSize, coverageMinorSemiAxis,  coverageMajorSemiAxis, altitude, cameraAngle, learning_rate, gamma, env.gridlowCorners, 
                                env.cellSideSize, env.targets, 
                                actions=list(range(env.n_actions)))
                    
                env.placeDrone(droneAgent)

            if(Base):
                [rBL, sBL, eBL, tBL] = runBaseline(env, droneAgent, targetsDatFolder)
            else:
                [rBL, sBL, eBL, tBL] = [0,0,0,0]

            rBL_List.append(rBL)
            sBL_List.append(sBL)
            eBL_List.append(eBL)
            tBL_List.append(tBL)
            
# #############
            
            print('Trained Model')
            print(rDRL)
            print(sDRL)
            print(tDRL)
            
            print('Benchmark')
            print(rBM)
            print(sBM)
            print(tBM)
            # expfile.write(str(sBM)+'\t'+str(rBM)+'\t'+#'ener_BM'+'\t'+'NumCovTargets_BL'+'\t'+
            #                  str(sDRL)+'\t'+str(rDRL)+'\t'+#'ener_DRL'+'\t'+'NumCovTargets_DRL'+'\t'+
            #                  str(sBL)+'\t'+str(rBL)+'\n') #'\t'+'ener_BL'+'\t'+'NumCovTargets_BL'+'\n')
            
            expfile.write(str(sBM)+'\t'+str(sDRL)+'\t'+str(sBL)+'\t'+
                           str(rBM)+'\t'+str(rDRL)+'\t'+str(rBL)+'\t'+
                           str(eBM)+'\t'+str(eDRL)+'\t'+str(eBL)+'\t'+
                           str(tBM)+'\t'+str(tDRL)+'\t'+str(tBL)+'\n')
            
    return [eBM_List, eDRL_List, eBL_List, rBM_List, rDRL_List, rBL_List, sBM_List, sDRL_List, sBL_List]



def runExperiments(variance, stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, squareSideLen, stateRep):
    

    
    targetsVals=[1, 5, 10, 30, 50]
    
    areaSideLenList=[999, 3000, 4998, 7000, 10000]
    numCellsList= [9, 25, 36, 49, 64]
    cellSideLenList= [333, 600, 833, 1000, 1250]
    altitudesForAreas= [40, 70, 100, 120, 150]
    cameraAngle= 55
    semiMinorAxisList= [235.46655813512035, 424.26406871192853, 589.0199487283942, 707.1067811865476, 883.8834764831845]
    semiMajorAxisList= [357.7172565323477, 645.6331250169183, 894.8621579652718, 1074.2898002735851, 1342.8622503419815]


    mobilityModelVals= ['TM', 'ManhattanPython', 'RPGM']
    
    if(variance == 'targets'):
        varList= targetsVals
    elif(variance == 'cells'):
        varList = numCellsList
    else:
        varList = mobilityModelVals

    
    titlePrefix="Title"
    filePrefix=variance+"Variation_"
    
    with open(filePrefix+"ener.dat", "w") as enerfile:
          enerfile.write(titlePrefix+
                      '\t'+'BM'+'\t'+'BM_min'+'\t'+'BM_max'+
                      '\t'+'DRL'+'\t'+'DRL_min'+'\t'+'DRL_max'+
                      '\t'+'BL'+'\t'+'BL_min'+'\t'+'BL_max'+
                      '\n')
    
    with open(filePrefix+"reward.dat", "w") as rewardfile:
          rewardfile.write(titlePrefix+
                      '\t'+'BM'+'\t'+'BM_min'+'\t'+'BM_max'+
                      '\t'+'DRL'+'\t'+'DRL_min'+'\t'+'DRL_max'+
                      '\t'+'BL'+'\t'+'BL_min'+'\t'+'BL_max'+
                      '\n')
    
    with open(filePrefix+"steps.dat", "w") as stepsfile:
          stepsfile.write(titlePrefix+
                      '\t'+'BM'+'\t'+'BM_min'+'\t'+'BM_max'+
                      '\t'+'DRL'+'\t'+'DRL_min'+'\t'+'DRL_max'+
                      '\t'+'BL'+'\t'+'BL_min'+'\t'+'BL_max'+
                      '\n')


    areaValsIndex= 2
    targetsNominal= 10
    mobilityNominal= 'ManhattanPython'

    numTargets= targetsNominal
    MobilityModel= mobilityNominal
    
        
    for val in varList: #targetsVariations: #areaSizeVariations: coverageVariations
        if(variance == 'targets'):
            numTargets= val
        elif(variance == 'cells'):
            areaValsIndex= numCellsList.index(val)
            numCells= val
        else:
            MobilityModel= val

        coverageMajorSemiAxis= semiMajorAxisList[areaValsIndex] #3.5355339059327
        coverageMinorSemiAxis= semiMinorAxisList[areaValsIndex] # 2.83 #2.53553390593275
        areaSquareSideLen= areaSideLenList[areaValsIndex] #36  #>> #numCells  #2*numCells  #1.5*numCells
        numCells= numCellsList[areaValsIndex] #6
        cellSideSize = cellSideLenList[areaValsIndex]  #4
        altitude= altitudesForAreas[areaValsIndex] 

        [eBM_List, eDRL_List, eBL_List, rBM_List, rDRL_List, rBL_List, sBM_List, sDRL_List, sBL_List]= runExperiment(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, squareSideLen)
        
        with open(filePrefix+"ener.dat", "a") as enerfile:
            enerfile.write(titlePrefix+
                      '\t'+str(sum(eBM_List)/len(eBM_List))+'\t'+str(min(eBM_List))+'\t'+str(max(eBM_List))+
                      '\t'+str(sum(eDRL_List)/len(eDRL_List))+'\t'+str(min(eDRL_List))+'\t'+str(max(eDRL_List))+
                      '\t'+str(sum(eBL_List)/len(eBL_List))+'\t'+str(min(eBL_List))+'\t'+str(max(eBL_List))+
                      '\n')
    
        with open(filePrefix+"reward.dat", "a") as rewardfile:
            rewardfile.write(titlePrefix+
                      '\t'+str(sum(rBM_List)/len(rBM_List))+'\t'+str(min(rBM_List))+'\t'+str(max(rBM_List))+
                      '\t'+str(sum(rDRL_List)/len(rDRL_List))+'\t'+str(min(rDRL_List))+'\t'+str(max(rDRL_List))+
                      '\t'+str(sum(rBL_List)/len(rBL_List))+'\t'+str(min(rBL_List))+'\t'+str(max(rBL_List))+
                      '\n')
    
        with open(filePrefix+"steps.dat", "a") as stepsfile:
            stepsfile.write(titlePrefix+
                      '\t'+str(sum(sBM_List)/len(sBM_List))+'\t'+str(min(sBM_List))+'\t'+str(max(sBM_List))+
                      '\t'+str(sum(sDRL_List)/len(sDRL_List))+'\t'+str(min(sDRL_List))+'\t'+str(max(sDRL_List))+
                      '\t'+str(sum(sBL_List)/len(sBL_List))+'\t'+str(min(sBL_List))+'\t'+str(max(sBL_List))+
                      '\n')

def TrainExperiment(variance, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, squareSideLen, stateRep):
    
    targetsVals=[1, 5, 10, 30, 50]
    
    areaSideLenList=[999, 3000, 4998, 7000, 10000]
    numCellsList= [9, 25, 36, 49, 64]
    cellSideLenList= [333, 600, 833, 1000, 1250]
    altitudesForAreas= [40, 70, 100, 120, 150]
    cameraAngle= 55
    semiMinorAxisList= [235.46655813512035, 424.26406871192853, 589.0199487283942, 707.1067811865476, 883.8834764831845]
    semiMajorAxisList= [357.7172565323477, 645.6331250169183, 894.8621579652718, 1074.2898002735851, 1342.8622503419815]

    mobilityModelVals= ['TM', 'ManhattanPython', 'RPGM']
    
    if(variance == 'targets'):
        varList= targetsVals
    elif(variance == 'cells'):
        varList = numCellsList
    else:
        varList = mobilityModelVals

    areaValsIndex= 2
    targetsNominal= 10
    mobilityNominal= 'ManhattanPython'

    numTargets= targetsNominal
    MobilityModel= mobilityNominal
    
        
    for val in varList: #targetsVariations: #areaSizeVariations: coverageVariations
        if(variance == 'targets'):
            numTargets= val
        elif(variance == 'cells'):
            areaValsIndex= numCellsList.index(val)
            numCells= val
        else:
            MobilityModel= val

        coverageMajorSemiAxis= semiMajorAxisList[areaValsIndex] #3.5355339059327
        coverageMinorSemiAxis= semiMinorAxisList[areaValsIndex] # 2.83 #2.53553390593275
        areaSquareSideLen= areaSideLenList[areaValsIndex] #36  #>> #numCells  #2*numCells  #1.5*numCells
        numCells= numCellsList[areaValsIndex] #6
        cellSideSize = cellSideLenList[areaValsIndex]  #4
        altitude= altitudesForAreas[areaValsIndex] 
    
        reward_scale= 10
        gamma = 0.95    # discount rate
        learning_rate = 0.001
        areaSize= np.power(areaSquareSideLen, 2) # keep area size as multiple of 4    
        targetsDatFolder='MobilityPatterns/'+MobilityModel+'/A'+str(areaSquareSideLen)+'_N'+ str(numTargets)
        modelName= "A"+str(areaSquareSideLen)+"_T"+str(numTargets)+"_"+MobilityModel+"_"+stateRep

        train(areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder)

def testGeneratedData(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, areaSquareSideLen, stateRep):

    testing = True
    env = OneDroneMobileTargetsEnv(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis*2, numCells, cellSideSize,  MobilityModel, reward_scale, testing, targetsDatFolder, stateRep) 

    startLocsForTargets={}
    for t in env.targets:
        startLocsForTargets[t]= t.initialLocation()

    droneAgent= drone.drone(MobilityModel, areaSize, coverageMinorSemiAxis,  coverageMajorSemiAxis, altitude, cameraAngle, learning_rate, gamma, env.gridlowCorners, 
                           env.cellSideSize, env.targets, 
                           actions=list(range(env.n_actions)))

    env.placeDrone(droneAgent)
    
    print('cellsPerSide: '+ str(env.numCellsPerSide))
    print('timeStepsScale: '+ str(env.timeStepsScale))
    print('cellSideSize:'+ str(env.cellSideSize))
                
    generateMobilityData(env.gridlowCorners, env.stepsLimit, numTargets, areaSquareSideLen, areaSquareSideLen, env.cellSideSize, MobilityModel, modelName, False, env.timeStepsScale, env.numCellsPerSide)


def main(args):

    stateRep= 'TargetCov'#'CurrSeen' #'TargetCov CurrSeen#@@@@@@@@*@*@*@*@*@*@*@*@*@*@*@*@ ((((( CHANGE ))))) @*@*@*@*@*@*@*@*@*@*@*@*@@@@@@@@@
    print(args)
    minEpisodes= int(args[1])
    MobilityModel= args[2] #"ManhattanPython" #RPGM #"TM" #StepsMatlab #Manhatten
    areaValsIndex= int(args[3]) #0-4 new vals, 5 old vals
    numTargets= int(args[4]) #[1, 5, 10, 30, 50]

    areaSideLenList=[999, 3000, 4998, 7000, 10000, 24, 12, 28]
    numCellsList= [9, 25, 36, 49, 64, 36, 9, 49]
    cellSideLenList= [333, 600, 833, 1000, 1250, 4, 4, 4]
    altitudesForAreas= [40, 70, 100, 120, 150, 20, 20, 20]
    cameraAngle= 55
    semiMinorAxisList= [235.46655813512035, 424.26406871192853, 589.0199487283942, 707.1067811865476, 883.8834764831845, 2.83, 2.83, 2.83]
    semiMajorAxisList= [357.7172565323477, 645.6331250169183, 894.8621579652718, 1074.2898002735851, 1342.8622503419815, 3.5355339059327, 3.5355339059327, 3.5355339059327]

    coverageMajorSemiAxis= semiMajorAxisList[areaValsIndex] #3.5355339059327
    coverageMinorSemiAxis= semiMinorAxisList[areaValsIndex] # 2.83 
    areaSquareSideLen= areaSideLenList[areaValsIndex] #36  #>> #numCells  #2*numCells  #1.5*numCells
    numCells= numCellsList[areaValsIndex] #6
    cellSideSize = cellSideLenList[areaValsIndex]  #4
    altitude= altitudesForAreas[areaValsIndex] #20

    stepsLimitPerEpisode= math.ceil(float(args[5])*numCells)


    reward_scale= 10 
    gamma = 0.95    # discount rate
    learning_rate = 0.001
    areaSize= np.power(areaSquareSideLen, 2) # keep area size as multiple of 4    
    targetsDatFolder='MobilityPatterns/'+MobilityModel+'/A'+str(areaSquareSideLen)+'_N'+ str(numTargets)
    modelName= "A"+str(areaSquareSideLen)+"_T"+str(numTargets)+"_"+MobilityModel+"_"+stateRep

    if(args[6] == "train"):
        train(minEpisodes, stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, stateRep)
    else:
        #testGeneratedData(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis, coverageMajorSemiAxis, numCells, cellSideSize, altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, areaSquareSideLen)

        runExperiment(stepsLimitPerEpisode, areaSize, numTargets, coverageMinorSemiAxis,  coverageMajorSemiAxis, numCells, cellSideSize,altitude, cameraAngle, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, areaSquareSideLen, stateRep)

    #test(areaSize, numTargets, coverageMinorSemiAxis, modelName, MobilityModel, reward_scale, learning_rate, gamma, targetsDatFolder, squareSideLen)



if __name__ == "__main__":
    #arguments       minEpisodes      approach    areaValsIndex      numTargets      stepsLimitPerEpisode   train/test
	main(sys.argv)

