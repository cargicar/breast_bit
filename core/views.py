import os
import cv2
#from PIL import Image
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import pydicom

import tensorflow as tf
from tensorflow import keras
#import tensorflow_hub as hub
#import tensorflow_datasets as tfds

from model.calidad_fisica import SDNR
from model.calidad_fisica import Dicom_to_Png as DtP

from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
 
#@login_required
def index(request):
    return render(request, 'index.html')

 
#@login_required
def cancer_detection(request):
    message = ""
    prediction = ""
    image_name= ""
    RESIZE_TO=160
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        path = str(settings.STATIC_DIR) + "/images/" + image.name
        _image = fss.save(path, image)
        image_name = "/images/" + image.name
        # image details

        # Read the image
        imag=cv2.imread(path)
        imag = tf.image.resize(imag, (RESIZE_TO, RESIZE_TO))
        resized_image = imag / 255.0
        #img_from_ar = Image.fromarray(imag, 'RGB')
                
        test_image =np.expand_dims(resized_image, axis=0) 

        # load model
        # model = tf.keras.models.load_model(os.getcwd() + '/model.h5')
        model = tf.keras.models.load_model(os.getcwd() + '/model') 
        result = model.predict(test_image)
        # ----------------
        # LABELS
        # Bening 0
        # Maling 1
        # ----------------
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "Benigno"
        elif (np.argmax(result) == 1):
            prediction = "Maligno"
        else:
            prediction = "Unknown"
        
        return TemplateResponse(
            request,
            "cancer_detection.html",
            {
                "message": message,
                "image": image,
                "image_name": image_name,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "cancer_detection.html",
            {"message": "Please upload a picture with a Region of Interest containing the suspicious mass (.png, .jpg, .jpeg)"},
        )

    
#@login_required
def quality_image(request):
    message = ""
    sdnr = ""
    calidad = ""
    fname=""
    image_name= ""
    fss = CustomFileSystemStorage()
    try:
        fdicom= request.FILES["fdicom"]
        fname = fdicom.name
        #print(f"dicom readed: {fdicom.name}")                                         
        path_dicom = str(settings.MEDIA_DIR) + "/"+ fname
        #print(f"path to dicom {path_dicom}")                                          
        _fdicom=fss.save(path_dicom, fdicom)

        to_image=DtP(path_dicom)
        path_fig = str(settings.STATIC_DIR) + "/images/" + fname[:-4]
        #print(f"path to figure {path_fig}.png")                                       
        # image details                                                                
        to_image.Pilimage(path_fig)
        image_name = "/images/"+ fname[:-4]+".png"
        #print(f"image_name : {image_name}")                                           
        sdnr_ex=SDNR(path_fig+".png")
        sdnr= int(sdnr_ex.sdnr(normal=True))
        print(f"SDNR : {sdnr}")
        if (sdnr > 500):
            calidad = "Excelente"
        elif (500> sdnr > 300):
            calidad = "Muy Buena"
        else:
            calidad= "Mala"


        return TemplateResponse(
            request,
            "quality_image.html",
            {
                "message": message,
                "sdnr" : sdnr,
                "image_name":image_name,
                "calidad": calidad,
                "fname" : fname
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "quality_image.html",
            {"message": "Please upload a DICOM file (.dcm)"},
        )

 
#@login_required
def jupyter_nb(request):
    return render(request, 'jupyter_nb.html')


# @login_required
def logout(request):
    return render(request,'logout.html')
