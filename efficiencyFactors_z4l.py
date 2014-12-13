
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

if (not os.path.exists("plots_z4l") and doPlots):
    os.system("mkdir plots_z4l")

from ROOT import *
from LoadData_ratio import *
LoadData(opt.SOURCEDIR)
save = ""

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    

if (opt.DOPLOTS and os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()

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

nfid = {}
nfs = {}
nrecofid = {}
nreconotfid = {}

dnfid = {}
dnfs = {}
dnrecofid = {}
dnreconotfid = {}

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

def geteffs_z4l_schan():

    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");

    processBinST_4l = 'qqZZst_4l_mass4l_genbin0_recobin0'
    processBinT_4l = 'qqZZtchan_4l_mass4l_genbin0_recobin0'
    processBinS_4l = 'SMZ4l_4l_mass4l_genbin0_recobin0'

    nfid[processBinS_4l] = 0.0
    nfs[processBinS_4l] = 0.0
    nrecofid[processBinS_4l] = 0.0
    nreconotfid[processBinS_4l] = 0.0

    nfid[processBinT_4l] = 0.0
    nfs[processBinT_4l] = 0.0
    nrecofid[processBinT_4l] = 0.0
    nreconotfid[processBinT_4l] = 0.0

    nfid[processBinST_4l] = 0.0
    nfs[processBinST_4l] = 0.0
    nrecofid[processBinST_4l] = 0.0
    nreconotfid[processBinST_4l] = 0.0


    # '4e','4mu','2e2mu'
    for channel in ['4e','4mu','2e2mu']:
        processBinST = 'qqZZst_'+channel+'_mass4l_genbin0_recobin0'
        processBinT = 'qqZZtchan_'+channel+'_mass4l_genbin0_recobin0'
        processBinS = 'SMZ4l_'+channel+'_mass4l_genbin0_recobin0'

        nfid[processBinS] = nfid[processBinST] - nfid[processBinT]
        nfs[processBinS] = nfs[processBinST] - nfs[processBinT]
        nrecofid[processBinS] = nrecofid[processBinST] - nrecofid[processBinT]
        nreconotfid[processBinS] = nreconotfid[processBinST] - nreconotfid[processBinT]

        nfid[processBinS_4l] += nfid[processBinS]
        nfs[processBinS_4l] += nfs[processBinS]
        nrecofid[processBinS_4l] += nrecofid[processBinS]
        nreconotfid[processBinS_4l] += nreconotfid[processBinS]

        nfid[processBinT_4l] += nfid[processBinT]
        nfs[processBinT_4l] += nfs[processBinT]
        nrecofid[processBinT_4l] += nrecofid[processBinT]
        nreconotfid[processBinT_4l] += nreconotfid[processBinT]

        nfid[processBinST_4l] += nfid[processBinST]
        nfs[processBinST_4l] += nfs[processBinST]
        nrecofid[processBinST_4l] += nrecofid[processBinST]
        nreconotfid[processBinST_4l] += nreconotfid[processBinST]


        acceptance[processBinS] =  nfid[processBinS] / nfs[processBinST]
        dacceptance[processBinS] = sqrt(acceptance[processBinS]*(1.0-acceptance[processBinS])/nfs[processBinST])

        effrecotofid[processBinS] = nrecofid[processBinS]/nfid[processBinS]
        deffrecotofid[processBinS] = sqrt(effrecotofid[processBinS]*(1-effrecotofid[processBinS])/nfid[processBinS])

        outinratio[processBinS] = nreconotfid[processBinS]/nrecofid[processBinS]
        doutinratio[processBinS] = outinratio[processBinS]*sqrt(1.0/(nreconotfid[processBinS])+1.0/(nrecofid[processBinS]))
    
        print processBinS,"acc",round(acceptance[processBinS],3),"eff",round(effrecotofid[processBinS],3),"outinratio",round(outinratio[processBinS],3)

    # '4l'    
    # s
    acceptance[processBinS_4l] =  nfid[processBinS_4l] / nfs[processBinST_4l] 
    dacceptance[processBinS_4l] = sqrt(acceptance[processBinS_4l]*(1.0-acceptance[processBinS_4l])/nfs[processBinST_4l])
    effrecotofid[processBinS_4l] = nrecofid[processBinS_4l]/nfid[processBinS_4l]
    deffrecotofid[processBinS_4l] = sqrt(effrecotofid[processBinS_4l]*(1-effrecotofid[processBinS_4l])/nfid[processBinS_4l])
    outinratio[processBinS_4l] = nreconotfid[processBinS_4l]/nrecofid[processBinS_4l]
    doutinratio[processBinS_4l] = outinratio[processBinS_4l]*sqrt(1.0/(nreconotfid[processBinS_4l])+1.0/(nrecofid[processBinS_4l]))
    # t
    acceptance[processBinT_4l] =  nfid[processBinT_4l] / nfs[processBinT_4l]
    dacceptance[processBinT_4l] = sqrt(acceptance[processBinT_4l]*(1.0-acceptance[processBinT_4l])/nfs[processBinT_4l])
    effrecotofid[processBinT_4l] = nrecofid[processBinT_4l]/nfid[processBinT_4l]
    deffrecotofid[processBinT_4l] = sqrt(effrecotofid[processBinT_4l]*(1-effrecotofid[processBinT_4l])/nfid[processBinT_4l])
    outinratio[processBinT_4l] = nreconotfid[processBinT_4l]/nrecofid[processBinT_4l]
    doutinratio[processBinT_4l] = outinratio[processBinT_4l]*sqrt(1.0/(nreconotfid[processBinT_4l])+1.0/(nrecofid[processBinT_4l]))
    # st
    acceptance[processBinST_4l] =  nfid[processBinST_4l] / nfs[processBinST_4l]
    dacceptance[processBinST_4l] = sqrt(acceptance[processBinST_4l]*(1.0-acceptance[processBinST_4l])/nfs[processBinST_4l])
    effrecotofid[processBinST_4l] = nrecofid[processBinST_4l]/nfid[processBinST_4l]
    deffrecotofid[processBinST_4l] = sqrt(effrecotofid[processBinST_4l]*(1-effrecotofid[processBinST_4l])/nfid[processBinST_4l])
    outinratio[processBinST_4l] = nreconotfid[processBinST_4l]/nrecofid[processBinST_4l]
    doutinratio[processBinST_4l] = outinratio[processBinST_4l]*sqrt(1.0/(nreconotfid[processBinST_4l])+1.0/(nrecofid[processBinST_4l]))

    print processBinS_4l,"acc",round(acceptance[processBinS_4l],3),"eff",round(effrecotofid[processBinS_4l],3),"outinratio",round(outinratio[processBinS_4l],3)


def geteffs_z4l(channel, List):    
    
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");
            

    for Sample in List:
    
        if (not Sample in TreesPassedEvents): continue
        if (not TreesPassedEvents[Sample]): continue
        if (not channel in Sample): continue 
        
        print Sample," ", channel

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
        processBin = shortname+'_'+channel+'_mass4l_genbin0_recobin0'

        # RECO level
        Histos[processBin+"recoz4l"] = TH1D(processBin+"recoz4l", processBin+"recoz4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoz4l"].Sumw2()
        Histos[processBin+"reconotz4l"] = TH1D(processBin+"reconotz4l", processBin+"reconotz4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reconotz4l"].Sumw2() 
                                    
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
        
        # GEN level 
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fid","("+genweight+")*("+cutm4l_gen+" && "+cutchan_gen+" && passedFiducialTopology==1)","goff") 
        TreesPassedEventsNoHLT[Sample].Draw("GENmZ1Z2 >> "+processBin+"fs","("+genweight+")*("+cutchan_gen_out+")","goff")
        
        # RECO level 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4l","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 )","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"reconotz4l","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && (!"+cutm4l_reco+"))","goff")  

        # RECO and GEN level ( i.e. f(in) and f(out) ) 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4lnotfid","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cutchan_gen_out+" && (passedFiducialTopology==0 || !("+cutm4l_gen+")) )","goff") 
        TreesPassedEvents[Sample].Draw("mass4l >> "+processBin+"recoz4lfid","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && passedFiducialTopology==1 && "+cutm4l_gen+" && "+cutchan_gen+")","goff")  
        
        if (Histos[processBin+"fs"].Integral()>0):
            acceptance[processBin] = Histos[processBin+"fid"].Integral()/Histos[processBin+"fs"].Integral()
            dacceptance[processBin] = sqrt(acceptance[processBin]*(1.0-acceptance[processBin])/Histos[processBin+"fs"].Integral())
            nfid[processBin] = Histos[processBin+"fid"].Integral()
            nfs[processBin] = Histos[processBin+"fs"].Integral()
        else:
            acceptance[processBin] = -1.0
            dacceptance[processBin] = -1.0                      
            nfid[processBin] = -1.0
            nfs[processBin] = -1.0               

        if (Histos[processBin+"fid"].Integral()>0.0):
            effrecotofid[processBin] = Histos[processBin+"recoz4lfid"].Integral()/Histos[processBin+"fid"].Integral()
            deffrecotofid[processBin] = sqrt(effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral())
            nrecofid[processBin] = Histos[processBin+"recoz4lfid"].Integral()
        else:
            effrecotofid[processBin] = -1.0
            deffrecotofid[processBin] = -1.0
            nrecofid[processBin] = -1.0

        if (Histos[processBin+"recoz4lfid"].Integral()>0.0):
            outinratio[processBin] = Histos[processBin+"recoz4lnotfid"].Integral()/(Histos[processBin+"recoz4lfid"].Integral())
            nreconotfid[processBin] = Histos[processBin+"recoz4lnotfid"].Integral()
            if (Histos[processBin+"recoz4lnotfid"].Integral()>0):
                doutinratio[processBin] = outinratio[processBin]*sqrt(1.0/(Histos[processBin+"recoz4lnotfid"].Integral())+1.0/(Histos[processBin+"recoz4lfid"].Integral()))
            else: doutinratio[processBin] = 0.0
        else:
            outinratio[processBin] = -1.0
            doutinratio[processBin] = -1.0
            nreconotfid[processBin] = -1.0 
           
        print processBin,"acc",round(acceptance[processBin],3),"eff",round(effrecotofid[processBin],3),"outinratio",round(outinratio[processBin],3)   
   
def plot_z4l(channel):

    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include");

    recoweight = RecoWeight
    hs = {}
    # draw for each process
    for process in ['qqZZst', 'qqZZtchan']:
        processBin = process+'_'+channel+'_mass4l_genbin0_recobin0'
        n_outsig = Histos[processBin+"recoz4lnotfid"].Integral()
        n_truesig = Histos[processBin+"recoz4lfid"].Integral()

        hs[process] = THStack("hs_"+process,"mass spectrum");
        Histos[processBin+"recoz4lnotfid"].SetFillColor(0)
        Histos[processBin+"recoz4lnotfid"].SetLineColor(kBlack)
        hs[process].Add(Histos[processBin+"recoz4lnotfid"])
        Histos[processBin+"recoz4lfid"].SetFillColor(0)
        Histos[processBin+"recoz4lfid"].SetLineColor(kRed)
        hs[process].Add(Histos[processBin+"recoz4lfid"])

        leg = TLegend(0.54,0.57,0.91,0.72);
        leg.SetShadowColor(0)
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        leg.AddEntry(Histos[processBin+"recoz4lnotfid"],"N_{out}^{MC} = "+str(int(n_outsig)), "F")

        c = TCanvas("c","c",750,750)
        SetOwnership(c,False)
        c.cd()

        hs[process].SetMaximum(1.15*hs[process].GetMaximum())
        hs[process].Draw("ehist")
        if (channel == "4l"): hs[process].GetXaxis().SetTitle("m_{4l} (GeV)")
        if (channel == "4e"): hs[process].GetXaxis().SetTitle("m_{4e} (GeV)")
        if (channel == "4mu"): hs[process].GetXaxis().SetTitle("m_{4#mu} (GeV)")
        if (channel == "2e2mu"): hs[process].GetXaxis().SetTitle("m_{2e2#mu} (GeV)")

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
        latex2.DrawLatex(0.20, 0.73, process.replace('_',' ')+' GeV');
        latex2.SetTextSize(0.35*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.20, 0.68, str(m4l_low)+" < m(4l) < "+str(m4l_high) )
        latex2.DrawLatex(0.20, 0.48, "N_{fiducial}^{gen} = "+str(int(Histos[processBin+"fid"].Integral())) )
        latex2.DrawLatex(0.20, 0.64, "N_{fid.}^{MC} = "+str(int(n_truesig)) )
        latex2.DrawLatex(0.20, 0.56, "N_{not fid.}^{MC} = "+str(int(n_outsig)) )
        latex2.DrawLatex(0.20, 0.44, "eff^{MC} = %.3f #pm %.3f" % (effrecotofid[processBin],deffrecotofid[processBin]))

        c.SaveAs("plots_z4l/"+processBin+"_effs_"+recoweight+".png")
        c.SaveAs("plots_z4l/"+processBin+"_effs_"+recoweight+".pdf")
        c.SaveAs("plots_z4l/"+processBin+"_effs_"+recoweight+".C")

    #plot qqZZst and qqZZtchan together
    c = TCanvas("c","c",750,750)
    SetOwnership(c,False)
    c.cd()
    hs['qqZZst'].Draw("ehist")
    hs['qqZZtchan'].Draw("ehistsame")
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
    latex2.DrawLatex(0.20, 0.73, process.replace('_',' ')+' GeV');
    latex2.SetTextSize(0.35*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.DrawLatex(0.20, 0.68, str(m4l_low)+" < m(4l) < "+str(m4l_high) ) 

    c.SaveAs("plots_z4l/qqZZst_qqZZtchan_"+channel+"_"+recoweight+".png")
    c.SaveAs("plots_z4l/qqZZst_qqZZtchan_"+channel+"_"+recoweight+".pdf") 
    c.SaveAs("plots_z4l/qqZZst_qqZZtchan_"+channel+"_"+recoweight+".C") 


#chans = ['4e','4mu','2e2mu','4l']
for chan in ['4e','4mu','2e2mu']:
    List =  ['ZZTo'+chan+'_8TeV-powheg-pythia6']
    geteffs_z4l(chan, List) 
 
for chan in ['4e','4mu','2e2mu']:
    List =  ['ZZTo'+chan+'_8TeV-powheg-pythia6_mll1_tchan']
    geteffs_z4l(chan, List)

geteffs_z4l_schan()

with open ('datacardInputs/inputs_sig_z4l_mass4l.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('dacc = '+str(dacceptance)+' \n')
    f.write('eff = '+str(effrecotofid)+' \n')
    f.write('deff = '+str(deffrecotofid)+' \n')
    f.write('outinratio = '+str(outinratio)+' \n')
    f.write('doutinratio = '+str(doutinratio)+' \n')
    
    
if (doPlots):
    for chan in ['4e','4mu','2e2mu']:
        plot_z4l(chan)

#write fout
fout = TFile("plots_z4l/qqZZst_qqZZtchan_"+recoweight+".root","recreate");
for chan in ['4e','4mu','2e2mu']:
    for process in ['qqZZst','qqZZtchan']:
        processBin = process+'_'+chan+'_mass4l_genbin0_recobin0'
        fout.WriteTObject(Histos[processBin+"recoz4lnotfid"])
        fout.WriteTObject(Histos[processBin+"recoz4lfid"])
        fout.WriteTObject(Histos[processBin+"fid"])
        fout.WriteTObject(Histos[processBin+"fs"])
        fout.WriteTObject(Histos[processBin+"recoz4l"])
        fout.WriteTObject(Histos[processBin+"reconotz4l"])
fout.Close()
