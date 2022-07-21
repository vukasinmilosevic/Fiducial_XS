import ROOT
import sys, os, pwd
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *
import json
from collections import OrderedDict as od
from collections import defaultdict
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#os.system("Xvfb :1 -screen 0 720x720x16 &")
#os.environ['DISPLAY']=":1.0"

#import Tkinter 

#import matplotlib as mpl
#if os.environ.get('DISPLAY','') == '':
#    print('no display found. Using non-interactive Agg backend')
#    mpl.use('Agg')


#import matplotlib
#matplotlib.use('Agg')



#sys.path.append('../inputs/')
from higgs_xsbr_13TeV import *

def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--asimovModelName',dest='ASIMOVMODEL',type='string',default='SM_125', help='Name of the Asimov Model')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.0', help='Asimov Mass')
    parser.add_option('',   '--ModelNames',dest='MODELNAMES',type='string',default='SM_125',help='Names of models for unfolding, separated by | . Default is "SM_125"')
    parser.add_option('',   '--theoryMass',dest='THEORYMASS',    type='string',default='125.38',   help='Mass value for theory prediction')
    parser.add_option('',   '--fixMass',  dest='FIXMASS',  type='string',default='125.0',   help='Fix mass, default is a string "125.09" or can be changed to another string, e.g."125.6" or "False"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='pT4l',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='|0|10|20|30|45|60|80|120|200|13000|',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Year -> 2016 or 2017 or 2018 or Full')
    parser.add_option('',   '--ZZfloating',action='store_true', dest='ZZ',default=False, help='Let ZZ normalisation to float')
    # Unblind option
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    # Calculate Systematic Uncertainties
    # parser.add_option('',   '--calcSys', action='store_true', dest='SYS', default=False, help='Calculate Systematic Uncertainties (in addition to stat+sys)')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
parseOptions()

# Define function for processing of os command
def processCmd(cmd, quiet = 0):
    output = '\n'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        # print line,
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))
    return output

def PlotCorrelation():
    for physicalModel in PhysicalModels:
        pois = []
        pois_plot = []
        if 'mass4l' in obsName and physicalModel == 'v2':
            pois = ['r4muBin0', 'r4eBin0', 'r2e2muBin0']
            pois_plot += ['$\sigma_{4\mu}$', '$\sigma_{4e}$', '$\sigma_{2e2\mu}$']
        # elif (obsName == 'massZ1' or obsName == 'massZ2' or obsName == 'costhetastar' or obsName == 'D0m' or obsName == 'Dint' or obsName == 'Dcp' or obsName == 'DL1' or obsName == 'DL1') and physicalModel == 'v4':
        elif physicalModel == 'v4':
            for obsBin in range(nBins):
                pois += ['r4lBin'+str(obsBin)]
                pois_plot += ['$\sigma_{4e+4\mu,'+str(obsBin)+'}$']
            for obsBin in range(nBins):
                pois += ['r2e2muBin'+str(obsBin)]
                pois_plot += ['$\sigma_{2e2\mu,'+str(obsBin)+'}$']
        else:
            # pois += ['CMS_eff_e']
            # pois_plot += ['eff_e']


