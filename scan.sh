

#combine -n _Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1_SigmaH \
#Combine_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1.root \
#-P SigmaH --setPhysicsModelParameterRanges SigmaH=0.0,2.0 \

combine -n _Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v2_SigmaH4mu \
-M MultiDimFit \
Combine_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v2.root \
-m 125.0 \
--saveWorkspace  -D data_obs \
--setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124 \
-P SigmaH4mu --setPhysicsModelParameterRanges SigmaH4mu=0.0,3.0 \
--floatOtherPOIs=1 \
--algo=grid --points=100


#combine -n _Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1 -M MultiDimFit Combine_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1.root -m 125.0  --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace  -D data_obs --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124  --floatOtherPOIs=1 -P SigmaH -P RatioSigmaHoZ

#combine -n njets_reco_pt30_eta4p7_SigmaBin0 -M MultiDimFit SM_125_all_8TeV_xs_njets_reco_pt30_eta4p7_bin_v3_exp.root -m 125.0   --setPhysicsModelParameters MH=125.0 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.0,125.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=10000
