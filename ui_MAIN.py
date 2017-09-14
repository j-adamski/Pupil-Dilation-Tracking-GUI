import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PIL import Image
import glob
import cv2
from ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import *
from uploadVideo import *
count = 0
image_list = []
frames= 0


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
   
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) 
        
#####################################################
#            Navigation code below
#####################################################


   
       
        self.L_button.clicked.connect(self.on_clickLeft)
        self.R_button.clicked.connect(self.on_clickRight)
        self.actionUpload_new.triggered.connect(self.openVidFile)
        
        
        self.horizontalSlider.sliderMoved.connect(self.sliderMoved)
        
        
        self.label.mousePressEvent = self.getPos
        
        
    @pyqtSlot()
    def on_clickLeft(self):
        global count
        if count > 0:
                count= count - 1 
                pixmap = QPixmap(image_list[count])
                self.label.setPixmap(pixmap)
                self.horizontalSlider.setSliderPosition(count)
    def on_clickRight(self):
        global count
        global image_list
        if count < len(image_list)-1:
                count = count + 1
                pixmap = QPixmap(image_list[count])
                self.label.setPixmap(pixmap)
                self.horizontalSlider.setSliderPosition(count)
    def sliderMoved(self, val):
        try:
            count = val
            pixmap = QPixmap(image_list[count])
            self.label.setPixmap(pixmap)
        except IndexError:
            print ("Error: No image at index"), val
        
    def keyPressEvent(self, event):
        global count
        global image_list
        key = event.key()
        if key == Qt.Key_A:
            if count > 0:
                count= count - 1 
                pixmap = QPixmap(image_list[count])
                self.label.setPixmap(pixmap)
                self.horizontalSlider.setSliderPosition(count)
                print ("viewing frame " + str(count))

        elif key == Qt.Key_D:
            if count < len(image_list)-1:
                count = count + 1
                pixmap = QPixmap(image_list[count])
                self.label.setPixmap(pixmap)
                self.horizontalSlider.setSliderPosition(count)
                print ("viewing frame " + str(count))

        elif key == Qt.Key_Escape:
            self.close()
            
    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y()
        print (x)
        print (y)
    
    def openVidFile(self):
        fileName = openFile()
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter the name of the folder to store frames')
        folderName = text
        splitVideo(fileName, image_list, folderName)
        for filename in glob.glob( folderName + '\\*.jpg'):
            image_list.append(filename)
            
        self.horizontalSlider.setRange(0,len(image_list)-1)
 
    
def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = MyMainWindow()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function