'''
Simple and Useful folder maker , which creates seqential and arbitary folders
'''
from distutils.log import error
import os
from functools import partial
import argparse
import sys


parser = argparse.ArgumentParser(prog='Folders maker',usage='%(prog)s [Makes folders with ordered and arbitary names]')
parser.add_argument("-help", default=False, action="store_true")
args = parser.parse_args()

  
class folderMaker():
    def __init__(self,mainFolderStr=os.path.join("C:/App"),nameOfFolderPrefix="prefix",nameOfFolderSufix="sufix",startCount=0,endCount=10,*folderNumbers):
        self.mainFolderStr = mainFolderStr
        self.nameOfFolderPrefix = nameOfFolderPrefix
        self.nameOfFolderSufix = nameOfFolderSufix
        self.startCount = startCount
        self.endCount = endCount
        self.folderNumbers = folderNumbers
        self.numberOfFolders = self.endCount - self.startCount
        acceptInput = [str(self.mainFolderStr),str(self.nameOfFolderPrefix),str(self.nameOfFolderSufix),int(self.startCount),int(self.endCount)]
        self.basePathToFolder = str(acceptInput[0]+"/"+str(self.nameOfFolderPrefix))
        
          
    def runFolderMaker(self):
        if not all(self.folderNumbers):
            for nFolder in range(self.numberOfFolders):
                fullPath = os.path.join(self.basePathToFolder+str(nFolder+1)+"_"+self.nameOfFolderSufix)
                os.makedirs(fullPath)
            print("folders created at: {}".format(self.mainFolderStr))    
            sys.exit(1)

        arbitaryFolders = self.folderNumbers
        if(self.startCount == 0 and self.endCount == 0):
            for nFolder in range(len(arbitaryFolders)):
                fullPath = os.path.join(self.basePathToFolder+str(arbitaryFolders[nFolder])+"_"+self.nameOfFolderSufix)
                os.makedirs(fullPath)
            print("folders created at: {}".format(self.mainFolderStr))    
            sys.exit(1)         

    #@dispatch(str,str,list)
    def makeFolders(self):
        print("Usage: fill in the baseFolder path,SuffixFolderName,PrefixFolderName,"
        "SequentialFolders_Startnumber,SequentialFolders_Endnumber\n,if its Sequential add a 0 at the end 0")
        print("______________________________________________________________________________________________")
        print("Usage: fill in the baseFolder path,SuffixFolderName,PrefixFolderName,"
        "0,0,\nif its Arbitary Folders add the folder numbers separated by commas at the end")
        print("______________________________________________________________________________________________")
        print("C to continue")

        waitForInput = input()
        if(waitForInput=="C"):
            if not os.path.isdir(self.basePathToFolder):
                self.runFolderMaker()
            else:
                print("Folders {} already exist".format(self.mainFolderStr))

        else:
            sys.exit(0)        
        
if __name__ == '__main__':
    newFolder = folderMaker("Drive/BaseFolder/FolderName","ShotNamePrefix","ShotNameSuufix",0,10,0,0,0)
    newFolder.makeFolders()

        

