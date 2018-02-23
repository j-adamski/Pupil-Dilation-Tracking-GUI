# -*- coding: utf-8 -*-
"""
Created on Tue May 23 15:51:55 2017

@author: Julia
"""
import sys
import cv2
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import time
import numpy as np
import os
global vidcap
    
def openFile():   
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Video Files (* avi);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)
    return fileName



def splitVideo(vidFileName, imageListInput, folderName):
    global vidcap
    framecount = 1 
    folder = folderName    
    vidcap = cv2.VideoCapture(str(vidFileName))
    success,image = vidcap.read()
    success = True
    while success:
            success,image = vidcap.read()
            print ('Read a new frame: '), success
            cv2.imwrite(os.path.join(folder,"frame{:d}.jpg".format(framecount)), image)     # save frame as JPEG file
            print("{} images are extacted in {}.".format(framecount,folder))
            framecount += 1
 
        
def getFPS():
    #note: This fuction does not work on the video from Dr. Gaynes because it does not have FPS in the vid properties.
    #      It works on other videos. For now we will just calculate the FPS for that specific video.
    global vidcap
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    return fps 

def calculateFPS():
    s = 41
    frames = 737
    fps = 737/41
    return fps
      
        
#Note:last frame come out as NULL image - so it need to be ignored
            
      
            



    
    
            