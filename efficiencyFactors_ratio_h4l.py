import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames import *

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)
    
### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    # input options
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--modelName',dest='MODELNAME',type='string',default='SM', help='Name of the Higgs production or spin-parity model, default is "SM", supported: "SM", "ggH", "VBF", "WH", "ZH", "ttH", "exotic","all"')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "mass4l", "pT4l", "massZ2", "rapidity4l", "cosThetaStar", "nets_reco_pt30_eta4p7"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('-f', '--doFit', action="store_true", dest='DOFIT', default=False, help='doFit, default false')
    parser.add_option('-p', '--doPlots', action="store_true", dest='DOPLOTS', default=False, help='doPlots, default false')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
                       
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

doFit = opt.DOFIT
doPlots = opt.DOPLOTS

if (not os.path.exists("plots") and doPlots):
    os.system("mkdir plots")

from ROOT import *
from LoadData_dsperka import *
LoadData(opt.SOURCEDIR)
save = ""

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    

if (opt.DOPLOTS and os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()

Histos = {}
wrongfrac = {}
dwrongfrac = {}
binfrac_wrongfrac = {}
dbinfrac_wrongfrac = {}
outfrac = {}
doutfrac = {}
binfrac_outfrac = {}
dbinfrac_outfrac = {}
outinratio = {}
doutinratio = {}
CB_mean_post = {}
CB_sigma_post = {}
CB_dmean_post = {}
CB_dsigma_post = {}
Landau_mean_post = {}
Landau_sigma_post = {}
#fidacc = {}
#dfidacc = {}
effrecotofid = {}
deffrecotofid = {}
#effreconotfid = {}
#deffreconotfid = {}
acceptance = {}
dacceptance = {}
acceptance_4l = {}
dacceptance_4l = {}
cfactor = {}
dcfactor = {}
lambdajesup = {}
lambdajesdn = {}
eff_fit = {}
deff_fit = {}
effanyreco = {}
deffanyreco = {}
folding = {}
dfolding = {}


nfid = {}
nfs = {}
nrecofid = {}
nreconotfid = {}

dnfid = {}
dnfs = {}
dnrecofid = {}
dnreconotfid = {}





def geteffs(channel, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin):    
    
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");
            
    recoweight = "eventMCWeight"
    #recoweight = "totalWeight"
    #recoweight = "1.0"

    obs_reco_low = obs_bins[recobin]
    obs_reco_high = obs_bins[recobin+1]

    obs_gen_low = obs_bins[genbin]
    obs_gen_high = obs_bins[genbin+1]

    obs_gen_lowest = obs_bins[0]
    obs_gen_highest = obs_bins[len(obs_bins)-1]
    
    i_sample = -1

    for Sample in List:

        if (not Sample in TreesPassedEvents): continue
        if (not TreesPassedEvents[Sample]): continue

        i_sample = i_sample+1

        cutobs_reco = "("+obs_reco+">="+str(obs_reco_low)+" && "+obs_reco+"<"+str(obs_reco_high)+")"
        cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+" && "+obs_gen+"<"+str(obs_gen_high)+")"
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            cutobs_reco_jesup = "("+obs_reco+"_jesup"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesup"+"<"+str(obs_reco_high)+")"
            cutobs_reco_jesdn = "("+obs_reco+"_jesdn"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesdn"+"<"+str(obs_reco_high)+")"
            
        cutobs_gen_otherfid = "(("+obs_gen+"<"+str(obs_gen_low)+" && "+obs_gen+">="+str(obs_gen_lowest)+") || ("+obs_gen+">="+str(obs_gen_high)+" && "+obs_gen+"<="+str(obs_gen_highest)+"))"
        #cutm4l_gen     = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
        cutm4l_gen     = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
        cutm4l_reco    = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")" 
        
        if (channel == "4l"):
            cutchan_gen      = "((abs(GENidLS3[GENlepIndex1])==11 || abs(GENidLS3[GENlepIndex1])==13) && (abs(GENidLS3[GENlepIndex3])==11 || abs(GENidLS3[GENlepIndex3])==13))"
            cutchan_gen_out  = "((Z1daughtersId==11 || Z1daughtersId==13) && (Z2daughtersId==11 || Z2daughtersId==13))"
            #cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+" && @GENidLS3.size()==4)"
            #cutm4l_reco      = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+" && nextraLep==0)"
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")"                        
        if (channel == "4e"):
            cutchan_gen      = "(abs(GENidLS3[GENlepIndex1])==11 && abs(GENidLS3[GENlepIndex3])==11)"
            cutchan_gen_out  = "(Z1daughtersId==11 && Z2daughtersId==11)"
            #cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+" && @GENidLS3.size()==4)"
            #cutm4l_reco      = "(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+" && nextraLep==0)" 
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+")"                        
        if (channel == "4mu"):
            cutchan_gen      = "(abs(GENidLS3[GENlepIndex1])==13 && abs(GENidLS3[GENlepIndex3])==13)"
            cutchan_gen_out  = "(Z1daughtersId==13 && Z2daughtersId==13)"
            #cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+" && @GENidLS3.size()==4)"
            #cutm4l_reco      = "(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+" && nextraLep==0)"
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+")"                        
        if (channel == "2e2mu"):
            #cutchan_gen      = "(abs(abs(GENidLS3[GENlepIndex1])-abs(GENidLS3[GENlepIndex3]))==2)"
            #cutchan_gen_out  = "(abs(Z1daughtersId-Z2daughtersId)==2)"
            cutchan_gen      = "((abs(GENidLS3[GENlepIndex1])==11 && abs(GENidLS3[GENlepIndex3])==13) ||(abs(GENidLS3[GENlepIndex1])==13 && abs(GENidLS3[GENlepIndex3])==11))"
            cutchan_gen_out  = "((Z1daughtersId==11 && Z2daughtersId==13) || (Z1daughtersId==13 && Z2daughtersId==11))" 
            #cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+" && @GENidLS3.size()==4)"    
            #cutm4l_reco      = "(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+" && nextraLep==0)"      
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+")"
                        

        cuth4l_gen  = "(GENisfromHLS3[GENlepIndex1]==1 && GENisfromHLS3[GENlepIndex2]==1 && GENisfromHLS3[GENlepIndex3]==1 && GENisfromHLS3[GENlepIndex4]==1)"
        cuth4l_reco = "(isFromH_L1==1 && MomID_L1==23 && isFromH_L2==1 && MomID_L2==23 && isFromH_L3==1 && MomID_L3==23 && isFromH_L4==1 && MomID_L4==23)"

        cutnoth4l_gen  = "(!"+cuth4l_gen+")"
        cutnoth4l_reco = "(!"+cuth4l_reco+")"
    
        if Sample.startswith("ZH"):
            if (channel == "4l"):
                cutchan_gen_out  = "((Z1momId==25 && Z2momId==25 && (Z1daughtersId==11 || Z1daughtersId==13) && (Z2daughtersId==11 || Z2daughtersId==13)) || (Z1momId==25 && Z3momId==25 && (Z1daughtersId==11 || Z3daughtersId==13) && (Z3daughtersId==11 || Z3daughtersId==13)) || (Z2momId==25 && Z3momId==25 && (Z2daughtersId==11 || Z2daughtersId==13) && (Z3daughtersId==11 || Z3daughtersId==13)))"
            if (channel == "4e"):
                cutchan_gen_out  = "((Z1momId==25 && Z2momId==25 && Z1daughtersId==11 && Z2daughtersId==11) || (Z1momId==25 && Z3momId==25 && Z1daughtersId==11 && Z3daughtersId==11) || (Z2momId==25 && Z3momId==25 && Z2daughtersId==11 && Z3daughtersId==11))"
            if (channel == "4mu"):
                cutchan_gen_out  = "((Z1momId==25 && Z2momId==25 && Z1daughtersId==13 && Z2daughtersId==13) || (Z1momId==25 && Z3momId==25 && Z1daughtersId==13 && Z3daughtersId==13) || (Z2momId==25 && Z3momId==25 && Z2daughtersId==13 && Z3daughtersId==13))"
            if (channel == "2e2mu"):
                cutchan_gen_out  = "((Z1momId==25 && (Z1daughtersId==11 || Z1daughtersId==13) && Z2momId==25 && (Z2daughtersId==11 || Z2daughtersId==13) && Z1daughtersId!=Z2daughtersId) || (Z1momId==25 && (Z1daughtersId==11 || Z1daughtersId==13) && Z3momId==25 && (Z3daughtersId==11 || Z3daughtersId==13) && Z1daughtersId!=Z3daughtersId) || (Z2momId==25 && (Z2daughtersId==11 || Z2daughtersId==13) && Z3momId==25 && (Z3daughtersId==11 || Z3daughtersId==13) && Z2daughtersId!=Z3daughtersId))"
 
                            
        if (recoweight=="totalWeight"): genweight = "19712.0*scaleWeight/"+str(nEvents[Sample])
        else: genweight = "1.0"

        shortname = sample_shortnames[Sample]
        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)

        # RECO level
        Histos[processBin+"reco_inc"] = TH1D(processBin+"reco_inc", processBin+"reco_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reco_inc"].Sumw2()        
        Histos[processBin+"recoh4l"] = TH1D(processBin+"recoh4l", processBin+"recoh4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4l"].Sumw2()
        Histos[processBin+"recoh4l_inc"] = TH1D(processBin+"recoh4l_inc", processBin+"recoh4l_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4l_inc"].Sumw2() 
        Histos[processBin+"reconoth4l"] = TH1D(processBin+"reconoth4l", processBin+"reconoth4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reconoth4l"].Sumw2() 
        Histos[processBin+"reconoth4l_inc"] = TH1D(processBin+"reconoth4l_inc", processBin+"reconoth4l_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reconoth4l_inc"].Sumw2()                 
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            Histos[processBin+"recoh4l_jesup"] = TH1D(processBin+"recoh4l_jesup", processBin+"recoh4l_jesup", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoh4l_jesup"].Sumw2()
            Histos[processBin+"recoh4l_jesdn"] = TH1D(processBin+"recoh4l_jesdn", processBin+"recoh4l_jesdn", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoh4l_jesdn"].Sumw2()
                                    
        # GEN level
        Histos[processBin+"fid"] = TH1D(processBin+"fid", processBin+"fid", m4l_bins, m4l_low, m4l_high)  
        Histos[processBin+"fid"].Sumw2()
        #Histos[processBin+"notfid_inc"] = TH1D(processBin+"notfid", processBin+"notfid_inc", m4l_bins, m4l_low, m4l_high) 
        #Histos[processBin+"notfid_inc"].Sumw2()
        Histos[processBin+"fs"] = TH1D(processBin+"fs", processBin+"fs", 100, 0, 10000)
        Histos[processBin+"fs"].Sumw2()
        
        # RECO and GEN level ( e.g. f(in) and f(out) )
        Histos[processBin+"recoh4lfid"] = TH1D(processBin+"recoh4lfid", processBin+"recoh4lfid", m4l_bins, m4l_low, m4l_high)        
        Histos[processBin+"recoh4lfid"].Sumw2()
        Histos[processBin+"anyrecoh4lfid"] = TH1D(processBin+"anyrecoh4lfid", processBin+"anyrecoh4lfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"anyrecoh4lfid"].Sumw2()                
        Histos[processBin+"recoh4lnotfid"] = TH1D(processBin+"recoh4lnotfid", processBin+"recoh4lnotfid", m4l_bins, m4l_low, m4l_high)        
        Histos[processBin+"recoh4lnotfid"].Sumw2() 
        Histos[processBin+"recoh4lnotfid_inc"] = TH1D(processBin+"recoh4lnotfid_inc", processBin+"recoh4lnotfid_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4lnotfid_inc"].Sumw2() 
        Histos[processBin+"recoh4lotherfid"] = TH1D(processBin+"recoh4lotherfid", processBin+"recoh4lotherfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4lotherfid"].Sumw2()
        
        # GEN level 
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fid","("+genweight+")*("+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+" && passedFiducialTopology==1 && "+cuth4l_gen+")","goff") 
        #TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"notfid_inc","("+genweight+")*("+cutchan_gen_out+" && (passedFiducialTopology==0 || !("+cuth4l_gen+") || !("+cutm4l_gen+")))","goff") 
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fs","("+genweight+")*("+cutchan_gen_out+")","goff")
        
        # RECO level 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"reco","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1)","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"reco_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1)","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4l","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+")","goff") 
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4l_jesup","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco_jesup+" && passedFullSelection==1 && "+cuth4l_reco+")","goff")
            TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4l_jesdn","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco_jesdn+" && passedFullSelection==1 && "+cuth4l_reco+")","goff")
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4l_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+")","goff")
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"reconoth4l","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutnoth4l_reco+")","goff")  
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"reconoth4l_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cutnoth4l_reco+")","goff") 

        # RECO and GEN level ( i.e. f(in) and f(out) ) 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4lnotfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && "+cutchan_gen_out+" && (passedFiducialTopology==0 || !("+cuth4l_gen+") || !("+cutm4l_gen+")) )","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4lnotfid_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && "+cutchan_gen_out+" && (passedFiducialTopology==0 || !("+cuth4l_gen+") || !("+cutm4l_gen+")) )","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4lfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialTopology==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen+")","goff")  
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoh4lotherfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialTopology==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen_otherfid+")","goff")
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"anyrecoh4lfid","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialTopology==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen+")","goff")
        
        if (Histos[processBin+"fs"].Integral()>0):
            acceptance[processBin] = Histos[processBin+"fid"].Integral()/Histos[processBin+"fs"].Integral()
            dacceptance[processBin] = sqrt(acceptance[processBin]*(1.0-acceptance[processBin])/Histos[processBin+"fs"].Integral())
            acceptance_4l[processBin] = Histos[processBin+"fid"].Integral()/nEvents[Sample]
            dacceptance_4l[processBin] = sqrt(acceptance_4l[processBin]*(1.0-acceptance_4l[processBin])/nEvents[Sample])                       
             
        else:
            acceptance[processBin] = -1.0
            dacceptance[processBin] = -1.0
            acceptance_4l[processBin] = -1.0
            dacceptance_4l[procesBin] = -1.0
            
        if (Histos[processBin+"reco_inc"].Integral()>0):
            wrongfrac[processBin] = Histos[processBin+"reconoth4l_inc"].Integral()/Histos[processBin+"reco_inc"].Integral()
            dwrongfrac[processBin] = sqrt(wrongfrac[processBin]*(1-wrongfrac[processBin])/Histos[processBin+"reco_inc"].Integral())
        else:
            wrongfrac[processBin] = -1.0
            dwrongfrac[processBin] = -1.0
            
        if (Histos[processBin+"reconoth4l_inc"].Integral()>0):
            binfrac_wrongfrac[processBin] = Histos[processBin+"reconoth4l"].Integral()/Histos[processBin+"reconoth4l_inc"].Integral()
            dbinfrac_wrongfrac[processBin] = sqrt(binfrac_wrongfrac[processBin]*(1-binfrac_wrongfrac[processBin])/Histos[processBin+"reconoth4l_inc"].Integral())
        else:
            binfrac_wrongfrac[processBin] = -1.0
            dbinfrac_wrongfrac[processBin] = -1.0
            
        if (Histos[processBin+"recoh4l_inc"].Integral()>0):
            outfrac[processBin] = Histos[processBin+"recoh4lnotfid_inc"].Integral()/Histos[processBin+"recoh4l_inc"].Integral()
            doutfrac[processBin] = sqrt(outfrac[processBin]*(1-outfrac[processBin])/Histos[processBin+"recoh4l_inc"].Integral())
        else:
            outfrac[processBin] =  -1.0
            doutfrac[processBin] = -1.0

        if (Histos[processBin+"recoh4lnotfid_inc"].Integral()>0):
            binfrac_outfrac[processBin] = Histos[processBin+"recoh4lnotfid"].Integral()/Histos[processBin+"recoh4lnotfid_inc"].Integral()
            dbinfrac_outfrac[processBin] = sqrt(binfrac_outfrac[processBin]*(1-binfrac_outfrac[processBin])/Histos[processBin+"recoh4lnotfid_inc"].Integral())
        else:
            binfrac_outfrac[processBin] =  -1.0
            dbinfrac_outfrac[processBin] = -1.0                                                                       

        if (Histos[processBin+"fid"].Integral()>=10.0):
            #effanyreco[processBin] =  Histos[processBin+"anyrecoh4lfid"].Integral()/Histos[processBin+"fid"].Integral()
            #deffanyreco[processBin] = sqrt(effanyreco[processBin]*(1-effanyreco[processBin])/Histos[processBin+"fid"].Integral())
            effrecotofid[processBin] = Histos[processBin+"recoh4lfid"].Integral()/Histos[processBin+"fid"].Integral()
            deffrecotofid[processBin] = sqrt(effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral())
            cfactor[processBin] = Histos[processBin+"recoh4l"].Integral()/Histos[processBin+"fid"].Integral()
        else:
            #effanyreco[processBin] = -1.0
            #deffanyreco[processBin] = -1.0
            effrecotofid[processBin] = -1.0
            deffrecotofid[processBin] = -1.0
            cfactor[processBin] = Histos[processBin+"recoh4l"].Integral()/1.0 # if N(fid) for a gen bin is 0.0, change it to 1.0
            #dcfactor[processBin] = -1.0

        if (Histos[processBin+"anyrecoh4lfid"].Integral()>0.0):
            folding[processBin] = Histos[processBin+"recoh4lfid"].Integral()/Histos[processBin+"anyrecoh4lfid"].Integral()
            dfolding[processBin] = sqrt(folding[processBin]*(1-folding[processBin])/Histos[processBin+"anyrecoh4lfid"].Integral())
        else:
            folding[processBin] = -1.0
            dfolding[processBin] = -1.0

        if ((Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral())>0.0):
            outinratio[processBin] = Histos[processBin+"recoh4lnotfid"].Integral()/(Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral())
            if (Histos[processBin+"recoh4lnotfid"].Integral()>0):
                doutinratio[processBin] = outinratio[processBin]*sqrt(1.0/(Histos[processBin+"recoh4lnotfid"].Integral())+1.0/(Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral()))
            else: doutinratio[processBin] = 0.0
        else:
            outinratio[processBin] = -1.0
            doutinratio[processBin] = -1.0
            
        #if (Histos[processBin+"notfid_inc"].Integral(0,m4l_bins+1)>0):
        #    effreconotfid[processBin] = Histos[processBin+"recoh4lnotfid"].Integral(0,m4l_bins+1)/Histos[processBin+"notfid_inc"].Integral(0,m4l_bins+1)   
        #    deffreconotfid[processBin] = sqrt(effreconotfid[processBin]*(1-effreconotfid[processBin])/Histos[processBin+"notfid_inc"].Integral(0,m4l_bins+1))  
        #else:
        #    effreconotfid[processBin] = -1.0
        #    deffreconotfid[processBin] = -1.0

        if (opt.OBSNAME == "nJets" or opt.OBSNAME.startswith("njets")):
            
            if (Histos[processBin+"recoh4l"].Integral()>0):                
                lambdajesup[processBin] = (Histos[processBin+"recoh4l_jesup"].Integral()-Histos[processBin+"recoh4l"].Integral())/Histos[processBin+"recoh4l"].Integral()
                lambdajesdn[processBin] = (Histos[processBin+"recoh4l_jesdn"].Integral()-Histos[processBin+"recoh4l"].Integral())/Histos[processBin+"recoh4l"].Integral()
            else:
                lambdajesup[processBin] = 0.0
                lambdajesdn[processBin] = 0.0
        else:
            lambdajesup[processBin] = 0.0
            lambdajesdn[processBin] = 0.0
            
        #fidacc[processBin] = Histos[processBin+"fid"].Integral()/nEvents[Sample]
        #dfidacc[processBin] = sqrt(fidacc[processBin]*(1-fidacc[processBin])/nEvents[Sample])

        if (doPlots or doFit):
            n_wrongsig = Histos[processBin+"reconoth4l"].Integral()
            n_outsig = Histos[processBin+"recoh4lnotfid"].Integral()
            n_truesig = Histos[processBin+"recoh4lfid"].Integral()                
            n_otherfid = Histos[processBin+"recoh4lotherfid"].Integral()
            
        print processBin,"acc",round(acceptance[processBin],3),"cfactor",round(cfactor[processBin],3),"eff",round(effrecotofid[processBin],3),"outfrac",round(outfrac[processBin],3),"binfrac_outfrac",round(binfrac_outfrac[processBin],3),"wrongfrac",round(wrongfrac[processBin],3),"binfrac_wrongfrac",round(binfrac_wrongfrac[processBin],3),"lambdajesup",lambdajesup[processBin]   
        
        if (doFit): 
        
            mass4l              = RooRealVar("mass4l", "mass4l", m4l_low, m4l_high)
            mass4e              = RooRealVar("mass4e", "mass4e", m4l_low, m4l_high)
            mass4mu             = RooRealVar("mass4mu", "mass4mu", m4l_low, m4l_high)
            mass2e2mu           = RooRealVar("mass2e2mu", "mass2e2mu", m4l_low, m4l_high)

            passedFullSelection = RooRealVar("passedFullSelection", "passedFullSelection", 0, 2)
            eventMCWeight       = RooRealVar("eventMCWeight", "eventMCWeight", 0.0, 10.0)
            totalWeight         = RooRealVar("totalWeight", "totalWeight", 0.0, 10.0)

            if (obs_reco.startswith('abs')):
                obs_reco_noabs = obs_reco.replace('abs(','')
                obs_reco_noabs = obs_reco_noabs.replace(')','')
                observable = RooRealVar(obs_reco_noabs, obs_reco_noabs, -1.0*max(float(obs_reco_high), float(obs_gen_high)), max(float(obs_reco_high), float(obs_gen_high)))
            else:
                observable = RooRealVar(obs_reco, obs_reco, max(float(obs_reco_low), float(obs_gen_low)), max(float(obs_reco_high), float(obs_gen_high)))
                
            a1 = RooRealVar("a1","a1",165.0, 145.0, 185.0) # Landau
            #a2 = RooRealVar("a2","a2",30.0, 2.0, 500.0) # Landau
            a3 = RooRealVar("a3","a3",89.0,84.0,94.0)
            a2 = RooFormulaVar("a2","a2","0.72*@0-@1",RooArgList(a1,a3))
            
            if (channel == "4l"): poly = RooLandau("poly", "PDF", mass4l, a1, a2)
            if (channel == "4e"): poly = RooLandau("poly", "PDF", mass4e, a1, a2)
            if (channel == "4mu"): poly = RooLandau("poly", "PDF", mass4mu, a1, a2)
            if (channel == "2e2mu"): poly = RooLandau("poly", "PDF", mass2e2mu, a1, a2)
            
            nbkg = RooRealVar("N_{wrong}^{fit}","N_{wrong}^{fit}", n_wrongsig, 0.5*n_wrongsig, 1.5*n_wrongsig)
            epoly = RooExtendPdf("epoly","extended bg",poly,nbkg);
            
            mh = shortname.split("_")
            mass = ""
            for i in range(len(mh)):
                if mh[i].startswith("1"): mass = mh[i]
            if (mass=="125p6"): mass="125.6"            

            massHiggs = ast.literal_eval(mass)
            
            MH = RooRealVar("MH", "MH", massHiggs)
            CMS_zz4l_sigma_sig = RooRealVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig",0.0,-0.2,0.2);
            CMS_zz4l_mean_sig  = RooRealVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig",0.0,-0.02,0.02);
        
            mean = ""
            if(channel=="2e2mu" or channel=="4l"): mean = "@0+((-10.9222)+(0.303444*@0)+(-0.00323681*@0*@0)+(1.63907e-05*@0*@0*@0)+(-3.96643e-08*@0*@0*@0*@0)+(3.6718e-11*@0*@0*@0*@0*@0))+@0*@1"
            if(channel=="4e"):    mean = "@0+((-4.03873)+(0.142765*@0)+(-0.00182324*@0*@0)+(1.04662e-05*@0*@0*@0)+(-2.78456e-08*@0*@0*@0*@0)+(2.78107e-11*@0*@0*@0*@0*@0))+@0*@1"
            if(channel=="4mu"):   mean = "@0+((-15.2428)+(0.42122*@0)+(-0.00447937*@0*@0)+(2.26779e-05*@0*@0*@0)+(-5.482e-08*@0*@0*@0*@0)+(5.05978e-11*@0*@0*@0*@0*@0))+@0*@1"
            
            sigma = "" 
            if(channel=="2e2mu" or channel=="4l"): sigma = "((-19.3154)+(0.526495*@0)+(-0.00518631*@0*@0)+(2.47189e-05*@0*@0*@0)+(-5.56479e-08*@0*@0*@0*@0)+(4.76618e-11*@0*@0*@0*@0*@0))*(1+@1)"
            if(channel=="4e"):    sigma = "((7.8429)+(-0.176575*@0)+(0.00186777*@0*@0)+(-8.96356e-06*@0*@0*@0)+(2.09583e-08*@0*@0*@0*@0)+(-1.91015e-11*@0*@0*@0*@0*@0))*(1+@1)"
            if(channel=="4mu"):   sigma = "((-7.90106)+(0.215914*@0)+(-0.00204471*@0*@0)+(9.51991e-06*@0*@0*@0)+(-2.05431e-08*@0*@0*@0*@0)+(1.67545e-11*@0*@0*@0*@0*@0))*(1+@1)"
        
            alpha = ""
            if(channel=="2e2mu" or channel=="4l"): alpha = "(-14.6609)+(0.399488*@0)+(-0.00385576*@0*@0)+(1.74976e-05*@0*@0*@0)+(-3.71685e-08*@0*@0*@0*@0)+(2.97992e-11*@0*@0*@0*@0*@0)"
            if(channel=="4e"):    alpha = "(-1.97072)+(0.0725852*@0)+(-0.000670387*@0*@0)+(2.75605e-06*@0*@0*@0)+(-4.67709e-09*@0*@0*@0*@0)+(2.41684e-12*@0*@0*@0*@0*@0)"
            if(channel=="4mu"):   alpha = "(-3.6088)+(0.107156*@0)+(-0.000832395*@0*@0)+(2.76884e-06*@0*@0*@0)+(-3.4753e-09*@0*@0*@0*@0)+(6.63626e-13*@0*@0*@0*@0*@0)"
        
            alpha2 = ""
            if(channel=="2e2mu" or channel=="4l"): alpha2 = "(10.0277)+(-0.243287*@0)+(0.0026732*@0*@0)+(-1.45571e-05*@0*@0*@0)+(3.9265e-08*@0*@0*@0*@0)+(-4.02105e-11*@0*@0*@0*@0*@0)"
            if(channel=="4e"):    alpha2 = "(134.772)+(-3.52321*@0)+(0.0358562*@0*@0)+(-0.000175381*@0*@0*@0)+(4.115e-07*@0*@0*@0*@0)+(-3.69445e-10*@0*@0*@0*@0*@0)"
            if(channel=="4mu"):   alpha2 = "(-19.5288)+(0.525804*@0)+(-0.00487398*@0*@0)+(2.03764e-05*@0*@0*@0)+(-3.66955e-08*@0*@0*@0*@0)+(2.20557e-11*@0*@0*@0*@0*@0)"
        
            n = ""
            if(channel=="2e2mu" or channel=="4l"): n = "TMath::Max((-13.9463)+(0.328247*@0)+(-0.00208904*@0*@0)+(5.30154e-06*@0*@0*@0)+(-4.91882e-09*@0*@0*@0*@0)+(4.42671e-13*@0*@0*@0*@0*@0),1)"
            if(channel=="4e"):    n = "TMath::Max((-68.5573)+(1.68878*@0)+(-0.0144006*@0*@0)+(5.76535e-05*@0*@0*@0)+(-1.11285e-07*@0*@0*@0*@0)+(8.38162e-11*@0*@0*@0*@0*@0),1)"
            if(channel=="4mu"):   n = "TMath::Max((21.8412)+(-0.457725*@0)+(0.00405228*@0*@0)+(-1.69485e-05*@0*@0*@0)+(3.3184e-08*@0*@0*@0*@0)+(-2.44899e-11*@0*@0*@0*@0*@0),1)"
    
            n2 = ""
            if(channel=="2e2mu" or channel=="4l"): n2 = "20"
            if(channel=="4e"):    n2 = "20"
            if(channel=="4mu"):   n2 = "20"
        
            rfv_mean_CB  = RooFormulaVar("mean", mean, RooArgList(MH,CMS_zz4l_mean_sig))
            rfv_sigma_CB = RooFormulaVar("sigma", sigma, RooArgList(MH,CMS_zz4l_sigma_sig))
        
            rfv_alpha_CB = RooFormulaVar("alpha", alpha, RooArgList(MH))
            rfv_n_CB     = RooFormulaVar("n", n,RooArgList(MH))
            
            rfv_alpha2_CB = RooFormulaVar("alpha2", alpha2, RooArgList(MH))
            rfv_n2_CB     = RooFormulaVar("n2", n2, RooArgList(MH))
        
            if (channel == "4l"): signal  = RooDoubleCB("signal","signal", mass4l, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            if (channel == "4e"): signal  = RooDoubleCB("signal","signal", mass4e, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            if (channel == "4mu"): signal  = RooDoubleCB("signal","signal", mass4mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            if (channel == "2e2mu"): signal  = RooDoubleCB("signal","signal", mass2e2mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            
            nsig    = RooRealVar("N_{right}^{fit}","N_{right}^{fit}", 0.5*n_truesig, 1.5*n_truesig)
            esignal = RooExtendPdf("esignal","esig", signal, nsig)

            #if (channel == "4l"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4l, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "4e"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4e, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "4mu"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "2e2mu"): outsignal  = RooDoubleCB("outsignal","outsignal", mass2e2mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)

            outsignal  = signal.Clone("outsignal")
            noutsig    = RooRealVar("N_{out}^{fit}","N_{out}^{fit}", 0.98*n_outsig, 1.02*n_outsig) 
            eoutsignal = RooExtendPdf("eoutsignal","eoutsig", outsignal, noutsig)            
 

            otherfid   = signal.Clone("otherfid")
            notherfid  = RooRealVar("N_{other fid}^{fit}","N_{other fid}^{fit}", 0.98*n_otherfid, 1.02*n_otherfid)
            eotherfid  = RooExtendPdf("eotherfid","eotherfid", otherfid, notherfid)
                                    
            ## sum sig and bkg pdf weighted by corresponding yield
            sum = RooAddPdf("sum","sig+otherfid+outsig+poly",RooArgList(esignal,eotherfid,eoutsignal,epoly))
            
            ## fitting
            r = RooFitResult()

            #print 'Defining RooDataSet:',Sample
            #print "TreesPassed Events slim Entries: ",TreesPassedEventsSlim[Sample].GetEntriesFast()
            
            # eventMCWeight
            if (recoweight=="eventMCWeight"):
                if (channel == "4l"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4l,eventMCWeight,observable), cutobs_reco.replace("abs","fabs"), "eventMCWeight")
                if (channel == "4e"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4e,eventMCWeight,observable), cutobs_reco.replace("abs","fabs"), "eventMCWeight")
                if (channel == "4mu"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4mu,eventMCWeight,observable), cutobs_reco.replace("abs","fabs"), "eventMCWeight")
                if (channel == "2e2mu"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass2e2mu,eventMCWeight,observable), cutobs_reco.replace("abs","fabs"), "eventMCWeight")

            ## totalWeight
            if (recoweight=="totalWeight"):
                if (channel == "4l"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4l,totalWeight,observable), cutobs_reco.replace("abs","fabs"), "totalWeight")
                if (channel == "4e"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4e,totalWeight,observable), cutobs_reco.replace("abs","fabs"), "totalWeight")
                if (channel == "4mu"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass4mu,totalWeight,observable), cutobs_reco.replace("abs","fabs"), "totalWeight")
                if (channel == "2e2mu"):
                    dataset_sig  = RooDataSet("dataset_sig","dataset_sig", TreesPassedEventsSlim[Sample], RooArgSet(mass2e2mu,totalWeight,observable), cutobs_reco.replace("abs","fabs"), "totalWeight")
   

            #print "RooDataSet sumEntries = ",dataset_sig.sumEntries()
            #print ' '
            #print 'Fitting....'
            
            r = sum.fitTo(dataset_sig, RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Verbose(kFALSE),RooFit.PrintLevel(-1),RooFit.Warnings(kFALSE))
            #r.Print()            
            #sum.Print()

            #print Sample,channel,"post fit CB mean:",rfv_mean_CB.getVal()," sigma: ",rfv_sigma_CB.getVal()
            CB_mean_post[processBin] = rfv_mean_CB.getVal()
            #CB_dmean_post[processBin] = rfv_mean_CB.getError()
            CB_sigma_post[processBin] = rfv_sigma_CB.getVal()
            #CB_dsigma_post[processBin] = rfv_sigma_CB.getVal()

            #print Sample,channel,"post fit Landau mean:",a1.getVal()," sigma: ",a2.getVal()
            Landau_mean_post[processBin] = a1.getVal()
            Landau_sigma_post[processBin] = a2.getVal()
        
        if (doPlots):
            ################################
            ######### Plotting #############
            ################################
        
            hs = THStack("hs","mass spectrum");
            Histos[processBin+"reconoth4l"].SetFillColor(0)
            Histos[processBin+"reconoth4l"].SetLineColor(kOrange)
            hs.Add(Histos[processBin+"reconoth4l"])
            Histos[processBin+"recoh4lotherfid"].SetFillColor(0)
            Histos[processBin+"recoh4lotherfid"].SetLineColor(kBlue)
            hs.Add(Histos[processBin+"recoh4lotherfid"])
            Histos[processBin+"recoh4lnotfid"].SetFillColor(0)
            Histos[processBin+"recoh4lnotfid"].SetLineColor(kBlack)
            hs.Add(Histos[processBin+"recoh4lnotfid"])                                    
            Histos[processBin+"recoh4lfid"].SetFillColor(0)
            Histos[processBin+"recoh4lfid"].SetLineColor(kRed)
            hs.Add(Histos[processBin+"recoh4lfid"])

            leg = TLegend(0.54,0.57,0.91,0.72);
            leg.SetShadowColor(0)
            leg.SetFillColor(0)
            leg.SetLineColor(0)
            leg.AddEntry(Histos[processBin+"recoh4lfid"],"N_{sig}^{MC} = "+str(int(n_truesig)), "F")
            leg.AddEntry(Histos[processBin+"reconoth4l"],"N_{wrong}^{MC} = "+str(int(n_wrongsig)), "F")
            leg.AddEntry(Histos[processBin+"recoh4lnotfid"],"N_{out}^{MC} = "+str(int(n_outsig)), "F")
            if (doFit):
                # Plot updated with fitting
                frame = RooPlot()
                if (channel == "4l"): frame = mass4l.frame(RooFit.Title("m4l"),RooFit.Bins(m4l_bins))
                if (channel == "4e"): frame = mass4e.frame(RooFit.Title("m4e"),RooFit.Bins(m4l_bins))
                if (channel == "4mu"): frame = mass4mu.frame(RooFit.Title("m4mu"),RooFit.Bins(m4l_bins))
                if (channel == "2e2mu"): frame = mass2e2mu.frame(RooFit.Title("m2e2mu"),RooFit.Bins(m4l_bins))
                
                dataset_sig.plotOn(frame, RooFit.LineColor(kRed), RooFit.MarkerSize(0))
                sum.plotOn(frame, RooFit.Components('poly,otherfid,outsignal'), RooFit.LineColor(ROOT.kBlack))                
                sum.plotOn(frame, RooFit.Components('poly,otherfid'),RooFit.LineColor(ROOT.kBlue))
                sum.plotOn(frame, RooFit.Components('poly'), RooFit.LineColor(ROOT.kOrange))
                sum.plotOn(frame, RooFit.LineColor(kRed) )
                
                # Uncorrelated
                if (Histos[processBin+"fid"].Integral()>0):
                    eff_fit[processBin]  = nsig.getVal()/Histos[processBin+"fid"].Integral()
                else:
                    eff_fit[processBin] = -1.0
                    
                if (eff_fit[processBin]<1.0 and eff_fit[processBin]>-0.1):
                    deff_fit[processBin] = sqrt(eff_fit[processBin]*(1-eff_fit[processBin])/Histos[processBin+"fid"].Integral()) 
                else:
                    deff_fit[processBin] = eff_fit[processBin]
                
                #print " "
                #print " "            
                #print "Passed Reco. Selection and true H->ZZ->4l (from fit) : ",nsig.getVal()
                #print "Passed Gen.  Selection and true H->ZZ->4l (from gen.): ",Histos[processBin+"fid"].Integral()
                #print "correction factor from fit: %.3f +/- %.3f "  % (cfactor[processBin], dcfactor[processBin])                
                #print " "
                #print " "   
                
            c = TCanvas("c","c",750,750)
            SetOwnership(c,False)
            c.cd()
            #c.SetLogy()
 
            hs.SetMaximum(1.15*hs.GetMaximum())
            hs.Draw("ehist")
            if (channel == "4l"): hs.GetXaxis().SetTitle("m_{4l} (GeV)")
            if (channel == "4e"): hs.GetXaxis().SetTitle("m_{4e} (GeV)")
            if (channel == "4mu"): hs.GetXaxis().SetTitle("m_{4#mu} (GeV)")
            if (channel == "2e2mu"): hs.GetXaxis().SetTitle("m_{2e2#mu} (GeV)")
            if (doFit): frame.Draw("same")
       
            latex2 = TLatex()
            latex2.SetNDC()
            latex2.SetTextSize(0.75*c.GetTopMargin())
            latex2.SetTextFont(62)
            latex2.SetTextAlign(11) # align right
            latex2.DrawLatex(0.22, 0.85, "CMS")
            latex2.SetTextSize(0.6*c.GetTopMargin())
            latex2.SetTextFont(52)
            latex2.SetTextAlign(11)
            latex2.DrawLatex(0.20, 0.8, "Simulation")
            latex2.SetTextSize(0.4*c.GetTopMargin())
            latex2.SetTextFont(42)
            latex2.SetTextAlign(11)
            latex2.DrawLatex(0.20, 0.73, shortname.replace('_',' ')+' GeV');
            latex2.SetTextSize(0.35*c.GetTopMargin())
            latex2.SetTextFont(42)
            latex2.DrawLatex(0.20, 0.68, str(obs_reco_low)+" < "+obs_reco+" < "+str(obs_reco_high) )
            latex2.DrawLatex(0.20, 0.48, "N_{fiducial}^{gen} = "+str(int(Histos[processBin+"fid"].Integral())) )                        
            if (doFit):
                latex2.DrawLatex(0.20, 0.64, "N_{fid.}^{fit} = "+str(int(nsig.getVal()))+" ("+str(int(n_truesig))+")" )
                latex2.DrawLatex(0.20, 0.60, "N_{other fid.}^{fit} = "+str(int(notherfid.getVal()))+" ("+str(int(n_otherfid))+")" )                        
                latex2.DrawLatex(0.20, 0.56, "N_{not fid.}^{fit} = "+str(int(noutsig.getVal()))+" ("+str(int(n_outsig))+")" )
                latex2.DrawLatex(0.20, 0.52, "N_{wrong comb.}^{fit} = "+str(int(nbkg.getVal()))+" ("+str(int(n_wrongsig))+")" )
            else:
                latex2.DrawLatex(0.20, 0.64, "N_{fid.}^{MC} = "+str(int(n_truesig)) )
                latex2.DrawLatex(0.20, 0.60, "N_{other fid.}^{MC} = "+str(int(n_otherfid)) )
                latex2.DrawLatex(0.20, 0.56, "N_{not fid.}^{MC} = "+str(int(n_outsig)) )
                latex2.DrawLatex(0.20, 0.52, "N_{wrong comb.}^{MC} = "+str(int(n_wrongsig)) )
            latex2.DrawLatex(0.20, 0.44, "eff^{MC} = %.3f #pm %.3f" % (effrecotofid[processBin],deffrecotofid[processBin]))
            #latex2.DrawLatex(0.20, 0.32, "C^{MC}"+str(recobin)+str(genbin)+"} = %.3f" % (cfactor[processBin]))
            if (doFit): latex2.DrawLatex(0.20, 0.40, "#sigma = %.3f " % (CB_sigma_post[processBin])+" GeV")
            
            c.SaveAs("plots/"+processBin+"_effs_"+recoweight+".png")
            c.SaveAs("plots/"+processBin+"_effs_"+recoweight+".pdf")


