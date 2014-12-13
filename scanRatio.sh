#!/bin/sh

#POIS="RatioSigmaHoZ SigmaH"
POIS="RatioSigmaHoZ4e RatioSigmaHoZ4mu RatioSigmaHoZ2e2mu SigmaH4e SigmaH4mu SigmaH2e2mu"

vers='v2'
for poi in $POIS; 
do
 tag="_Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_${vers}_${poi}"

combine -n ${tag} -M MultiDimFit -m 125.0 --saveWorkspace  -D data_obs \
Combine_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_${vers}.root \
 --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124 \
 -P ${poi} --setPhysicsModelParameterRanges ${poi}=0.0,3.0  \
 --floatOtherPOIs=1 --algo=grid --points=100 \
&> Combine_Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_${vers}_${poi}.log &

 
done

