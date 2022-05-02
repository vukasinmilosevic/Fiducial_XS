# mass4l
#nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4mu"  --year="2016" --bkg="zz" >& effs_mass4l_4mu_zzfloating_2016.log & 
#nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4e"  --year="2016" --bkg="zz" >& effs_mass4l_4e_zzfloating_2016.log &
#nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "2e2mu"  --year="2016" --bkg="zz" >& effs_mass4l_2e2mu_zzfloating_2016.log &
#nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4l"  --year="2016" --bkg="zz" >& effs_mass4l_4l_zzfloating_2016.log &

nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4mu"  --year="2016"  >& effs_mass4l_4mu_extended_2016.log & 
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4e"  --year="2016"  >& effs_mass4l_4e_extended_2016.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "2e2mu"  --year="2016"  >& effs_mass4l_2e2mu_extended_2016.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" -c "4l"  --year="2016"  >& effs_mass4l_4l_extended_2016.log &

#nohup python -u getUnc_Unc.py -l -q -b --obsName="mass4l" --obsBins="|105.0|160.0|" --year="2016" --bkg="zz" >& unc_mass4l_zzfloating_2016.unc &