m4l_bins = 45
m4l_low = 50.0 
m4l_high = 140.0

# Default to inclusive cross section
obs_reco = 'mass4l'
obs_gen = 'GENmZ1Z2'
obs_reco_low = 50.0
obs_reco_high = 140.0
obs_gen_low = 50.0
obs_gen_high = 140.0

if (opt.OBSNAME == "massZ2"):
    obs_reco = "massZ2"
    obs_gen = "GENmZ2"
if (opt.OBSNAME == "pT4l"):
    obs_reco = "pT4l"
    obs_gen = "GENpT4l"
if (opt.OBSNAME == "eta4l"):
    obs_reco = "eta4l"
    obs_gen = "GENeta4l"
if (opt.OBSNAME == "nJets" or opt.OBSNAME== "njets"):
    obs_reco = "njets_reco_pt30_eta4p7"
    obs_gen = "njets_gen_pt30_eta4p7"
if (opt.OBSNAME== "njets_reco_pt30_eta4p7"):
    obs_reco = "njets_reco_pt30_eta4p7"
    obs_gen = "njets_gen_pt30_eta4p7"
if (opt.OBSNAME== "njets_reco_pt30_eta2p5"):
    obs_reco = "njets_reco_pt30_eta2p5"
    obs_gen = "njets_gen_pt30_eta2p5"
