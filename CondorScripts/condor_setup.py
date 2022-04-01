import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--StringToChange', type=str,
                    default='TEST',
                    help='String to be added in the output file name')
parser.add_argument('--DASNames', type=str,
                    required=True,
                    help='''Text file name, where all DAS names are added
                     on which condor jobs need to be submitted.''')
parser.add_argument('--OutputPath', type=str,
                    default='/eos/user/r/rasharma/post_doc_ihep/double-higgs/ntuples/ResonantAna/nanoAOD_skim/',
                    help='''
                    ''')
parser.add_argument('--condorQueue', type=str,
                    default="espresso",
                    help='''
                    ''',
                    # Reference: https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor#Queue_Flavours
                    choices=['espresso',  # 20min
                             'microcentury',  # 1h
                             'longlunch',  # 2h
                             'workday',  # 8h
                             'tomorrow',  # 1d
                             'testmatch',  # 3d
                             'nextweek'  # 1w
                             ])
parser.add_argument('--postProc', type=str,
                    default='post_proc_DoubleHiggs.py',
                    help='''
                    ''')
parser.add_argument('--entriesToRun', type=int,
                    default=0,
                    help='''0 => run over all events.
                    Else add number of entries to run over.
                    ''')
args = parser.parse_args()

from color_style import style

# Variables to be changed by user
StringToChange = args.StringToChange
InputFileFromWhereReadDASNames = args.DASNames

Initial_path = args.OutputPath
Initial_path += StringToChange
condor_file_name = 'submit_condor_jobs_lnujj_' + StringToChange

customEOS = False
customEOS_cmd = 'eos root://cmseos.fnal.gov find -name "*.root" /store/group/lnujj/VVjj_aQGC/custom_nanoAOD'

condor_queue = args.condorQueue

# Create log files
import infoCreaterGit
SumamryOfCurrentSubmission = raw_input("\n\nWrite summary for current job submission: ")
infoLogFiles = infoCreaterGit.BasicInfoCreater('summary.dat', SumamryOfCurrentSubmission)
infoLogFiles.GenerateGitPatchAndLog()

# Get CMSSW directory path and name
cmsswDirPath = os.environ['CMSSW_BASE']
CMSSWRel = cmsswDirPath.split("/")[-1]

# Create directories for storing log files and output files at EOS.
import fileshelper
dirsToCreate = fileshelper.FileHelper('condor_logs/' + StringToChange, Initial_path)
output_log_path = dirsToCreate.CreateLogDirWithDate()
storeDir = dirsToCreate.CreateSotreArea(Initial_path)
dirName = dirsToCreate.dirName

# create tarball of present working CMSSW base directory
os.system('rm -f CMSSW*.tgz')
import makeTarFile
makeTarFile.make_tarfile(cmsswDirPath, CMSSWRel + ".tgz")
print "copying the " + CMSSWRel + ".tgz  file to eos path: " + storeDir + "\n"
os.system('cp ' + CMSSWRel + ".tgz" + ' ' + storeDir + '/' + CMSSWRel + ".tgz")

Transfer_Input_Files = ("data/jsonFiles/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt, "
                        + "data/jsonFiles/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt, "
                        + "data/jsonFiles/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt, "
                        + "keep_and_drop_data.txt, "
                        + "keep_and_drop_inclusive.txt")

