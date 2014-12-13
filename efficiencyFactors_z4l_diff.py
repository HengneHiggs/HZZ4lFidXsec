
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames_bkg import *

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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
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


from ROOT import *
from LoadData_ratio import *
LoadData(opt.SOURCEDIR)
save = ""

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    


Histos = {}
outinratio = {}
doutinratio = {}
CB_mean_post = {}
CB_sigma_post = {}
CB_dmean_post = {}
CB_dsigma_post = {}
Landau_mean_post = {}
Landau_sigma_post = {}
effrecotofid = {}
deffrecotofid = {}
acceptance = {}
dacceptance = {}
eff_fit = {}
deff_fit = {}


lambdajesup = {}
lambdajesdn = {}

nfid = {}
nfs = {}
nreco = {}
nrecofid = {}
nreconotfid = {}
nrecootherfid = {}
nrecojesup = {}
nrecojesdn = {}

dnfid = {}
dnfs = {}
dnreco = {}
dnrecofid = {}
dnreconotfid = {}
dnrecootherfid = {}
dnrecojesup = {}
dnrecojesdn = {}

m4l_bins = 20
m4l_low = 50
m4l_high = 105

dotchanCorr = True
Tag=''
if (not dotchanCorr): Tag="_NoTchanCorr"

#recoweight = "eventMCWeight"
RecoWeight = "totalWeight"
#recoweight = "1.0"

recoweight = RecoWeight

