# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 10:53:29 2021

@author: HG19230
"""

areaSizeLimit= 24
fileName= 'Steps200KRotOut.txt'


f = open(fileName, "r")
lines= f.readlines()

maxVal= 0

for line in lines:

    lineVals=line.split('   ')
    
    for val in lineVals:
        
        valSplitted= val.split('  ')

        if len(valSplitted) >0:
            
            for val2 in valSplitted:
                
                if not val2=='' and float(val2) > areaSizeLimit:
                    print('invalid')
                    
                if not val2=='' and float(val2) > maxVal:
                    maxVal= float(val2)
                
        else:
            if not val=='' and float(val) > areaSizeLimit:
                print('invalid')
                
            if not val=='' and float(val) > maxVal:
                maxVal= float(val)
                
            
print(maxVal)