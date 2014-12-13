CB_mean = {} 
CB_sigma = {} 
folding = {'ggH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggHToZG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_125_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH7_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH7_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq1M_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_125_4l_mass4l_genbin0_recobin0': 1.0, 'qq1P_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_126_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2MH9_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_126_4e_mass4l_genbin0_recobin0': 1.0, 'gg2MH10_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_126_4e_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'jjH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2HM_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'VBF_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'gg2MH10_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH2_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'jjH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_126_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_125_4mu_mass4l_genbin0_recobin0': 1.0, 'WH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH2_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_125_4l_mass4l_genbin0_recobin0': 1.0, 'qq2HM_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ZH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_125_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_126_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH7_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_125_4l_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_125_4mu_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_125_4l_mass4l_genbin0_recobin0': 1.0, 'gg2MH9_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_126_4l_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_125_4l_mass4l_genbin0_recobin0': 1.0, 'ggH0MToZG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggHToGG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH2_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq2MH10_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_126_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH2_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH6_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_125_4e_mass4l_genbin0_recobin0': 1.0, 'qq2MH10_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggHToZG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ZH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq2HM_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggHToGG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH0MToZG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH6_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH7_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2HP_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH3_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'qq2MH9_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH7_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_125_4l_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_126_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2HP_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH6_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'WH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_125_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH6_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_126_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH6_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'gg2PH3_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH0MToGG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_125_4e_mass4l_genbin0_recobin0': 1.0, 'qq1P_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggHToZG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ZH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_125_4e_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'jjH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_125_4e_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_126_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_126_4mu_mass4l_genbin0_recobin0': 1.0, 'WH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH3_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_125_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_126_4e_mass4l_genbin0_recobin0': 1.0, 'qq2MH9_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH3_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'gg2MH9_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_126_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH7_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH0MToZG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH6_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_126_4l_mass4l_genbin0_recobin0': 1.0, 'gg2MH10_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_126_4e_mass4l_genbin0_recobin0': 1.0, 'qq2MH10_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH3_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2HM_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq1M_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_126_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_126_4mu_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_126_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_126_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH3_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_125_4mu_mass4l_genbin0_recobin0': 1.0, 'VBF_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2HP_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq1M_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH2_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq1P_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_126_4l_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_125_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH0MToGG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_125_4e_mass4l_genbin0_recobin0': 1.0, 'ggH0MToGG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2HP_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'qq2MH9_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_126_4l_mass4l_genbin0_recobin0': 1.0, 'ggHToZG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'gg2MH9_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'qq2PH3_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_126_4mu_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH3_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_125_4mu_mass4l_genbin0_recobin0': 1.0, 'ZH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'jjH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH2_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH7_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggHToGG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'VBF_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'qq1M_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_126_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2MH9_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg15_JHUgen_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH0MToGG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2MH10_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH6_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'WH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_126_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_125_4l_mass4l_genbin0_recobin0': 1.0, 'ggH_powheg_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2MH10_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_125_4mu_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_125_4e_mass4l_genbin0_recobin0': 1.0, 'WH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq1P_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'ggHToGG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ttH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 1.0, 'qq2PH2_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'gg2PH7_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ggH_minloHJJ_125_4mu_mass4l_genbin0_recobin0': 1.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 1.0, 'VBF_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'qq2PH2_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 1.0, 'gg2PH6_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 1.0, 'ZH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 1.0, 'ggH0MToZG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 1.0, 'VBF_powheg_126_2e2mu_mass4l_genbin0_recobin0': 1.0} 
dfolding = {'ggH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggHToZG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_125_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH7_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH7_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq1M_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_125_4l_mass4l_genbin0_recobin0': 0.0, 'qq1P_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_126_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2MH9_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_126_4e_mass4l_genbin0_recobin0': 0.0, 'gg2MH10_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_126_4e_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'jjH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2HM_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'VBF_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'gg2MH10_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH2_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'jjH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_126_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_125_4mu_mass4l_genbin0_recobin0': 0.0, 'WH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH2_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_125_4l_mass4l_genbin0_recobin0': 0.0, 'qq2HM_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ZH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_125_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_126_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH7_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_125_4l_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_125_4mu_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_125_4l_mass4l_genbin0_recobin0': 0.0, 'gg2MH9_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_126_4l_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_125_4l_mass4l_genbin0_recobin0': 0.0, 'ggH0MToZG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggHToGG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH2_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq2MH10_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_126_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH2_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH6_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_125_4e_mass4l_genbin0_recobin0': 0.0, 'qq2MH10_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggHToZG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ZH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq2HM_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggHToGG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH0MToZG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH6_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH7_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2HP_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH3_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'qq2MH9_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH7_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_125_4l_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_126_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2HP_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH6_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'WH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_125_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH6_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_126_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH6_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'gg2PH3_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH0MToGG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_125_4e_mass4l_genbin0_recobin0': 0.0, 'qq1P_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggHToZG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ZH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_125_4e_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'jjH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_125_4e_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_126_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_126_4mu_mass4l_genbin0_recobin0': 0.0, 'WH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH3_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_125_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_126_4e_mass4l_genbin0_recobin0': 0.0, 'qq2MH9_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH3_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'gg2MH9_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_126_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH7_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH0MToZG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH6_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_126_4l_mass4l_genbin0_recobin0': 0.0, 'gg2MH10_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_126_4e_mass4l_genbin0_recobin0': 0.0, 'qq2MH10_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH3_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2HM_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq1M_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_126_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_126_4mu_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_126_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_126_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH3_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_125_4mu_mass4l_genbin0_recobin0': 0.0, 'VBF_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2HP_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq1M_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH2_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq1P_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_126_4l_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_125_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH0MToGG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_125_4e_mass4l_genbin0_recobin0': 0.0, 'ggH0MToGG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2HP_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'qq2MH9_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_126_4l_mass4l_genbin0_recobin0': 0.0, 'ggHToZG_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'gg2MH9_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'qq2PH3_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_126_4mu_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH3_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_125_4mu_mass4l_genbin0_recobin0': 0.0, 'ZH_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'jjH_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH2_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH7_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggHToGG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'VBF_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'qq1M_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph90_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_126_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2MH9_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg15_JHUgen_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH0MToGG_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2MH10_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH6_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'WH_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_126_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_125_4l_mass4l_genbin0_recobin0': 0.0, 'ggH_powheg_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2MH10_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_125_4mu_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_125_4e_mass4l_genbin0_recobin0': 0.0, 'WH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq1P_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'ggHToGG_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ttH_pythia_125_2e2mu_mass4l_genbin0_recobin0': 0.0, 'qq2PH2_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'gg2PH7_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ggH_minloHJJ_125_4mu_mass4l_genbin0_recobin0': 0.0, 'qq1Mf05ph01Pf05ph0_JHUgen_125p6_4mu_mass4l_genbin0_recobin0': 0.0, 'VBF_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'qq2PH2_JHUgen_125p6_2e2mu_mass4l_genbin0_recobin0': 0.0, 'gg2PH6_JHUgen_125p6_4e_mass4l_genbin0_recobin0': 0.0, 'ZH_pythia_126_2e2mu_mass4l_genbin0_recobin0': 0.0, 'ggH0MToZG_JHUgen_125p6_4l_mass4l_genbin0_recobin0': 0.0, 'VBF_powheg_126_2e2mu_mass4l_genbin0_recobin0': 0.0} 