def geteffs_z4l_schan_diff(recobin, genbin):

    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");

    processBinST_4l = 'qqZZst_4l_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)
    processBinT_4l = 'qqZZtchan_4l_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)
    processBinS_4l = 'SMZ4l_4l_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)

    nfid[processBinS_4l] = 0.0
    nfs[processBinS_4l] = 0.0
    nrecofid[processBinS_4l] = 0.0
    nreconotfid[processBinS_4l] = 0.0
    nrecootherfid[processBinS_4l] = 0.0
    nreco[processBinS_4l] = 0.0
    nrecojesup[processBinS_4l] = 0.0
    nrecojesdn[processBinS_4l] = 0.0

    nfid[processBinT_4l] = 0.0
    nfs[processBinT_4l] = 0.0
    nrecofid[processBinT_4l] = 0.0
    nreconotfid[processBinT_4l] = 0.0
    nrecootherfid[processBinT_4l] = 0.0
    nreco[processBinT_4l] = 0.0
    nrecojesup[processBinT_4l] = 0.0
    nrecojesdn[processBinT_4l] = 0.0

    nfid[processBinST_4l] = 0.0
    nfs[processBinST_4l] = 0.0
    nrecofid[processBinST_4l] = 0.0
    nreconotfid[processBinST_4l] = 0.0
    nrecootherfid[processBinST_4l] = 0.0
    nreco[processBinST_4l] = 0.0
    nrecojesup[processBinST_4l] = 0.0
    nrecojesdn[processBinST_4l] = 0.0


    # '4e','4mu','2e2mu'
    for channel in ['4e','4mu','2e2mu']:
        processBinST = 'qqZZst_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)
        processBinT = 'qqZZtchan_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)
        processBinS = 'SMZ4l_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)

        nfid[processBinS] = nfid[processBinST] - nfid[processBinT]
        nfs[processBinS] = nfs[processBinST] - nfs[processBinT]
        nrecofid[processBinS] = nrecofid[processBinST] - nrecofid[processBinT]
        nreconotfid[processBinS] = nreconotfid[processBinST] - nreconotfid[processBinT]
        nrecootherfid[processBinS] = nrecootherfid[processBinST] - nrecootherfid[processBinT]
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            nreco[processBinS] = nreco[processBinST] - nreco[processBinT]
            nrecojesup[processBinS] = nrecojesup[processBinST] - nrecojesup[processBinT]
            nrecojesdn[processBinS] = nrecojesdn[processBinST] - nrecojesdn[processBinT]

        nfid[processBinS_4l] += nfid[processBinS]
        nfs[processBinS_4l] += nfs[processBinS]
        nrecofid[processBinS_4l] += nrecofid[processBinS]
        nreconotfid[processBinS_4l] += nreconotfid[processBinS]
        nrecootherfid[processBinS_4l] += nrecootherfid[processBinS]
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            nreco[processBinS_4l] += nreco[processBinS]
            nrecojesup[processBinS_4l] += nrecojesup[processBinS]
            nrecojesdn[processBinS_4l] += nrecojesdn[processBinS]

        nfid[processBinT_4l] += nfid[processBinT]
        nfs[processBinT_4l] += nfs[processBinT]
        nrecofid[processBinT_4l] += nrecofid[processBinT]
        nreconotfid[processBinT_4l] += nreconotfid[processBinT]
        nrecootherfid[processBinT_4l] += nrecootherfid[processBinT]
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            nreco[processBinT_4l] += nreco[processBinT]
            nrecojesup[processBinT_4l] += nrecojesup[processBinT]
            nrecojesdn[processBinT_4l] += nrecojesdn[processBinT]

        nfid[processBinST_4l] += nfid[processBinST]
        nfs[processBinST_4l] += nfs[processBinST]
        nrecofid[processBinST_4l] += nrecofid[processBinST]
        nreconotfid[processBinST_4l] += nreconotfid[processBinST]
        nrecootherfid[processBinST_4l] += nrecootherfid[processBinST]
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            nreco[processBinST_4l] += nreco[processBinST]
            nrecojesup[processBinST_4l] += nrecojesup[processBinST]
            nrecojesdn[processBinST_4l] += nrecojesdn[processBinST]


        if (nfs[processBinST]>0.0): acceptance[processBinS] =  nfid[processBinS] / nfs[processBinST]
        else: acceptance[processBinS] = -1.0
        dacceptance[processBinS] = 0.0#sqrt(acceptance[processBinS]*(1.0-acceptance[processBinS])/nfs[processBinST])

        if (nfid[processBinS]>0.0): effrecotofid[processBinS] = nrecofid[processBinS]/nfid[processBinS]
        else: effrecotofid[processBinS] = -1.0
        deffrecotofid[processBinS] = 0.0#sqrt(effrecotofid[processBinS]*(1-effrecotofid[processBinS])/nfid[processBinS])

        if (nrecofid[processBinS]+nrecootherfid[processBinS]>0.0): outinratio[processBinS] = nreconotfid[processBinS]/(nrecofid[processBinS]+nrecootherfid[processBinS])
        else: outinratio[processBinS] = -1.0
        doutinratio[processBinS] = 0.0#outinratio[processBinS]*sqrt(1.0/(nreconotfid[processBinS]+nrecootherfid[processBinS])+1.0/(nrecofid[processBinS]))

        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            if(nreco[processBinS]>0.0):
                lambdajesup[processBinS] = (nrecojesup[processBinS]-nreco[processBinS])/nreco[processBinS]
                lambdajesdn[processBinS] = (nrecojesdn[processBinS]-nreco[processBinS])/nreco[processBinS]
            else: 
                lambdajesup[processBinS] = 0.0
                lambdajesdn[processBinS] = 0.0
    
        print processBinS,"acc",round(acceptance[processBinS],3),"eff",round(effrecotofid[processBinS],3),"outinratio",round(outinratio[processBinS],3)

    # '4l'    
    # s
    if (nfs[processBinST_4l]>0.0): acceptance[processBinS_4l] =  nfid[processBinS_4l] / nfs[processBinST_4l] 
    else: acceptance[processBinS_4l] = -1.0
    dacceptance[processBinS_4l] = 0.0#sqrt(acceptance[processBinS_4l]*(1.0-acceptance[processBinS_4l])/nfs[processBinST_4l])
    if (nfid[processBinS_4l]>0.0): effrecotofid[processBinS_4l] = nrecofid[processBinS_4l]/nfid[processBinS_4l]
    else: effrecotofid[processBinS_4l] = -1.0
    deffrecotofid[processBinS_4l] = 0.0#sqrt(effrecotofid[processBinS_4l]*(1-effrecotofid[processBinS_4l])/nfid[processBinS_4l])
    if (nrecofid[processBinS_4l]+nrecootherfid[processBinS_4l]>0.0): outinratio[processBinS_4l] = nreconotfid[processBinS_4l]/(nrecofid[processBinS_4l]+nrecootherfid[processBinS_4l])
    else: outinratio[processBinS_4l] =  -1.0
    doutinratio[processBinS_4l] = 0.0#outinratio[processBinS_4l]*sqrt(1.0/(nreconotfid[processBinS_4l]+nrecootherfid[processBinS_4l])+1.0/(nrecofid[processBinS_4l]))
    if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
        if(nreco[processBinS_4l]>0.0):
            lambdajesup[processBinS_4l] = (nrecojesup[processBinS_4l]-nreco[processBinS_4l])/nreco[processBinS_4l]
            lambdajesdn[processBinS_4l] = (nrecojesdn[processBinS_4l]-nreco[processBinS_4l])/nreco[processBinS_4l]
        else: 
            lambdajesup[processBinS_4l] = 0.0
            lambdajesdn[processBinS_4l] = 0.0

    # t
    if (nfs[processBinT_4l]>0.0): acceptance[processBinT_4l] =  nfid[processBinT_4l] / nfs[processBinT_4l]
    else: acceptance[processBinT_4l] = -1.0
    dacceptance[processBinT_4l] = 0.0#sqrt(acceptance[processBinT_4l]*(1.0-acceptance[processBinT_4l])/nfs[processBinT_4l])
    if (nfid[processBinT_4l]>0.0): effrecotofid[processBinT_4l] = nrecofid[processBinT_4l]/nfid[processBinT_4l]
    else: effrecotofid[processBinT_4l] = -1.0
    deffrecotofid[processBinT_4l] = 0.0#sqrt(effrecotofid[processBinT_4l]*(1-effrecotofid[processBinT_4l])/nfid[processBinT_4l])
    if (nrecofid[processBinT_4l]+nrecootherfid[processBinT_4l]>0.0): outinratio[processBinT_4l] = nreconotfid[processBinT_4l]/(nrecofid[processBinT_4l]+nrecootherfid[processBinT_4l])
    else: outinratio[processBinT_4l] = -1.0
    doutinratio[processBinT_4l] = 0.0#outinratio[processBinT_4l]*sqrt(1.0/(nreconotfid[processBinT_4l]+nrecootherfid[processBinT_4l])+1.0/(nrecofid[processBinT_4l]))
    if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
        if (nreco[processBinT_4l]>0.0):
            lambdajesup[processBinT_4l] = (nrecojesup[processBinT_4l]-nreco[processBinT_4l])/nreco[processBinT_4l]
            lambdajesdn[processBinT_4l] = (nrecojesdn[processBinT_4l]-nreco[processBinT_4l])/nreco[processBinT_4l]
        else:
            lambdajesup[processBinT_4l] = 0.0
            lambdajesdn[processBinT_4l] = 0.0
    # st
    if (nfs[processBinST_4l]>0.0): acceptance[processBinST_4l] =  nfid[processBinST_4l] / nfs[processBinST_4l]
    else: acceptance[processBinST_4l] = -1.0
    dacceptance[processBinST_4l] = 0.0#sqrt(acceptance[processBinST_4l]*(1.0-acceptance[processBinST_4l])/nfs[processBinST_4l])
    if (nfid[processBinST_4l]>0.0): effrecotofid[processBinST_4l] = nrecofid[processBinST_4l]/nfid[processBinST_4l]
    else: effrecotofid[processBinST_4l] = -1.0
    deffrecotofid[processBinST_4l] = 0.0#sqrt(effrecotofid[processBinST_4l]*(1-effrecotofid[processBinST_4l])/nfid[processBinST_4l])
    if (nrecofid[processBinST_4l]+nrecootherfid[processBinST_4l]>0.0): outinratio[processBinST_4l] = nreconotfid[processBinST_4l]/(nrecofid[processBinST_4l]+nrecootherfid[processBinST_4l])
    else: outinratio[processBinST_4l] = -1.0
    doutinratio[processBinST_4l] = 0.0#outinratio[processBinST_4l]*sqrt(1.0/(nreconotfid[processBinST_4l]+nrecootherfid[processBinST_4l])+1.0/(nrecofid[processBinST_4l]))
    if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
        if (nreco[processBinST_4l]>0.0):
            lambdajesup[processBinST_4l] = (nrecojesup[processBinST_4l]-nreco[processBinST_4l])/nreco[processBinST_4l]
            lambdajesdn[processBinST_4l] = (nrecojesdn[processBinST_4l]-nreco[processBinST_4l])/nreco[processBinST_4l]
        else:
            lambdajesup[processBinST_4l] = 0.0
            lambdajesdn[processBinST_4l] = 0.0

    print processBinS_4l,"acc",round(acceptance[processBinS_4l],3),"eff",round(effrecotofid[processBinS_4l],3),"outinratio",round(outinratio[processBinS_4l],3)