# with open('input_data_Files/sample_list_v6_2017_campaign.dat') as in_file:
with open('input_data_Files/' + InputFileFromWhereReadDASNames) as in_file:
  outjdl_file = open(condor_file_name + ".jdl", "w")
  outjdl_file.write("+JobFlavour   = \"" + condor_queue + "\"\n")
  outjdl_file.write("Executable = "+condor_file_name+".sh\n")
  outjdl_file.write("Universe = vanilla\n")
  outjdl_file.write("Notification = ERROR\n")
  outjdl_file.write("Should_Transfer_Files = YES\n")
  outjdl_file.write("WhenToTransferOutput = ON_EXIT\n")
  #outjdl_file.write("Transfer_Input_Files = "+Transfer_Input_Files + ",  " + args.postProc+"\n")
  outjdl_file.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
  count = 0
  count_jobs = 0
  for lines in in_file:
     if lines[0] == "#": continue
     count = count +1
     #if count > 1: break
     print(style.RED +"="*51+style.RESET+"\n")
     print "==> Sample : ",count
     sample_name = lines.split('/')[1]
     campaign = lines.split('/')[2].split('-')[0]
     print "==> sample_name = ",sample_name
     print "==> campaign = ",campaign
     ########################################
     #
     #      Create output directory
     #
     ########################################
     if sample_name.find("SingleMuon") != -1 or sample_name.find("SingleElectron") != -1 or sample_name.find("EGamma") != -1 or sample_name.find("DoubleMuon") != -1 or sample_name.find("MuonEG") != -1 or sample_name.find("DoubleEG") != -1:
       output_string = sample_name + os.sep + campaign + os.sep + dirName
       output_path = Initial_path + os.sep + output_string
       os.system("mkdir "+Initial_path + os.sep + sample_name)
       os.system("mkdir "+Initial_path + os.sep + sample_name + os.sep + campaign)
       os.system("mkdir "+ Initial_path + os.sep + sample_name + os.sep + campaign + os.sep + dirName)
       infoLogFiles.SendGitLogAndPatchToEos(Initial_path + os.sep + sample_name + os.sep + campaign + os.sep + dirName)
     else:
       output_string = sample_name+os.sep+dirName
       output_path = Initial_path+ os.sep + output_string
       os.system("mkdir "+Initial_path + os.sep + sample_name)
       os.system("mkdir "+Initial_path + os.sep + sample_name+os.sep+dirName)
       infoLogFiles.SendGitLogAndPatchToEos(Initial_path + os.sep + sample_name + os.sep + dirName)
     print "==> output_path = ",output_path

     ########################################
     #print 'dasgoclient --query="file dataset='+lines.strip()+'"'
     #print "..."
     if customEOS:
       xrd_redirector = 'root://cmseos.fnal.gov/'
       output = os.popen(customEOS_cmd + lines.strip()).read()
     else:
       xrd_redirector = 'root://cms-xrd-global.cern.ch/'
       output = os.popen('dasgoclient --query="file dataset='+lines.strip()+'"').read()

     count_root_files = 0
     for root_file in output.split():
       #print "=> ",root_file
       count_root_files+=1
       count_jobs += 1
       outjdl_file.write("Output = "+output_log_path+"/"+sample_name+"_$(Process).stdout\n")
       outjdl_file.write("Error  = "+output_log_path+"/"+sample_name+"_$(Process).stderr\n")
       outjdl_file.write("Log  = "+output_log_path+"/"+sample_name+"_$(Process).log\n")
       outjdl_file.write("Arguments = "+(xrd_redirector+root_file).replace('/','\/')+" "+output_path+"  "+Initial_path+"\n")
       outjdl_file.write("Queue \n")
     print "Number of files: ",count_root_files
     print "Number of jobs (till now): ",count_jobs
  outjdl_file.close();


outScript = open(condor_file_name + ".sh","w")
outScript.write('#!/bin/bash')
outScript.write("\n" + 'echo "Starting job on " `date`')
outScript.write("\n" + 'echo "Running on: `uname -a`"')
outScript.write("\n" + 'echo "System software: `cat /etc/redhat-release`"')
outScript.write("\n" + 'source /cvmfs/cms.cern.ch/cmsset_default.sh')
outScript.write("\n" + 'echo "copy cmssw tar file from store area"')
outScript.write("\n" + 'cp -s ${3}/' + CMSSWRel + '.tgz  .')
outScript.write("\n" + 'tar -xf ' + CMSSWRel + '.tgz')
outScript.write("\n" + 'rm ' + CMSSWRel + '.tgz')
outScript.write("\n" + 'cd ' + CMSSWRel + '/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_vvVBS/')
# outScript.write("\n" + 'echo "====> List files : " ')
# outScript.write("\n" + 'ls -alh')
outScript.write("\n" + 'rm *.root')
outScript.write("\n" + 'scramv1 b ProjectRename')
outScript.write("\n" + 'eval `scram runtime -sh`')
outScript.write("\n" + 'sed -i "s/testfile = .*/testfile = \\"${1}\\"/g" ' + args.postProc)
outScript.write("\n" + 'sed -i "s/entriesToRun = .*/entriesToRun = ' + str(args.entriesToRun) + '/g" ' + args.postProc)
outScript.write("\n" + 'echo "========================================="')
outScript.write("\n" + 'echo "cat ' + args.postProc + '"')
outScript.write("\n" + 'echo "..."')
outScript.write("\n" + 'cat '+args.postProc)
outScript.write("\n" + 'echo "..."')
outScript.write("\n" + 'echo "========================================="')
outScript.write("\n" + 'python ' + args.postProc)
outScript.write("\n" + 'echo "====> List root files : " ')
outScript.write("\n" + 'ls *.root')
outScript.write("\n" + 'echo "====> copying *.root file to stores area..." ')
outScript.write("\n" + 'if ls *_Skim.root 1> /dev/null 2>&1; then')
outScript.write("\n" + '    echo "File *_Skim.root exists. Copy this."')
outScript.write("\n" + '    echo "cp *_Skim.root ${2}"')
outScript.write("\n" + '    cp  *_Skim.root ${2}')
outScript.write("\n" + 'else')
outScript.write("\n" + '    echo "file *_Skim.root does not exists, so copy *.root file."')
outScript.write("\n" + '    echo "cp *.root ${2}"')
outScript.write("\n" + '    cp  *.root ${2}')
outScript.write("\n" + 'fi')
outScript.write("\n" + 'rm *.root')
outScript.write("\n" + 'cd ${_CONDOR_SCRATCH_DIR}')
outScript.write("\n" + 'rm -rf ' + CMSSWRel)
outScript.write("\n")
outScript.close()
os.system("chmod 777 " + condor_file_name + ".sh")

print "===> Set Proxy Using:";
print "\tvoms-proxy-init --voms cms --valid 168:00";
print "\"condor_submit "+condor_file_name+".jdl\" to submit";
#os.system("condor_submit "+condor_file_name+".jdl")
