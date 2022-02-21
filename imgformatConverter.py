from PyQt5 import QtCore, uic, QtWidgets
from pathlib import Path
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QMessageBox
import sys,os
from PIL import Image, ImageFilter
import numpy as np
import cv2
import imageio


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget,self).__init__()
        self.setFixedSize(1072, 719)
        ui_file = 'C:\\Users\\matrix\\Documents\\scripts\\fileformatCoverter.ui'
        self.ui = uic.loadUi(ui_file,self)
        self.home()
        self.listExt()
        self.show()

    def home(self):
        self.gifPath = "C:\\Users\\matrix\\uiInterface\\seqImg.gif"

        self.dspl = self.ui.displayImg

        self.pBar = self.ui.progressBar
        self.pBar.reset()

        self.fpButton = self.ui.fileInButton
        self.fpButton.clicked.connect(self.showFileIn)

        self.foutpButton = self.ui.fileOutButton
        self.foutpButton.clicked.connect(self.showFileOut)

        self.fextCbox = self.ui.imgExtDispayComboBox
        self.fextCbox.currentIndexChanged.connect(self.getValExt)

        self.makeAnimGifButton = self.ui.animGifButton
        self.makeAnimGifButton.clicked.connect(self.runMakeAnimatedGif)

        self.execButton = self.ui.changFileFormatButton
        self.execButton.clicked.connect(self.fileFormatChange)

        self.covertExrButton = self.ui.exrToPngButton
        self.covertExrButton.clicked.connect(self.convert_exr_png)
        

        self.labelAnim = self.ui.labelAnimGif
        self.gif = QMovie(self.gifPath)
        self.labelAnim.setMovie(self.gif)
        self.gif.start()
        self.showError()

    def showUsageDefaults(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Default Usage : ", "can convert gif,bmp,ico,png,sgi formats from one format to another , select image input -> select extension -> select output -> change image format ")  

    def showspecialCaseUsage(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Default Usage : ", "to convert from exr to png , select image input -> select extension as exr -> select output -> exr to png button")           

    def convert_exr_png(self):
        try:
            self.pBar.reset()
            self.imgSeqInExr = self.fileSeqIn()
            self.outPng = ""    
            self.inExr = ""
            self.dspl = self.ui.displayImg

            count = len(self.imgSeqInExr)-1
            i = 0
            self.pBar.setMaximum(count)

            for imgNum in range(len(self.imgSeqInExr)):
                self.pBar.setValue(i)
                self.outPng = self.ExtReplacedFiles(self.imgSeqInExr[imgNum])
                self.fileNamePng, self.fileExtensionPng = os.path.splitext(self.outPng)
                self.outPng = self.fileNamePng+"."+"png"

                im=cv2.imread(self.imgSeqInExr[imgNum],-1)
                im=im*65535
                im[im>65535]=65535
                im=np.uint16(im)
                cv2.imwrite(self.outPng,im)
                self.gamma_correct(self.outPng)
                i = i + 1
                self.imgseq = QMovie(self.outPng)
                self.dspl.setMovie(self.imgseq)
                self.dspl.setScaledContents(True)    
                self.imgseq.start()  
            self.listDirListOut(os.path.abspath(self.dirOut))

        except:
            self.showspecialCaseUsage()


    def exrToPngMessage(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Usage -> :", " select input direcory -> select exr image format -> select output directory -> press exr to Png Button ") 

    def endOfProcess():
        self.mb = QMessageBox()
        self.mb.about(self, "Task Complete", " exr images converted and written our here -> %s"%self.dirOut) 

    def gamma_correct(self,pngRead):
        im = np.array(Image.open(pngRead), 'f')
        im_1_22 = 255.0 * (im / 255.0)**(1 / 2.2)
        im_22 = 255.0 * (im / 255.0)**2.2
        im_gamma = np.concatenate((im_1_22, im, im_22), axis=1)
        pil_img = Image.fromarray(np.uint8(im_1_22))
        pil_img.save(self.outPng)    

    def make_animatedgif(self):
        self.pBar.reset()
        i = 0
        self.dspl.setStyleSheet("*{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 0));}") 
        self.images = []
        self.imgSeqIn = self.fileSeqIn()
        count = len(self.imgSeqIn)-1
        self.pBar.setMaximum(count)
        for imgNum in range(len(self.imgSeqIn)):
            self.pBar.setValue(i)
            self.im = Image.open(self.imgSeqIn[imgNum])
            self.images.append(self.im)
            i = i + 1
        return self.images    
           
    def runMakeAnimatedGif(self):
        try:
            images = self.make_animatedgif()
            self.outAnim = self.dirOut
            self.im.save(self.outAnim+"\\out.gif",  save_all=True, append_images=images[1:], duration=40, loop=0)
            self.listDirListOut(os.path.abspath(self.dirOut)) 
            self.gifseq = QMovie(self.outAnim+"\\out.gif")
            self.dspl.setMovie(self.gifseq)
            self.dspl.setScaledContents(True)
            self.gifseq.start()

        except:
            self.animGifError()   

    def animGifError(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Usage:", " select input direcory -> select Gif image format -> select output directory -> press make animated gif Button")        
         

    def ExtReplacedFiles(self,fileP):
        self.fileInP = fileP
        self.fileOutP = self.dirOut
        self.fileName, self.fileExtension = os.path.splitext(self.fileInP)
        self.splitPth = self.fileName.split("\\")
        self.stripFileName = self.splitPth[len(self.splitPth)-1]
        self.fileOutExtension = self.getValExt()

        self.reconstructNewFileName = ""
        self.reconstructNewFileName = os.path.abspath(self.fileOutP)+"\\"+self.stripFileName+"."+self.fileOutExtension
#       print("filePath to the extension replaced imagefile -> %s  "%self.reconstructNewFileName)
        return self.reconstructNewFileName   


    def showError(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Usage:for converting image formats", " select input direcory -> select image format to change -> select output directory -> press change image format Button ") 

    def fileFormatChange(self):
#       try:
        self.pBar.reset()
        i = 0
        self.valIn = self.fileSeqIn()
        count = len(self.valIn)-1
        self.pBar.setMaximum(count)
        self.dspl.setStyleSheet("*{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 0));}")
        for imgNum in range(len(self.valIn)):
            self.pBar.setValue(i)
            self.fileIn = self.valIn[imgNum] 
            if self.getValExt() == "jpg":
                self.im = Image.open(self.valIn[imgNum]).convert("RGB")
            else:            
                self.im = Image.open(self.valIn[imgNum])
            self.replacedFile = self.ExtReplacedFiles(self.valIn[imgNum])
            self.im.save(self.fileIn.replace(self.valIn[imgNum], self.replacedFile))
            i = i + 1
            self.imgseq = QMovie(self.replacedFile)
            self.dspl.setMovie(self.imgseq)
            self.dspl.setScaledContents(True)
            self.imgseq.start()
#               self.pixmap = QPixmap(self.replacedFile)
#               self.dspl.setPixmap(self.pixmap)
#               self.dspl.setScaledContents(True)
#               self.setCentralWidget(label)
#               self.resize(pixmap.width(), pixmap.height())
        
        self.listDirListOut(os.path.abspath(self.dirOut)) 

#       except:
#           self.showUsageDefaults()
 

    def listDirList(self,getDir):
        self.listD=[]
        self.dirName = str(getDir)
        root = self.dirName
        iterable = os.walk(root)
        d,dirlist,files = next(iterable)   # throw away first iteration
        for file_ in files:
            self.listD.append(str(file_))
        self.populateDirCbox(self.listD)

    def listDirListOut(self,getDir):
        self.listD=[]
        self.dirName = str(getDir)
        root = self.dirName
        iterable = os.walk(root)
        d,dirlist,files = next(iterable)   # throw away first iteration
        for file_ in files:
            self.listD.append(str(file_))
        self.populateInDirCbox(self.listD)        

    def listExt(self):
        self.listE=[]
        self.listE = ["gif","bmp","ico","png","sgi","exr","jpg","tiff"]
        self.populateExtCbox(self.listE)        

    def showFileIn(self):
        self.pBar.reset()
        self.selectedInDirPath = ""
        qDir = QtWidgets.QFileDialog
        self.dirIn = qDir.getExistingDirectory(self,"Open Directory",str(Path.home()))

        if self.dirIn:
            self.selectedInDirPath = str(os.path.abspath(self.dirIn))
            print(self.selectedInDirPath)
            self.listDirList(os.path.abspath(self.selectedInDirPath))
            return self.dirIn    
            
    def showFileOut(self):
        self.pBar.reset()
        self.selectedOutDirPath = ""
        qDir = QtWidgets.QFileDialog
        self.dirOut = qDir.getExistingDirectory(self,"Open Directory",str(Path.home()))

        if self.dirOut:
            self.selectedOutDirPath = str(os.path.abspath(self.dirOut))
            self.listDirListOut(os.path.abspath(self.selectedOutDirPath))
            return self.dirOut           

    def fileSeqIn(self):
        self.inFileFullPath = []
        self.pBar.reset()
        Path = os.path.abspath(self.dirIn)     
        files = os.listdir(os.path.abspath(self.dirIn))
        count = len(files)-1
        i = 0
        self.pBar.setMaximum(count)
        for file in files:
            self.pBar.setValue(i)
            self.inFileFullPath.append(os.path.abspath(os.path.join(Path, file)))
            i = i + 1
        return self.inFileFullPath    

    def fileSeqOut(self):
        self.dirOutFilePath = ""
        self.dirOutFilePath = self.dirOut
        return self.dirOutFilePath
        
    def showIcoSizeDialog(self):
        pNum, ok = QtWidgets.QInputDialog.getText(self, 'Input Padding Dialog', 'Enter size ex:0 for 16 , 1 for 32')
        if ok:
            self.pNum = pNum
            return self.pNum                  

    def populateDirCbox(self,getList):
        self.fCbox = self.ui.imgFileDispayComboBox
        self.fCbox.clear()
        self.dirList = getList
        text = ""
        for text in self.dirList:
            self.fCbox.addItem(text)

    def populateInDirCbox(self,getList):
            self.fCobox = self.ui.imgOutDispayComboBox
            self.fCobox.clear()
            self.dirList = getList
            text = ""
            for text in self.dirList:
                self.fCobox.addItem(text)
            

    def onValChanged(self, text):
        self.text = text
        return self.text

    def populateExtCbox(self,getExtList):
        self.fextCbox = self.ui.imgExtDispayComboBox
        self.fextCbox.clear()
        self.extList = getExtList
        textExt = ""
        for textExt in self.extList:
            self.fextCbox.addItem(textExt)

    def getValExt(self):
        self.extTextVal = self.fextCbox.currentText()
        return self.extTextVal            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.setWindowTitle(" Image format converter ")
    app.exec()

"""
import numpy as np
import cv2
im=cv2.imread("torus.exr",-1)
im=im*65535
im[im>65535]=65535
im=np.uint16(im)
cv2.imwrite("torus.png",im)

import sys, os
import imageio

def convert_exr_to_jpg(exr_file, jpg_file):
    if not os.path.isfile(exr_file):
        return False

    filename, extension = os.path.splitext(exr_file)
    if not extension.lower().endswith('.exr'):
        return False

    # imageio.plugins.freeimage.download() #DOWNLOAD IT
    image = imageio.imread(exr_file)
    print(image.dtype)

    # remove alpha channel for jpg conversion
    image = image[:,:,:3]


    data = 65535 * image
    data[data>65535]=65535
    rgb_image = data.astype('uint16')
    print(rgb_image.dtype)
    #rgb_image = imageio.core.image_as_uint(rgb_image, bitdepth=16)

    imageio.imwrite(jpg_file, rgb_image, format='jpeg')
    return True


if __name__ == '__main__':
    exr = "torus.exr"
    jpg = "torus3.jpeg"
    convert_exr_to_jpg(exr, jpg)


im = imageio.imread("image.exr")
im_gamma_correct = numpy.clip(numpy.power(im, 0.45), 0, 1)
im_fixed = Image.fromarray(numpy.uint8(im_gamma_correct*255))

"""









