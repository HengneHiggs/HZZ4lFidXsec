#!/bin/sh


combine -n _Z4l_SMZ4l_njets_reco_pt30_eta2p5_floatPOIs_fixMZ_all_8TeV_xs_v3_result_Scan_SigmaBin2 \
-M MultiDimFit \
Combine_Z4l_SMZ4l_njets_reco_pt30_eta2p5_floatPOIs_fixMZ_all_8TeV_xs_v3_result.root \
-m 91.1876  \
--saveWorkspace  -D data_obs \
--setPhysicsModelParameters MH=91.1876  --freezeNuisances MH  \
--setPhysicsModelParameterRanges SigmaBin3=0.0,0.2 \
-P SigmaBin3 \
--floatOtherPOIs=1 \
--algo=grid --points=100
