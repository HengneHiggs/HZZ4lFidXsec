

import sys, os, pwd, commands
from subprocess import *

from ROOT import *

from array import array

#observables = ['pT4l','rapidity4l','njets_reco_pt30_eta4p7','njets_reco_pt30_eta2p5','massZ1','massZ2','cosThetaStar','cosTheta2','Phi','Phi1','cosTheta1']
observables = ['pT4l','rapidity4l','massZ2','cosThetaStar','cosTheta2','Phi','Phi1','cosTheta1']

#observables = ['njets_reco_pt30_eta4p7']
#observables = ['njets_reco_pt30_eta4p7','njets_reco_pt30_eta2p5']
def processCmd(cmd, quiet = 0):
    output=""
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        print line,
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))
    return output


print "observable","-2.0 delta ln L","pvalue"
for obsName in observables:
   

    #cmd = 'grep -m 1 "data \[" testz4l_SMZ4l_'+obsName+'_resultsOnly_finalplotsOnly_floatPOIs_fixMZ_tchanCorr.log | sed "s~data \[~~g" | sed "s~, ~ ~g" | sed "s~\]~~g" | awk {\'print "SigmaBin0="$1",SigmaBin1="$2",SigmaBin2="$3",SigmaBin3="$4\'} '
    cmd = 'grep -m 1 "SMZ4l \[" testz4l_SMZ4l_'+obsName+'_resultsOnly_finalplotsOnly_floatPOIs_fixMZ_tchanCorr.log | sed "s~SMZ4l \[~~g" | sed "s~, ~ ~g" | sed "s~\]~~g" | awk {\'print i"SigmaBin0="$1",SigmaBin1="$2",SigmaBin2="$3",SigmaBin3="$4\'} '
    setvalue = processCmd(cmd)
    setvalue.rstrip()

    cmd = 'combine -n _Z4l_SMZ4l_'+obsName+'_floatPOIs_fixMZ_all_8TeV_xs_v3_BestFit ' 
    cmd += '-M MultiDimFit -m 91.1876  --saveWorkspace  -D data_obs '
    cmd += ' Combine_Z4l_SMZ4l_'+obsName+'_floatPOIs_fixMZ_all_8TeV_xs_v3.root '
    cmd += ' --freezeNuisances MH  '
    cmd += '-P SigmaBin0 -P SigmaBin1 -P SigmaBin2 -P SigmaBin3 --floatOtherPOIs=1 --saveNLL'
    cmd += ' --setPhysicsModelParameters MH=91.1876,'+setvalue

    print cmd
    os.system(cmd)

    cmd = 'grep -m 1 "SMZ4l \[" testz4l_SMZ4l_'+obsName+'_resultsOnly_finalplotsOnly_floatPOIs_fixMZ_tchanCorr.log | sed "s~SMZ4l \[~~g" | sed "s~, ~ ~g" | sed "s~\]~~g" | awk {\'print i"SigmaBin0="$1",SigmaBin1="$2",SigmaBin2="$3",SigmaBin3="$4\'} '

    setvalue = processCmd(cmd)
    setvalue.rstrip()

    cmd = 'combine -n _Z4l_SMZ4l_'+obsName+'_floatPOIs_fixMZ_all_8TeV_xs_v3_SM '
    cmd += '-M MultiDimFit -m 91.1876  --saveWorkspace  -D data_obs '
    cmd += ' Combine_Z4l_SMZ4l_'+obsName+'_floatPOIs_fixMZ_all_8TeV_xs_v3.root '
    cmd += ' --freezeNuisances MH,SigmaBin0,SigmaBin1,SigmaBin2,SigmaBin3  '
    cmd += '-P SigmaBin0 -P SigmaBin1 -P SigmaBin2 -P SigmaBin3 --floatOtherPOIs=1 --saveNLL'
    cmd += ' --setPhysicsModelParameters MH=91.1876,'+setvalue

    print cmd
    os.system(cmd)
    
    f_bestfit = TFile("higgsCombine_Z4l_SMZ4l_"+obsName+"_floatPOIs_fixMZ_all_8TeV_xs_v3_BestFit.MultiDimFit.mH91.1876.root","READ")
    limit_bestfit = f_bestfit.Get("limit") 
    limit_bestfit.GetEntry(0)  
    nll_bestfit = limit_bestfit.nll
        
    f_sm = TFile("higgsCombine_Z4l_SMZ4l_"+obsName+"_floatPOIs_fixMZ_all_8TeV_xs_v3_SM.MultiDimFit.mH91.1876.root","READ")
    limit_sm = f_sm.Get("limit")
    limit_sm.GetEntry(0)
    nll_sm = limit_sm.nll
        
    chi2 = -2.0*(nll_bestfit-nll_sm)

    #pval = ROOT.TMath.Prob(chi2,4)
    pval = TMath.Prob(chi2,4)

    print "P-Value: ",obsName,chi2,pval
