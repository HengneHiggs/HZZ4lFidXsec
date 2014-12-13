#!/bin/sh

# _Z4l_SMZ4l_cosTheta1_floatPOIs_fixMZ_all_8TeV_xs_v3 -M MultiDimFit Combine_Z4l_SMZ4l_cosTheta1_floatPOIs_fixMZ_all_8TeV_xs_v3.root

combine -n _Z4l_SMZ4l_cosTheta1_floatPOIs_fixMZ_all_8TeV_xs_v3_result_Scan_SigmaBin2 \
-M MultiDimFit \
Combine_Z4l_SMZ4l_cosTheta1_floatPOIs_fixMZ_all_8TeV_xs_v3_result.root \
-m 91.1876  \
--saveWorkspace  -D data_obs \
--setPhysicsModelParameters MH=91.1876  --freezeNuisances MH  \
--setPhysicsModelParameterRanges SigmaBin1=0.0,3.0 \
-P SigmaBin1 \
--floatOtherPOIs=1 \
--algo=grid --points=100