#            _obsName = {'pT4l': 'PTH', 'rapidity4l': 'YH', 'pTj1': 'PTJET', 'njets_pt30_eta4p7': 'NJ'} # TJ
#            if obsName not in _obsName:
#                _obsName[obsName] = obsName
            for obsBin in range(nBins):
                pois += ['SigmaBin'+str(obsBin)]
                #pois_plot += ['r_'+str(obsBin)]
                pois_plot += ['r_'+str(obsBin)]
		#pois_plot += ['$\sigma_{4\mu}$', 'ZZ', '$\sigma_{4e}$', '$\sigma_{2e2\mu}$']
        if obsName == 'mass4l_zzfloating':
            if physicalModel == 'v3':
                pois += ['zz_norm_0']
                pois_plot += ['ZZ']
            else:
                pois = ['r4muBin0', 'zz_norm_0', 'r4eBin0', 'r2e2muBin0']
                pois_plot = ['$\sigma_{4\mu}$', 'ZZ', '$\sigma_{4e}$', '$\sigma_{2e2\mu}$']

        pars = od()
        modes = od()

        #inFile    = ROOT.TFile('../combine_files/robustHesse_'+obsName+'_'+physicalModel+'.root','READ')

				#robustHesse_pT4l_v3.root
        inFile    = ROOT.TFile('robustHesse_'+obsName+'_'+physicalModel+'.root','READ')
        #inFile    = ROOT.TFile('fitDiagnostics'+obsName+'.root','READ')
        theMatrix = inFile.Get('h_correlation')
        theList   = inFile.Get('floatParsFinal')

	print "theList:  ", theList
 
        for iPar in range(len(theList)):
            print( theList[iPar].GetName() )
            if not (theList[iPar].GetName() in pois): continue
            print(iPar, theList[iPar])
            pars[theList[iPar].GetName()] = iPar

        nPars = len(pars.keys())
        print ('Procesing the following %g parameters:'%nPars)
        for par in pars.keys(): print (par)
        revPars = {i:name for name,i in pars.items()}

        # theHist = ROOT.TH2F('corr', '', nPars, -0.5, nPars-0.5, nPars, -0.5, nPars-0.5)
        theMap = {}
        for iBin,iPar in enumerate(pars.values()):
            for jBin,jPar in enumerate(pars.values()):
                proc = theMatrix.GetXaxis().GetBinLabel(iPar+1)
                theVal = theMatrix.GetBinContent(iPar+1,jPar+1)
                theMap[(revPars[iPar],revPars[jPar])] = theVal

        rows = []
        for i in pois:
            row = []
            for j in pois:
                row.append(theMap[(i,j)])
            rows.append(row)
        #for b in pois:
         #   rows.append([theMap[i] for i in theMap if i[0]==b])

        theMap = pd.DataFrame(rows, pois_plot, pois_plot)
        print(theMap)

        fig, ax = plt.subplots(figsize = (20, 10))
        #fig, ax = plt.subplots()
        ax.text(0., 1.005, r'$\bf{{CMS}}$', fontsize = 35, transform = ax.transAxes)

        ax.text(0.7, 1.005, r'138 fb$^{-1}$ (13 TeV)', fontsize = 20, transform = ax.transAxes)
        ax.text(0.63, 0.9, r'H$\rightarrow$ ZZ', fontsize = 25, transform = ax.transAxes)
        ax.text(0.55, 0.85, r'm$_{\mathrm{H}}$ = 125.38 GeV', fontsize = 25, transform = ax.transAxes)

        mask = np.zeros_like(theMap)
        mask[np.triu_indices_from(mask, k = 1)] = True


        palette = sns.diverging_palette(240, 10, n=20, as_cmap = True)

        hmap = sns.heatmap(theMap,
                mask = mask,
                vmin=-1.0, vmax=1.0,
        #         xticklabels=ticks,
        #         yticklabels=ticks,
                annot = True,
                fmt = '.2f',
                square = True,
                annot_kws={'size': 12, 'weight': 'bold'},
                cmap = palette,
                cbar_kws={'pad': .005, 'ticks':np.arange(-1.2, 1.2, 0.2)})
        hmap.figure.axes[-1].tick_params(axis = 'y', labelsize =24, direction='in', length = 10)

        for t in hmap.texts:
            if '-0.00' in t.get_text():
                t.set_text('0.00')

        plt.yticks(rotation=0, fontsize = 20)
        plt.xticks(fontsize = 20)

        plt.axhline(y=0, color='k',linewidth=2.5)
        plt.axhline(y=theMap.shape[1], color='k',linewidth=2.5)
        plt.axvline(x=0, color='k',linewidth=2.5)
        plt.axvline(x=theMap.shape[0], color='k',linewidth=2.5)

        if opt.UNBLIND:
            #plt.savefig('/home/llr/cms/bonanomi/fiducial/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/FidJJes/fit/corr_matrix/corr_'+obsName+'_'+physicalModel+'.pdf', bbox_inches='tight')
            plt.savefig('corr_'+obsName+'_'+physicalModel+'.pdf', bbox_inches='tight')
            #plt.savefig('/home/llr/cms/tarabini/CMSSW_10_2_13/src/HiggsAnalysis/FiducialXSFWK/plots/'+obsName+'/data/corr_'+obsName+'_'+physicalModel+'.png')
        else:
            #plt.savefig('/home/llr/cms/bonanomi/fiducial/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/FidJJes/fit/corr_matrix/corr_'+obsName+'_'+physicalModel+'.pdf', bbox_inches='tight')
            plt.savefig('corr_'+obsName+'_'+physicalModel+'.pdf', bbox_inches='tight')
            #plt.savefig('/home/llr/cms/tarabini/CMSSW_10_2_13/src/HiggsAnalysis/FiducialXSFWK/plots/'+obsName+'/asimov/corr_'+obsName+'_'+physicalModel+'.png')


        # pois_reverse = list(pois)
        # pois_reverse.reverse()
        # translate = defaultdict(list)
        # for p in pois:
        #     translate[p] = p.replace('','')
        #
        # for iBin,iPar in enumerate(pois):
        #     for jBin,jPar in enumerate(pois_reverse):
        #         theHist.GetXaxis().SetBinLabel(iBin+1, translate[iPar])
        #         theHist.GetYaxis().SetBinLabel(jBin+1, translate[jPar])
        #         if iBin <= (theHist.GetNbinsX()-1-jBin): theHist.Fill(iBin, jBin, theMap[(iPar,jPar)])
        #
        # print ('Final correlation map used is:')
        # print (theMap)
        #
        # ROOT.gStyle.SetNumberContours(500)
        # ROOT.gStyle.SetPaintTextFormat('1.2f')
        # ROOT.gStyle.SetTextFont(42)
        # theHist.GetXaxis().SetTickLength(0.)
        # theHist.GetXaxis().SetLabelSize(0.06)
        # theHist.GetXaxis().SetLabelFont(42)
        # theHist.GetYaxis().SetTickLength(0.)
        # theHist.GetYaxis().SetLabelSize(0.06)
        # theHist.GetYaxis().SetLabelFont(42)
        # theHist.GetZaxis().SetRangeUser(-1.,1.)
        # theHist.GetZaxis().SetTickLength(0.)
        # theHist.GetZaxis().SetLabelSize(0.03)
        #
        # theHist.SetStats(0)
        #
        # theHist.GetXaxis().LabelsOption("h")
        # theHist.GetYaxis().SetLabelOffset(0.007)
        # theHist.SetMarkerSize(2.5)
        # theHist.GetXaxis().SetLabelSize(0.07)
        # theHist.GetYaxis().SetLabelSize(0.07)
        #
        # c1 = ROOT.TCanvas()
        # c1.SetLeftMargin(0.2)
        # theHist.Draw('colz,text')
        # c1.SaveAs('corr_'+obsName+'_'+physicalModel+'.png')


