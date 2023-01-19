# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 13:30:55 2021

@author: j.schoeggl
"""

import os
#volumen, durchmasser
#next neighbour
os.chdir(r"D:\Johanna\fraktal_dim")

import numpy as np

import scipy.ndimage as nd
import matplotlib.pyplot as plt

from skimage import color
from skimage.measure import find_contours, regionprops

import numpy as np
#from scipy import ndimage as nd
from skimage import io

from skimage.transform import rescale, resize, downscale_local_mean
import sys
from sys import argv
    
from LZW import LZW
from struct import *
from helferleinNEU import *
import time
import tqdm

#%%
def border(arr):

    dist = nd.distance_transform_edt(arr)

    return dist==1
#border gibt bool zuyück

#%%

def my_range(start, end, steps):
    while start <= end:
        yield start
        start+=steps

#%%

save_raw = r"D:\Johanna\fraktal_dim\ims_raw"

# step -1

#mit region props die 10 größten silicium 
im300c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment #2 C300 v2\c300v2_prediction\images_fixed.npy"
lp300c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment #2 C300 v2\c300v2_prediction\prediction_fixed.npy"
save_r300c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment #2 C300 v2\c300v2_prediction\silicon"

im3c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 1 C3\c3_prediction\images_fixed.npy"
lp3c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 1 C3\c3_prediction\prediction_fixed.npy"
save_r3c=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 1 C3\c3_prediction\silicon"

imP=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 3 pristine\Pristine_prediction\silicon\images_fixed.npy"
lpP=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 3 pristine\Pristine_prediction\prediction_fixed.npy"
save_P=r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 3 pristine\Pristine_prediction\silicon"


l=np.load(lpP)
im=np.load(imP)

im = np.array([io.imread(os.path.join(imP, i), as_gray=True) 
                    for i in files(imP)]) 
l = np.array([io.imread(os.path.join(lpP, i), as_gray=True) 
                    for i in files(lpP)]) 


#lab=nd.label(l==2)[0] # label gibt 2 objekte (labelbild und anzahl der labels)
#%%%
"""für 3D export der silicia"""

lab=nd.label(l==2)[0]
rl=regionprops(lab,im)
sor=np.argsort([i.area for i in rl])[::-1]
#images = [rl[i].intensity_image for i in sor[:10]]
images = [rl[i].image for i in sor[:10]]
    
for u, imgs in enumerate(images):
    for l, o in enumerate(imgs):
        io.imsave(save_P+os.sep+"P_{}_{}.tif".format(u,l), o) #jedes imgs = 3d
        #images[0] bis [bla].shape für die shapes
    np.save(save_P+os.sep+"siliconimagesC3.npy", images) #in avizo shape vom np angeben!!!

"""3D ende"""
#%%



for k, n in enumerate(la):
    lap=regionprops(n)
    sor=np.argsort([i.area for i in lap])[::-1]
    images = [lap[i].image for i in sor[:10]]

    for u, imgs in enumerate(images):
        io.imsave(rawfolder+os.sep+"300c_{}_{}.tif".format(k,u), imgs.astype("uint8"))    

sav=r"D:\Johanna\fraktal_dim\rawfolder"
np.save(sav+os.sep+"siliconimagesP.npy", la)



#%%Funktioniert Sicher!!!!!!!!!
""""preparation for 100 images of all samples"""

l=np.load(lpP)

la=np.zeros_like(l[1])

la=np.where(l==2,1,0)



pap=r"D:\Johanna\fraktal_dim\rawfolder"
# =============================================================================
# la = np.array([io.imread(os.path.join(pap, i), as_gray=True) 
#                     for i in files(pap)]) 
# =============================================================================

stap=r"D:\Johanna\fraktal_dim\startfolder"

l=la

for k, u in enumerate(l):
    lab=nd.label(u==1)[0]
    rl=regionprops(lab)
    sor=np.argsort([i.area for i in rl])[::-1]
    images = [rl[i].image for i in sor[:10]]
    n= [j[:-4] for j in files(pap)]
    for r, imgs in enumerate(images):
        io.imsave(pap+os.sep+"P_{}_{}.tif".format(k,r), imgs.astype("uint8"))

ima=np.array(images)
print(ima.shape)
# =============================================================================
# lu = np.array([io.imread(os.path.join(pap, i), as_gray=True) 
#                     for i in files(pap)]) 
# =============================================================================

lol=[]
for i in my_range(1, len(files(pap)), 14):#c3 120, c300 182, P 147
     lol.append(io.imread(os.path.join(pap,os.listdir(pap)[i])))

lop=np.array(lol)
     
for i,j in enumerate(lol):     
     nam = os.listdir(pap)[i][:-4]
     io.imsave(stap+os.sep+"{}.tif".format(i),j)
    

#%%

"""Colored Images for Roland"""

import skimage
from skimage import color

colors = ['blue', 'deepskyblue', 'red', 'fuchsia', 'palegreen']
lc3=np.load(r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 1 C3\c3_prediction\prediction_fixed.npy")
ic3=np.load(r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 1 C3\c3_prediction\images_fixed.npy")

l300=io.imread(r"D:\Johanna\fcholletneu\presentation\present\2_prediction.png")
i300=io.imread(r"D:\Johanna\fcholletneu\presentation\present\2.png")

prl=np.load(r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 3 pristine\Pristine_prediction\prediction_fixed.npy")
pri=np.load(r"G:\projects\nk188 (ECo2LIB)\F_data\E_MIK\01\Zeiss\Experiment 3 pristine\Pristine_prediction\images_fixed.npy")

arr=-1*np.ones_like(prl[71])
arr=arr.astype("int8")

op=color.label2rgb(prl[71],arr, bg_label=-1, colors=colors)

io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\c3_image_1000.png", ic3[1000])
io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\c3_pred_1000.png", op)

io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\c300_image_2.png", i300)
io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\c300_pred_2.png", op)

io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\p_image_71.png", pri[71])
io.imsave(r"C:\Users\J.Schoeggl\Pictures\roland\p_pred_71.png", op)


#%%