# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:12:09 2021 

@author: HG19230
"""

import random
import math
from MobilityPatterns.IntersectTest import IntersectTest #MobilityPatterns.

class ManhattanMobileTarget:
    
    def __init__(self, xDim, yDim, street_width, block_width, min_speed, max_speed, randomLoc, timeStepScale):
        
        self.xDim= xDim
        self.yDim= yDim
        
        self.line_manhattan =0
        self.column_manhattan =0
        self.speed= 0
        self.direction=0
        self.block_width= block_width
        self.street_width= street_width
        
        self.timeStepScale= timeStepScale # 1 timeStep equal how many seconds
        
        self.line_count = math.ceil(yDim / block_width) #number of lines (#rows)
        self.line_manhattan = random.randrange(1, self.line_count) #random integer between 1 and line_count.
        self.column_count = math.ceil(xDim / block_width) #number of lines (#columns)
        self.column_manhattan = random.randrange(1, self.column_count) #random integer between 1 and column_count.

        #initialize location
        #if(randomLoc):
            
        self.createRandomLocation()

        minScaledSpeed= min_speed * self.timeStepScale
        maxScaledSpeed= max_speed * self.timeStepScale

        k= random.random() #1x1 matrix of random number
        self.speed = (maxScaledSpeed-minScaledSpeed)*k + minScaledSpeed#;gudxb
        if (k < 0.5):
            self.direction = 1
        
        
        if not self.line_manhattan == 0:
            self.LorC = 1
        else:
            self.LorC = 0

        # for i = 1 : column_count
        #     ListCol(i) = (i-1)* block_width + 1;
        # end
        
        self.ListCol= [0]*self.column_count
        for i in range(self.column_count):
            self.ListCol[i]= (i)* block_width+1

        # for i = 1 : column_countfhghv
        #     ListLine(i) = (i-1)* block_width + 1;
        # endfkdhs
        self.ListLine= [0]*self.line_count
        for i in range(self.column_count):
            self.ListLine[i]= (i)* block_width + 1
            

    def setTargetLoc(self, values):
        self.X= float(values[1])
        self.Y= float(values[2])
        self.direction= float(values[3])
        self.line_manhattan= float(values[4])
        self.column_manhattan= float(values[5])
        self.speed= float(values[6])
        
    def createRandomLocation(self):
        self.X=-1
        self.Y=-1
        
        while self.X < 0 or self.X > self.xDim or self.Y <0 or self.Y > self.yDim:

            k= random.random()
            
            if(k < 0.5):
                rand = random.random()
                self.X= rand * self.xDim
                self.Y = (self.line_manhattan)* self.block_width + 1
                delta = self.street_width*rand - (self.street_width/2)
                self.Y = self.Y + delta
            else:
                self.X = (self.column_manhattan)* self.block_width + 1
                rand= random.random()
                delta = self.street_width*rand - (self.street_width/2)
                self.X = self.X + delta
                rand = random.random()
                self.Y = rand * self.yDim
            
            print('created X and Y==========='+ str(self.X)+", "+ str(self.Y))

    def move(self): #one time step move
        

        # Point_A(1) = X(index_target, index_time - 1);
        # Point_A(2) = Y(index_target, index_time - 1);
        # if direct == 0
        #     speedo = - speed(index_target);
        # elsegi9togp
        #     speedo = speed(index_target);
        # end
        # if(LorC)    % line
        #     Point_B(1) = Point_A(1) + speedo;
        #     Point_B(2) = Point_A(2);
        # else
        #     Point_B(1) = Point_A(1);
        #     Point_B(2) = Point_A(2) + speedo;
        # end
        # Point_A;
        # Point_B;
        # LorC;
        # direct;
        
        Point_A=[self.X, self.Y]
        
        if self.direction ==0:
            speedo= -(self.speed)
        else:
            speedo= self.speed
        
        if(self.LorC ==1): #line
            Point_B=[Point_A[0]+speedo, Point_A[1]]
        else:
            Point_B=[Point_A[0], Point_A[1]+speedo]
        
        print('Intersect Test call 1')
        result = IntersectTest(self.xDim, self.yDim, Point_A, Point_B, self.LorC, self.direction, self.ListLine, self.ListCol)
        print(result)
        # next_point(1) = result(2);
        # next_point(2) = result(3);
        next_point=[0]*2
        next_point[0]= result[1]
        next_point[1]= result[2]
        
        # Point_C(1) = result(2);
        # Point_C(2) = result(3);
        Point_C=[0]*2
        Point_C[0]= result[1]
        Point_C[1]= result[2]
        
        # direct = result(4);
        self.direction= result[3]
        
        
        # while(result(1) > 0)
        while result[0] > 0:
        #     random = rand;
            rand= random.random()
            print('rand:'+str(rand))
            
        #     if random > 0.66    %keep the same direction and the same LorC
        #         random1 = random;
        #         %result = IntersectTest(Point_C, Point_B, LorC, result(4), ListLine, ListCol);
        #         %Point_C = [result(2), result(3)];
            if(rand > 0.33): #0.88
                print('move condition 1 --- same direction - same axis --------------------------')
                rand1= rand
            else:
                print('move condition 2')
        #     else
        #         if random < 0.33  %turn and keep the same direction
        #             random2 = random;
        #             if LorC == 1                % on a line
        #                 if direct == 1         % positive direction so turn left
        #                     Point_B(2) = Point_C(2) + (Point_B(1) - Point_C(1));    % C(1) always < B(1) because direct = 1
        #                     Point_B(1) = Point_C(1);  % new B has the same x than C
        #                 else                    % negative direction so turn left
        #                     Point_B(2) = Point_C(2) - (Point_C(1) - Point_B(1));    % B(1) always < C(1) because direct = 0
        #                     Point_B(1) = Point_C(1);
        #                 end
        #                 %result = IntersectTest(Point_C, Point_B, LorC, result(4), ListLine, ListCol);
        #             else        % on a column
        #                 if direct == 1     % positive direction so turn right
        #                     Point_B(1) = Point_C(1) + (Point_B(2) - Point_C(2));   % C(2) always < B(2) because direct = 1
        #                     Point_B(2) = Point_C(2);
        #                 else
        #                     Point_B(1) = Point_C(1) - (Point_C(2) - Point_C(2));    % B(2) always < C(2) because direct = 0
        #                     Point_B(2) = Point_C(2);
        #                 end
        #             end
        #             LorC = abs(LorC - 1);   % turn
                if rand < 0.22: # 0.33 turn and keep same direction (0- 0.22)
                    print(' turn and keep same direction -----------------------------------')
                    print('point B')
                    print(Point_B)
                    
                    print('point C')
                    print(Point_C)
                    
                    rand2= rand
                    if self.LorC ==1: #on a line
                        print('LorC 1')
                        if self.direction ==1: # positive direction so turn left
                            print('direction 1')
                            Point_B[1] = Point_C[1] + (Point_B[0] - Point_C[0])
                            Point_B[0] = Point_C[0]
                        else:
                            print('direction 0')
                            print('Point_C[0] - Point_B[0]')
                            print(Point_C[0] - Point_B[0])
                            
                            Point_B[1] = Point_C[1] - (Point_C[0] - Point_B[0])
                            Point_B[0] = Point_C[0]

                            print('point B after editing')
                            print(Point_B)
                            
                    else: # on a column 
                        print('LorC 0')

                        if self.direction ==1: #positive direction so turn right
                            print('direction 1')
                            Point_B[0] = Point_C[0] + (Point_B[1] - Point_C[1])
                            Point_B[1] = Point_C[1]
                        else:
                            print('direction 0')
                            Point_B[0] = Point_C[0] - (Point_C[1] - Point_B[1]) ##### # MODIFIED
                            Point_B[1] = Point_C[1]
                    self.LorC= abs(self.LorC-1) #turn
                        
        #         else     %turn and change direction
        #             random3 = random;
        #             if LorC == 1    %on a line
        #                 if direct == 1 %positive direction turn right
        #                     Point_B(2) = Point_C(2) - (Point_B(1) - Point_C(1));   % C(1) always < B(1) because direct = 1
        #                     Point_B(1) = Point_C(1);
        #                 else
        #                     Point_B(2) = Point_C(2) + (Point_C(1) - Point_B(1));    % B(1) always < C(1) because direct = 0
        #                     Point_B(1) = Point_C(1);
        #                 end
        #             else    % on a column
        #                 if direct == 1 % positive direction turn left
        #                     Point_B(1) = Point_C(1) - (Point_B(2) - Point_C(2));   % C(2) always < B(2) because direct = 1
        #                     Point_B(2) = Point_C(2);
        #                 else
        #                     Point_B(2) = Point_C(1) + (Point_C(2) - Point_B(2));   % B(2) always < C(2) because direct = 0
        #                     Point_B(2) = Point_C(2);
        #                 end
        #             end
        #             direct = abs(direct - 1);  % change direction
        #             LorC = abs(LorC - 1);   % turn
        #         end
        #     end
                else: # turn and change direction (0.22-0.33)
                    print('turn and change direction -----------------------------------------------')
                    rand3= rand
                    if(self.LorC==1): #on a line
                        if self.direction ==1: #positive direction turn right
                            Point_B[1] = Point_C[1] - (Point_B[0] - Point_C[0])
                            Point_B[0] = Point_C[0]
                        else:
                            Point_B[1] = Point_C[1] + (Point_C[0] - Point_B[0])
                            Point_B[0] = Point_C[0]
                    else: # on a column
                        if self.direction ==1: #positive direction turn left
                            Point_B[0] = Point_C[0] - (Point_B[1] - Point_C[1])
                            Point_B[1] = Point_C[1]
                        else:
                            Point_B[1] = Point_C[0] + (Point_C[1] - Point_B[1])
                            Point_B[1] = Point_C[1]
                        
                    self.direction= abs(self.direction -1)
                    self.LorC= abs(self.LorC -1)
                
        #     Point_C;
        #     Point_B;
        #     LorC;
        
        #     if Point_C(1)> Point_B(1) || Point_C(2)> Point_B(2)
        #         direct = 0;
        #     else
        #         direct = 1;
        #     end
            if Point_C[0] > Point_B[0] or Point_C[1] > Point_B[1]:
                self.direction=0
            else:
                self.direction=1
        
        #     result;
        
        #     result = IntersectTest(Point_C, Point_B, LorC, direct, ListLine, ListCol);
            print('Intersect Test call 2')

            result= IntersectTest(self.xDim, self.yDim, Point_C, Point_B, self.LorC, self.direction, self.ListLine, self.ListCol)
            print('result[0]: '+ str(result[0]))
        #     next_point(1) = result(2);
        #     next_point(2) = result(3);
        #     direct = result(4);
            next_point=[0]*2
            next_point[0]= result[1]
            next_point[1]= result[2]
            self.direction= result[3]
            
            print('before synthesizing')
            print(next_point[0])
            print(next_point[1])
            
        ############# END WHILE result[0] 
        self.X= next_point[0]
        self.Y= next_point[1]
        

        # deltaX= self.X-Point_A[0]
        # deltaY= self.Y-Point_A[1]
        
        # if(deltaY < 0): 
        #     self.Y += (1-self.timeStepScale) * abs(deltaY) 
        # elif(deltaY > 0):
        #     self.Y -= (1-self.timeStepScale) * deltaY 
        # elif(deltaX < 0): 
        #     self.X+= (1-self.timeStepScale) * abs(deltaX)
        # else: 
        #    self.X-= (1-self.timeStepScale) * deltaX
            

        # if(self.Y < 0 or self.X < 0):
        #      print(' POINT Y  <  0 '+str(self.Y)+'-------------OR PointX < 0'+str(self.X)+'----------------------------------------------')
        #      return
        
        print("moved target  >>>>>>>>>>>>> ")
        print(str(self.X)+','+ str(self.Y))
        print(self.direction)
        print(self.LorC)
        print(">>>>>>>>>>>> >>>>>>>>>>>>> ")

        # end
        # X(index_target, index_time) = next_point(1);
        # Y(index_target, index_time) = next_point(2);
        # Z(index_target, index_time) = 0;
        
        