obsName = opt.OBSNAME

DataModelName = 'SM_125'
if obsName.startswith("mass4l"):
    PhysicalModels = ['v2','v3']
elif obsName == 'D0m' or obsName == 'Dcp' or obsName == 'D0hp' or obsName == 'Dint' or obsName == 'DL1' or obsName == 'DL1Zg' or obsName == 'costhetaZ1' or obsName == 'costhetaZ2'or obsName == 'costhetastar' or obsName == 'phi' or obsName == 'phistar' or obsName == 'massZ1' or obsName == 'massZ2':
    PhysicalModels = ['v3','v4']
elif 'kL' in obsName:
    PhysicalModels = ['kLambda']
else:
    PhysicalModels = ['v3']

# prepare the set of bin boundaries to run over, it is retrieved from inputs file
# _temp = __import__('inputs_sig_'+obsName+'_'+opt.YEAR, globals(), locals(), ['observableBins', 'acc'], -1)
#_temp = __import__('inputs_sig_'+obsName+'_'+opt.YEAR, globals(), locals(), ['observableBins', 'acc'])
#observableBins = _temp.observableBins

observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
nbins = len(observableBins)

obs_bins = opt.OBSBINS.split("|") 
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins.pop()
obs_bins.pop(0)
print "obs_bins:  ", obs_bins
nbins = len(observableBins)




#acc = _temp.acc
# print 'Running Fiducial XS computation - '+obsName+' - bin boundaries: ', observableBins, '\n'
# print 'Theory xsec and BR at MH = '+_th_MH
# print 'Current directory: python'

doubleDiff = False
if type(observableBins) is dict: doubleDiff = True # If binning is a dictionary it is a double differential analysis

nBins = len(observableBins)
if not doubleDiff: nBins = nBins-1 #in case of 1D measurement the number of bins is -1 the length of the list of bin boundaries

#os.chdir('../combine_files/')
PlotCorrelation()

#sys.path.remove('../inputs/')
