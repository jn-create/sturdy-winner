from distutils.log import error
import os
from functools import partial
import argparse
import sys


parser = argparse.ArgumentParser(prog='Folders maker',usage='%(prog)s [Makes folders with ordered and arbitary names]')
parser.add_argument("-help", default=False, action="store_true")
args = parser.parse_args()

  
class folderMaker():
    def __init__(self,mainFolderStr=os.path.join("C:/App"),nameOfFolder="default",startCount=0,endCount=10,*folderNumbers):
        self.mainFolderStr = mainFolderStr
        self.nameOfFolder = nameOfFolder
        self.startCount = startCount
        self.endCount = endCount
        self.folderNumbers = folderNumbers
        self.numberOfFolders = self.endCount - self.startCount
        acceptInput = [str(self.mainFolderStr),str(self.nameOfFolder),int(self.startCount),int(self.endCount)]
        self.basePathToFolder = str(acceptInput[0])+"/"+str(acceptInput[1])

          
    def waitForUserInput(self):
        inputStatus = input()
        if(inputStatus==input()=='Y'):
            return inputStatus
        if(inputStatus==input()=='N'):
            sys.exit(1)
        if not (inputStatus==input()=='Y' or inputStatus==input()=='N'):
            print('Input needs to be Y or N')
            sys.exit(1)

    def runFolderMaker(self):
        if not all(self.folderNumbers):
            for nFolder in range(self.numberOfFolders):
                fullPath = os.path.join(self.basePathToFolder+"_"+str(nFolder+1))
                os.makedirs(fullPath)
            print("folders created at: {}".format(self.basePathToFolder))    
            sys.exit(1)

        arbitaryFolders = self.folderNumbers
        if(self.startCount == 0 and self.endCount == 0):
            for nFolder in range(len(arbitaryFolders)):
                fullPath = os.path.join(self.basePathToFolder+"_"+str(arbitaryFolders[nFolder]))
                os.makedirs(fullPath)
            print("folders created at: {}".format(self.basePathToFolder))    
            sys.exit(1)         

    #@dispatch(str,str,int,int)
    def makeSequentialFolders(self):
        self.folderNumbers = [0]
        if self.startCount == 0:
            print("start value shoul be 1 and above")
            exit(1)
        else:    
            self.numberOfFolders += 1

        if not os.path.isdir(self.basePathToFolder):
            #inputStatus = self.waitForUserInput()
            #if inputStatus=='Y':
            self.runFolderMaker()
        else:
            print("Folders {} already exist".format(self.basePathToFolder))
            sys.exit(1)
            
        
    #@dispatch(str,str,list)
    def makeArbitaryFolders(self):
        if not os.path.isdir(self.basePathToFolder):
            #inputStatus = self.waitForUserInput()
            #if inputStatus=='Y':
            self.runFolderMaker()
        else:
            print("Folders {} already exist".format(self.basePathToFolder))
              

if __name__ == '__main__':
    newFolder = folderMaker("/Folder","Py",0,0,8)
    #newFolder.makeSequentialFolders()
    newFolder.makeArbitaryFolders()

        