if (opt.OBSNAME== "njets_reco_pt25_eta2p5"):
    obs_reco = "njets_reco_pt25_eta2p5"
    obs_gen = "njets_gen_pt25_eta2p5"
if (opt.OBSNAME == "rapidity4l"):
    obs_reco = "abs(rapidity4l)"
    obs_gen = "abs(GENrapidity4l)"
if (opt.OBSNAME == "cosThetaStar"):
    obs_reco = "abs(cosThetaStar)"
    obs_gen = "abs(GENcosThetaStar)"
    
#obs_bins = {0:(opt.OBSBINS.split("|")[1:((len(opt.OBSBINS)-1)/2)]),1:['0','inf']}[opt.OBSNAME=='inclusive'] 
obs_bins = opt.OBSBINS.split("|") 
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins.pop()
obs_bins.pop(0) 

List = []
for long, short in sample_shortnames.iteritems():
    #print long,short
    if (opt.MODELNAME=='SM'):
        if (opt.OBSNAME=="mass4l"):
            List.append(long)
            continue
        if (not '125' in short): continue
        if short.startswith('ggH_powheg15_JHUgen') or short.startswith('ggH_minloHJJ') or short.startswith('VBF_powheg') or short.startswith('WH_pythia') or short.startswith('ZH_pythia') or short.startswith('ttH_pythia'): List.append(long)
        if (short=='ggH0MToZG_JHUgen_125p6'): List.append(long)
        if (short=='qq1M_JHUgen_125p6'): List.append(long)



