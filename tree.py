# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:54:33 2023

@author: Vincent.Bevilacqua
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from tqdm import *

##################################################
###Video to PNG###############
##################################################


# cap = cv2.VideoCapture('vid.mp4')
# fps = round(cap.get(cv2.CAP_PROP_FPS))

# cf = 0

# with tqdm(total = 2983) as pbar:
    
#     while True:
        
#         ret,frame = cap.read()
        
#         if ret:
            
#             name = '.\\frames\\'+str(cf)+'.png'
#             cv2.imwrite(name,frame)
#             cf+=1
#             pbar.update(1)
#         else:
#             break

# cap.release()
frames = []
#################################################
for i in trange(2983):
    name = '.\\frames\\'+str(i)+'.png'
    img = Image.open(name)
    nimg = np.array(img)
    img.close()
    
    nimg = nimg[:530,:,:]
    scale = 10
    newimg = np.zeros((5*scale,10*scale,3)).astype(int)
    
    y,x = nimg.shape[0]//5,nimg.shape[1]//10
    
    for i in range(5):
        for j in range(10):
            newimg[scale*i:scale*i+scale,scale*j:scale*j+scale,0] = int(nimg[i*y:(i+1)*y,j*x:(j+1)*x,2].mean())
            newimg[scale*i:scale*i+scale,scale*j:scale*j+scale,1] = int(nimg[i*y:(i+1)*y,j*x:(j+1)*x,1].mean())
            newimg[scale*i:scale*i+scale,scale*j:scale*j+scale,2] = int(nimg[i*y:(i+1)*y,j*x:(j+1)*x,0].mean())
    # frames.append(Image.fromarray(np.uint8(newimg)))
    frames.append(np.uint8(newimg))

video = cv2.VideoWriter('compvid.mkv',cv2.VideoWriter.fourcc(*'mp4v'),24,(10*scale,5*scale))

for frame in frames:
    video.write(frame)
    
video.release()

##################################################
# minas = Image.open('mt.png','r')

# mt = np.array(minas)

# mt = mt[:,:,:3]

# temp = np.zeros((mt.shape[0]*3,mt.shape[1]))

# temp[:mt.shape[0],:] = mt[:,:,0]
# temp[mt.shape[0]:2*mt.shape[0],:] = mt[:,:,1]
# temp[2*mt.shape[0]:3*mt.shape[0],:] = mt[:,:,2]

# newimg = np.zeros((5,10,3))

# clip = mt[(mt.shape[0]%newimg.shape[0])//2:mt.shape[0]-((mt.shape[0]%newimg.shape[0])-(mt.shape[0]%newimg.shape[0])//2),
#           (mt.shape[1]%newimg.shape[1])//2:mt.shape[1]-((mt.shape[1]%newimg.shape[1])-(mt.shape[1]%newimg.shape[1])//2),:]

# y,x = clip.shape[0]//newimg.shape[0],clip.shape[1]//newimg.shape[1]

# div = x*y

# for i in range(newimg.shape[0]):
#     for j in range(newimg.shape[1]):
#         for rgb in range(3):
#             newimg[i,j,rgb] = mt[i*y:(i+1)*y,j*x:(j+1)*x,rgb].max()
# newimg = newimg.astype(int)

# plt.imshow(newimg)         

# U,S,V = np.linalg.svd(temp)

# S2 = np.zeros(S.shape[0])

# compress = 50

# S2[:compress] = S[:compress]

# S3 = np.zeros((U.shape[0],V.shape[0]))

# S3[:S2.shape[0],:S2.shape[0]] = np.diag(S2)

# res = U@S3@V

# newimg = np.zeros(mt.shape)

# newimg[:,:,0] = res[:mt.shape[0],:]
# newimg[:,:,1] = res[mt.shape[0]:2*mt.shape[0],:]
# newimg[:,:,2] = res[2*mt.shape[0]:3*mt.shape[0],:]

# newimg = newimg.astype(int)

# plt.imshow(newimg)
