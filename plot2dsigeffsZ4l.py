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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    
# parse the arguments and options
global opt, args
parseOptions()
sys.argv = grootargs
    
if (not os.path.exists("plots_z4l")):
    os.system("mkdir plots_z4l")
        
from ROOT import *
from tdrStyle import *
setTDRStyle()

ROOT.gStyle.SetPaintTextFormat("1.2f")
#ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetNumberContours(99)

obsName = opt.OBSNAME
if (obsName=='pT4l'):
    label = 'p_{T}(Z)'
if (obsName=='massZ2'):    
    label = 'm(Z_{2})'
if (obsName=='njets_reco_pt30_eta4p7'):
    label = "N(jets)"
if (obsName=='rapidity4l'):
    label = "|y(Z)|" 
if (obsName=='cosThetaStar'):
    label = "|cos(#theta*)|"

obs_bins = opt.OBSBINS.split("|")
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins.pop()
obs_bins.pop(0)
if float(obs_bins[len(obs_bins)-1])>150:
    obs_bins[len(obs_bins)-1]='150'
if (opt.OBSNAME=="nJets" or opt.OBSNAME.startswith("njets")):
    obs_bins[len(obs_bins)-1]='4'
                        

sys.path.append('./datacardInputs')
_temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['eff','deff'], -1)
eff = _temp.eff
deff = _temp.deff
_temp = __import__('moreinputs_sig_z4l_'+obsName, globals(), locals(), ['folding','dfolding','effanyreco','deffanyreco'], -1)
folding = _temp.folding
dfolding = _temp.dfolding
effanyreco = _temp.effanyreco
deffanyreco = _temp.deffanyreco

#modelNames = ['ggH_powheg15_JHUgen_125','VBF_powheg_125','WH_pythia_125','ZH_pythia_125','ttH_pythia_125']
modelNames = ['SMZ4l']
fStates = ['4e','4mu','2e2mu']

a_bins = array('d',[float(obs_bins[i]) for i in range(len(obs_bins))])
print a_bins        
for model in modelNames:
    for fState in fStates:
        eff2d = TH2D("eff2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        folding2d = TH2D("folding2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        eff2d4l = TH2D("eff2d4l", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        for x in range(0,4):
            for y in range(0,4):
                #eff2d.GetXaxis().SetBinLabel(x+1,str(x))
                #eff2d.GetYaxis().SetBinLabel(y+1,str(y))                
                bin = eff2d.GetBin(x+1,y+1)
                eff2d.SetBinContent(bin,eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #folding2d.GetXaxis().SetBinLabel(x+1,str(x))
                #folding2d.GetYaxis().SetBinLabel(y+1,str(y))
                folding2d.SetBinContent(bin,folding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                folding2d.SetBinError(bin,dfolding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #eff2d4l.GetXaxis().SetBinLabel(x+1,str(x))
                #eff2d4l.GetYaxis().SetBinLabel(y+1,str(y))
                #eff2d4l.SetBinContent(bin,effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #deff2d4l = sqrt((effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*dfolding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2+(folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*deffanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2)
                #eff2d4l.SetBinError(bin,deff2d4l) 
        c=TCanvas("c","c",1000,800)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d.GetXaxis().SetTitle(label+'(gen.)')
        eff2d.GetYaxis().SetTitle(label+'(reco.)')
        eff2d.GetZaxis().SetTitle('#epsilon^{ij} ('+fState.replace('mu','#mu')+')')
        eff2d.GetZaxis().SetRangeUser(0.0,1.0) 
        eff2d.Draw("colzTEXTE0")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Simulation")
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.45, 0.92, model.replace("_"," ")+" GeV")
        c.SaveAs("plots_z4l/eff2d_"+model+"_"+obsName+"_"+fState+".png")
        c.SaveAs("plots_z4l/eff2d_"+model+"_"+obsName+"_"+fState+".pdf")
        del c
        c=TCanvas("c","c",1000,800)                               
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        folding2d.GetXaxis().SetTitle(label+' (gen.)')
        folding2d.GetYaxis().SetTitle(label+' (reco.)')
        folding2d.GetZaxis().SetTitle('P^{ij} ('+fState.replace('mu','#mu')+')')
        folding2d.GetZaxis().SetRangeUser(0.0,1.0) 
        folding2d.Draw("colzTEXT0E") 
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Simulation")
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.45, 0.92, model.replace("_"," ")+" GeV")                        
        c.SaveAs("plots_z4l/folding2d_"+model+"_"+obsName+"_"+fState+".png")
        c.SaveAs("plots_z4l/folding2d_"+model+"_"+obsName+"_"+fState+".pdf")
        del c 
        c=TCanvas("c","c",1000,800)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d4l.GetXaxis().SetTitle(label+' (gen.)')
        eff2d4l.GetYaxis().SetTitle(label+' (reco.)')
        eff2d4l.GetZaxis().SetTitle('P^{ij}(4l)#epsilon^{i} ('+fState.replace('mu','#mu')+')')
        eff2d4l.GetZaxis().SetRangeUser(0.0,1.0)
        eff2d4l.Draw("colzTEXT0E")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Simulation")
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.45, 0.92, model.replace("_"," ")+" GeV")                        
        c.SaveAs("plots_z4l/eff2d4l_"+model+"_"+obsName+"_"+fState+".png")
        c.SaveAs("plots_z4l/eff2d4l_"+model+"_"+obsName+"_"+fState+".pdf")
        del c
        del eff2d
        del folding2d
        del eff2d4l
        