if (obs_reco=="mass4l"):
    chans = ['4e','4mu','2e2mu','4l']
else:
    chans = ['4e','4mu','2e2mu']

for chan in chans:
    for recobin in range(len(obs_bins)-1):
        for genbin in range(len(obs_bins)-1): 
            geteffs(chan,List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin)  

with open('datacardInputs/inputs_sig_ratio_h4l_'+opt.OBSNAME+'.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('dacc = '+str(dacceptance)+' \n')
    f.write('acc_4l = '+str(acceptance_4l)+' \n')
    f.write('dacc_4l = '+str(dacceptance_4l)+' \n')
    f.write('eff = '+str(effrecotofid)+' \n')
    f.write('deff = '+str(deffrecotofid)+' \n')
    f.write('inc_outfrac = '+str(outfrac)+' \n') 
    f.write('binfrac_outfrac = '+str(binfrac_outfrac)+' \n') 
    f.write('outinratio = '+str(outinratio)+' \n')
    f.write('doutinratio = '+str(doutinratio)+' \n')
    f.write('inc_wrongfrac = '+str(wrongfrac)+' \n') 
    f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac)+' \n') 
    f.write('cfactor = '+str(cfactor)+' \n')
    f.write('lambdajesup = '+str(lambdajesup)+' \n')
    f.write('lambdajesdn = '+str(lambdajesdn)+' \n')
    
with open('datacardInputs/moreinputs_sig_ratio_h4l_'+opt.OBSNAME+'.py', 'w') as f:
    f.write('CB_mean = '+str(CB_mean_post)+' \n')
    #f.write('CB_dmean = '+str(CB_dmean_post)+' \n')
    f.write('CB_sigma = '+str(CB_sigma_post)+' \n')
    #f.write('CB_dsigma = '+str(CB_dsigma_post)+' \n')
    f.write('folding = '+str(folding)+' \n')
    f.write('dfolding = '+str(dfolding)+' \n')
    #f.write('effanyreco = '+str(effanyreco)+' \n')
    #f.write('deffanyreco = '+str(deffanyreco)+' \n')
    