def geteffs_z4l_diff(channel, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin):    
    
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");
            

    obs_reco_low = obs_bins[recobin]
    obs_reco_high = obs_bins[recobin+1]

    obs_gen_low = obs_bins[genbin]
    obs_gen_high = obs_bins[genbin+1]

    obs_gen_lowest = obs_bins[0]
    obs_gen_highest = obs_bins[len(obs_bins)-1]

    for Sample in List:
    
        if (not Sample in TreesPassedEvents): continue
        if (not TreesPassedEvents[Sample]): continue
        if (not channel in Sample): continue 
        
        print Sample," ", channel


        cutobs_reco = "("+obs_reco+">="+str(obs_reco_low)+" && "+obs_reco+"<"+str(obs_reco_high)+")"
        cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+" && "+obs_gen+"<"+str(obs_gen_high)+")"
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            cutobs_reco_jesup = "("+obs_reco+"_jesup"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesup"+"<"+str(obs_reco_high)+")"
            cutobs_reco_jesdn = "("+obs_reco+"_jesdn"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesdn"+"<"+str(obs_reco_high)+")"

        cutobs_gen_otherfid = "(("+obs_gen+"<"+str(obs_gen_low)+" && "+obs_gen+">="+str(obs_gen_lowest)+") || ("+obs_gen+">="+str(obs_gen_high)+" && "+obs_gen+"<="+str(obs_gen_highest)+"))"

        cutm4l_gen     = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
        cutm4l_reco    = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")" 
 
        if (channel == "4l"):
            cutchan_gen      = "(abs(GENidLS3[GENlepIndex1])==11 || abs(GENidLS3[GENlepIndex1])==13)"
            cutchan_gen_out  = "(Z1daughtersId==11 || Z1daughtersId==13)"
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")"   
        if (channel == "4e"):
            cutchan_gen      = "(abs(GENidLS3[GENlepIndex1])==11 && abs(GENidLS3[GENlepIndex3])==11)"
            cutchan_gen_out  = "(Z1daughtersId==11 && Z2daughtersId==11)"
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+")"                        
        if (channel == "4mu"):
            cutchan_gen      = "(abs(GENidLS3[GENlepIndex1])==13 && abs(GENidLS3[GENlepIndex3])==13)"
            cutchan_gen_out  = "(Z1daughtersId==13 && Z2daughtersId==13)"
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+")"                        
        if (channel == "2e2mu"):
            cutchan_gen      = "((abs(GENidLS3[GENlepIndex1])==11 && abs(GENidLS3[GENlepIndex3])==13) ||(abs(GENidLS3[GENlepIndex1])==13 && abs(GENidLS3[GENlepIndex3])==11))"
            cutchan_gen_out  = "((Z1daughtersId==11 && Z2daughtersId==13) || (Z1daughtersId==13 && Z2daughtersId==11))" 
            cutm4l_gen       = "(GENmZ1Z2>"+str(m4l_low)+" && GENmZ1Z2<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+")"

        cutz4l_gen = cutm4l_gen
        cutz4l_reco =  cutm4l_reco

        cutnotz4l_gen  = "(!"+cutz4l_gen+")"
        cutnotz4l_reco = "(!"+cutz4l_reco+")"

           
        recoweight = RecoWeight 
        if (recoweight=="totalWeight"): genweight = "19712.0*scaleWeight/"+str(nEvents[Sample])
        else: genweight = "1.0"

        # correct t-channel xsec
        if (dotchanCorr and ("tchan" in Sample)) :
            if (channel=='4e'):
                genweight += "*1.3921097"
                recoweight += "*1.3921097"
            elif (channel=='4mu'):
                genweight += "*1.246817"
                recoweight += "*1.246817"
            elif (channel=='2e2mu'):
                genweight += "*1.25846135"
                recoweight += "*1.25846135"

        shortname = sample_shortnames_bkg[Sample]
        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)

        # RECO level
        Histos[processBin+"recoz4l"] = TH1D(processBin+"recoz4l", processBin+"recoz4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoz4l"].Sumw2()
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            Histos[processBin+"recoz4l_jesup"] = TH1D(processBin+"recoz4l_jesup", processBin+"recoz4l_jesup", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoz4l_jesup"].Sumw2()
            Histos[processBin+"recoz4l_jesdn"] = TH1D(processBin+"recoz4l_jesdn", processBin+"recoz4l_jesdn", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoz4l_jesdn"].Sumw2()


                                    
        # GEN level
        Histos[processBin+"fid"] = TH1D(processBin+"fid", processBin+"fid", m4l_bins, m4l_low, m4l_high)  
        Histos[processBin+"fid"].Sumw2()
        Histos[processBin+"fs"] = TH1D(processBin+"fs", processBin+"fs", 100, 0, 10000)
        Histos[processBin+"fs"].Sumw2()
        
        # RECO and GEN level ( e.g. f(in) and f(out) )
        Histos[processBin+"recoz4lfid"] = TH1D(processBin+"recoz4lfid", processBin+"recoz4lfid", m4l_bins, m4l_low, m4l_high)        
        Histos[processBin+"recoz4lfid"].Sumw2()
        Histos[processBin+"recoz4lnotfid"] = TH1D(processBin+"recoz4lnotfid", processBin+"recoz4lnotfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoz4lnotfid"].Sumw2()
        Histos[processBin+"recoz4lotherfid"] = TH1D(processBin+"recoz4lotherfid", processBin+"recoz4lotherfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoz4lotherfid"].Sumw2()   

     
        # GEN level 
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fid","("+genweight+")*("+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+" && passedFiducialTopology==1 && "+cutz4l_gen+")","goff")
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fs","("+genweight+")*("+cutchan_gen_out+")","goff")       


        # RECO level 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4l","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutz4l_reco+")","goff")
        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
            TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4l_jesup","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco_jesup+" && passedFullSelection==1 && "+cutz4l_reco+")","goff")
            TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4l_jesdn","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco_jesdn+" && passedFullSelection==1 && "+cutz4l_reco+")","goff")

 

        # RECO and GEN level ( i.e. f(in) and f(out) ) 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4lnotfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutz4l_reco+" && "+cutchan_gen_out+" && (passedFiducialTopology==0 || !("+cutz4l_gen+") || !("+cutm4l_gen+")) )","goff")
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4lfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutz4l_reco+" && passedFiducialTopology==1 && "+cutz4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen+")","goff")
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4lotherfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutz4l_reco+" && passedFiducialTopology==1 && "+cutz4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen_otherfid+")","goff")

 
        if (Histos[processBin+"fs"].Integral()>0):
            acceptance[processBin] = Histos[processBin+"fid"].Integral()/Histos[processBin+"fs"].Integral()
            dacceptance[processBin] = 0.0#sqrt(acceptance[processBin]*(1.0-acceptance[processBin])/Histos[processBin+"fs"].Integral())
            nfid[processBin] = Histos[processBin+"fid"].Integral()
            nfs[processBin] = Histos[processBin+"fs"].Integral()
        else:
            acceptance[processBin] = -1.0
            dacceptance[processBin] = -1.0                      
            nfid[processBin] = -1.0
            nfs[processBin] = -1.0               

        if (Histos[processBin+"fid"].Integral()>0.0):
            effrecotofid[processBin] = Histos[processBin+"recoz4lfid"].Integral()/Histos[processBin+"fid"].Integral()
            deffrecotofid[processBin] = 0.0#sqrt(effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral())
            nrecofid[processBin] = Histos[processBin+"recoz4lfid"].Integral()
        else:
            effrecotofid[processBin] = -1.0
            deffrecotofid[processBin] = -1.0
            nrecofid[processBin] = -1.0

        if ( (Histos[processBin+"recoz4lfid"].Integral()+Histos[processBin+"recoz4lotherfid"].Integral())>0.0):
            outinratio[processBin] = Histos[processBin+"recoz4lnotfid"].Integral()/(Histos[processBin+"recoz4lfid"].Integral()+Histos[processBin+"recoz4lotherfid"].Integral())
            nreconotfid[processBin] = Histos[processBin+"recoz4lnotfid"].Integral()
            nrecootherfid[processBin] = Histos[processBin+"recoz4lotherfid"].Integral()
            if (Histos[processBin+"recoz4lnotfid"].Integral()>0):
                doutinratio[processBin] = 0.0#outinratio[processBin]*sqrt(1.0/(Histos[processBin+"recoz4lnotfid"].Integral())+1.0/(Histos[processBin+"recoz4lfid"].Integral()+Histos[processBin+"recoz4lotherfid"].Integral()))
            else: doutinratio[processBin] = 0.0
        else:
            outinratio[processBin] = -1.0
            doutinratio[processBin] = -1.0
            nreconotfid[processBin] = -1.0 
            nrecootherfid[processBin] = -1.0 

          
        if (opt.OBSNAME == "nJets" or opt.OBSNAME.startswith("njets")):

            if (Histos[processBin+"recoz4l"].Integral()>0):
                lambdajesup[processBin] = (Histos[processBin+"recoz4l_jesup"].Integral()-Histos[processBin+"recoz4l"].Integral())/Histos[processBin+"recoz4l"].Integral()
                lambdajesdn[processBin] = (Histos[processBin+"recoz4l_jesdn"].Integral()-Histos[processBin+"recoz4l"].Integral())/Histos[processBin+"recoz4l"].Integral()
                nreco[processBin] = Histos[processBin+"recoz4l"].Integral()
                nrecojesup[processBin] = Histos[processBin+"recoz4l_jesup"].Integral()
                nrecojesdn[processBin] = Histos[processBin+"recoz4l_jesdn"].Integral()
            else:
                lambdajesup[processBin] = 0.0
                lambdajesdn[processBin] = 0.0
                nreco[processBin] = 0.0
                nrecojesup[processBin] = 0.0
                nrecojesdn[processBin] = 0.0
        else:
            lambdajesup[processBin] = 0.0
            lambdajesdn[processBin] = 0.0
            nreco[processBin] = 0.0
            nrecojesup[processBin] = 0.0
            nrecojesdn[processBin] = 0.0
 
        print processBin,"acc",round(acceptance[processBin],3),"eff",round(effrecotofid[processBin],3),"outinratio",round(outinratio[processBin],3)   
        print processBin,"nfs",round(nfs[processBin],3),"nfid",round(nfid[processBin],3),"nrecofid",round(nrecofid[processBin],3),"nreconotfid",round(nreconotfid[processBin],3),"nrecootherfid",round(nrecootherfid[processBin],3)   
   

