# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:56:02 2023

@author: Vincent.Bevilacqua
"""


import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from tqdm import *

fil = open('characters.txt','w')

st=''

for i in range(12):
    st+='_'
st+='\n|'

cnt = 1
for i in range(33,127):
    st += chr(i)
    if cnt%10== 0:
        st+='|\n|'
    cnt+=1

st+='\n'
for i in range(12):
    st+='_'    
    
print(st)

fil.write(st)

fil.close()

with Image.open('characters.png','r') as img:
    nimg = np.array(img)

r = 0.2126
g = 0.7152
b = 0.0722

charims = [np.zeros((16,8))]

for i in range(0,160,16):
    for j in range(0,80,8):
        temp = nimg[i:i+16,j:j+8,:3]
        if (abs(temp-np.zeros((16,8,3)))).sum() > 0:
            charims.append(temp[:,:,0]*r+temp[:,:,1]*g+temp[:,:,2]*b)

fact = 2

with tqdm(total = 2983*(384000+25*120*94)) as pbar:
    for imgidx in range(2983):
        with Image.open(f'..\\frames\\{imgidx}.png') as img:
            nimg = np.array(img)
            
        nimg = nimg[:,:,0]*r+nimg[:,:,1]*g+nimg[:,:,2]*b
        nimg2 = np.zeros((nimg.shape[0]//2,nimg.shape[1]//2))
        for i in range(nimg.shape[0]//fact):
            for j in range(nimg.shape[1]//fact):
                nimg2[i,j] = nimg[fact*i:fact*(i+1),fact*j:fact*(j+1)].mean()
                pbar.update(1)
        
        
        with open(f'..\\tframes\\{imgidx}.txt','w') as fil:
            for i in range(0,nimg2.shape[0],16):
                string = ''
                for j in range(0,nimg2.shape[1],8):
                    snip = nimg2[i:i+16,j:j+8]
                    vals = np.zeros(94)
                    for k in range(94):
                        vc = charims[k]
                        vals[k] = ((snip-vc)**2).sum()
                        pbar.update(1)
                    string+=chr(vals.argmin()+32)
                fil.write(string+'\n')
    
