# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 08:58:50 2021

@author: HG19230
"""
from MobilityPatterns.GenerateMobilityGroupRandom import Generate_Mobility_group_random #MobilityPatterns.
import random
import scipy
import math
from scipy import interpolate

class RPGM_Mobility:

    
    ################### One Target Class #########################
    class RPGM_MobileTarget(object):
        
        def __init__(self, tID, xDim, yDim, numGroups, radiusGroup, min_speed, max_speed):
            self.ID=tID

            self.X=[]
            self.Y= []
            
            
    ####################### RPGM Mobility ########################
    def __init__(self,  xDim, yDim, numGroups, numNodes, maxTime, timeStepsScale):

        self.xDim= xDim
        self.yDim= yDim
        self.timeStepsScale= timeStepsScale
        
        xDim_min = 0
        xDim_max = xDim
        yDim_min = 0
        yDim_max = yDim
        
        self.numSimSteps= maxTime
        self.radiusGroup= 3
        self.numNodes= numNodes
        self.numGroups= numGroups
        
        rows, cols = (numGroups, self.numSimSteps) 
        
        self.LocationX_Group={}
        self.LocationY_Group={}
        self.NodeGroups= [random.randint(0, self.numGroups-1) for iter in range(self.numNodes)]

        #print(self.targetGroups)

        #scaled SPEED WALK Interval and Pause Interval ######################################################################
        
        minSpeedScaled= (3/3.6) #* timeStepsScale
        maxSpeedScaled= (5/3.6) #* timeStepsScale
                
        self.s_input = {'V_POSITION_X_INTERVAL': [xDim_min, xDim_max], 
                   'V_POSITION_Y_INTERVAL':[yDim_min, yDim_max],
                   'V_SPEED_INTERVAL':[minSpeedScaled, maxSpeedScaled], #[4/3.6, 5/3.6],#[3/3.6, 5/3.6], ####################
                   'V_PAUSE_INTERVAL':[0, 1*timeStepsScale], #[0.5, 1], #[0, 1], #(s)
                   'V_WALK_INTERVAL':[2.00*timeStepsScale, 6.00*timeStepsScale], #[4.0, 6.0],#[2.00, 6.00], #(s)
                   'V_DIRECTION_INTERVAL':[-180, 180], #[-90, 90], #[-180, 180],
                   'SIMULATION_TIME': self.numSimSteps * timeStepsScale, #(s)
                   'NB_NODES':self.numGroups, ################# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ TEST ^^^^^^^^^^^^^^^^^^^
                   'seed':200,
                   'RADIUS':self.radiusGroup, ###########################################
                   'NB_GROUPS':self.numGroups}
        
        self.gmgr=  Generate_Mobility_group_random(self.s_input, self.NodeGroups, timeStepsScale)
        
        self.GroupsInitLocX= self.gmgr.groupsXLocDict
        self.GroupsInitLocY= self.gmgr.groupsYLocDict
        # self.s_mobility= gmgr.s_mobility

        # # v_t = 1 : MaxTime;
        # # for groupIndex = 1 : numGroups
        # #     disp(groupIndex)
        # #     vs_node(groupIndex).v_x = interp1(s_mobility.VS_NODE(groupIndex).V_TIME,s_mobility.VS_NODE(groupIndex).V_POSITION_X,v_t);
        # #     vs_node(groupIndex).v_y = interp1(s_mobility.VS_NODE(groupIndex).V_TIME,s_mobility.VS_NODE(groupIndex).V_POSITION_Y,v_t);
        # #     for time_index = 1 : MaxTime
        # #         disp(time_index ...
        # #             )
        # #         LocationX_Group(groupIndex, time_index) = vs_node(groupIndex).v_x(time_index);
        # #         LocationY_Group(groupIndex, time_index) = vs_node(groupIndex).v_y(time_index);
        # #         LocationZ_Group(groupIndex, time_index) = 0;
        # #     end
        # # end
        
        # vs_node=[{} for _ in range(self.numGroups)]
        # v_t i= self.numSimSteps
        # for gi in range(self.numGroups):
        #         vs_node[gi]['v_x']= []
        #         vs_node[gi]['v_y']= []
        #         #set v_x and v_y
        #         for t in range(self.numSimSteps):
        #             self.LocationX_Group[gi][t]= vs_node[gi]['v_x'][t]
        #             self.LocationY_Group[gi][t]= vs_node[gi]['v_y'][t]
                    #self.LocationZ_Group[gi][t]=0
        

    def setGroupsAndLocs(self, nodeGroups, groupsXLoc, groupsYLoc):
        self.NodeGroups= nodeGroups
        self.gmgr.targetGroups= nodeGroups
        self.GroupsInitLocX=groupsXLoc
        self.GroupsInitLocY= groupsYLoc
        self.gmgr.groupsXLocDict = self.GroupsInitLocX
        self.gmgr.groupsYLocDict = self.GroupsInitLocY
        
        print('set groups and locations ')
        print(self.NodeGroups)
        print( self.gmgr.groupsXLocDict)
        print(self.gmgr.groupsYLocDict)
        
    def generateMobility(self):
        print('generating mobility' + str(self.numSimSteps))
        self.gmgr.generateMobility()
        self.s_mobility= self.gmgr.s_mobility
        
        v_t= list(range(self.numSimSteps))
        #print(self.s_mobility)
        vs_node= [0]*self.numGroups
        
        print('RPGM.NodeGroups')
        print(self.NodeGroups)
        
        print('gmgr.groupsXLocDict')
        print( self.gmgr.groupsXLocDict)
        
        print('gmgr.groupsYLocDict')
        print(self.gmgr.groupsYLocDict)
        
        for groupIndex in range(0, self.numGroups):
            vs_node[groupIndex]={}
            self.LocationX_Group[groupIndex]=[0]* self.numSimSteps
            self.LocationY_Group[groupIndex]=[0]* self.numSimSteps
        
            print('vsNode_groupIndx _'+str(groupIndex))
            print('RPGM.LocationX_Group')
            print(self.LocationX_Group[groupIndex][0])
            print('RPGM.LocationY_Group')
            print(self.LocationY_Group[groupIndex][0])
                    
            #print(self.s_mobility)
           # print(self.s_mobility['VS_NODE'][groupIndex]['V_POSITION_Y'])
            
            #for t in range(self.numSimSteps):
            print('V_TIME')
            print(self.s_mobility['VS_NODE'][groupIndex]['V_TIME'])
            print('V_POSITION_X')
            print( self.s_mobility['VS_NODE'][groupIndex]['V_POSITION_X'])
            print('V_POSITION_Y')
            print( self.s_mobility['VS_NODE'][groupIndex]['V_POSITION_Y'])

            vs_node[groupIndex]['v_x']= interpolate.interp1d(self.s_mobility['VS_NODE'][groupIndex]['V_TIME'], self.s_mobility['VS_NODE'][groupIndex]['V_POSITION_X'])
            # print('v_x function')
            # print(vs_node[groupIndex]['v_x'])
            vs_node[groupIndex]['v_y']= interpolate.interp1d(self.s_mobility['VS_NODE'][groupIndex]['V_TIME'], self.s_mobility['VS_NODE'][groupIndex]['V_POSITION_Y'])

            for time_index in range(0, self.numSimSteps):
                self.LocationX_Group[groupIndex][time_index] = vs_node[groupIndex]['v_x'](time_index*self.timeStepsScale)
                self.LocationY_Group[groupIndex][time_index] = vs_node[groupIndex]['v_y'](time_index*self.timeStepsScale)
                
               # if(time_index==0 and groupIndex==3):
                print('gIndx: '+ str(groupIndex) +' .. time_index: '+ str(time_index) +' val '+str(time_index*self.timeStepsScale))
                print('RPGM.LocationX_Group')
                print(self.LocationX_Group[groupIndex][time_index])
                print('RPGM.LocationY_Group')
                print(self.LocationY_Group[groupIndex][time_index])

            print('Group X - Y')
            print(self.LocationX_Group[groupIndex])
            print(self.LocationY_Group[groupIndex])
            
            
    def moveNode(self, node, time):
        locX=-1
        locY=-1
        while (locX > self.xDim or locX < 0 or locY > self.yDim or locY < 0):
                    #i+=1
            omega = random.random() * math.pi
            radius= random.random() * self.radiusGroup
            deltaX = math.sqrt(radius) * math.cos(omega)
            deltaY = math.sqrt(radius) * math.sin(omega)
            j = self.NodeGroups[node]
            
            print(j)
            print(time)
            print(len( self.LocationX_Group))

            locX = self.LocationX_Group[j][time] + deltaX
            locY = self.LocationY_Group[j][time] + deltaY
            
            print(self.LocationX_Group[j][time])
            print(locX)
            
            print( self.LocationY_Group[j][time])
            print(locY)
        # if(node ==1 and time==0):
        #     print('moving node .....'+ str(node)+'...'+ str(self.NodeGroups[node]) +" ..... "+ str(time))

        #     j= self.NodeGroups[node]
        #     print(j)
        #     print('RPGM.LocationX_Group' + str(self.LocationX_Group[j][time]))
        #     print('RPGM.LocationY_Group' + str(self.LocationY_Group[j][time]))

        #     print((locX, locY))
        
        return (locX, locY)
    
    def GenerateNodesLocAtGivenTimeStep(self, time):

        NodesLocs={}
        for node in range(self.numNodes):
            loc= self.moveNode(node, time)
            NodesLocs[node]=loc

        return NodesLocs


    def moveNodes(self):
# for target = 1 : TargetNum
#     disp('moving targets')
#     for t = 1 : MaxTime
#         X(target, t) = -1;
#         Y(target, t) = -1;
#         while (X(target, t) > dim1 || X(target, t) < 0 || Y(target, t) > dim2 || Y(target, t) < 0)
#             omega = rand * pi;
#             radius = rand * radiusGroup;
#             deltaX = sqrt(radius) * cos(omega);
#             deltaY = sqrt(radius) * sin(omega);
#             j = group(target);
#             X(target, t) = LocationX_Group(j, t) + deltaX;
#             Y(target, t) = LocationY_Group(j, t) + deltaY;
#         end
#             disp(X);
#             disp(Y);
            
        print('moving Nodes')
        self.X = [[-1]*self.numSimSteps]*self.numNodes
        self.Y = [[-1]*self.numSimSteps]*self.numNodes
        
        for node in range(self.numNodes):
            for t in range(self.numSimSteps):
                # self.X[target][t]=-1
                # self.Y[target][t]=-1
                #debugMax=10
                #i=0
                while (self.X[node][t] > self.xDim or self.X[node][t] < 0 or self.Y[node][t] > self.yDim or self.Y[node][t] < 0):
                    #i+=1
                    omega = random.random() * math.pi
                    radius= random.random() * self.radiusGroup
                    deltaX = math.sqrt(radius) * math.cos(omega)
                    deltaY = math.sqrt(radius) * math.sin(omega)
                    #print('deltaY' + str(deltaY))
                    j = self.NodeGroups[node]
                    print('self.LocationY_Group[j][t]'+ str(self.LocationY_Group[j][t]))

                    self.X[node][t] = self.LocationX_Group[j][t] + deltaX
                    self.Y[node][t] = self.LocationY_Group[j][t] + deltaY
                    #print('self.X[target][t]: '+str(self.X[target][t]))
                    #print('self.Y[target][t]: '+ str(self.Y[target][t]))
                    
                #if(i == debugMax):
                 #   print("ISSUUUUUUUUUUUUUUUUUUUUUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
#     end
# end
        