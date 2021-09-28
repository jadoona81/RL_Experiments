# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 10:17:13 2021

@author: HG19230
"""

import random
import math
import numpy as np

class Generate_Mobility_group_random:
    

# function s_mobility = Generate_Mobility_group_random(s_input)
#     %The Random Waypoint mobility model.
#     global s_mobility_tmp;
#     global nodeIndex_tmp;
#     rng(s_input.seed);
#     s_mobility.NB_NODES = s_input.NB_NODES;
#     s_mobility.SIMULATION_TIME = s_input.SIMULATION_TIME;
#     radiusGroup = s_input.RADIUS;

    
    def __init__(self, s_input, targetGroups, timeStepsScale):
        
        self.timeStepsScale= timeStepsScale
        self.s_input= s_input
        self.xDim= self.s_input['V_POSITION_X_INTERVAL'][1]
        self.yDim= self.s_input['V_POSITION_Y_INTERVAL'][1]
        
        #s_mobility.NB_NODES = s_input.NB_NODES
        #s_mobility.SIMULATION_TIME = s_input.SIMULATION_TIME
        
        self.s_mobility= {'NB_NODES': s_input['NB_NODES'], 'SIMULATION_TIME': s_input['SIMULATION_TIME']}
        self.s_mobility_tmp= {}#'NB_NODES': s_input['NB_NODES'], 'SIMULATION_TIME': s_input['SIMULATION_TIME']}

        
        self.radiusGroup = s_input['RADIUS']
        self.nbGroups = s_input['NB_GROUPS']
        self.groupsXLocDict={}
        self.groupsYLocDict={}
#     group = randi([1 nbGroups], 1, s_mobility.NB_NODES);  %random assignation of group for targets
        random.seed(s_input['seed'])
        #self.targetGroups= [random.randint(0, self.nbGroups-1) for iter in range(self.s_mobility['NB_NODES'])]
        self.targetGroups= targetGroups
        # print('targetGroups')
        # print(self.targetGroups)

#     for groupIndex = 1 : nbGroups
#         LocationX_Group(groupIndex) = unifrnd(s_input.V_POSITION_X_INTERVAL(1),s_input.V_POSITION_X_INTERVAL(2));
#         LocationY_Group(groupIndex) = unifrnd(s_input.V_POSITION_Y_INTERVAL(1),s_input.V_POSITION_Y_INTERVAL(2));
#     end
    
        for gi in range(0, self.nbGroups):
            self.groupsXLocDict[gi]= random.randrange(s_input['V_POSITION_X_INTERVAL'][0], s_input['V_POSITION_X_INTERVAL'][1])
            self.groupsYLocDict[gi]= random.randrange(s_input['V_POSITION_Y_INTERVAL'][0], s_input['V_POSITION_Y_INTERVAL'][1])

        # print(self.groupsXLocDict)
        # print(self.groupsYLocDict)
        
    

    def generateMobility(self ):
            
    #     for nodeIndex_tmp = 1 : s_mobility.NB_NODES
    #         %%%%%%%%%%%%%%%%%%%%%%%%%%%Initialize:
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING = [];
    #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION = [];
            
    #         %previousX = unifrnd(s_input.V_POSITION_X_INTERVAL(1),s_input.V_POSITION_X_INTERVAL(2));
    #         %previousY = unifrnd(s_input.V_POSITION_Y_INTERVAL(1),s_input.V_POSITION_Y_INTERVAL(2));
            self.s_mobility['VS_NODE']=[]#{} for _ in range(self.s_mobility['NB_NODES'])]
            self.s_mobility_tmp['VS_NODE']=[{} for _ in range(self.s_mobility['NB_NODES'])]
    
    #        print(len(self.s_mobility_tmp['VS_NODE']))
    
            #print('NB Nodes')
           # print(self.s_mobility['NB_NODES'])
            for nodeIndex_tmp in range(self.s_mobility['NB_NODES']):
                print('NEW ITERATION FOR '+str(nodeIndex_tmp)+ '=====================================================================')
                #self.s_mobility_tmp['VS_NODE'].append({})
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME']=[]
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X']=[]#np.array([])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y']=[]#np.array([])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION']=[]#np.array([])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE']=[]#np.array([])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING']=[]#np.array([])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION']=[]#np.array([])
            
    #            print('initializing s_mob_tmp')
    #            print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp])
    
    #         omega = rand * pi;
    #         radius = rand * radiusGroup;
    #         deltaX = sqrt(radius) * cos(omega);
    #         deltaY = sqrt(radius) * sin(omega);
    #         j = group(nodeIndex_tmp);
            
    #         previousX = LocationX_Group(j) + deltaX;
    #         previousY = LocationY_Group(j) + deltaY;
            
    #         previousDuration = 0;
    #         previousTime = 0;
    #         Out_setRestrictedWalk_random_waypoint(previousX,previousY,previousDuration,previousTime,s_input, 1);
                previousX=-1
                previousY=-1
                
                while previousX> self.xDim or previousX < 0 or previousY> self.yDim or previousY < 0:
    
                    omega= random.random() * math.pi
                    radius = random.random() * self.radiusGroup
                    deltaX = math.sqrt(radius) * math.cos(omega)
                    deltaY = math.sqrt(radius) * math.sin(omega)
                    j = nodeIndex_tmp #self.targetGroups[nodeIndex_tmp] ############## ^^^^^^^^^^^^^^^^^^^ TEST 
                    
                    # print(self.targetGroups)
                    # print(nodeIndex_tmp)
                    # print(j)
                    previousX = self.groupsXLocDict[j] + deltaX
                    previousY = self.groupsYLocDict[j] + deltaY
                
                print('prevX, prevY')
                print(previousX, previousY)
                
                previousDuration = 0
                previousTime = 0
    
                print(previousX,previousY,previousDuration,previousTime,self.s_input, 1)
    
                self.Out_setRestrictedWalk_random_waypoint(nodeIndex_tmp, previousX,previousY,previousDuration,previousTime, 1)
    
                #print('initializing s_mob_tmp')
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp])
                
    #    def Out_setRestrictedWalk_random_waypoint(nodeIndex_tmp,previousX,previousY,previousDuration,previousTime,s_input, init):
    
        
    #         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #         %%Promenade     
    #         while (s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end) < s_input.SIMULATION_TIME)
    #             if (s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(end) == false)
    #                 previousX = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end);
    #                 previousY = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end);
    #                 previousDuration = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end);
    #                 previousTime = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end);
    #                 Out_setRestrictedWalk_random_waypoint(previousX,previousY,previousDuration,previousTime,s_input, 0);
    #             else
    #                 %%%%%%%%Node is taking a pause:
    #                 previousDirection = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(end);
    #                 previousSpeed = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end);
    #                 previousX = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end);
    #                 previousY = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end);
    #                 previousTime = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end);
    #                 previousDuration = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end);
    #                 distance = previousDuration*previousSpeed;
    #                 %%%
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end+1,1) = previousTime + previousDuration;
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end+1,1) = (previousX + distance*cosd(previousDirection));
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end+1,1) = (previousY + distance*sind(previousDirection));
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(end+1,1) = 0;
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end+1,1) = 0;
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(end+1,1) = false;
    #                 s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end+1,1) = Out_adjustDuration_random_waypoint(s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end),unifrnd(s_input.V_PAUSE_INTERVAL(1),s_input.V_PAUSE_INTERVAL(2)),s_input);
    #             end
    #         end
    
            
                while(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1] < self.s_input['SIMULATION_TIME']):
    
                    print("another WHILE ITERATION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print('V_TIME')
                    print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1])
                    print("SIMULATION TIME: "+str(self.s_input['SIMULATION_TIME']))
                    
                    
                    if self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'][-1] == False:
                        print('node not moving ... +++++++++++++++++++++++++++++++++++++++++++++++++++')
                        previousX = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'][-1]
                        previousY = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'][-1]
                        previousDuration = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'][-1]
                        print('prevDuration'+ str(previousDuration))
                        previousTime = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1]
                        print('prevTime'+ str(previousTime))
                        
                        #print('data points: x,y,dur,time -------------')
                        #print(previousX,previousY,previousDuration,previousTime)
                        
                        self.Out_setRestrictedWalk_random_waypoint(nodeIndex_tmp, previousX,previousY,previousDuration,previousTime, 0)
    
                    else:
                        print('node moving ... adding Y ++++++++++++++++++++++++++++++++++++++++++++++++')
                        previousDirection = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'][-1]
                        previousSpeed = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'][-1]
                        previousX = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'][-1]
                        previousY = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'][-1]
                        previousTime = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1]
                        previousDuration = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'][-1]
                        distance = previousDuration*previousSpeed
    

                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'])
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'].append(previousTime + previousDuration)
    
                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'])
                        
                        #fixedLoc= self.fixNewLocBasedOnTimeScale((previousX, previousY) , (previousX + distance*self.cosd(previousDirection), previousY + distance*self.sind(previousDirection)))
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'].append(previousX + distance*self.cosd(previousDirection))
    
                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'])
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'].append(previousY + distance*self.sind(previousDirection))
                        # print('prevY: '+str(previousY))
                        print('distance: '+ str(distance))
                        # print('sind(previousDirection): '+ str(self.sind(previousDirection)))
                        # print(previousY + distance*self.sind(previousDirection))
                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'])
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'].append(0)
    
                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'])
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'].append(0)
    
                       # arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'])
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'].append(False)
    
                        ##### Uniform Dist
                        #unifrnd= np.random.uniform(self.s_input['V_PAUSE_INTERVAL'][0],self.s_input['V_PAUSE_INTERVAL'][0])
                        #### Normal Dist
                        mean= (self.s_input['V_PAUSE_INTERVAL'][0]+self.s_input['V_PAUSE_INTERVAL'][1])/2
                        unifrnd= random.gauss(mean, 0.25*mean)
    
                        #arrLength= len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'])
                        print('arwp call 1 --- pause interval')
                        dur= self.Out_adjustDuration_random_waypoint(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1], unifrnd)
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'].append(dur)
                        
                        print('data points: x,y,dur,time -------------')
                        print(previousX+distance*self.cosd(previousDirection),previousY+distance*self.sind(previousDirection),dur,previousTime+previousDuration)

                print("ENDDDDDDDDDDDD WHILE  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                ############## END WHILE ###############################
    
        #         %%%%%%%%%%%%%%%%%%To have speed vectors as well rather than
        #         %%%%%%%%%%%%%%%%%%only the scalar value:
        #         nb_speed = length(s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE);
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X = zeros(nb_speed,1);
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y = zeros(nb_speed,1);
        #         for s = 1:nb_speed
        #             speed = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(s);
        #             direction = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(s);
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X(s) = speed*cosd(direction);
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y(s) = speed*sind(direction);
        #         end
    
                #print('After whie for time steps s_mob_tmp')
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp])
                
                nb_speed = len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'] = [0]*nb_speed  #np.zeros((nb_speed,1))
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'] = [0]*nb_speed #np.zeros((nb_speed, 1))
                print('nb_speed'+ str(nb_speed))
                
                for s in range(nb_speed):
                    speed = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'][s]
                    direction = self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'][s]
                    print('speed: '+ str(speed))
                    #print(direction)
                    self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'][s] = speed*self.cosd(direction)
                    self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'][s] = speed*self.sind(direction)
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'])
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'])

    
        #         %%%%%%%%%%%%%%%%%%To remove null pauses:
                        #will giove a logical vector which has 1 in the index that is 0
        #         v_index = s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(1:end-1) == 0;
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X(v_index) = [];
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y(v_index) = [];
    
                v_index = [i for i, x in enumerate(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION']) if x == 0]
                #print(v_index)
                #print("before replacing indicies")
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'])
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME']= self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X']= self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y']= self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION']=self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE']=self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING']=self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION']=self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X']=self.replaceIndiciesWithValue(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'], v_index)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y']=self.replaceIndiciesWithValue (self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'], v_index)
    
                #print("after replacing indicies")
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'])
        #         %%%%%%%%%%%%%%%%%%To remove the too small difference at the end, if
        #         %%%%%%%%%%%%%%%%%%there is one:
        #         if ((s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end) - s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end-1)) < 1e-14)
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X(end) = [];
        #             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y(end) = [];
        #         end
    
                #print(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'])
                if (len(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME']) >1  and (self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1] - self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-2]) < 1e-14):
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'].pop(-1)
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'].pop(-1) #[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'].pop(-1) #[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'].pop(-1) #[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'].pop(-1) #[-1]= []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'].pop(-1)#[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'].pop(-1)#[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'].pop(-1)#[-1] = []
                        self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'].pop(-1) #[-1] = []
    
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end) = s_input.SIMULATION_TIME;
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end) = 0;
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end) = 0;
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X(end) = 0;
        #         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y(end) = 0;
    
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'][-1] = self.s_input['SIMULATION_TIME']
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'][-1] = 0
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'][-1] = 0
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'][-1] = 0
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y'][-1] = 0
    
        #         s_mobility.VS_NODE(nodeIndex_tmp) = struct('V_TIME',s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME,...
        #                                               'V_POSITION_X',s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X,...
        #                                               'V_POSITION_Y',s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y,...
        #                                               'V_SPEED_X',s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_X,...
        #                                               'V_SPEED_Y',s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_Y);
    
    
            #print(nodeIndex_tmp)
            
                self.s_mobility['VS_NODE'].append({
                    'V_TIME':self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'],
                    'V_POSITION_X':self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'],
                    'V_POSITION_Y':self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'],
                    'V_SPEED_X':self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_X'],
                    'V_SPEED_Y':self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_Y']})
                #print('S_MOBILITY ******************************************************************************')
                #print(self.s_mobility)
    
            self.s_mobility_tmp.clear()
            #print("after clearing smoility tmp")
            #print(self.s_mobility_tmp)

    def expandArray(self, arr, value):
       # print('expand array')
        # length= len(arr)
        # extension= [0]*(length-1)
        # print(arr.shape)
        # print(extension.shape)
        # np.append(arr, [[value]+extension], axis=0)
        
        # print(value)
        # print(arr)
        if(len(arr)==0):
            arr.append([])
            arr[0]= value
            return arr
        
        r,c= len(arr), len(arr[0])
        #print(np.shape(arr))
        #print(c==0)
        
        if(c==0):
            c+=1
            
        #print(c)
        arr= np.resize(arr, (r+1, c))
        #print(np.shape(arr))

        arr[r]= 9
        #print(arr)

        return arr

    def fixNewLocBasedOnTimeScale(self, prevLoc, newLoc):
        
        dist= math.sqrt((newLoc[0]-prevLoc[0])**2 + (newLoc[1]-prevLoc[1])**2)
        if(dist > 0):
            newDist= self.timeStepsScale * dist
            ratio= newDist/dist
            newX= (1-ratio)*prevLoc[0] + ratio * newLoc[0]
            newY= (1-ratio)*prevLoc[1] + ratio * newLoc[1]
            return (newX, newY)
        
        return newLoc

    def replaceIndiciesWithValue(self, arr, indiciesList):
        
        newArray=[]
        for indx in range(len(arr)):
            if not indx in indiciesList: #if indx in indiciesList:
            #     newArray.append([])
            # else:
                newArray.append(arr[indx])
             
                
        # for i in indiciesList:
        #     print('arr[i]')
        #     print(arr2[i])
        #     print(np.shape(arr2[i]))
        #     arr2=np.delete(arr2[i],0)
        #     print(arr2)

       # print(newArray)
        return newArray
    
######################################################################################################################
######################################################################################################################
# function Out_setRestrictedWalk_random_waypoint(previousX,previousY,previousDuration,previousTime,s_input, init)
    def Out_setRestrictedWalk_random_waypoint(self, nodeIndex_tmp,previousX,previousY,previousDuration,previousTime, init):

        print('Out_setRestrictedWalk_random_waypoint ---- '+ str(init))
#     global s_mobility_tmp;
#     global nodeIndex_tmp;

#     x_tmp = previousX;
#     y_tmp = previousY;
#     time_tmp = previousTime + previousDuration;
#     duration_tmp = Out_adjustDuration_random_waypoint(time_tmp,unifrnd(s_input.V_WALK_INTERVAL(1),s_input.V_WALK_INTERVAL(2)),s_input);
#     direction_tmp = unifrnd(s_input.V_DIRECTION_INTERVAL(1),s_input.V_DIRECTION_INTERVAL(2));
#     if init == 1
#         speed = 0;
#     else
#         speed = unifrnd(s_input.V_SPEED_INTERVAL(1),s_input.V_SPEED_INTERVAL(2));
#     end
        x_tmp = previousX
        y_tmp = previousY
        time_tmp = previousTime + previousDuration #currTime
        ### Uniform Dist
        #randWalkVal= np.random.uniform(self.s_input['V_WALK_INTERVAL'][0],self.s_input['V_WALK_INTERVAL'][1])
        # Normal Dist
        mean= (self.s_input['V_WALK_INTERVAL'][0]+self.s_input['V_WALK_INTERVAL'][1])/2
        randWalkVal= random.gauss(mean, 0.25*mean)
        print('arwp call 2-- randomwalk duration')
        duration_tmp = self.Out_adjustDuration_random_waypoint(time_tmp, randWalkVal) #currDuration
        #print('V_WALK_INTERVAL')
        #print(self.s_input['V_WALK_INTERVAL'])
        ##### uniform Dist
        #direction_tmp = np.random.uniform(self.s_input['V_DIRECTION_INTERVAL'][0],self.s_input['V_DIRECTION_INTERVAL'][1])
        ##### Normal Dist
        mean= (self.s_input['V_DIRECTION_INTERVAL'][0]+self.s_input['V_DIRECTION_INTERVAL'][1])/2
        direction_tmp= random.gauss(mean, 0.25*mean)
        if init == 1:
            speed = 0
        else:
            #### Uniform Dist 
            #speed = np.random.uniform(self.s_input['V_SPEED_INTERVAL'][0],self.s_input['V_SPEED_INTERVAL'][1])
            #### normal Dist
            mean= (self.s_input['V_SPEED_INTERVAL'][0]+self.s_input['V_SPEED_INTERVAL'][1])/2
            speed = random.gauss(mean, 0.25*mean)
#     distance_tmp = speed*duration_tmp;
#     if (distance_tmp == 0)
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end+1,1) = time_tmp;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end+1,1) =  x_tmp;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end+1,1) =  y_tmp;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(end+1,1) = direction_tmp;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end+1,1) = speed;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(end+1,1) = true;
#         s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end+1,1) = duration_tmp;

        print('speed, duration_tmp'+ str(speed), str(duration_tmp))
        distance_tmp = speed*duration_tmp
        if (distance_tmp == 0):
           # print('dist==0')
            #print(nodeIndex_tmp)
            #print(self.s_mobility_tmp['VS_NODE'])
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'].append(time_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'], time_tmp)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'].append(x_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'], x_tmp)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'].append(y_tmp) #self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'], y_tmp)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'].append(direction_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'],direction_tmp)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'].append(speed) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'],speed)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'].append(True) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'], True)
            self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'].append(duration_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'], duration_tmp)

            print('data points: x,y,dur,time -------------')
            print(x_tmp, y_tmp, duration_tmp, time_tmp)
            #print(self.s_mobility_tmp['VS_NODE'])
#     else
#         %The loop begins:
#         flag_mobility_finished = false;
#         while (~flag_mobility_finished)
#             x_dest = x_tmp + distance_tmp*cosd(direction_tmp);
#             y_dest = y_tmp + distance_tmp*sind(direction_tmp);
#             flag_mobility_was_outside = false;
#             if (x_dest > s_input.V_POSITION_X_INTERVAL(2))
#                 flag_mobility_was_outside = true;
#                 new_direction = 180 - direction_tmp;
#                 x_dest = s_input.V_POSITION_X_INTERVAL(2);
#                 y_dest = y_tmp + diff([x_tmp x_dest])*tand(direction_tmp);  
#             end
#             if (x_dest < s_input.V_POSITION_X_INTERVAL(1))
#                 flag_mobility_was_outside = true;
#                 new_direction = 180 - direction_tmp;
#                 x_dest = s_input.V_POSITION_X_INTERVAL(1);
#                 y_dest = y_tmp + diff([x_tmp x_dest])*tand(direction_tmp);
#             end
#             if (y_dest > s_input.V_POSITION_Y_INTERVAL(2))
#                 flag_mobility_was_outside = true;
#                 new_direction = -direction_tmp;
#                 y_dest = s_input.V_POSITION_Y_INTERVAL(2);
#                 x_dest = x_tmp + diff([y_tmp y_dest])/tand(direction_tmp); 
#             end
#             if (y_dest < s_input.V_POSITION_Y_INTERVAL(1))
#                 flag_mobility_was_outside = true;
#                 new_direction = -direction_tmp;
#                 y_dest = s_input.V_POSITION_Y_INTERVAL(1);
#                 x_dest = x_tmp + diff([y_tmp y_dest])/tand(direction_tmp);
#             end
#             current_distance = abs(diff([x_tmp x_dest]) + 1i*diff([y_tmp y_dest]));
#             current_duration = Out_adjustDuration_random_waypoint(time_tmp,current_distance/speed,s_input);
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_TIME(end+1,1) = time_tmp;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_X(end+1,1) = x_tmp;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_POSITION_Y(end+1,1) = y_tmp;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DIRECTION(end+1,1) = direction_tmp;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_SPEED_MAGNITUDE(end+1,1) = speed;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_IS_MOVING(end+1,1) = true;
#             s_mobility_tmp.VS_NODE(nodeIndex_tmp).V_DURATION(end+1,1) = current_duration;
#             if(flag_mobility_was_outside)
#                 time_tmp = time_tmp + current_duration;
#                 duration_tmp = duration_tmp - current_duration;
#                 distance_tmp = distance_tmp - current_distance;
#                 x_tmp = x_dest;
#                 y_tmp = y_dest;
#                 direction_tmp = new_direction;
#             else
#                 flag_mobility_finished = true;
#             end
#         end
#         %the loop ended
#     end
# end

        else:
            #print('else')
            flag_mobility_finished = False
            
            prevLoc= (x_tmp, y_tmp)
            #debugMax=10
            #i=0
            while (not flag_mobility_finished):# and i<debugMax):
                
                newLoc= (x_tmp, y_tmp)
             #   i+=1
               # print('while debugging ---------------------- '+str(i) +'-----------------')
                x_dest = x_tmp + distance_tmp*self.cosd(direction_tmp)
                y_dest = y_tmp + distance_tmp*self.sind(direction_tmp)
                print('x_tmp'+str(x_tmp))
                print('y_tmp'+str(y_tmp))
                
                # print('direction_tmp'+ str(direction_tmp))
                # print('distance_tmp'+ str(distance_tmp))
                
                # print('self.cosd(direction_tmp) '+ str(self.cosd(direction_tmp)))
                # print('self.sind(direction_tmp)'+ str(self.sind(direction_tmp)))
                
                print('x_dest'+str(x_dest))
                print('y_dest'+ str(y_dest))
                
                flag_mobility_was_outside = False
                
                if (x_dest > self.s_input['V_POSITION_X_INTERVAL'][1]):
                    flag_mobility_was_outside = True
                    new_direction = 180 - direction_tmp
                    x_dest = self.s_input['V_POSITION_X_INTERVAL'][1]
                    y_dest = y_tmp + (x_dest-x_tmp)*self.tand(direction_tmp)  
                
                if (x_dest < self.s_input['V_POSITION_X_INTERVAL'][0]):
                    flag_mobility_was_outside = True
                    new_direction = 180 - direction_tmp
                    x_dest = self.s_input['V_POSITION_X_INTERVAL'][0]
                    y_dest = y_tmp + (x_dest-x_tmp)*self.tand(direction_tmp)
                
                if (y_dest > self.s_input['V_POSITION_Y_INTERVAL'][1]):
                    flag_mobility_was_outside = True
                    new_direction = -direction_tmp
                    y_dest = self.s_input['V_POSITION_Y_INTERVAL'][1]
                    x_dest = x_tmp + (y_dest-y_tmp)/self.tand(direction_tmp)
              
                if (y_dest < self.s_input['V_POSITION_Y_INTERVAL'][0]):
                    flag_mobility_was_outside = True
                    new_direction = -direction_tmp
                    y_dest = self.s_input['V_POSITION_Y_INTERVAL'][0]
                    x_dest = x_tmp + (y_dest-y_tmp)/self.tand(direction_tmp)
              
                current_distance = abs((x_dest-x_tmp) + 1j*(y_dest-y_tmp)) #????????????????????????
                print('arwp call 3 --- moving distance duration ')
                print(time_tmp)
                print(current_distance)
                print(speed)
                current_duration = self.Out_adjustDuration_random_waypoint(time_tmp, current_distance/speed)
                print('dur: '+str(current_duration))
                #print(self.s_mobility_tmp['VS_NODE'])

                #fixedLoc= self.fixNewLocBasedOnTimeScale(prevLoc, newLoc)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'].append(time_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_TIME'], time_tmp)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'].append(x_tmp) #x_tmp #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_X'], x_tmp)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'].append(y_tmp) #y_tmp #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_POSITION_Y'], y_tmp)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'].append(direction_tmp) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DIRECTION'],direction_tmp)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'].append(speed) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_SPEED_MAGNITUDE'],speed)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'].append(True) #= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_IS_MOVING'],True)
                self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'].append(current_duration)#= self.expandArray(self.s_mobility_tmp['VS_NODE'][nodeIndex_tmp]['V_DURATION'],current_duration)
                #print(self.s_mobility_tmp['VS_NODE'])
                
                print('data points: x,y,dur,time -------------')
                print(x_tmp, y_tmp, current_duration, time_tmp)
                
                prevLoc= (x_tmp, y_tmp)


                #print(flag_mobility_was_outside)
                if(flag_mobility_was_outside):
                     time_tmp = time_tmp + current_duration
                     duration_tmp = duration_tmp - current_duration
                     distance_tmp = distance_tmp - current_distance
                     x_tmp = x_dest
                     y_tmp = y_dest
                     direction_tmp = new_direction
                else:
                    flag_mobility_finished = True

           # if(i == debugMax):
            #    print("ISSUUUUUUUUUUUUUUUUUUUUUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

#######################################################################################################
#######################################################################################################
# function duration = Out_adjustDuration_random_waypoint(time,duration,s_input)

#     if ((time+duration) >= s_input.SIMULATION_TIME)
#         duration = s_input.SIMULATION_TIME - time;
#     end
# end
    def Out_adjustDuration_random_waypoint(self, time, duration):
        print('adjust rand waypoint')
        print('time '+str(time)+' duration: '+str(duration))
        if ((time+duration) >= self.s_input['SIMULATION_TIME']):
            duration = self.s_input['SIMULATION_TIME'] - time
        #print('duration'+str(duration))
        return duration
    

#     nbGroups = s_input.NB_GROUPS;

#######################################################################################################
#######################################################################################################
#https://stackoverflow.com/questions/31072815/cosd-and-sind-with-sympy
    def tand(self, x):
        return math.tan(x * math.pi / 180)
    
    def sind(self, x):
        return math.sin(x * math.pi / 180)
    
    def cosd(self, x):
        #print('cosd -- '+ str(x))
        return math.cos(x * math.pi / 180)