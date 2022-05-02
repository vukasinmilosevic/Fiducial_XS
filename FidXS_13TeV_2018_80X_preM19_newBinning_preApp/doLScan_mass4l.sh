echo "will do scan for :" $1
if [[ "$2" == "zz" ]]; then
  channels=("SigmaBin0" "r4eBin0" "r4muBin0" "r2e2muBin0" "zz_norm_0")
elif [[ "$2" == "zz_chan" ]]; then
  channels=("SigmaBin0" "r4eBin0" "r4muBin0" "r2e2muBin0" "zz_norm_4e" "zz_norm_4mu" "zz_norm_2e2mu")
else
  channels=("SigmaBin0" "r4eBin0" "r4muBin0" "r2e2muBin0")
fi
echo "channels are ",${channels[*]}
#for ch in SigmaBin0 r4eBin0 r4muBin0 r2e2muBin0; do
for ch in ${channels[@]}; do
 for model in v2 v3; do
  if [[ "$ch" == "SigmaBin0" && $model == "v2" ]]; then 
   continue; #  model="v3"; #fi 
  fi
  if [[ ( "$ch" == "r4eBin0" || "$ch" == "r4muBin0" || "$ch" == "r2e2muBin0" ) && $model == "v3" ]]; then 
   continue; #  
  fi 
  echo "channel is : " $ch
  echo "model is: " $model

  if [[ "$ch" == "zz_norm_0" ]]; then
    #range="289.4985,489.4985"
    #range="189.4985,1000.4985"
    #range="189.4985,700.4985"
    range="0.0,700.4985"
  elif [[ "$ch" == "zz_norm_2e2mu" || "$ch" == "zz_norm_4mu" ]]; then
    range="0.0,250.0"
  elif [[ "$ch" == "zz_norm_4e" ]]; then
    range="0.0,100.0"
  elif [[ "$ch" == "SigmaBin0" || "$ch" == "r2e2muBin0" || "$ch" == "r4muBin0"|| "$ch" == "r4eBin0" ]]; then
    range="0.0,5.0"
  fi

  echo "range is : " $range
# with systematics
    #combine -n mass4l_$ch -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_$model\_exp.root -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=0.0,5.0 --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4
    #echo 'mass4l_$ch -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_$model$2\_exp.root -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4'
    combine -n mass4l_$ch -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_$model$2\_exp.root -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4
# no systematics, full Run 2 ZZ floating
    if [[ "$1" == "Full" && "$2"!="" ]];
     then
#    echo "running stat. fit for full Run 2"
    #combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_12016,CMS_fakeH_p1_22016,CMS_fakeH_p1_32016,CMS_fakeH_p3_12016,CMS_fakeH_p3_22016,CMS_fakeH_p3_32016,CMS_fakeH_p1_12017,CMS_fakeH_p1_22017,CMS_fakeH_p1_32017,CMS_fakeH_p3_12017,CMS_fakeH_p3_22017,CMS_fakeH_p3_32017,CMS_fakeH_p1_12018,CMS_fakeH_p1_22018,CMS_fakeH_p1_32018,CMS_fakeH_p3_12018,CMS_fakeH_p3_22018,CMS_fakeH_p3_32018,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_2016,CMS_hzz4e_Zjets_2016,CMS_hzz4mu_Zjets_2016,CMS_hzz2e2mu_Zjets_2017,CMS_hzz4e_Zjets_2017,CMS_hzz4mu_Zjets_2017,CMS_hzz2e2mu_Zjets_2018,CMS_hzz4e_Zjets_2018,CMS_hzz4mu_Zjets_2018,lumi_13TeV_2016_uncorrelated,lumi_13TeV_2017_uncorrelated,lumi_13TeV_2018_uncorrelated,lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18,norm_fakeH,CMS_zz4l_sigma_e_sig_2016,CMS_zz4l_sigma_e_sig_2017,CMS_zz4l_sigma_e_sig_2018,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_n_sig_1_2016,CMS_zz4l_n_sig_1_2017,CMS_zz4l_n_sig_1_2018,CMS_zz4l_n_sig_2_2016,CMS_zz4l_n_sig_2_2017,CMS_zz4l_n_sig_2_2018,CMS_zz4l_n_sig_3_2016,CMS_zz4l_n_sig_3_2017,CMS_zz4l_n_sig_3_2018,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_sig_2018
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_2016,CMS_hzz4e_Zjets_2016,CMS_hzz4mu_Zjets_2016,CMS_hzz2e2mu_Zjets_2017,CMS_hzz4e_Zjets_2017,CMS_hzz4mu_Zjets_2017,CMS_hzz2e2mu_Zjets_2018,CMS_hzz4e_Zjets_2018,CMS_hzz4mu_Zjets_2018,lumi_13TeV_2016_uncorrelated,lumi_13TeV_2017_uncorrelated,lumi_13TeV_2018_uncorrelated,lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18,norm_fakeH,CMS_zz4l_sigma_e_sig_2016,CMS_zz4l_sigma_e_sig_2017,CMS_zz4l_sigma_e_sig_2018,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_n_sig_1_2016,CMS_zz4l_n_sig_1_2017,CMS_zz4l_n_sig_1_2018,CMS_zz4l_n_sig_2_2016,CMS_zz4l_n_sig_2_2017,CMS_zz4l_n_sig_2_2018,CMS_zz4l_n_sig_3_2016,CMS_zz4l_n_sig_3_2017,CMS_zz4l_n_sig_3_2018,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_sig_2018
    elif [[ "$1" == "Full" && "$2"=="" ]]; 
    then    # full Run 2 ZZ not floating
