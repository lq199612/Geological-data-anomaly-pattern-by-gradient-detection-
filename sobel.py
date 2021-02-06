#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:21:23 2021

@author: lq
"""

import numpy as np
from scipy import ndimage
import pandas as pd
from scipy.ndimage import sobel, generic_gradient_magnitude
import os
import math   

def calculate(inputFile):
    a = np.loadtxt(inputFile)  
    b = np.reshape(a, (540, 410, 138)) 
    o = generic_gradient_magnitude(b, sobel)  # magnitude
    dx = ndimage.sobel(b, 0)  # x derivative
    dy = ndimage.sobel(b, 1)  # y derivative
    dz = ndimage.sobel(b, 2)  # z derivative

    r = pd.DataFrame({'gx':dx.reshape(-1), 'gy':dy.reshape(-1), 'gz':dz.reshape(-1)}) 
    R = r.loc[(r['gx'] != 0) & (r['gy'] != 0) & (r['gz'] != 0)]  # about 400 000 
    S = np.array(R.values)
    L = len(S)

    output_file = open(f"output/{inputFile.replace('.txt','')}.csv", 'w')
    for a in range(0, 360):  
        for b in range(0, 90):
            i = (math.cos(b * math.pi / 180)) * (math.sin(a * math.pi / 180))
            j = (math.cos(b * math.pi / 180)) * (math.cos(a * math.pi / 180))
            k = math.sin(b * math.pi / 180)
            g = np.array([i, j, k])
            All_list = np.dot(S, g.T)
            A = pd.DataFrame(All_list, columns=['dot'])
            z = A.loc[A['dot'] > 0]
            f = A.loc[A['dot'] < 0]
            Z = z.mean()[0]
            F = f.mean()[0]
            l1 = len(z)
            l2 = len(f)
            V = (l1 * Z + (- l2 * F)) / (l1 + l2)
            output_file.write( ','.join([str(a) , str(b) , str(l1) , str(Z) , str(l2) , str(F) , str(V)]) + '\n')
    output_file.close()
    print(f'{inputFile} calculate done!')  

os.chdir('/Volumes/T7/data')   # locate document path
inputFiles = ['Cu_2.txt', 'Cu_3.txt']  # file path
for inputFile in inputFiles:
    calculate(inputFile)


    