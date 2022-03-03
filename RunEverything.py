import os
import argparse

from python.collectInputs import collect
from python.obsList import obsNamesBinsDict

# Kept for record of models (copied from runHZZFiducialXS.py)
# modelNames = "SM_125,SMup_125,SMdn_125" #,'VBF_powheg_JHUgen_125']
# # do all models
# #if (not 'jet' in obsName):
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125', 'ttH_powheg_JHUgen_125']
# #else:
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125']

parser = argparse.ArgumentParser(description='Input arguments')
parser.add_argument( '-s', dest='step', default=1, choices=[1, 2, 3, 4, 5], type=int, help='Which step to run')
parser.add_argument( '-c', dest='channels', nargs="+",  default=["4mu", "4e", "2e2mu", "4l"], help='list of channels')
parser.add_argument( '-model', dest='modelNames', default="SM_125,SMup_125,SMdn_125",
                        help='Names of models for unfolding, separated by , (comma) . Default is "SM_125"')
parser.add_argument( '-p', dest='NtupleDir', default="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/", help='Path of ntuples')
parser.add_argument( '-m', dest='HiggsMass', default=125.0, type=float, help='Higgs mass')
parser.add_argument( '-r', dest='RunCommand', default=0, type=int, choices=[0, 1], help="if 1 then it will run the commands else it will just print the commands")

args = parser.parse_args()

if not os.path.isdir('datacardInputs'): os.mkdir('datacardInputs')
if not os.path.isdir('log'): os.mkdir('log')

for obsName, obsBin in obsNamesBinsDict.items():
    print("="*51)
    print("==> Obs: {:25}  {}".format(obsName,obsBin))
    if (args.step == 1):
        print("="*51)
        print("Running the efficiencies step")
        print("="*51)
        for channel in args.channels:
            print("==> channel: {}".format(channel))
            command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" >& log/effs_{obsName}_{channel}.log &'.format(
            # command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
                obsName = obsName, obsBins = obsBin, channel = channel
            )
            print("Command: {}".format(command))
            if (args.RunCommand): os.system(command)
        os.system('ps -t')

    if (args.step == 2):
        print("="*51)
        print("Running collect inputs")
        print("="*51)
        collect(obsName)
        print("="*51)
        if (not obsName.startswith("mass4l")):
            command = 'python python/plot2dsigeffs.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}"'.format(
                obsName = obsName, obsBins = obsBin
            )
            print("Command: {}".format(command))
            if (args.RunCommand): os.system(command)

    if (args.step == 3):
        print("="*51)
        print("Running getUnc")
        print("="*51)
        # command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" >& log/unc_{obsName}.log &'.format(
        command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}"'.format(
                obsName = obsName, obsBins = obsBin
        )
        print("Command: {}".format(command))
        if (args.RunCommand): os.system(command)


    if (args.step == 4):
        print("="*51)
        print("Running Background template maker")
        print("="*51)
        # FIXME: Check if we need modelNames in step-4 or not
        command = 'python -u runHZZFiducialXS.py --dir="{NtupleDir}" --obsName="{obsName}" --obsBins="{obsBins}" --modelNames {modelNames} --redoTemplates --templatesOnly '.format(
                obsName = obsName, obsBins = obsBin, NtupleDir = args.NtupleDir, modelNames= args.modelNames
        )
        print("Command: {}".format(command))
        if (args.RunCommand): os.system(command)

    if (args.step == 5):
        print("="*51)
        print("Running final measurement and plotters")
        print("="*51)
        # Copy model from model directory to combine path
        CMSSW_BASE = os.getenv('CMSSW_BASE')
        copyCommand = 'cp models/HZZ4L*.py {CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python/'.format(CMSSW_BASE=CMSSW_BASE)
        os.system(copyCommand)

        # command = 'nohup python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass}  >& log/log_{obsName}_Run2Fid.txt &'.format(
        command = 'python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass} --modelNames {modelNames}'.format(
                obsName = obsName, obsBins = obsBin, HiggsMass = args.HiggsMass, modelNames= args.modelNames
        )
        print("Command: {}".format(command))
        if (args.RunCommand): os.system(command)
