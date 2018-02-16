import sys, random
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image
import glob
from main import *
from PyQt5 import QtWidgets
from PyQt5 import *
from uploadVideo import *
import pyqtgraph as pg
from PIL import Image
from numpy import *
import numpy
import math
import csv

count = 1
frames= 0
image_list = [] #stores paths of all frames extracted from video
coordinates = [] #array stores coordinates during double clicks to draw ROI
diameter_data = [] #array that contains ROI diameters
for x in range(0,787):    #TO DO: add unique range based on # of image frames. Left like this for now for testing purposes
    diameter_data.append(0)
global cir #circle ROI
added = False #True if ROI object added to viewBox

Y_plot = []


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) 
        self.gv = self.graphicsView  # setting up graphics view
        self.gv.enableAutoRange('xy') # the axis will NOT automatically rescale when items are added/removed or change their shape. 
        self.L_button.clicked.connect(self.on_clickLeft) # connecting L mouse button to on_clickLeft function
        self.R_button.clicked.connect(self.on_clickRight) # connecting R mouse button to on_clickRight function
        self.actionUpload_new.triggered.connect(self.openVidFile) # connecting upload button to openVideoFile function
        self.horizontalSlider.sliderMoved.connect(self.sliderMoved) # when slider is moved, it will trigger sliderMoved function
        self.graphicsView.scene().sigMouseClicked.connect(self.onClick) # Connect onClick function to mouse click
        self.checkBox_StoreData.stateChanged.connect(self.saveData) #Connects checkbox to saveData function
        self.actionSave.triggered.connect(self.export_to_csv)
        
        
        
    @pyqtSlot()
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
        key = event.key()
        if key == Qt.Key_A:
            if count > 0:
                count= count - 1 
                self.update()

        elif key == Qt.Key_D:
            if count < len(image_list)-1:
                count = count + 1
                self.plot()
                self.update()
                            
        elif key == Qt.Key_Escape: #if ESC key is pressed, program close
            self.close()    
            
    def openVidFile(self):
        fileName = openFile() #openFile() opens file browser and returns name of selected video file
        directory = str(QFileDialog.getExistingDirectory(self, "Select Folder to Store Frames")) # File dialog opens for user to create/selet a folder to store the frames extracted from video
        splitVideo(fileName, image_list, directory) 
        
        #TO DO: instead of a given range, feed it the num of frames extracted from video. Left like this for testing purposes for now.
        #TO DO: add loading status bar while frames are being uploaded        
       
        for x in range(1, 738):
            image_list.append(directory + "/frame" + str(x) + ".jpg")
            
        self.horizontalSlider.setRange(0,len(image_list)-1)
        self.video_title.setText(fileName)

        
    def onClick(self,ev):
        global coordinates
        global cir
        global added
        global img_arr
        cor = img_arr.mapFromScene(ev.scenePos()) #maps coordinate from image pixels
        x = cor.x()
        y = cor.y()
        if len(coordinates) == 0: 
            coordinates.append((x,y))
        elif len(coordinates) == 1:
            coordinates.append((x,y))
            print(coordinates)
            x1 = coordinates[0][0]
            y1 = coordinates[0][1] 
            x2 = coordinates[1][0]
            y2 = coordinates[1][1]
            d = 2*np.sqrt((x1-x2)**2 + (y1-y2)**2)   #diameter
            LLC = (x1 - (d/2), (y1 - (d/2))) # lower left corner of bounding box
            cir = pg.CircleROI(LLC, [d,d], pen=(4,8)) #blue
            print("CIR DIAMETER:", d)
            self.gv.addItem(cir)
            added = True
            # coordinates[:] = []   #resets array - allows you to draw several circles in one session (just for testing purposes for now) 

    def saveData(self,ev):
        global added
       
        #If checkbox is checked, save the data
        if self.checkBox_StoreData.isChecked():
            if added == False:
                print("No ROI on screen.")
            else:
                d = cir.size() #function to get width and height, returned as tuple
                d = d[1] #since width = height, we just need to store one of the numbers
                diameter_data[count-1] = d
                #print(diameter_data)                   
                print("data added at count =", count)
                Y_plot.append(d)
                
        else:
            ##delete data
            diameter_data[count-1] = 0
            #print("current data in", count, "in array:", diameter_data[count])
            #print(diameter_data)
            print("data deleted at count =", count)
     
    
  
    def delROI(self, event):
        global diameter_data 
        if event.key() == Qt.Key_Delete: #if del key is pressed, ROI is removed. #STILL have to manually remove data though. #TO DO
            self.gv.removeItem(cir)
            print("del key pressed")


             
    def plot(self):
        global diameter_data
        global Y_plot
        #when calling, use self.plot
        fps = calculateFPS()
        fps_inverse = 1/fps
        frames = 787 #TO DO: automate later
        
        Xx = []  #holds the time at each frame
        for i in range(1,frames+1):
            r=i*fps_inverse
            Xx.append(r)
            
        len_y = len(Y_plot)
        X = []
        for i in range(0, len_y):
            X.append(Xx[i])
             
        pen=pg.mkPen(color='r',width=5)
        self.graphicsView_Plot.plot(X,Y_plot,pen=pen,clear=True)
        
        
    def export_to_csv(self):
        global diameter_data
        #Writing to csv file
        with open ('diameter_data.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n', delimiter=' ')
            for num in diameter_data:
                writer.writerow([num])
                
                
    def update(self):
        global img_arr
        img = Image.open(image_list[count])  #
        arr = array(img)
        arr = np.rot90(arr, -1)
        img_arr = pg.ImageItem(arr)
        self.graphicsView.addItem(img_arr)
        self.label_frameNum.setText("Frame " + str(count))
        self.horizontalSlider.setSliderPosition(count)
        if (self.checkBox_StoreData.isChecked() == True and diameter_data[count-1] == 0):
            self.checkBox_StoreData.setChecked(False)
        elif(self.checkBox_StoreData.isChecked() == False and diameter_data[count -1] != 0):
            self.checkBox_StoreData.setChecked(True) 
        print ("viewing frame " + str(count))
        print("count", count)
        print(len(diameter_data))
        
   


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = MyMainWindow()  # Set form
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main functiond