if (opt.OBSNAME == "massZ1"):
    obs_reco = "massZ1"
    obs_gen = "GENmZ1"
if (opt.OBSNAME == "massZ2"):
    obs_reco = "massZ2"
    obs_gen = "GENmZ2"
if (opt.OBSNAME == "pT4l"):
    obs_reco = "pT4l"
    obs_gen = "GENpT4l"
if (opt.OBSNAME == "eta4l"):
    obs_reco = "eta4l"
    obs_gen = "GENeta4l"
if (opt.OBSNAME== "njets_reco_pt30_eta4p7"):
    obs_reco = "njets_reco_pt30_eta4p7"
    obs_gen = "njets_gen_pt30_eta4p7"
if (opt.OBSNAME== "njets_reco_pt25_eta4p7"):
    obs_reco = "njets_reco_pt25_eta4p7"
    obs_gen = "njets_gen_pt25_eta4p7"
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
if (opt.OBSNAME == "cosTheta1"):
    obs_reco = "abs(cosTheta1)"
    obs_gen = "abs(GENcosTheta1)"
if (opt.OBSNAME == "cosTheta2"):
    obs_reco = "abs(cosTheta2)"
    obs_gen = "abs(GENcosTheta2)"
if (opt.OBSNAME == "Phi"):
    obs_reco = "abs(Phi)"
    obs_gen = "abs(GENPhi)"
