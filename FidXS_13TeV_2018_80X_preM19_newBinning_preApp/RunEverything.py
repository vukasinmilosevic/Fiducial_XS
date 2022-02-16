import os

from collectInputs import collect

# later when we add more than one obsNames then create a dict for obsNames and obsBins
obsNames = ["mass4l"]
obsBins = "|105.0|140.0|"

channels = ["4mu", "4e", "2e2mu", "4l"]

for obsName in obsNames:
    for channel in channels:
        print(channel)
        # command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" >& effs_{obsName}_{channel}.log &'.format(
        command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
            obsName = obsName, obsBins = obsBins, channel = channel
        )
        print("Command: {}".format(command))
        os.system(command)
    # os.system('python collectInputs.py')
    # collect(obsName)
