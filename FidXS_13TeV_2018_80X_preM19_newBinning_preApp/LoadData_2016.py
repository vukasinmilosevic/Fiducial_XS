from ROOT import *
from array import array
import os
from datapaths_full import *

dirMC_80 = datapaths["2016"]["MC"] 
print "the sample directory is : ", dirMC_80

dirMC_80_1 = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'

dirData_80 = '/eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/legacy_2016/'
SamplesMC_80 = [
'GluGluHToZZTo4L_M124_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M126_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M130_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'WH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUGenV709_pythia8_slimmed.root',
'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUGenV709_pythia8_slimmed.root',
'ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
#'testGGH_nnlops_GENonly_slimmed.root',
#'ggH_amcatnloFXFX_2018_slimmed.root'
]

SamplesData_80 = [
'data_legacy2016_17Jul2018_noDuplicates.root'
#'Data_Run2016-03Feb2017_noDuplicates.root'
]


###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}


# 80X MC
for i in range(0,len(SamplesMC_80)):

    #sample = SamplesMC_80[i].rstrip('.root')
    sample = SamplesMC_80[i].replace('.root','')
    print "sample is", sample
    if ("nnlops" in sample or "amcatnloFXFX" in sample):
        RootFile[sample] = TFile.Open(dirMC_80_1+'/'+sample+'.root',"READ")
    else:
        RootFile[sample] = TFile.Open(dirMC_80+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    if (not Tree[sample]): Tree[sample] = RootFile[sample].Get("passedEvents")

    h_nevents = RootFile[sample].Get("Ana/passedEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    #if (h_nevents): nEvents[sample] = h_nevents.Integral()
    if (h_nevents): nEvents[sample] = h_nevents.GetEntries() #Integral()

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]



for i in range(0,len(SamplesData_80)):

    sample = SamplesData_80[i].rstrip('.root')

    RootFile[sample] = TFile.Open(dirData_80+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("passedEvents")

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
    
