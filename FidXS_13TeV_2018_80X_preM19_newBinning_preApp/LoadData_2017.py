from ROOT import *
from array import array
import os
from datapaths_full import *

dirMC_94= datapaths["2017"]["MC"]
dirMC_94_1 = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'


#SamplesData_80 = [
#'Data_2016_4lskim.root'
#]

SamplesMC_94 = [
'GluGluHToZZTo4L_M124_2017_newMuonSF_all_slimmed.root',
'GluGluHToZZTo4L_M125_2017_newMuonSF_slimmed.root',
'GluGluHToZZTo4L_M126_2017_newMuonSF_all_slimmed.root',
'VBF_HToZZTo4L_M125_2017_newMuonSF_slimmed.root',
'WH_HToZZTo4L_M125_2017_newMuonSF_slimmed.root',
'ZH_HToZZ_4LFilter_M125_2017_newMuonSF_slimmed.root',
'ttH_HToZZ_4LFilter_M125_2017_newMuonSF_slimmed.root',
]

SamplesData_94 = [
#'DoubleEG_Run2017B-17Nov2017-v1.root','DoubleEG_Run2017C-17Nov2017-v1.root','DoubleEG_Run2017D-17Nov2017-v1.root','DoubleEG_Run2017E-17Nov2017-v1.root','DoubleEG_Run2017F-17Nov2017-v1.root',
#'DoubleMuon_Run2017-17Nov2017-v1.root','DoubleMuon_Run2017B-17Nov2017-v1.root','DoubleMuon_Run2017C-17Nov2017-v1.root'
]
###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}


# 80X MC
for i in range(0,len(SamplesMC_94)):

#    sample = SamplesMC_80[i].rstrip('.root')

    sample = SamplesMC_94[i].rstrip('.root')
#    sample = SamplesMC_94[i].replace('.root','')

#    RootFile[sample] = TFile(dirMC_94+'/'+sample+'.root',"READ")
#ROOT.TFile.Open("root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/blah.root")
##    if ("NNLOPS" in processBin):

    #if ("NNLOPS" in sample):
    if ("nnlops" in sample or "amcatnloFXFX" in sample):
        RootFile[sample] = TFile(dirMC_94_1+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
#    elif ("M124" in sample  or "M126" in sample): 
#        RootFile[sample] = TFile.Open(dirMC_94_2+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    else: 
        RootFile[sample] = TFile.Open(dirMC_94+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("Ana/passedEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    if (h_nevents): nEvents[sample] = h_nevents.GetEntries() #Integral()
    else: nEvents[sample] = 0.

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]

for i in range(0,len(SamplesData_94)):

    sample = SamplesData_94[i].rstrip('.root')

    RootFile[sample] = TFile(dirData_94+'/'+sample+'.root',"READ")

    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("nEvents")
    h_sumw = RootFile[sample].Get("sumWeights")

    if (h_nevents):
        nEvents[sample] = h_nevents.Integral()
        sumw[sample] = h_sumw.Integral()
    else:
        nEvents[sample] = 0.
        sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]
    
