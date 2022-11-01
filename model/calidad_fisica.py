# Author: Carlos Cardona

import os
import sys

import matplotlib.pyplot as plt
import pydicom
import numpy as np
import cv2 as cv
#from PIL import Image

class SDNR(object):
    
    def __init__(self, image_path: str, windows_size=100, color=False):
        self.color=color
        self.image_path=image_path
        self.size=windows_size
        self.image = cv.imread(self.image_path, cv.IMREAD_UNCHANGED)
         
    def background_window(self):
        """ Return a window containing only background pixels"""
        size=self.size
        image=self.image
        if self.color:
            image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(image,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        rows=thresh.shape[0]
        cols=thresh.shape[1]
        coords=[]
        #random.randint(0, rows)
        for i in range(rows-size):
            j=0
            while j <cols-size-1:
    #             print(j)
                j+=1
                if coords:
                    break
                else:
                #print(f"thresh {i} = {thresh[i,j]}, thresh {i+size}= {thresh[i+size,j]}")
                    if thresh[i,j]==255 and thresh[i+size,j+size]==255 :
                        coords.extend([(i,j),(i,j+size),
                                             (i+size,j),(i+size,j+size)]
                                        )
                    else:
                        continue

        return coords
    
    def Ns(self):
        """ Return size of object in pixels and total size in pixels"""
        image=self.image
        if self.color:
            image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(image,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        rows=thresh.shape[0]
        cols=thresh.shape[1]
        N=int(rows*cols)
        object_pix=[]
        N_obj=0
        #random.randint(0, rows)
        for i in range(rows):
            for j in range(cols):
                if thresh[i,j]==0 :
                    N_obj+=1

        return N, N_obj
    
    def mean_std_dev_win(self, whole=False):
        """ Return pixel standard deviation of a window of pixels """
        
        image=self.image
        
        if whole:
            window=[(0,0),(0,image.shape[0]),(image.shape[1],0),(image.shape[1],image.shape[0])]
        else:
            window= self.background_window()  
        
        window_img = image[window[0][0]:window[2][0], window[0][1]:window[1][1]]
        window_img=window_img.reshape(-1)
        mean=window_img.sum()/window_img.size

        sqr_dist=np.array([(item-mean)**2 for item in window_img])
        std=np.sqrt(sqr_dist.sum()/ window_img.size)
        return mean, std
    
    def sdnr(self, normal=False):
        """ Computed mean signal difference to noise ratio from an image """
        if normal:
            mean_background, std_background=0, 1
        else:   
            mean_background, std_background=self.mean_std_dev_win()
        mean_total, std_total=self.mean_std_dev_win(whole=True)
        
        N_s=self.Ns()
        
        Sdnr=(N_s[0]/N_s[1])*np.abs(mean_total-mean_background)/std_background
        return Sdnr
    
    def cnr(self, normal=False):
        """ Computed mean signal difference to noise ratio from an image """
        if normal:
            mean_background, std_background=0, 1
        else:   
            mean_background, std_background=self.mean_std_dev_win()
      
        return Cnr
        
    def fom(self):
        return Fom
       
        
class Dicom_to_Png(object):

    def __init__(self, fdicom):

        self.mammo_cont=pydicom.dcmread(fdicom)
        self.image_array=self.mammo_cont.pixel_array

    def Pilimage(self, path):
        normalizedImg = np.zeros((800, 800))
        image_array=cv.normalize(self.image_array,  normalizedImg, 0, 255, cv.NORM_MINMAX)
        image_array=image_array.astype(dtype="uint8")
        cv.imwrite(path+".png", image_array)

    # def Pilimage(self, path):
    #     plt.imshow(self.image_array, cmap='gray')
    #     plt.savefig(path+".png")
