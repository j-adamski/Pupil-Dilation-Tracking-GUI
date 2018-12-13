import sys, random
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image
import glob
import pyqtgraph as pg
import numpy as np
import math
import csv
import upload
from saveData import *
import saveData
from main import *

import pylab as py
import ellipseFitting

count = 1
frames= 0
image_list = [] #stores paths of all frames extracted from video
coordinates = [] #array stores coordinates during double clicks to draw ROI
diameter_data = [] #array that contains ROI diameters
saveState= []
maxCount = 0

for x in range(0,15):    #TO DO: add unique range based on # of image frames. Left like this for now for testing purposes
    diameter_data.append(0)
    saveState.append(0)

image_list = upload.image_list



class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) 
        self.graphicsView.enableAutoRange('xy') # the axis will NOT automatically rescale when items are added/removed or change their shape. 
        self.L_button.clicked.connect(self.on_clickLeft) # connecting L mouse button to on_clickLeft function
        self.R_button.clicked.connect(self.on_clickRight) # connecting R mouse button to on_clickRight function
        self.actionUpload_new.triggered.connect(self.FILEMENU_upload) # connecting upload button to FILEMENU_upload
        self.horizontalSlider.sliderMoved.connect(self.sliderMoved) # when slider is moved, it will trigger sliderMoved function
        self.menubar.triggered.connect(self.fileMenu)  #FOR TESTING... DELETE LATER
        self.action1.triggered.connect(self.manualSelection)
        self.action2.triggered.connect(self.gaussianFilter)
        self.checkBox_StoreData.stateChanged.connect(self.save)
        self.actionSave.triggered.connect(self.csv)
        
        
# - - - - - - - - Keyboard/Click Events - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def connection(self):
        print("checked")

    def on_clickLeft(self): 
        global count
        if count > 0:
                count= count - 1              
        self.update()
                
    def on_clickRight(self):
        global count
        if count < len(image_list)-1:
                count = count + 1
        self.update()
                
    def sliderMoved(self, val): 
        global count
        count = val
        self.update()
        
    def keyPressEvent(self, event):
        global count
        global navigation
        key = event.key()
        if key == Qt.Key_A:
            if count > 0:
                count= count - 1 
                self.update()
                navigation = "L"

        elif key == Qt.Key_D:
            if count < len(image_list)-1:
                count = count + 1
            
                self.update()
                navigation = "R"
                
        elif key == Qt.Key_Escape: #if ESC key is pressed, program close
            self.close()    
            
        elif key == Qt.Key_Delete: #if del key is pressed, ROI is removed. #STILL have to manually remove data though. #TO DO
            self.graphicsView.removeItem(cir)
            self.checkBox_StoreData.setChecked(False) 
            coordinates[:] = []
            print("  ")
            print("delete", diameter_data)
            print(" ")
            
    def clicked(self, event):
        manualSelection.onClick(self, event)
    
    def do_nothing(self):
        pass
        
# - - - - - - - - - - - - - - - - -  File Menu - - - - - - - - - - - - - - - - - #
    def FILEMENU_upload(self):
        upload.openVidFile()
        self.update()
                        
    def fileMenu(self):  #FOR TESTING -- delete later
        print("fileMenu triggered")
        if self.action1.isChecked() == True:
            pass
    
    def manualSelection(self):
        print("action1")
        self.graphicsView.scene().sigMouseClicked.connect(self.clicked) # Connect onClick function to mouse click             
        
    def gaussianFilter(self):
        self.graphicsView.scene().sigMouseClicked.disconnect(self.clicked) 
        
        
