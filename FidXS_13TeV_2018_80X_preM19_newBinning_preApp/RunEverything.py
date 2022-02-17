import os
import argparse

from python.collectInputs import collect

# later when we add more than one obsNames then create a dict for obsNames and obsBins
obsNames = ["mass4l"]
obsBins = "|105.0|140.0|"


# channels = ["4mu"]
channels = ["4mu", "4e", "2e2mu", "4l"]
NtupleDir = "/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/"
HiggsMass = 125.0

parser = argparse.ArgumentParser(description='Input arguments')
parser.add_argument( '--step', default=1, type=int, help='Which step to run')
args = parser.parse_args()

if not os.path.isdir('datacardInputs'): os.mkdir('datacardInputs')
if not os.path.isdir('log'): os.mkdir('log')

print("Obs Name: {}".format(args.step))

for obsName in obsNames:
    print("Obs Name: {}".format(obsName))
    if (args.step == 1):
        for channel in channels:
            print(channel)
            command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" >& log/effs_{obsName}_{channel}.log &'.format(
            # command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
                obsName = obsName, obsBins = obsBins, channel = channel
            )
            print("Command: {}".format(command))
            os.system(command)
    if (args.step == 2):
        print("="*51)
        print("Running collect inputs")
        print("="*51)
        collect(obsName)

    if (args.step == 3):
        print("="*51)
        print("Running getUnc")
        print("="*51)
        # command = 'python -u getUnc_Unc.py --obsName="{obsName}" --obsBins="{obsBins}" >& log/unc_{obsName}.log &'.format(
        command = 'python -u getUnc_Unc.py --obsName="{obsName}" --obsBins="{obsBins}"'.format(
                obsName = obsName, obsBins = obsBins
        )
        print("Command: {}".format(command))
        os.system(command)


    if (args.step == 4):
        print("="*51)
        print("Running Background template maker")
        print("="*51)
        command = 'python -u runHZZFiducialXS.py --dir="{NtupleDir}" --obsName="{obsName}" --obsBins="{obsBins}" --redoTemplates --templatesOnly'.format(
                obsName = obsName, obsBins = obsBins, NtupleDir = NtupleDir
        )
        print("Command: {}".format(command))
        os.system(command)

    if (args.step == 5):
        print("="*51)
        print("Running final measurement and plotters")
        print("="*51)
        # command = 'nohup python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass}  >& log/log_{obsName}_Run2Fid.txt &'.format(
        command = 'python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass}'.format(
                obsName = obsName, obsBins = obsBins, HiggsMass = HiggsMass
        )
        print("Command: {}".format(command))
        os.system(command)
