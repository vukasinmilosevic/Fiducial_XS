import os
import sys
import argparse

import makeTarFile

# create tarball of present working CMSSW base directory
os.system('rm -f CMSSW*.tgz')

storeDir = "/eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/"

# Get CMSSW directory path and name
cmsswDirPath = os.environ['CMSSW_BASE']
CMSSWRel = cmsswDirPath.split("/")[-1]
makeTarFile.make_tarfile(cmsswDirPath, CMSSWRel + ".tgz")
print "copying the " + CMSSWRel + ".tgz  file to eos path: " + storeDir + "\n"
os.system('cp ' + CMSSWRel + ".tgz" + ' ' + storeDir + '/' + CMSSWRel + ".tgz")

