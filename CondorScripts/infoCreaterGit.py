import os

class BasicInfoCreater():
    """docstring for BasicInfoCreater"""

    GITPATCH = 'gitDiff.patch'

    def __init__(self, logFileName="summary.dat", optionalString=""):
        self.CMSSWDirPath = os.environ['CMSSW_BASE']
        self.CMSSWRel = self.CMSSWDirPath.split("/")[-1]
        self.logFileName = logFileName
        self.optionalString = optionalString

    def GenerateGitLog(self):
        outScript = open(self.logFileName,"w");
        outScript.write('CMSSW Version used: ',self.CMSSWRel)
        outScript.write('Current directory path: ',self.CMSSWDirPath)
        outScript.write('Summary for current setup: ',self.optionalString)
        outScript.close()

        os.system('echo -e "\n\n============\n== Latest commit summary \n\n" >> '+self.logFileName )
        os.system("git log -1 --pretty=tformat:' Commit: %h %n Date: %ad %n Relative time: %ar %n Commit Message: %s' >> "+self.logFileName )
        os.system('echo -e "\n\n============\n" >> '+self.logFileName )
        os.system('git log -1 --format="%H" >> '+self.logFileName )

    def GenerateGitPatch(self):
        os.system('git diff > '+self.GITPATCH)
        
    def GenerateGitPatchAndLog(self):
        os.system('git diff > '+self.GITPATCH)

        outScript = open(self.logFileName,"w");
        outScript.write('\nCMSSW Version used: '+self.CMSSWRel+'\n')
        outScript.write('\nCurrent directory path: '+self.CMSSWDirPath+'\n')
        outScript.write('\nSummary for current setup: '+self.optionalString+'\n')
        outScript.close()

        os.system('echo -e "\n\n============\n== Latest commit summary \n\n" >> '+self.logFileName )
        os.system("git log -1 --pretty=tformat:' Commit: %h %n Date: %ad %n Relative time: %ar %n Commit Message: %s' >> "+self.logFileName )
        os.system('echo -e "\n\n============\n" >> '+self.logFileName )
        os.system('git log -1 --format="SHA: %H" >> '+self.logFileName )

    def SendGitLogAndPatchToEos(self, outputFolder):
        print "\ncopying "+self.logFileName+" to path: "+outputFolder
        os.system('xrdcp -f ' + self.logFileName + ' root://cmseos.fnal.gov/' + outputFolder + os.sep + self.logFileName)
        print "\ncopying "+self.GITPATCH+" to path: "+outputFolder
        os.system('xrdcp -f ' + self.GITPATCH + ' root://cmseos.fnal.gov/' + outputFolder + os.sep + self.GITPATCH)
        # print "\n\n"