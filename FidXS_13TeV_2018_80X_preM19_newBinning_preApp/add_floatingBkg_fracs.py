import optparse
import os
import sys

from rates_full import *
#from Input_Info import datacardInputs
#from Utils import *

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='mass4l',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='|105.0|160.0|',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    parser.add_option('',   '--era',  dest='ERA',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ')
    parser.add_option('', '--bkg',      dest='BKG',type='string',default='zz', help='run with the type of zz background to float e.g. zz or zz_chan')
    parser.add_option('',   '--debug',  dest='DEBUG',  type='int',default=0,   help='0 if debug false, else debug True')
    global opt, args
    (opt, args) = parser.parse_args()

def add_bkgfrac_floating(nbins, obsName, DEBUG = 0):
 #   border_msg("Start of module `add_bkgfrac_floating_zz.py`")
    if (opt.ERA == '2016'): years = ['2016']
    if (opt.ERA == '2017'): years = ['2017']
    if (opt.ERA == '2018'): years = ['2018']
    if (opt.ERA == 'Full'): years = ['2016','2017','2018']

    channels=['4mu','2e2mu','4e']
    modes= ['ggZZ_','ZZTo']
    for year in years:
	print "year: ", year
	sys.path.append('./datacardInputs_'+year+opt.BKG+'/')
	_temp = __import__('inputs_bkg_'+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
	print "_temp:    ",_temp
	bins_all = _temp.observableBins
	frac_all = _temp.fractionsBackground
	ljesup_all = _temp.lambdajesupBkg
	ljesdn_all = _temp.lambdajesdnBkg
#	print "frac_all: ", frac_all
        for mode in modes:
            for channel in channels:
                for recoBin in range(0, nbins-1):
		    if (mode=='ggZZ_'): gen='_MCFM67_'
		    if (mode=='ZZTo'): gen='_powheg_'
		    #frac_all[mode+channel+gen+channel+'_'+obsName+'_recobin'+str(recoBin)]=1.0
                    key_bkg = mode+channel+gen+channel+'_'+obsName+'_recobin'+str(recoBin)+opt.BKG
                    print("=== ===>{:15} : {}".format("dict key", key_bkg))
		    if (mode=='ggZZ_'): num=rates_full[year]['ggZZ'+channel]
		    if (mode=='ZZTo'): num=rates_full[year]['qqZZ'+channel]
		    if (opt.BKG=='zz'): den=rates_full[opt.ERA]['ZZ']
                    if (opt.BKG=='zz_chan'): den=rates_full[opt.ERA]['ZZ'+channel]
                    frac_all[key_bkg] = num/den
		    print "after updating ::   "
		    print " key_bkg: ", key_bkg, " frac_all[key_bkg]:     " ,frac_all[key_bkg]
                    #################################################################
                    if (DEBUG): print("=== ===>{:15} : {}".format("frac_all", frac_all))

        OutputDictFileName = 'datacardInputs_'+year+opt.BKG+'/inputs_bkg_'+obsName+'.py' 
        os.system('cp ' + OutputDictFileName + " " + OutputDictFileName.replace('.py','_beforewriting.py'))
        with open( OutputDictFileName, 'w') as f:
            print("going to write background fractions in  "+OutputDictFileName)
            f.write('observableBins = '+str(bins_all)+' \n')
            f.write('fractionsBackground = '+str(frac_all)+' \n')
            f.write('lambdajesupBkg = '+str(ljesup_all)+' \n')
            f.write('lambdajesdnBkg = '+str(ljesdn_all)+' \n')


if __name__ == "__main__":
    global opt, args
    parseOptions()
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)
    print("Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))
    add_bkgfrac_floating(nbins, opt.OBSNAME, opt.DEBUG)
    print("fraction writing completed... :) ")
