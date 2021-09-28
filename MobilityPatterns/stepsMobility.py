# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 09:46:21 2021

# @author: HG19230
# """

from MobilityPatterns.mobilityGroup import mobilityGroup

class StepsMobility:


# function Location = GenerateStepsMobility(grid_size, zone_size, min_speed, max_speed, TargetNum, MaxTime, animation)
# % an example of simulation with STEPS mobility model
# % author: Anh-Dung Nguyen 
# % email: anh-dung.nguyen@isae.fr

# simu.duration = MaxTime; % number of time steps
# simu.number_of_nodes = uint64([TargetNum/2 TargetNum/2]);
# simu.alpha = [0 100];
# simu.grid_size = grid_size; 
# simu.zone_size = zone_size;
# simu.time_step = 2.00; % seconds
# simu.rwp_speed = [min_speed max_speed];
# simu.rwp_pause_time = [0 1];
# simu.zone_speed = [3 10] / 3.6;
# simu.zone_time = [20 30];
# simu.radio_range = 1;

# disp('--------------STARTING SIMULATIONS------------------')
# X = zeros(TargetNum, simu.duration);
# Y = zeros(TargetNum, simu.duration);
# Z = zeros(TargetNum, simu.duration);


    def __init__(self,  xDim, yDim, numGroups, numTargets, maxTime):

        self.duration = maxTime
        self.number_of_nodes = [numTargets/2, numTargets/2]
        self.alpha = [0, 100]
        self.grid_size = xDim
        self.zone_size = 4
        self.time_step = 2.00#seconds
        self.rwp_speed = [3/3.6, 5/3.6] #################
        self.rwp_pause_time = [0, 1]
        self.zone_speed = [3/3.6, 10/3.6]
        self.zone_time = [20, 30]
        self.radio_range = 1
        
    
# % creation of nodes
# nodes = Group(simu.alpha,simu.number_of_nodes,simu.grid_size,simu.rwp_speed,simu.rwp_pause_time,simu.zone_speed,simu.zone_time,simu.zone_size,simu.time_step,simu.radio_range);

    def generateMobility(self):
        self.nodes = mobilityGroup(self.alpha,self.number_of_nodes,self.grid_size,self.rwp_speed,self.rwp_pause_time,self.zone_speed,self.zone_time,self.zone_size,self.time_step,self.radio_range);


# for ii = 1:simu.duration
#     % movement of nodes
#     nodes.move;
#     X(:, ii) = nodes.coords(:,1);
#     Y(:, ii) = nodes.coords(:,2);
#     Z(:, ii) = 0;
    
    def moveTargets(self):

        for i in range(self.duration):
            self.nodes.move()
            self.nodesXLoc[:][i] = self.nodes.coords[:][0]
            self.nodesYLoc[:][i] = self.nodes.coords[:][0]