#- - - - - - - Displaying image on GUI and updating - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def update(self):
        global img_arr
        global maxCount
        global cir
        global img
        img = Image.open(image_list[count])
        arr = np.array(img)
        arr = np.rot90(arr, -1)
        img_arr = pg.ImageItem(arr)
        self.graphicsView.addItem(img_arr)
        self.label_frameNum.setText("Frame " + str(count))
        self.horizontalSlider.setSliderPosition(count) #setting the slider proportionate to the position of the current frame
       
        
        print("Current array:", diameter_data)
        
        
        if (count>maxCount):  #Checks the maximum frame # that was reached
            maxCount = count
            
        if count == maxCount:
            if(diameter_data[count-2] != 0):
                self.checkBox_StoreData.setChecked(True)
                #TO DO: set ROI if someone goes back and then goes forward to this frame
            else:
                self.checkBox_StoreData.setChecked(False)
            #    self.graphicsView.removeItem(cir)   # set this later
                
        elif count < maxCount: #If true, then that means that the user is going back through the frames 
            print("count:", count)
            print("maxCount:", maxCount)
            if(diameter_data[count-1] != 0):  #There is data stored in current frame
                print("1")
                self.checkBox_StoreData.setChecked(True)
                self.graphicsView.removeItem(cir)
                self.graphicsView.addItem(cir)
                cir.setState(saveState[count-1])
    
            elif(diameter_data[count-1] == 0):
                print("2")
                self.checkBox_StoreData.setChecked(False)
        
        self.save()
        if(diameter_data != 0):
            cir.sigRegionChangeFinished.connect(self.updateROIdata) #If the ROI is changed in current frame, the updateROIdata function is called
          

    def save(self): #needed in order to properly connect 
        save.saveData(self, cir, diameter_data, saveState, count) 
        
    def csv(self):
        save.export_to_csv(self, diameter_data)
        
                
    def updateROIdata(self):
        global cir
        global count
        d = cir.size() #function to get width and height, returned as tuple
        d = d[1] #since width = height, we just need to store one of the numbers
        diameter_data[count-1] = d   
        
        saveState[count-1]=cir.saveState()                
        #also change Y plot................
        print(" ")
        print("CHANGED SAVE:", diameter_data)
        print(" ")
        
#- - - - - - Classes for Automation Levels below - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class manualSelection(MyMainWindow):
    def onClick(self,event):
        global coordinates
        global cir
        global img_arr
        global img
        cor = img_arr.mapFromScene(event.scenePos()) #maps coordinate from image pixels
        x = cor.x()
        y = cor.y()
        if len(coordinates) == 0: 
            coordinates.append((x,y))
            
        elif len(coordinates) == 1:  #Waiting for second click
            coordinates.append((x,y))
            x1 = coordinates[0][0]
            y1 = coordinates[0][1] 
            x2 = coordinates[1][0]
            y2 = coordinates[1][1]          
            d = 2*np.sqrt((x1-x2)**2 + (y1-y2)**2)   #diameter
            estimate_radius = d/2
            estimate_center = np.array([x,y])
            
            print("estimate_center:", estimate_center, "estimate_radius:", estimate_radius)
            imgg = ellipseFitting.get_image_mat(image_list[count])
            threshold = imgg.mean(axis=0).mean()*0.6
            imgg = ellipseFitting.get_binary_image_mat(image_list[count],threshold)
            ellipseFitting.show_image(imgg)
        
            ''' estimate_center and estimate_radius are defined above with 2 clicks from user '''
            
            test_estimate_center = estimate_center
            test_estimate_radius = estimate_radius
            
            test_estimate_a = test_estimate_radius
            test_estimate_b = test_estimate_radius
            
            points = ellipseFitting.find_edge_points(test_estimate_center,test_estimate_radius,imgg)
            #print(points)
            a_points = np.array(points)
            x = a_points[:, 0]
            y = a_points[:, 1]
            py.scatter(x,y)
            
            eye = ellipseFitting.fitEllipse(x,y)
            center = ellipseFitting.ellipse_center(eye)
            
            if isinstance(center[0], complex):
                center = test_estimate_center
                r = test_estimate_radius
                a = test_estimate_a
                b = test_estimate_b        
            else:
                phi = ellipseFitting.ellipse_angle_of_rotation2(eye)
                axes = ellipseFitting.ellipse_axis_length(eye)
                a, b = axes
                area = np.pi*a*b
                r = np.sqrt(a*b)
                
         
               
#Old portion of code from before - remove later.         
'''     
            
            LLC = (x1 - (d/2), (y1 - (d/2))) # lower left corner of bounding box
            cir = pg.CircleROI(LLC, [d,d], pen=(4,8)) #blue
            self.graphicsView.addItem(cir)
            self.checkBox_StoreData.setChecked(True)
'''  


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = MyMainWindow()  # Set form
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main functiond