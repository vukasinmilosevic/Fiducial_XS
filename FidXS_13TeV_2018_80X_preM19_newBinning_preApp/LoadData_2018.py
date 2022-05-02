from ROOT import *
from array import array
import os
from datapaths_full import *
dirMC_94 = datapaths["2018"]["MC"]

print "samples directory: ", dirMC_94


SamplesMC_94 = [
###
'GluGluHToZZTo4L_M124_2018_slimmed.root',
'GluGluHToZZTo4L_M125_2018_slimmed.root',
'GluGluHToZZTo4L_M126_2018_slimmed.root',
'VBF_HToZZTo4L_M125_2018_slimmed.root',
'WH_HToZZTo4L_M125_2018_slimmed.root', 
'ZH_HToZZ_4LFilter_M125_2018_slimmed.root',
'ttH_HToZZ_4LFilter_M125_2018_slimmed.root',
'ggH_amcatnloFXFX_2018_slimmed.root',
'testGGH_nnlops_GENonly_slimmed.root',
]

SamplesData_94 = [
'DoubleEG_Run2017B-17Nov2017-v1.root','DoubleEG_Run2017C-17Nov2017-v1.root','DoubleEG_Run2017D-17Nov2017-v1.root','DoubleEG_Run2017E-17Nov2017-v1.root','DoubleEG_Run2017F-17Nov2017-v1.root',
'DoubleMuon_Run2017-17Nov2017-v1.root','DoubleMuon_Run2017B-17Nov2017-v1.root','DoubleMuon_Run2017C-17Nov2017-v1.root'
]


RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}

for i in range(0,len(SamplesMC_94)):

    sample = SamplesMC_94[i].rstrip('.root')


    if ("NNLOPS" in sample):
        RootFile[sample] = TFile(dirMC_94_1+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    elif ("ggH_amcatnloFXFX" in sample):
        RootFile[sample] = TFile(dirMC_94+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    else: 
        RootFile[sample] = TFile.Open(dirMC_94+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("Ana/nEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    if (h_nevents): nEvents[sample] = h_nevents.Integral()
    else: nEvents[sample] = 0.

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]

for i in range(0,len(SamplesData_94)):
    break
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
