# Instructions to run the BBBF differential xs code for CMSSW_10_X releases

## 1. CMSSW and cobmine release setup

Taken from Combine official instructions: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/

CC7 release CMSSW_10_2_X - recommended version
Setting up the environment (once):

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
```

Update to a recommended tag - currently the recommended tag is v8.2.0: see release notes

```
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b # always make a clean build
```
Depending on where the data/mc is stored, one might need:

```
voms-proxy-init -voms cms
```
Final step is to clone the correct verison of the code. At the moment the working version can be found on the ```CMSSW_10_X``` branch, which can be cloned via the following command:
```
cd $CMSSW_BASE/src/
#git clone -b CMSSW_10_X git@github.com:vukasinmilosevic/Fiducial_XS.git
#git clone -b CMSSW_10_X_Combine git@github.com:vukasinmilosevic/Fiducial_XS.git
git clone -b CMSSW_10_X_Combine_zz git@github.com:vukasinmilosevic/Fiducial_XS.git
```

## 2. Running the measurement

### 2.1 Running the efficiencies step

Current example running ```mass4l``` variable via ```nohup```. For local testing remove ```nohup``` (and pipelining into a .log file if wanting terminal printout).

```
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4mu"  --year="2018" >& effs_mass4l_4mu_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4e"  --year="2018" >& effs_mass4l_4e_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "2e2mu"  --year="2018" >& effs_mass4l_2e2mu_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4l"  --year="2018" >& effs_mass4l_4l_2018.log &


# for the various observables and all three years:

sh doAllEffs_channels_2016.sh
sh doAllEffs_channels_2017.sh
sh doAllEffs_channels_2018.sh

# merge the channel outputs to single:
python -u collectInputs.py --obsName="mass4l" --year="2018"
# for the various observables and all three years:

sh collectInputs_2016.sh
sh collectInputs_2017.sh
sh collectInputs_2018.sh

```

Running the plotter:

```
#skipping for mass4l 
#python -u plot2dsigeffs.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|"
```

### 2.2. Running the uncertainties step

```
nohup python -u getUnc_Unc.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --year="2018" >& unc_mass4l_2018.unc &

# for the various observables :
sh doAllUnc_2018.sh
```

### 2.3. Obtaining the interpolated values of eff./acc. for 125.38 (run only if the channel output is merged, all three years in case of full Run2 measurement.)

```
nohup python -u interpolate_differential_full.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --year="2018" >& full_interpolation_mass4l_2018.txt &

# for the various observables in years:
sh interpolate_differential_full_all_2016.sh
sh interpolate_differential_full_all_2017.sh
sh interpolate_differential_full_all_2018.sh

## for theory uncertainties interpolation
nohup python -u interpolate_differential_pred.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --year="2018" >& pred_interpolation_mass4l_2018.txt &
# for several observables:
sh interpolate_differential_pred_all_2018.sh

```
### 2.4 Running the background template maker

```
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly --era="2018" >& templates_mass4l_2018.log &
# suggested to simultaneously run for all three years
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly --era="Full" >& templates_mass4l_Full.log &
# for various observables (full Run2):
sh doAllTemplates_Full.sh

```

### 2.5 Runing the final measurement and plotters

```

# for individual year:
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --era="2018"  >& log_mass4l_2018.txt &

# for full Run 2:

nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --era="Full"  >& log_mass4l_Full.txt & 

# channel wise XS plotter for all three years

nohup python -u producePlots_mass4l_comb.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --unfoldModel="SM_125" --theoryMass="125.38"  --era="Full" >&  final_plots_only_mass4l_combine.log &
nohup python -u producePlots_mass4l_comb.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --unfoldModel="SM_125" --theoryMass="125.38"  --era="Full" --setLog >&  final_plots_only_mass4l_combine_log.log &



#full Run2 and various observables

sh doAllObs_Full.sh

# output of this step are likelihood scan, asimov fits, differential yield and differential measurement plots. 

# channel wise inclusive XS plotter 

nohup python -u producePlots_mass4l_comb.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --unfoldModel="SM_125" --theoryMass="125.38"  >&  final_plots_only_mass4l_combine.log &
nohup python -u producePlots_mass4l_comb.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --unfoldModel="SM_125" --theoryMass="125.38"  --setLog >&  final_plots_only_mass4l_combine_log.log &


# plotting the observed cross section as function of Center of mass energies (only for observed cross section)

python plot_XS_vs_sqrts_Paper.py


```

### Measurement with the floating ZZ background in the fit
The branch ```CMSSW_10_X_Combine_zz``` currently supports to perform such measurement for inclusive case. 
This can be done by adding an argument e.g. ```--bkg="zz"``` or ```--bkg="zz_chan"``` at the end of each commandline. (bash scripts are added with full command lines)
The measurement is done with extended mass range i.e. ```|105.0|160.0|``` for which all the supplement inputs are covered with choice of ```--bkg``` argument. 

#### Prepration of datacards
Template datacards e.g. for `2018` and `4e` are given for two scenarios of floating zz background in `channels` [link](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/xs_125.0_1bin_2018zz_chan/hzz4l_4eS_13TeV_xs_inclusive_bin0.txt) and as inclusively for `all channels` [link](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/xs_125.0_1bin_2018zz/hzz4l_4eS_13TeV_xs_inclusive_bin0.txt). 
First we introduce a `rate parameter` correlated or uncorrelated among the `channels` depending upon the scenarios (e.g. `zz_norm_0` for the correlated case) as described in the [combine tool](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/settinguptheanalysis/#rate-parameters). It is initiated with the expected `MC` yield given some range to float. Then in the `rate` line of the datacard we put `1.0` instead of the actual MC yield both for `qqZZ` and `ggZZ` background. Further, we remove all the `theory nuisances` affecting these backgrounds leaving us with fewer `nuisances` w.r.t. to usual measurements. 

#### Treatment for workspace
Usually, for inclusive case in `datacardInputs/inputs_bkg_mass4l.py` we put `1.0` in the fraction keys. However, while floating the ZZ background we need to put the actual fraction of the MC yields in the respective `ZZ background` and `channel`. The [macro](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/add_floatingBkg_fracs.py) is meant to do this job which reads the total rates saved in [pyton file](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/rates_full.py) and saves the fractions the computed fractions in the `channels` (depending upon the floating `scenario` i.e. `correlated` or `uncorrelated`) in `datacardInputs_{year}{opt.BKG}/inputs_bkg_mass4l.py`. Then in the [`workspace`](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/createXSworkspace.py#L440-L444) the background fractions are read depending upon the `scenario` of floating the background. 
 
#### Running the combine
While running the `MultiDimFit` using `combine` tool we float the defined `rateParam` (e.g. [here](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/runHZZFiducialXS.py#L323-L326)) alongwith other parameters and the fitted values are [saved](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/runHZZFiducialXS.py#L385-L394) accordingly for cases of full systematic and stat-only fits. 

#### Plotting the fitted ZZ background alongwith the cross section
Prior to run the likelihood scan plotter, we run usual [combine commands](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/doLScan_mass4l.sh) for `mass4l` to include the `ratePram` for ZZ background. Later we can [plot likelihood scans](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/plotLHScans.py) also for fitted ZZ background. Finally, fitted background can be [plotted](https://github.com/vukasinmilosevic/Fiducial_XS/blob/CMSSW_10_X_Combine_zz/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/producePlots.py) with the measured cross section depending upon the `scenario` i.e. `opt.BKG` type. 

