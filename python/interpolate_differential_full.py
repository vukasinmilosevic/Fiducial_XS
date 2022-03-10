import optparse
import os
import sys

from scipy import interpolate
import matplotlib.pyplot as plt

from Input_Info import datacardInputs

def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ')
    global opt, args
    (opt, args) = parser.parse_args()

def interpolate_fun(x, nbins, obsName):
    sys.path.append(datacardInputs)

    x_points = [124, 125, 126]
    channels=['4mu','2e2mu','4e']

    if obsName=='mass4l': channels=['4mu','2e2mu','4e','4l']

    acceptance={}
    dacceptance={}
    efficiency={}
    defficiency={}
    inc_wrongfrac = {}
    binfrac_outfrac = {}
    outinratio = {}
    doutinratio = {}
    inc_outfrac = {}
    # acc_4l = {}
    # dacc_4l = {}
    binfrac_wrongfrac = {}
    cfactor = {}
    lambdajesup = {}
    lambdajesdn = {}

    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc','dacc','eff','deff','inc_outfrac','binfrac_outfrac','outinratio','doutinratio','inc_wrongfrac', 'inc_outfrac','binfrac_wrongfrac','cfactor','lambdajesup','lambdajesdn'], -1)
    acc_ggH_powheg = _temp.acc
    dacc_ggH_powheg = _temp.dacc
    eff_ggH_powheg = _temp.eff
    deff_ggH_powheg = _temp.deff
    inc_wrongfrac_ggH_powheg = _temp.inc_wrongfrac
    binfrac_outfrac_ggH_powheg = _temp.binfrac_outfrac
    outinratio_ggH_powheg = _temp.outinratio
    doutinratio_ggH_powheg = _temp.doutinratio
    # acc_4l_ggH_powheg = _temp.acc_4l
    # dacc_4l_ggH_powheg = _temp.dacc_4l
    inc_outfrac_ggH_powheg = _temp.inc_outfrac
    binfrac_wrongfrac_ggH_powheg = _temp.binfrac_wrongfrac
    cfactor_ggH_powheg = _temp.cfactor
    lambdajesup_ggH_powheg = _temp.lambdajesup
    lambdajesdn_ggH_powheg = _temp.lambdajesdn

    for channel in channels:
        for obsBin in range(0, nbins-1):
            for recoBin in range(0, nbins-1):
                thread='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)
                print("{:15} : {}".format("thread", thread))

                acceptance[thread]=0.0
                dacceptance[thread]=0.0
                efficiency[thread]=0.0
                defficiency[thread]=0.0
                inc_wrongfrac[thread]=0.0
                binfrac_outfrac[thread]=0.0
                outinratio[thread]=0.0
                doutinratio[thread]=0.0
                #                acc_4l[thread]=0.0
                #                dacc_4l[thread]=0.0
                inc_outfrac[thread]=0.0
                binfrac_wrongfrac[thread]=0.0
                cfactor[thread]=0.0
                lambdajesup[thread]=0.0
                lambdajesdn[thread]=0.0

                acc_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                dacc_points = [dacc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                eff_points = [eff_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],eff_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],eff_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                deff_points = [deff_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],deff_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],deff_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                inc_wrongfrac_points = [inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                binfrac_outfrac_points = [binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                outinratio_points = [outinratio_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],outinratio_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],outinratio_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                doutinratio_points = [doutinratio_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],doutinratio_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],doutinratio_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                # acc_4l_points = [acc_4l_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_4l_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_4l_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                # dacc_4l_points = [dacc_4l_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_4l_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_4l_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                inc_outfrac_points = [inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                binfrac_wrongfrac_points = [binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                cfactor_points = [cfactor_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],cfactor_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],cfactor_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                lambdajesup_points = [lambdajesup_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesup_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesup_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                lambdajesdn_points = [lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]

                print("{:15} : {}".format("obsName", obsName))
                print("{:15} : {}".format("channel", channel))
                print("{:15} : {}".format("x_points", x_points))
                print("{:15} : {}".format("acc_points", acc_points))
                print("{:15} : {}".format("eff_points", eff_points))

                # # if you want to check the interpolate line uncomment below 4 lines
                # x2_points = x_points
                # y2 = interpolate.splev(x2_points, tck1)
                # plt.plot(x_points, acc_points, 'o', x2_points, y2)
                # plt.show()


                # tck = interpolate.splrep(x_points, y_points)
                spl_acc_points  = interpolate.splrep(x_points, acc_points, k=2)
                spl_dacc_points = interpolate.splrep(x_points, dacc_points, k=2)
                spl_eff_points = interpolate.splrep(x_points, eff_points, k=2)
                spl_deff_points = interpolate.splrep(x_points, deff_points, k=2)
                spl_inc_wrongfrac_points = interpolate.splrep(x_points, inc_wrongfrac_points, k=2)
                spl_binfrac_outfrac_points = interpolate.splrep(x_points, binfrac_outfrac_points, k=2)
                spl_outinratio_points = interpolate.splrep(x_points, outinratio_points, k=2)
                spl_doutinratio_points = interpolate.splrep(x_points, doutinratio_points, k=2)
                # spl_acc_4l_points = interpolate.splrep(x_points, acc_4l_points, k=2)
                # spl_dacc_4l_points = interpolate.splrep(x_points, dacc_4l_points, k=2)
                spl_inc_outfrac_points = interpolate.splrep(x_points, inc_outfrac_points, k=2)
                spl_binfrac_wrongfrac_points = interpolate.splrep(x_points, binfrac_wrongfrac_points, k=2)
                spl_cfactor_points = interpolate.splrep(x_points, cfactor_points, k=2)
                spl_lambdajesup_points = interpolate.splrep(x_points, lambdajesup_points, k=2)
                spl_lambdajesdn_points = interpolate.splrep(x_points, lambdajesdn_points, k=2)

                acceptance[thread]=float(interpolate.splev(x, spl_acc_points))
                dacceptance[thread]= float(interpolate.splev(x, spl_dacc_points))
                efficiency[thread]=float(interpolate.splev(x, spl_eff_points))
                defficiency[thread]=float(interpolate.splev(x, spl_deff_points))
                inc_wrongfrac[thread]=float(interpolate.splev(x, spl_inc_wrongfrac_points))
                binfrac_outfrac[thread]=float(interpolate.splev(x, spl_binfrac_outfrac_points))
                outinratio[thread]=float(interpolate.splev(x, spl_outinratio_points))
                doutinratio[thread]=float(interpolate.splev(x, spl_doutinratio_points))
                # acc_4l[thread]=float(interpolate.splev(x, spl_acc_4l_points))
                # dacc_4l[thread]=float(interpolate.splev(x, spl_dacc_4l_points))
                inc_outfrac[thread]= float(interpolate.splev(x, spl_inc_outfrac_points))
                binfrac_wrongfrac[thread]= float(interpolate.splev(x, spl_binfrac_wrongfrac_points))
                cfactor[thread]= float(interpolate.splev(x, spl_cfactor_points))
                lambdajesup[thread]= float(interpolate.splev(x, spl_lambdajesup_points))
                lambdajesdn[thread]= float(interpolate.splev(x, spl_lambdajesdn_points))

                # initializing new thread in list
                acc_ggH_powheg[str(thread)]={}
                dacc_ggH_powheg[str(thread)]={}
                eff_ggH_powheg[str(thread)]={}
                deff_ggH_powheg[str(thread)]={}
                inc_wrongfrac_ggH_powheg[str(thread)]={}
                binfrac_outfrac_ggH_powheg[str(thread)]={}
                outinratio_ggH_powheg[str(thread)]={}
                doutinratio_ggH_powheg[str(thread)]={}
                #	        acc_4l_ggH_powheg[str(thread)]={}
                #	        dacc_4l_ggH_powheg[str(thread)]={}
                inc_outfrac_ggH_powheg[str(thread)]={}
                binfrac_wrongfrac_ggH_powheg[str(thread)]={}
                cfactor_ggH_powheg[str(thread)]={}
                lambdajesup_ggH_powheg[str(thread)]={}
                lambdajesdn_ggH_powheg[str(thread)]={}
                #################################################################
                acc_ggH_powheg.update(acceptance)
                dacc_ggH_powheg.update(dacceptance)
                eff_ggH_powheg.update(efficiency)
                deff_ggH_powheg.update(defficiency)
                inc_wrongfrac_ggH_powheg.update(inc_wrongfrac)
                binfrac_outfrac_ggH_powheg.update(binfrac_outfrac)
                outinratio_ggH_powheg.update(outinratio)
                doutinratio_ggH_powheg.update(doutinratio)
                #               acc_4l_ggH_powheg.update(acc_4l)
                #               dacc_4l_ggH_powheg.update(dacc_4l)
                inc_outfrac_ggH_powheg.update(inc_outfrac)
                binfrac_wrongfrac_ggH_powheg.update(binfrac_wrongfrac)
                cfactor_ggH_powheg.update(cfactor)
                lambdajesup_ggH_powheg.update(lambdajesup)
                lambdajesdn_ggH_powheg.update(lambdajesdn)

                #print "interpol.           acceptance is  ....................", acc_ggH_powheg[str(thread)]#acc_ggH_powheg
                #print "pdfunc_ggH_powheg                           ",pdfunc_ggH_powheg
                print "the thread is ...........", thread
                print "acceptance is.             ", acceptance[thread] #=float(interpolate.splev(x, tck2))
                print "dacceptance is.             ", dacceptance[thread] #=float(interpolate.splev(x, tck2))
                #            qcdunc_ggH_powheg[str(thread2)]['uncerDn']=qcd_uncerDn[thread]
                os.system('cp datacardInputs/inputs_sig_'+opt.OBSNAME+'.py datacardInputs/inputs_sig_'+opt.OBSNAME+'_beforeInterpolation.py')
                with open('datacardInputs/inputs_sig_'+obsName+'.py', 'w') as f:
                    print "going write interpolated values   "
                    f.write('acc = '+str(acc_ggH_powheg)+' \n')
                    f.write('dacc = '+str(dacc_ggH_powheg)+' \n')
                    f.write('eff = '+str(eff_ggH_powheg)+' \n')
                    f.write('deff = '+str(deff_ggH_powheg)+' \n')
                    f.write('inc_wrongfrac = '+str(inc_wrongfrac_ggH_powheg)+' \n')
                    f.write('binfrac_outfrac = '+str(binfrac_outfrac_ggH_powheg)+' \n')
                    f.write('outinratio = '+str(outinratio_ggH_powheg)+' \n')
                    f.write('doutinratio = '+str(doutinratio_ggH_powheg)+' \n')
                #                  f.write('acc_4l = '+str(acc_4l_ggH_powheg)+' \n')
                #                  f.write('dacc_4l = '+str(dacc_4l_ggH_powheg)+' \n')
                    f.write('inc_outfrac = '+str(inc_outfrac_ggH_powheg)+' \n')
                    f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac_ggH_powheg)+' \n')
                    f.write('cfactor = '+str(cfactor_ggH_powheg)+' \n')
                    f.write('lambdajesup = '+str(lambdajesup_ggH_powheg)+' \n')
                    f.write('lambdajesdn = '+str(lambdajesdn_ggH_powheg)+' \n')


if __name__ == "__main__":
    global opt, args
    parseOptions()
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)

    print("Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))

    interpolate_fun(125.38, nbins, opt.OBSNAME)