if (opt.OBSNAME == "Phi1"):
    obs_reco = "abs(Phi1)"
    obs_gen = "abs(Phi1)"


obs_bins = opt.OBSBINS.split("|")
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins.pop()
obs_bins.pop(0)





for chan in ['4e','4mu','2e2mu']:
    List =  ['ZZTo'+chan+'_8TeV-powheg-pythia6']
    for recobin in range(len(obs_bins)-1):
        for genbin in range(len(obs_bins)-1):
            geteffs_z4l_diff(chan, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin) 
 
for chan in ['4e','4mu','2e2mu']:
    List =  ['ZZTo'+chan+'_8TeV-powheg-pythia6_mll1_tchan']
    for recobin in range(len(obs_bins)-1):
        for genbin in range(len(obs_bins)-1):
            geteffs_z4l_diff(chan, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin)

for recobin in range(len(obs_bins)-1):
    for genbin in range(len(obs_bins)-1):
        geteffs_z4l_schan_diff(recobin, genbin)


with open ('datacardInputs/inputs_sig_z4l_'+opt.OBSNAME+'.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('dacc = '+str(dacceptance)+' \n')
    f.write('eff = '+str(effrecotofid)+' \n')
    f.write('deff = '+str(deffrecotofid)+' \n')
    f.write('outinratio = '+str(outinratio)+' \n')
    f.write('doutinratio = '+str(doutinratio)+' \n')
    if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
        f.write('lambdajesup = '+str(lambdajesup)+' \n')
        f.write('lambdajesdn = '+str(lambdajesdn)+' \n')
    f.write('nfid = '+str(nfid)+' \n')
    f.write('nfs = '+str(nfs)+' \n')
    f.write('nreco = '+str(nreco)+' \n')
    f.write('nrecofid = '+str(nrecofid)+' \n')
    f.write('nreconotfid = '+str(nreconotfid)+' \n')
    f.write('nrecootherfid = '+str(nrecootherfid)+' \n')
    f.write('nrecojesup = '+str(nrecojesup)+' \n')
    f.write('nrecojesdn = '+str(nrecojesdn)+' \n')
    

#write fout
fout = TFile("plots_z4l/qqZZst_qqZZtchan_"+opt.OBSNAME+"_"+recoweight+".root","recreate");
for chan in ['4e','4mu','2e2mu']:
    for process in ['qqZZst','qqZZtchan']:
        for recobin in range(len(obs_bins)-1):
            for genbin in range(len(obs_bins)-1):
                processBin = process+'_'+chan+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)
                fout.WriteTObject(Histos[processBin+"recoz4lfid"])
                fout.WriteTObject(Histos[processBin+"recoz4lnotfid"])
                fout.WriteTObject(Histos[processBin+"recoz4lotherfid"])
                fout.WriteTObject(Histos[processBin+"fid"])
                fout.WriteTObject(Histos[processBin+"fs"])
                fout.WriteTObject(Histos[processBin+"recoz4l"])
                if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
                    fout.WriteTObject(Histos[processBin+"recoz4l_jesup"])
                    fout.WriteTObject(Histos[processBin+"recoz4l_jesdn"])


fout.Close()
