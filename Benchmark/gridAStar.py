# -*- coding: utf-8 -*-
#https://stackoverflow.com/questions/59509383/how-could-i-add-more-than-start-point-and-goal-point-in-a-star-algorithm

from __future__ import print_function

class AStarGridPathPlanning:


    def  __init__(self, numCellsPerSide, cellSideSize):
        
            
        # grid = [[0, 1, 0, 0, 0, 0],
        #         [0, 1, 0, 0, 0, 0],#0 are free path whereas 1's are obstacles
        #         [0, 1, 0, 0, 0, 0],
        #         [0, 1, 0, 0, 1, 0],
        #         [0, 0, 0, 0, 1, 0]]
        
        # self.grid = [[0, 0, 0, 0],
        #         [0, 0, 0, 0],#0 are free path whereas 1's are obstacles
        #         [0, 0, 0, 0],
        #         [0, 0, 0, 0]]
        
        self.cellSideSize= cellSideSize
        
        rows, cols = (numCellsPerSide, numCellsPerSide) 
        self.grid= [[0]*cols]*rows 


        # init = [0, 0]
        # goal = [len(grid)-1, len(grid[0])-1] #all coordinates are given in format [y,x] 
        self.cost = 1
        
        
        #the actions we can take
        self.delta = [[-1, 0 ], # go up
                 [ 0, -1], # go left
                 [ 1, 0 ], # go down
                 [ 0, 1 ], # go right
                 [-1, 1],#upR
                 [-1, -1], #upL
                 [1, 1], #downR
                 [1, -1] #downL
                 ] 
    
    
    #function to search the path
    def search(self, init,goal):
    
        
            #the cost map which pushes the path closer to the goal
        heuristic = [[0 for row in range(len(self.grid[0]))] for col in range(len(self.grid))]
        for i in range(len(self.grid)):    
            for j in range(len(self.grid[0])):            
                heuristic[i][j] = abs(i - goal[0]) + abs(j - goal[1])
                
                
        closed = [[0 for col in range(len(self.grid[0]))] for row in range(len(self.grid))]# the referrence grid
        closed[init[0]][init[1]] = 1
        action = [[0 for col in range(len(self.grid[0]))] for row in range(len(self.grid))]#the action grid
    
        x = init[0]
        y = init[1]
        g = 0
    
        f = g + heuristic[init[0]][init[0]]
        cell = [[f, g, x, y]]
    
        found = False  # flag that is set when search is complete
        resign = False # flag set if we can't find expand
    
        while not found and not resign:
            if len(cell) == 0:
                resign = True
                return "FAIL"
            else:
                cell.sort()#to choose the least costliest action so as to move closer to the goal
                cell.reverse()
                next = cell.pop()
                x = next[2]
                y = next[3]
                g = next[1]
                f = next[0]
    
    
                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    for i in range(len(self.delta)):#to try out different valid actions
                        x2 = x + self.delta[i][0]
                        y2 = y + self.delta[i][1]
                        if x2 >= 0 and x2 < len(self.grid) and y2 >=0 and y2 < len(self.grid[0]):
                            if closed[x2][y2] == 0 and self.grid[x2][y2] == 0:
                                g2 = g + self.cost
                                f2 = g2 + heuristic[x2][y2]
                                cell.append([f2, g2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = i
        invpath = []
        x = goal[0]
        y = goal[1]
        invpath.append([x, y])#we get the reverse path from here
        while x != init[0] or y != init[1]:
            x2 = x - self.delta[action[x][y]][0]
            y2 = y - self.delta[action[x][y]][1]
            x = x2
            y = y2
            invpath.append([x, y])
    
        path = []
        pathScaled= []
        for i in range(len(invpath)):
            e= invpath[len(invpath) - 1 - i]
           # print(e[0])
            path.append(e)
            pathScaled.append((e[0]*self.cellSideSize, e[1]*self.cellSideSize))
        # print("ACTION MAP")
        # for i in range(len(action)):
        #     print(action[i])
    
        return pathScaled
    
    # a = search(grid,init,goal,cost,heuristic)
    # for i in range(len(a)):
    #     print(a[i]) 