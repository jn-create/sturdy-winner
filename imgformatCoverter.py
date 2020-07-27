from PyQt5 import QtCore, uic, QtWidgets
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
import sys,os
from PIL import Image, ImageFilter
import sys,os,pathlib

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget,self).__init__()
        ui_file = ' path to ui file '
        self.ui = uic.loadUi(ui_file,self)
        self.home()
        self.listExt()
        self.show()

    def home(self):
        self.gifPath = "path to animated gif"
        self.hLabelPath = 'path to hlabel animated gif'
        self.cnLabelPath = 'path to cn label animated gif'
        self.pdLabelPath = 'path to pd label anumated gif'

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

        self.labelAnim = self.ui.animatedGifLabel
        self.gif = QMovie(self.gifPath)
        self.labelAnim.setMovie(self.gif)
        self.gif.start()

        self.showError()

    def make_animatedgif(self): 
        self.images = []
        self.imgSeqIn = self.fileSeqIn()
        for imgNum in range(len(self.imgSeqIn)):
            self.im = Image.open(self.imgSeqIn[imgNum])
            self.images.append(self.im)
        return self.images    
           
    def runMakeAnimatedGif(self):
        try:
            images = self.make_animatedgif()
            self.outAnim = self.dirOut
            self.im.save(self.outAnim+"\\out.gif", save_all=True, append_images=images[1:], duration=10, loop=0)
        except:
            self.animGifError()   

    def animGifError(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Usage:", " select input direcory -> select Gif image format -> select output directory -> press make animated gif ")        
         

    def ExtReplacedFiles(self,fileP):
        self.fileInP = fileP
        self.fileOutP = self.dirOut
        self.fileName, self.fileExtension = os.path.splitext(self.fileInP)
        self.splitPth = self.fileName.split("\\")
        self.stripFileName = self.splitPth[len(self.splitPth)-1]

        self.fileOutExtension = self.getValExt()

        self.reconstructNewFileName = ""
        self.reconstructNewFileName = os.path.abspath(self.fileOutP)+"\\"+self.stripFileName+"."+self.fileOutExtension
        print("filePath to the extension replaced imagefile -> %s  "%self.reconstructNewFileName)
        return self.reconstructNewFileName   


    def showError(self):
        self.mb = QMessageBox()
        self.mb.about(self, "Usage:for converting image formats", " select input direcory -> select image format to change -> select output directory -> press change image format ") 

    def fileFormatChange(self):
        try:
            self.valIn = self.fileSeqIn()
            for imgNum in range(len(self.valIn)):
                self.fileIn = self.valIn[imgNum] 
                self.im = Image.open(self.valIn[imgNum])
                self.replacedFile = self.ExtReplacedFiles(self.valIn[imgNum])
                self.im.save(self.fileIn.replace(self.valIn[imgNum], self.replacedFile))

            self.listDirList(os.path.abspath(self.dirOut)) 

        except:
            self.showError()    

    def listDirList(self,getDir):
        self.listD=[]
        self.dirName = str(getDir)
        root = self.dirName
        iterable = os.walk(root)
        d,dirlist,files = next(iterable)   # throw away first iteration
        for file_ in files:
            self.listD.append(str(file_))
        self.populateDirCbox(self.listD)

    def listExt(self):
        self.listE=[]
        self.listE = ["gif","bmp","ico","png","sgi"]
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
            self.listDirList(os.path.abspath(self.selectedOutDirPath))
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
            i += 1
            self.inFileFullPath.append(os.path.abspath(os.path.join(Path, file)))

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
