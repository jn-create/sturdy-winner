import hou

from PySide2 import QtCore, QtUiTools, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget,self).__init__()
        ui_file = 'C:\Users\matrix\uiInterface\ui_d.ui'
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.node = hou.node("/stage")
        self.home()
        self.stageLightColorValues()
        
    def home(self):
        self.list = self.getChildren(self)
        
        for text in self.list:
            self.ui.comboBox.addItem(text)
            
        self.ui.comboBox.activated[str].connect(self.onValChanged)
        self.lcdDisplay = self.ui.lcd
        self.progress = self.ui.progressBar 
        self.ui.pushButton.clicked.connect(self.activate)
        
        
    def onValChanged(self, text):
        self.text = text
        return self.text

 
    def activate(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
            self.lcdDisplay = self.ui.lcd.display(self.completed)
 
    def getChildren(self,listM):
        self.listM = []
        od = self.node.children()
        lenod = len(od)
        for nd in range(lenod):
            self.listM.append(str(od[nd]))

        return self.listM


    def lightNodePaths(self,lightPaths):
        lightName = str(self.rtcb())
        lightnode = str(self.node) + "/" +str(lightName)
        rColor = lightnode + "/" + "colorr"
        gColor = lightnode + "/" + "colorg"
        bColor = lightnode + "/" + "colorb"

    
        self.lightPaths = [lightName, lightnode, rColor, gColor, bColor]
#       print self.lightPaths[2]
        return self.lightPaths

    def stageLightColorValues(self):

        lightNPaths = self.lightNodePaths(self)
        self.lightName = lightNPaths[0]
        self.lightnode = lightNPaths[1]
        self.rColoPath = lightNPaths[2]
           
        if hou.node(self.lightnode).type().name() == "light" or hou.node(self.lightnode).type().name() == "domelight":
            print ("light node selected  %s"%self.lightName)
            self.redDial = self.ui.rDial
            self.redDial.valueChanged.connect(self.dValChng)
            self.greenDial = self.ui.gDial
            self.greenDial.valueChanged.connect(self.dValChng)
            self.blueDial = self.ui.bDial
            self.blueDial.valueChanged.connect(self.dValChng)

        else:
            print "not a light"
            
    def dValChng(self,rVal):
        lightNPaths = self.lightNodePaths(self)
        self.lightName = lightNPaths[0]
        self.lightnode = lightNPaths[1]
        self.rColoPath = lightNPaths[2]
        self.gColoPath = lightNPaths[3]
        self.bColoPath = lightNPaths[4]


        if hou.node(self.lightnode).type().name() == "light" or hou.node(self.lightnode).type().name() == "domelight":
            self.rVal = self.redDial.value()
            hou.parm(self.rColoPath).set(float(self.rVal))

            self.gVal = self.greenDial.value()
            hou.parm(self.gColoPath).set(float(self.gVal))

            self.bVal = self.blueDial.value()
            hou.parm(self.bColoPath).set(float(self.bVal))

#           print "Red color value selected is : %s"%self.rVal
        else:
            print "not a light"    
  

    def rtcb(self):    
        curntTextVal = self.ui.comboBox.currentText()
        return str(curntTextVal)   


                
    
def showWinMyWidget():
    win = MyWidget()
    win.setWindowTitle("stageLightColorSet")
    win.show()


showWinMyWidget()
