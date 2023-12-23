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
import pickle

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

bvals = []

for i in charims:
    bvals.append(i.sum())

bvals = np.array(bvals)
bidxs = bvals.argsort()

cscale = 16*8*255/bvals.max()

krnls = []
krnls.append(np.array([[1,1],[-1,-1]]))
krnls.append(np.array([[-1,1],[-1,1]]))
krnls.append(np.array([[0,1],[-1,0]]))
krnls.append(np.array([[1,0],[0,-1]]))

for i in range(4):
    krnls.append(-krnls[-4])
    
def fltr(inpt):
    temp = np.zeros((inpt.shape[0]//2,inpt.shape[1]//2))
    for i in range(inpt.shape[0]//2):
        for j in range(inpt.shape[1]//2):
            for k in krnls:
                temp[i,j] += abs((k*inpt[2*i:2*(i+1),2*j:2*(j+1)]).sum())
    return (temp/temp.max())

fact = 2
bal = 0.5
drk = [np.zeros((16,8))]
med = []
brt = []

fdrk = [np.zeros((8,4))]
fmed = []
fbrt = []

for i in bidxs[1:bidxs.shape[0]//3]:
    drk.append(charims[i])
    fdrk.append(fltr(charims[i]))
for i in bidxs[bidxs.shape[0]//3:2*bidxs.shape[0]//3]:
    med.append(charims[i])
    fmed.append(fltr(charims[i]))
for i in bidxs[2*bidxs.shape[0]//3:]:
    brt.append(charims[i])
    fbrt.append(fltr(charims[i]))

with tqdm(total = 2983*31*60*50) as pbar:
    for imgidx in range(2983):
        # with Image.open(f'.\\frames\\{imgidx}.png').convert('L').resize((1920//2,400)) as img:
            # img.save(f'.\\hframes\\{imgidx}.png')
            # pbar.update(1)
        with Image.open(f'.\\hframes\\{imgidx}.png')as img:
            nimg = np.array(img)
        
        
        with open(f'.\\tframes\\{imgidx}.txt','w') as fil:
            for i in range(0,nimg.shape[0],16):
                string = ''
                for j in range(0,nimg.shape[1],8):
                    snip = nimg[i:i+16,j:j+8]
                    chknum = snip.sum()
                    if chknum <= 10880:
                        chk = drk
                        fchk = fdrk
                        adj = 0
                    elif chknum <= 21760:
                        chk = med
                        fchk = fmed
                        adj = len(drk)
                    else:
                        chk = brt
                        fchk = fbrt
                        adj = len(drk)+len(med)
                    vals = np.zeros(len(chk))
                    fsnip = fltr(snip)
                    for k in range(len(chk)):
                        fvc = fchk[k]
                        vc = chk[k]
                        vals[k] = ((fsnip-fvc)**2).sum()*(1-bal)+(((snip-vc*cscale)/32640)**2).sum()*bal
                        pbar.update(1)
                    string+=chr(bidxs[vals.argmin()+adj]+32)
                fil.write(string+'\n')
    
