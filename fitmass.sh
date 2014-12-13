

combine -n _Mass_Ratio_SM_125_mass4l_Data_floatPOIs_all_8TeV_xs_v1 \
-D data_obs \
-M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v1.root \
-m 125.0  --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace \
--setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124,SigmaH=1.16128032747,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,RatioSigmaHoZ=0.253639146015,RatioSigmaHoZ4e=0.237491352122,RatioSigmaHoZ4mu=0.184642509883 --floatOtherPOIs=1 \
-P MH -P DeltaMHmZ

combine -n _Mass_Ratio_SM_125_mass4l_Data_floatPOIs_all_8TeV_xs_v2 \
-D data_obs \
-M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2.root \
-m 125.0  --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace \
--setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,SigmaH2e2mu=0.540451422836,RatioSigmaHoZ4e=0.237491352122,RatioSigmaHoZ4mu=0.184642509883,RatioSigmaHoZ2e2mu=0.343956946258 --floatOtherPOIs=1 \
-P MH -P DeltaMHmZ 

#combine -n _Mass_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2 \
#-M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2.root -m 125.0 \
# --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace -t -1 --setPhysicsModelParameters \
#MH=125.0,DeltaMHmZ=33.8124,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,SigmaH2e2mu=0.540451422836,RatioSigmaHoZ4e=0.218808136155,RatioSigmaHoZ4mu=0.174952081717,RatioSigmaHoZ2e2mu=0.314525444755 \
# --floatOtherPOIs=0 \
#-P MH -P DeltaMHmZ  --saveToys


#combine -n _Mass_Ratio_SM_125_mass4l_data_floatPOIs_all_8TeV_xs_v2 \
#-D data_obs \
#-M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2.root -m 125.0 \
# --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace --setPhysicsModelParameters \
#MH=125.0,DeltaMHmZ=33.8124,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,SigmaH2e2mu=0.540451422836,RatioSigmaHoZ4e=0.218808136155,RatioSigmaHoZ4mu=0.174952081717,RatioSigmaHoZ2e2mu=0.314525444755 \
# --floatOtherPOIs=1 \
#-P MH -P DeltaMHmZ  

#combine -n _Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2 -M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v2.root -m 125.0  --saveWorkspace -t -1 --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,SigmaH2e2mu=0.540451422836,RatioSigmaHoZ4e=0.218808136155,RatioSigmaHoZ4mu=0.174952081717,RatioSigmaHoZ2e2mu=0.314525444755 --floatOtherPOIs=1  --saveToys

#combine -n _Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v1 -M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v1.root -m 125.0  --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace -t -1 --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124,SigmaH=1.16128032747,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,RatioSigmaHoZ=0.235587726409,RatioSigmaHoZ4e=0.218808136155,RatioSigmaHoZ4mu=0.174952081717 --floatOtherPOIs=1 -P SigmaH -P RatioSigmaHoZ  --saveToys

#combine -n _Mass_Ratio_SM_125_mass4l_data_floatPOIs_all_8TeV_xs_v1 \
#-D data_obs \
#-M MultiDimFit Combine_Ratio_SM_125_mass4l_Asimov_floatPOIs_all_8TeV_xs_v1.root -m 125.0  \
#--algo=singles --cl=0.68 --robustFit=1 --saveWorkspace --setPhysicsModelParameters \
#MH=125.0,DeltaMHmZ=33.8124,SigmaH=1.16128032747,SigmaH4e=0.29466792975,SigmaH4mu=0.326160974886,RatioSigmaHoZ=0.235587726409,RatioSigmaHoZ4e=0.218808136155,RatioSigmaHoZ4mu=0.174952081717 \
#--floatOtherPOIs=1 -P MH -P DeltaMHmZ

