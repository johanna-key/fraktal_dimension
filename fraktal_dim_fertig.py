# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 10:56:43 2022

@author: j.schoeggl
"""


import os
import sys
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
from shutil import copyfile
from PIL import Image

#file distributor
from fnmatch import fnmatch
import os
import shutil

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
dirpath=r"D:\Johanna\fraktal_dim"
rawfolder='rawfolder'
startfolder='startfolder'
compfolder = 'Compression'
Images = 'Images'

def inputmanager(dirpath):
    imi=[]
    compfolder = 'Compression'
    Images = 'Images' #vll auf images reduction folder umbenennen #temp

    rawfolder='rawfolder'
    startfolder='startfolder'
    
    for i,j in enumerate(files(rawfolder)): #raw folder can have  pngs thy will be convertet and saved to startfolder
        images_topng = []
        if 'png' in j:
            images_topng.append(io.imread(os.path.join(rawfolder, j), as_gray=True))
            names=[j[:-4] for j in files(rawfolder)]
            for a,b in enumerate(images_topng):
                io.imsave(startfolder+os.sep+'_{}_{}.tif'.format(names[i],a),b.astype("uint8"))
                
        if '.tif' in j:
            copyfile(os.path.join(rawfolder,j), os.path.join(startfolder,j))
            #imi.append(io.imread(os.path.join(rawfolder, j), as_gray=True))
            
        elif ('.npy' in j):
                    l = Image.fromarray(np.load(os.path.join(rawfolder,j), allow_pickle=True).squeeze())
                    for k, n in enumerate(l):
                        lab=nd.label(n==1)[0]
                        rl=regionprops(lab)
                        sor=np.argsort([i.area for i in rl])[::-1]
                        images = [rl[i].image for i in sor[:10]]
                        n= [j[:-4] for j in files(rawfolder)]
                        for u, imgs in enumerate(images):
                            io.imsave(startfolder+os.sep+"{}_{}_{}.tif".format(n[i],k,u), imgs.astype("uint8"))
        elif ('.tif' in j) and (j[:-4] not in files(startfolder)): #step zero
            imi.append(io.imread(os.path.join(rawfolder, j), as_gray=True))
                    
        else:
            for i, j in enumerate(files(startfolder)):
                imi.append(io.imread(os.path.join(startfolder, j), as_gray=True))
                #imi=np.array(imi) 
            temp_files = files(rawfolder)
            for f in temp_files:
                os.remove(rawfolder+os.sep+f)
        return imi


#%%

"""step 1:
#s= 1,2, . . . 9. This corresponds to reducing the image size to
#10%,20%,· · · ,90% of the original ﬁle size."""

"""A: mit vorbearbeiteten images via inputmanager"""
#im=np.array(imi) #mit vorbearbeitung, im wird dann an den distributer übergeben.

#%%
# =============================================================================
# """B: direkter input falls die files nur noch reduced und compressed werden müssen"""
# imo=([io.imread(os.path.join(startfolder,i), as_gray=True) for i in files(startfolder)])
# im=np.array(imo) #images ohne vorbearbeitung direkt aus startfolder
#         
# =============================================================================
#%%
#distribute files in chunks an subfolder 
#chunk ordner 0 soll mir chunk 0 befüllt werden


def distributer(im):
   #reduction
    scalingfactor=0.1
    for u, z in enumerate(im):
        reducedims=[] 
        #distribution
        root_dir = r"Images"

        subfolder = "chunks_{}".format(u)
        new_dir = os.path.join(root_dir, subfolder)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
    
        for i in range(1,11):
            reducedims.append(rescale(z,i*scalingfactor))
    
        ims=[(i*255).astype("uint8") for i in reducedims]
       
        for j, iml in enumerate(ims):
            io.imsave(new_dir+os.sep+"{}.tif".format(j), border(iml).astype("uint8"), check_contrast=False)

#%%
#LWZ Compressio
# ab hier für jeden chunk ordner einmal compressio durchführen!!!!
        
#step 2:
# compression mittels lwz algorithmus; decompression => optional"""
#compressor:
#Ergebnise plotten
#step 3: 
# Measure the file sizes S(s) and plot log(S) versus log(s) and determine the
# physical scaling range."""
    
def compression(impath):
    cop=r"D:\Johanna\fraktal_dim\CompressedFiles"
    steigung = []
    for i,j in enumerate(os.listdir(impath)):
        pspc = os.path.join(impath, j)
        print(j)
        sizelist = [] #pro chunk
   
    
        for g,h in enumerate(files(pspc)):        
            compressor = LZW(os.path.join(pspc,h))
            compressor.compress()
#decompressor :  
    #for i, j in eunumerate(files(compfolder)):
        #decompressor = LZW(os.path.join(compfolder,j))
        #decompressor.decompress()      

        for co in files(cop):
            sizelist.append(os.stat(cop+os.sep+co).st_size)
        o=[oi for oi in range(1,11)]# ?1x ausrücken???
        #plt.plot(np.log(o),np.log(sizelist), label="fractal_dimension_ {}".format(i))
          
    #step4 find k  
        k, d = np.polyfit(np.log(o),np.log(sizelist), deg=1)
        steigung.append(k)

        print(steigung, file=open("steigung_mean_P_test.txt", "a"))
        print("steigung k:", steigung)
    print("mean:",np.mean(np.array(steigung)))
        
    #plt.legend()

#%%
p=r"D:\Johanna\fraktal_dim\rawfolder"
inputmanager(p)

#%%

#Testlauf:
"""B: direkter input falls die files nur noch reduced und compressed werden müssen"""
imo=([io.imread(os.path.join(startfolder,i), as_gray=True) for i in files(startfolder)])
im=np.array(imo) #images ohne vorbearbeitung direkt aus startfolder
    
#%%

impath=r"D:\Johanna\fraktal_dim\Images"

distributer(im)

compression(impath)



#%%

#tests:

steigung =[]
sizelist = [] 
cop=r"D:\Johanna\fraktal_dim\CompressedFiles"
for co in files(cop):
    sizelist.append(os.stat(cop+os.sep+co).st_size)
si = np.array(sizelist)
o=[oi for oi in range(1,11)]

k, d = np.polyfit(np.log(o),np.log(sizelist), deg=1)
steigung.append(k)

steig=[r for r in range(1,101)]
print("steigung k:", steig, file=open("steigung_output.txt", "a"))

import sys

print('This message will be displayed on the screen.')

original_stdout = sys.stdout # Save a reference to the original standard output

#%%%

with open('steigung_output_300C.txt', 'r') as f:
    text = f.readlines() # Change the standard output to the file we created.

tex=[]
for i in text:
    tex.append(eval(i.split('k: ')[1][:-1]))


texi=np.array(tex)
m=np.mean(texi)

f = open('steigung_output_3C.txt', "r")
text = f.readline
f.close()

tex=np.array(text)
[-10:]
