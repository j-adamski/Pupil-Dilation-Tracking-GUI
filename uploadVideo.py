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
    
def openFile():   
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Video Files (* avi);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)
    return fileName

def splitVideo(vidFileName, imageListInput, folderName):
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
            
        
    #Note:last frame come out as NULL image - so it need to be ignored
            
            
            

    
    
            