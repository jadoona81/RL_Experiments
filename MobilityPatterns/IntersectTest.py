# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:17:13 2021

@author: HG19230
"""
import math

def IntersectTest(xDim, yDim, Point_A, Point_B, LorC, direction, ListLine, ListCol):
    
    #PointA : currPoint
    #PointB : nextPoint in the direction (1) positive , (0) negative
    
# result = 10000;
# min = 10000;
# max = -10000;
# dim1 = 50;
# dim2 = 50;

    result= 100000 #10000
    minimum= 100000 #10000

    # if LorC  %on a line
    print("LorC"+ str(LorC))
    print("dircetion"+str(direction))
    
    if LorC==1: #################### on a line

        #if direct %positive
#         if Point_A(1) > Point_B(1) % by def Point_A(x) < Point_B(x)
#             intersection = -1;     % error
#             return;
#         end
#         for i = 1 : length(ListCol)
#             if (ListCol(i) - Point_A(1) < min) && (ListCol(i) > Point_A(1)) % look for intersection "after" Point_A(x) so ListCol(i) should be > Point_A(1)
#                 min = ListCol(i) - Point_A(1);
#                 result = ListCol(i); %X of next intersection
#             end
#         end
#         if result < Point_B(1) && result ~= 10000
#             intersection = [1, result, Point_A(2), 1];
#         else
#             if Point_B(1) > dim1
#                 Point_B(1) = dim1 - (Point_B(1) - dim1);
#                 Point_A(1) = dim1;
#                 for i = 1 : length(ListCol)
#                     if (Point_A(1) - ListCol(i) < min) && (Point_A(1) > ListCol(i))
#                         min = Point_A(1) - ListCol(i);
#                         result = ListCol(i); %X of next intersection
#                     end
#                 end
#                 if result > Point_B(1)
#                     intersection = [1, result, Point_A(2), 0];
#                 else
#                     intersection = [0, Point_B(1), Point_B(2), 0];    %no intersection
#                 end
#             else
#                 intersection = [0, Point_B(1), Point_B(2), 1];    %no intersection
#             end
#         end
        if direction==1: # positive
            if Point_A[0] > Point_B[0]: # by def Point_A(x) < Point_B(x)
                 #intersection = -1 #error
                 return -1
            
            for i in range(len(ListCol)): 
                if (ListCol[i] - Point_A[0] < minimum) and (ListCol[i] > Point_A[0]): #% look for intersection "after" Point_A(x) so ListCol(i) should be > Point_A(1)
                    min = ListCol[i] - Point_A[0]
                    result = ListCol[i]# %X of next intersection
            if result < Point_B[0] and not result==100000:
                intersection = [1, result, Point_A[1], 1]
                return intersection
            else:
                if Point_B[0] > xDim:
                    Point_B[0] = xDim - (Point_B[0] - xDim)
                    Point_A[0] = xDim
                    for i in range(len(ListCol)):
                        if (Point_A[0] - ListCol[i] < minimum) and (Point_A[0] > ListCol[i]):
                            minimum = Point_A[0] - ListCol[i]
                            result = ListCol[i]#X of next intersection

                    if result > Point_B[0]:
                         intersection = [1, result, Point_A[1], 0]
                         return intersection
                    else:
                         intersection = [0, Point_B[0], Point_B[1], 0]#no intersection
                         return intersection
                else:
                    intersection = [0, Point_B[0], Point_B[1], 1]#no intersection
                    return intersection

#     else %direct negative
#         if Point_B(1) > Point_A(1) % by def Point_A(x) > Point_B(x)
#             intersection = -1;     % error
#             return;
#         end
#         for i = 1 : length(ListCol)
#             if (Point_A(1) - ListCol(i) < min) && (Point_A(1) > ListCol(i))
#                 min = Point_A(1) - ListCol(i);
#                 result = ListCol(i); %X of next intersection
#             end
#         end
#         if result > Point_B(1) && result ~= 10000
#             intersection = [1, result, Point_A(2), 0];
#         else
#             if Point_B(1) < 0
#                 Point_B(1) = abs(Point_B(1));
#                 Point_A(1) = 0;
#                 for i = 1 : length(ListCol)
#                     if (ListCol(i) - Point_A(1) < min) && (Point_A(1) < ListCol(i))
#                         min = ListCol(i) - Point_A(1);
#                         result = ListCol(i); %X of next intersection
#                     end
#                 end
#                 if result < Point_B(1) && result ~= 10000
#                     intersection = [1, result, Point_A(2), 1];
#                 else
#                     intersection = [0, Point_B(1), Point_B(2), 1];    %no intersection
#                 end
#             else
#                 intersection = [0, Point_B(1), Point_B(2), 0];    %no intersection
#             end
#         end
#     end
        else: # negative
             print('suspicious case')
             print('Point B')
             print(Point_B)
             
             if Point_B[0] > Point_A[0]: # by def Point_A(x) > Point_B(x)
                 return -1
             for i in range(len(ListCol)):
                 if (Point_A[0] - ListCol[i] < minimum) and (Point_A[0] > ListCol[i]):
                     minimum = Point_A[0] - ListCol[i]
                     result = ListCol[i]#X of next intersection
            
             print('result: '+ str(result))
            
             if result > Point_B[0] and not result==100000:
                 print('subcase 1')
                 intersection = [1, result, Point_A[1], 0]
                 return intersection
             else:
                if Point_B[0] < 0:
                     Point_B[0] = abs(Point_B[0])
                     Point_A[0] = 0
                     for i in range(len(ListCol)):
                         if (ListCol[i] - Point_A[0] < minimum) and (Point_A[0] < ListCol[i]):
                             minimum = ListCol[i] - Point_A[0]
                             result = ListCol[i]#X of next intersection
                             
                     if result < Point_B[0] and not result == 10000:
                         intersection = [1, result, Point_A[1], 1]
                         print('subcase 2')
                         return intersection
                     else:
                         intersection = [0, Point_B[0], Point_B[1], 1]#no intersection
                         print('subcase 3')
                         return intersection
                else:
                    intersection = [0, Point_B[0], Point_B[1], 0]#no intersection
                    print('subcase 4')
                    return intersection


    else:#################### on a column
# else %on a column

#     if direct %positive
#         if Point_A(2) > Point_B(2) % by def Point_A(2) < Point_B(2)
#             intersection = -1;     % error
#             return;
#         end
#         for i = 1 : length(ListLine)
#             if (ListLine(i) - Point_A(2) < min) && (ListLine(i) > Point_A(2))
#                 min = ListLine(i) - Point_A(2);
#                 result = ListLine(i); %X of next intersection
#             end
#         end
#         if result < Point_B(2) && result ~= 10000
#             intersection = [1, Point_A(1), result, 1];
#         else
#             if Point_B(2) > dim2
#                 Point_B(2) = dim2 - (Point_B(2) - dim2);
#                 Point_A(2) = dim2;
#                 for i = 1 : length(ListLine)
#                     if (Point_A(2) - ListLine(i) < min) && (Point_A(2) > ListLine(i))
#                         min = Point_A(2) - ListLine(i);
#                         result = ListLine(i); %Y of next intersection
#                     end
#                 end
#                 if result > Point_B(2)
#                     intersection = [1, Point_A(1), result, 0];
#                 else
#                     intersection = [0, Point_B(1), Point_B(2), 0];    %no intersection
#                 end
#             else
#                 intersection = [0, Point_B(1), Point_B(2), 1];    %no intersection
#             end
#         end

        if direction==1:
            if Point_A[1] > Point_B[1]:#  by def Point_A(2) < Point_B(2):
                return -1
            for i in range(len(ListLine)):
                if (ListLine[i] - Point_A[1] < minimum) and (ListLine[i] > Point_A[1]):
                    minimum = ListLine[i] - Point_A[1]
                    result = ListLine[i]#X of next intersection
            if result < Point_B[1] and not result == 10000:
                intersection = [1, Point_A[0], result, 1]
                return intersection
            else:
                if Point_B[1] > yDim:
                    Point_B[1] = yDim - (Point_B[1] - yDim)
                    Point_A[1] = yDim
                    for i in range(len(ListLine)):
                        if (Point_A[1] - ListLine[i] < minimum) and (Point_A[1] > ListLine[i]):
                             minimum = Point_A[1] - ListLine[i]
                             result = ListLine[i]#Y of next intersection
                    if result > Point_B[1]:
                        intersection = [1, Point_A[0], result, 0]
                        return intersection

                    else:
                        intersection = [0, Point_B[0], Point_B[1], 0]#no intersection
                        return intersection

                else:
                    intersection = [0, Point_B[0], Point_B[1], 1]#no intersection
                    return intersection

                    
#     else %direct negative
#         if Point_B(2) > Point_A(2) % by def Point_A(y) > Point_B(y)
#             intersection = -1;     % error
#             return;
#         end
#         for i = 1 : length(ListLine)
#             if (Point_A(2) - ListLine(i) < min) && (Point_A(2) > ListLine(i))
#                 min = Point_A(2) - ListLine(i);
#                 result = ListLine(i); %Y of next intersection
#             end
#         end
#         if result > Point_B(2) && result ~= 10000
#             intersection = [1, Point_A(1), result, 0];
#         else
#             if Point_B(2) < 0
#                 Point_B(2) = abs(Point_B(2));
#                 Point_A(2) = 0;
#                 for i = 1 : length(ListLine)
#                     if (ListLine(i) - Point_A(2) < min) && (Point_A(2) < ListLine(i))
#                         min = ListLine(i) - Point_A(2);
#                         result = ListLine(i); %X of next intersection
#                     end
#                 end
#                 if result < Point_B(2) && result ~= 10000
#                     intersection = [1, Point_A(1), result, 1];
#                 else
#                     intersection = [0, Point_B(1), Point_B(2), 1];    %no intersection
#                 end
#             else
#                 intersection = [0, Point_B(1), Point_B(2), 0];    %no intersection
#             end
#         end
#     end
# end

        else: #direction negative
            if Point_B[1] > Point_A[1]: # by def Point_A(y) > Point_B(y)
                return -1
            
            for i in range(len(ListLine)):
                if (Point_A[1] - ListLine[i] < minimum) and (Point_A[1] > ListLine[i]):
                     minimum = Point_A[1] - ListLine[i]
                     result = ListLine[i]#Y of next intersection
            if result > Point_B[1] and not result == 10000:
                 intersection = [1, Point_A[0], result, 0]
                 return intersection

            else:
                if Point_B[1] < 0:
                     Point_B[1] = abs(Point_B[1])
                     Point_A[1] = 0
                     for i in range(len(ListLine)):
                         if (ListLine[i] - Point_A[1] < minimum) and (Point_A[1] < ListLine[i]):
                             minimum = ListLine[i] - Point_A[1]
                             result = ListLine[i]#X of next intersection
                     if result < Point_B[1] and not result == 10000:
                         intersection = [1, Point_A[0], result, 1]
                         return intersection

                     else:
                         intersection = [0, Point_B[0], Point_B[1], 1]#no intersection
                         return intersection

                else:
                     intersection = [0, Point_B[0], Point_B[1], 0]#no intersection
                     return intersection


        print("testing intersection"+ str(intersection))
        return intersection