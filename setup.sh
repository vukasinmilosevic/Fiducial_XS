# load cmsenv
eval `scramv1 runtime -sh`

# load necessary modules in the python PATH
export PYTHON27PATH=$PYTHON27PATH:$(pwd)/python
export PYTHON27PATH=$PYTHON27PATH:$(pwd)/Inputs

export PYTHONPATH=$PYTHONPATH:$(pwd)/python
export PYTHONPATH=$PYTHONPATH:$(pwd)/Inputs

# following line we can uncomment if we use python3
# export PYTHON3PATH=$PYTHON3PATH:$(pwd)/python
# export PYTHON3PATH=$PYTHON3PATH:$(pwd)/Inputs

# Compile the template maker
cd $(pwd)/templates
echo "Remove the executable main_fiducialXSTemplates if exists"
rm main_fiducialXSTemplates
echo "Compile fiducialXSTemplates"
make
echo "Done."
cd ..
