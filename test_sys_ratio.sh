#!/bin/sh


combine -n _Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1_nosys \
-M MultiDimFit \
Combine_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1.root \
-m 125.0  \
--algo=singles \
--cl=0.68 --robustFit=1 \
--saveWorkspace \
 -D data_obs \
--setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124 \
--setPhysicsModelParameterRange SigmaH=0.0,2.0:RatioSigmaHoZ=0.0,1.0:\
SigmaH4e=0.0,1.0:SigmaH4mu=0.0,2.0:\
RatioSigmaHoZ4e=0.0,1.0:RatioSigmaHoZ4mu=0.0,1.0\
 --floatOtherPOIs=1 \
#--systematics=0 \
-P SigmaH \
-P RatioSigmaHoZ
