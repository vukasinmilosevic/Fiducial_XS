#!/bin/sh -e
obsName=$1
channel=$2
obsBins=$3

echo "obsName: ${obsName}"
echo "obsBins: ${obsBins}"
echo "channel: ${channel}"

cp /eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/CMSSW_10_2_13.tgz .
echo "==============="
ls
echo "==============="
tar -xf CMSSW_10_2_13.tgz
echo "==============="
ls
echo "==============="
rm CMSSW_10_2_13.tgz
cd CMSSW_10_2_13/src/
echo "==============="
ls
echo "==============="
scramv1 b ProjectRename
eval `scram runtime -sh`
cd Fiducial_XS
echo "==============="
ls
echo "==============="
eval `scramv1 runtime -sh`
# load necessary modules in the python PATH
export PYTHON27PATH=$PYTHON27PATH:$(pwd)/python
export PYTHON27PATH=$PYTHON27PATH:$(pwd)/Inputs

export PYTHONPATH=$PYTHONPATH:$(pwd)/python
export PYTHONPATH=$PYTHONPATH:$(pwd)/Inputs
echo "==============="
rm -rf datacardInputs
ls
echo "==============="
echo "Start of efficiency script"
python -u efficiencyFactors.py -l -q -b --obsName="${obsName}" --obsBins="${obsBins}" -c "${channel}"
echo "==============="
echo "End of efficiency script"
echo "content of eos datacard directory: "
ls /eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/datacardInputs/
echo "==============="
echo "Copy datacardInputs directory to eos"
cp -r datacardInputs/* /eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/datacardInputs/
echo "content of eos datacard directory: "
ls /eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/datacardInputs/
echo "==============="
ls
echo "==============="
echo -e "DONE"
