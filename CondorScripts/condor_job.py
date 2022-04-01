import yaml
import argparse

parser = argparse.ArgumentParser(description='Input arguments')
parser.add_argument( '-i', dest='inYAMLFile', default="Inputs/observables_list.yml", type=str, help='Input YAML file having observable names and bin information')
parser.add_argument( '-obs', dest='OneDOr2DObs', default=1, type=int, choices=[1, 2], help="1 for 1D obs, 2 for 2D observable")
args = parser.parse_args()

InputYAMLFile = args.inYAMLFile
ObsToStudy = "1D_Observables" if args.OneDOr2DObs == 1 else "2D_Observables"

with open(InputYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

    if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
        print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                 Please check your YAML file format!!!'''.format(InputYAMLFile))


    if ObsToStudy in cfg['Observables']:
        arguments = []
        for obsName, obsBin in cfg['Observables'][ObsToStudy].items():
            print("Observable: {:11} Bins: {}".format(obsName, obsBin['bins']))
            for channel in ["4mu", "4e", "2e2mu", "4l"]:
                    arguments.append("{:27} {:7} {}".format(obsName, channel, obsBin["bins"]))

        with open("arguments.txt", "w") as args:
            args.write("\n".join(arguments))


#condor_jdl = '''executable              = {SHScriptName}
#output                  = output/output_$(ClusterId)_$(ProcId).out
#error                   = output/output_$(ClusterId)_$(ProcId).out
#log                     = output/output_$(ClusterId)_$(ProcId).out
#should_transfer_files   = YES
#transfer_input_files    = {SHScriptName}, efficiencyFactors.py
#when_to_transfer_output = ON_EXIT
#+JobFlavour             = "espresso"
#+AccountingGroup        = "group_u_CMS.CAF.ALCA"
#queue arguments from arguments.txt
#'''
#
#condor_sh = '''#!/bin/sh -e
#obsName=$1
#channel=$2
#obsBins=$3
#
#echo "obsName: ${obsName}"
#echo "obsBins: ${obsBins}"
#echo "channel: ${channel}"
#
#python -u efficiencyFactors.py -l -q -b --obsName="${obsName}" --obsBins="${obsBins}" -c "${channel}"
#
#echo -e "DONE"
#'''

# arguments = []
# for obsName, obsBin in obsNamesBinsDict.items():
#     for channel in ["4mu", "4e", "2e2mu", "4l"]:
#         arguments.append("{:25} {:5} {}".format(obsName, channel, obsBin))

# with open("arguments.txt", "w") as args:
#     args.write("\n".join(arguments))

#with open("condor_job.jdl", 'w') as jdl_out:
#    jdl_out.write(condor_jdl.format(SHScriptName = "condor_job.sh"))

#with open("condor_job.sh", "w") as rs:
#    rs.write(condor_sh)
