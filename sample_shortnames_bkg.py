#background_samples = {
#    'ZZTo2e2mu_powheg':'ZZTo2e2mu_mZZ95-160.root',
#    'ZZTo4e_powheg':'ZZTo4e_mZZ95-160.root',
#    'ZZTo4mu_powheg':'ZZTo4mu_mZZ95-160.root',
#    'ggZZ_2e2mu_MCFM67':'GluGluTo2e2mu_Contin_8TeV-MCFM67.root',
#    'ggZZ_4mu_MCFM67':'GluGluTo4mu_Contin_8TeV-MCFM67.root',
#    'ggZZ_4e_MCFM67':'GluGluTo4e_Contin_8TeV-MCFM67.root',
#    'ZX4l_CR':'Data_ZX.root'
#}

background_samples = {
    'ZZTo2e2mu_powheg':'ZZTo2e2mu_8TeV_mll8_mZZ95-160-powheg15-pythia6.root',
    'ZZTo4e_powheg':'ZZTo4e_8TeV_mll8_mZZ95-160-powheg15-pythia6.root',
    'ZZTo4mu_powheg':'ZZTo4mu_8TeV_mll8_mZZ95-160-powheg15-pythia6.root',
    'ggZZ_2e2mu':'GluGluTo2L2Lprime_Contin_8TeV-gg2vv315-pythia6.root',
    'ggZZ_4mu':'GluGluToZZTo4L_8TeV-gg2zz-pythia6.root',
    'ggZZ_4e':'GluGluToZZTo4L_8TeV-gg2zz-pythia6.root',
    'ggZZ_2e2mu_MCFM67':'GluGluTo2e2mu_Contin_8TeV-MCFM67-pythia6.root',
    'ggZZ_4mu_MCFM67':'GluGluTo4mu_Contin_8TeV-MCFM67-pythia6.root',
    'ggZZ_4e_MCFM67':'GluGluTo4e_Contin_8TeV-MCFM67-pythia6.root',
    'ZX4l_CR':'Data_ZX.root',
    'ZZTo2e2mu_powheg_tchan':'ZZTo2e2mu_8TeV-powheg-pythia6_mll1_tchan.root',
    'ZZTo4e_powheg_tchan':'ZZTo4e_8TeV-powheg-pythia6_mll1_tchan.root',
    'ZZTo4mu_powheg_tchan':'ZZTo4mu_8TeV-powheg-pythia6_mll1_tchan.root'
}

sample_shortnames_bkg = {
  #'ZZTo4e_8TeV-powheg-pythia6':'SMZ4l',
  #'ZZTo4mu_8TeV-powheg-pythia6':'SMZ4l',
  #'ZZTo2e2mu_8TeV-powheg-pythia6':'SMZ4l',
  'ZZTo4e_8TeV-powheg-pythia6':'qqZZst',
  'ZZTo4mu_8TeV-powheg-pythia6':'qqZZst',
  'ZZTo2e2mu_8TeV-powheg-pythia6':'qqZZst',
  'ZZTo4e_8TeV-powheg-pythia6_mll1_tchan':'qqZZtchan',
  'ZZTo4mu_8TeV-powheg-pythia6_mll1_tchan':'qqZZtchan',
  'ZZTo2e2mu_8TeV-powheg-pythia6_mll1_tchan':'qqZZtchan',
  #'GluGluToZZTo2L2L_TuneZ2star_8TeV-gg2zz-pythia6':'ggZZ',
  'GluGluTo2L2Lprime_Contin_8TeV-gg2vv315-pythia6':'ggZZ',
  'GluGluToZZTo4L_8TeV-gg2zz-pythia6':'ggZZ'
}

process_to_samples = {
    'SMZ4l': {'ZZTo4e_8TeV-powheg-pythia6', 'ZZTo4mu_8TeV-powheg-pythia6', 'ZZTo2e2mu_8TeV-powheg-pythia6'},
    'qqZZtchan': {'ZZTo4e_8TeV-powheg-pythia6_mll1_tchan', 'ZZTo4mu_8TeV-powheg-pythia6_mll1_tchan', 'ZZTo2e2mu_8TeV-powheg-pythia6_mll1_tchan'}
}
