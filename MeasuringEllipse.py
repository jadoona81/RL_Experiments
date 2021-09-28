# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 10:23:09 2021

@author: HG19230
"""
import math 
import numpy as np

def CalculateEllipse(AOV, altitude, cameraAngle):
        
        halfAOV= AOV/2.0
        AO= altitude * math.tan(math.radians(cameraAngle) - math.radians(halfAOV))
     #   print("AO: "+ str(AO))
        DO= altitude * math.tan(math.radians(cameraAngle) + math.radians(halfAOV))
     #   print("DO: "+ str(DO))
        b= (DO-AO)/2.0
        
        CO= b+AO
     #   print("CO: "+ str(CO))

        HC= math.sqrt(math.pow(altitude, 2)+ math.pow(CO, 2))
     #   print("HC: "+ str(HC))

        a= HC * math.tan(math.radians(halfAOV))
        
     #   print("a: "+ str(a) +" b: "+ str(b))
        
        return[a, b]
    
def getSemiMajorGivenSemiMinor(AOV, altitude, cameraAngle, semiMinorAxis):
    
    halfAOV= AOV/2.0
    AO= altitude * math.tan(math.radians(cameraAngle) - math.radians(halfAOV))
     #   print("AO: "+ str(AO))
    DO= altitude * math.tan(math.radians(cameraAngle) + math.radians(halfAOV))
    b= (DO-AO)/2.0
    
    CO= b+AO
    # print("CO: "+ str(CO))
    HC= math.sqrt(math.pow(altitude, 2)+ math.pow(CO, 2))
    # print("HC: "+ str(HC))

    # print('b before a')
    # print(b)
    
    HC =  semiMinorAxis/math.tan(math.radians(halfAOV))
    # print("HC: "+ str(HC))

    CO = np.sqrt(HC**2 - altitude**2)
    # print("CO: "+ str(CO))

    b= CO-AO
    # print('b based on a')
    # print(b)
    return b

def calculateNumCells(squareSideLen, areaSideLen):
    numberCellsPerSide= areaSideLen/squareSideLen
    return numberCellsPerSide**2

# def reverseNumCells(areaSideLen):
    
    
#     return semiMinorAxis

def getCellSquareSide(semiMinorAxis):
    droneCoverageDiameter=  semiMinorAxis * 2#2.53553390593275
    squareDiagonal= droneCoverageDiameter
    squareSide= squareDiagonal / np.sqrt(2)
    return squareSide

def getSquareDiagonal(squareSide):
    d= np.sqrt(2) * squareSide
    return (d)


    
def testingEnvbuildGridCode():
    squareSideLen= 3000
    semiMinorAxis= 245.047
    areaSize=  np.power(squareSideLen, 2)
    droneCoverageDiameter=  semiMinorAxis * 2#2.53553390593275
    squareDiagonal= droneCoverageDiameter
    squareSide= squareDiagonal / np.sqrt(2)
    cellSideSize= int(round(squareSide))
    areaNumCells= int(round(areaSize / np.power(cellSideSize, 2)))
    print(cellSideSize)
    print(areaNumCells)


AOV= 64
altitudesList=[40, 70, 100, 120, 150]
cameraAnglesList=[0, 15, 25, 35, 45, 55]

# cameraAngle= 55
# altitude = 120
# areaSideLen=  3000

# semiMinorAxis= CalculateEllipse(AOV, altitude, cameraAngle)
# squareSideLen= getCellSquareSide(semiMinorAxis)
# numCells= calculateNumCells(squareSideLen, areaSideLen)
# print(numCells)

areaSideLenList=[999, 3000, 4998, 7000, 10000]
numCells= [9, 25, 36, 49, 64]
squareSideLen= [333, 600, 833, 1000, 1250]
altitudesForAreas= [40, 70, 100, 120, 150]
cameraAngleForAreas= 55
semiMinorAxis= [235.46655813512035, 424.26406871192853, 589.0199487283942, 707.1067811865476, 883.8834764831845]
semiMajorAxis= [357.7172565323477, 645.6331250169183, 894.8621579652718, 1074.2898002735851, 1342.8622503419815]


for i in range(len(squareSideLen)):
    #print(areaSideLenList[i]/np.sqrt(numCells[i]))
    semiMinorAxis= getSquareDiagonal(squareSideLen[i])/2.0
   # print(semiMinorAxis)
    print(getSemiMajorGivenSemiMinor(AOV, altitudesForAreas[i], cameraAngleForAreas, semiMinorAxis))
    
# areaSideLen= 5000
# for cameraAngle in cameraAnglesList:
#     print('CamAngle ('+str(cameraAngle)+") ********")
#     for altitude in altitudesList:
#         semiMinorAxis= CalculateEllipse(AOV, altitude, cameraAngle)[0]
#         squareSideLen= getCellSquareSide(semiMinorAxis)
#         numCells= calculateNumCells(squareSideLen, areaSideLen)
#         if(numCells <= 64 and numCells >= 4):
#             print(str(altitude)+'\t'+str(numCells))


# ellipseDimsListAngle55={(245.047, 373.133), (612.618, 932.83), (735.142, 1119.399), (918.927,1399.2496)}

# testingEnvbuildGridCode()