#    echo "running stat. fit for full Run 2"
    #combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_12016,CMS_fakeH_p1_22016,CMS_fakeH_p1_32016,CMS_fakeH_p3_12016,CMS_fakeH_p3_22016,CMS_fakeH_p3_32016,CMS_fakeH_p1_12017,CMS_fakeH_p1_22017,CMS_fakeH_p1_32017,CMS_fakeH_p3_12017,CMS_fakeH_p3_22017,CMS_fakeH_p3_32017,CMS_fakeH_p1_12018,CMS_fakeH_p1_22018,CMS_fakeH_p1_32018,CMS_fakeH_p3_12018,CMS_fakeH_p3_22018,CMS_fakeH_p3_32018,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_2016,CMS_hzz4e_Zjets_2016,CMS_hzz4mu_Zjets_2016,CMS_hzz2e2mu_Zjets_2017,CMS_hzz4e_Zjets_2017,CMS_hzz4mu_Zjets_2017,CMS_hzz2e2mu_Zjets_2018,CMS_hzz4e_Zjets_2018,CMS_hzz4mu_Zjets_2018,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_2016_uncorrelated,lumi_13TeV_2017_uncorrelated,lumi_13TeV_2018_uncorrelated,lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_2016,CMS_zz4l_sigma_e_sig_2017,CMS_zz4l_sigma_e_sig_2018,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_n_sig_1_2016,CMS_zz4l_n_sig_1_2017,CMS_zz4l_n_sig_1_2018,CMS_zz4l_n_sig_2_2016,CMS_zz4l_n_sig_2_2017,CMS_zz4l_n_sig_2_2018,CMS_zz4l_n_sig_3_2016,CMS_zz4l_n_sig_3_2017,CMS_zz4l_n_sig_3_2018,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_sig_2018
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_2016,CMS_hzz4e_Zjets_2016,CMS_hzz4mu_Zjets_2016,CMS_hzz2e2mu_Zjets_2017,CMS_hzz4e_Zjets_2017,CMS_hzz4mu_Zjets_2017,CMS_hzz2e2mu_Zjets_2018,CMS_hzz4e_Zjets_2018,CMS_hzz4mu_Zjets_2018,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_2016_uncorrelated,lumi_13TeV_2017_uncorrelated,lumi_13TeV_2018_uncorrelated,lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_2016,CMS_zz4l_sigma_e_sig_2017,CMS_zz4l_sigma_e_sig_2018,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_n_sig_1_2016,CMS_zz4l_n_sig_1_2017,CMS_zz4l_n_sig_1_2018,CMS_zz4l_n_sig_2_2016,CMS_zz4l_n_sig_2_2017,CMS_zz4l_n_sig_2_2018,CMS_zz4l_n_sig_3_2016,CMS_zz4l_n_sig_3_2017,CMS_zz4l_n_sig_3_2018,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_sig_2018
    elif [[ "$1" != "Full" && "$2"!="" ]]; 
    then # for an year and  ZZ floating
#    echo "running stat. fit for 1" $1
    #combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_1$1,CMS_fakeH_p1_2$1,CMS_fakeH_p1_3$1,CMS_fakeH_p3_1$1,CMS_fakeH_p3_2$1,CMS_fakeH_p3_3$1,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_$1,CMS_hzz4e_Zjets_$1,CMS_hzz4mu_Zjets_$1,lumi_13TeV_$1\_uncorrelated,norm_fakeH,CMS_zz4l_sigma_e_sig_$1,CMS_zz4l_sigma_m_sig_$1,CMS_zz4l_n_sig_1_$1,CMS_zz4l_n_sig_2_$1,CMS_zz4l_n_sig_3_$1,CMS_zz4l_mean_e_sig_$1,CMS_zz4l_mean_m_sig_$1   # FIXME
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_$1,CMS_hzz4e_Zjets_$1,CMS_hzz4mu_Zjets_$1,lumi_13TeV_$1\_uncorrelated,norm_fakeH,CMS_zz4l_sigma_e_sig_$1,CMS_zz4l_sigma_m_sig_$1,CMS_zz4l_n_sig_1_$1,CMS_zz4l_n_sig_2_$1,CMS_zz4l_n_sig_3_$1,CMS_zz4l_mean_e_sig_$1,CMS_zz4l_mean_m_sig_$1   # FIXME
    elif [[ "$1" != "Full" && "$2"=="" ]]; 
    then  # for an year and ZZ not floating
#    echo "running stat. fit for 1" $1
    #combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_1$1,CMS_fakeH_p1_2$1,CMS_fakeH_p1_3$1,CMS_fakeH_p3_1$1,CMS_fakeH_p3_2$1,CMS_fakeH_p3_3$1,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_$1,CMS_hzz4e_Zjets_$1,CMS_hzz4mu_Zjets_$1,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_$1\_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_$1,CMS_zz4l_sigma_m_sig_$1,CMS_zz4l_n_sig_1_$1,CMS_zz4l_n_sig_2_$1,CMS_zz4l_n_sig_3_$1,CMS_zz4l_mean_e_sig_$1,CMS_zz4l_mean_m_sig_$1   # FIXME
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model$2\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=$range --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_$1,CMS_hzz4e_Zjets_$1,CMS_hzz4mu_Zjets_$1,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_$1\_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_$1,CMS_zz4l_sigma_m_sig_$1,CMS_zz4l_n_sig_1_$1,CMS_zz4l_n_sig_2_$1,CMS_zz4l_n_sig_3_$1,CMS_zz4l_mean_e_sig_$1,CMS_zz4l_mean_m_sig_$1   # FIXME
    fi;
done;
done
#
