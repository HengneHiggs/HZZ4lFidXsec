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
    parser.add_option('',   '--resultFile',dest='resultFile',type='string',default='resultFile.root', help='result root file from the combine fit.')
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

if (not os.path.exists("plots_ratio")):
    os.system("mkdir plots_ratio")
    
from ROOT import *
from tdrStyle import *
setTDRStyle()

def plotAsimov(fstate):

    channel = {"4mu":"1", "4e":"2", "2e2mu":"3", "4l":"1"}

    # Load some libraries                                 
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")
    
    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
    
    f_asimov = TFile(opt.resultFile, 'READ')
    data = f_asimov.Get("toys/toy_asimov");
    #data.Print("v");
    w_asimov = f_asimov.Get("w")
    #w_asimov.loadSnapshot("MultiDimFit")
    w_asimov.loadSnapshot("clean")

    trueH_asimov = {}
    trueZ_asimov = {}
    zjets_asimov = {}
    ggzz_asimov = {}
    fakeH_asimov = {}
    out_trueH_asimov = {}
    out_trueZ_asimov = {}
    qqzz_asimov = {}
    n_trueH_asimov = {}
    n_trueH_asimov["4l"] = 0.0
    n_trueZ_asimov = {}
    n_trueZ_asimov["4l"] = 0.0
    n_zjets_asimov = {}
    n_zjets_asimov["4l"] = 0.0
    n_ggzz_asimov = {}
    n_ggzz_asimov["4l"] = 0.0
    n_fakeH_asimov = {}
    n_fakeH_asimov["4l"] = 0.0
    n_out_trueH_asimov = {}
    n_out_trueH_asimov["4l"] = 0.0
    n_out_trueZ_asimov = {}
    n_out_trueZ_asimov["4l"] = 0.0
    n_qqzz_asimov = {}
    n_qqzz_asimov["4l"] = 0.0
    n_zz_asimov = {}
    n_zz_asimov["4l"] = 0.0
    
                                                                        
    fStates = ['4mu','4e','2e2mu']    
    for fState in fStates:
        trueH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_trueH"+fState)
        trueZ_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_trueZ"+fState)
        zjets_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_zjets")
        ggzz_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_ggzz")
        fakeH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_fakeH")
        out_trueH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueH")
        out_trueZ_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueZ")
        qqzz_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_qqzz")
        n_trueH_asimov[fState] = trueH_asimov[fState].getVal()
        n_trueZ_asimov[fState] = trueZ_asimov[fState].getVal()
        n_zjets_asimov[fState] = zjets_asimov[fState].getVal()
        n_ggzz_asimov[fState] = ggzz_asimov[fState].getVal() 
        n_fakeH_asimov[fState] = fakeH_asimov[fState].getVal()
        n_out_trueH_asimov[fState] = out_trueH_asimov[fState].getVal()
        n_out_trueZ_asimov[fState] = out_trueZ_asimov[fState].getVal()
        n_qqzz_asimov[fState] = qqzz_asimov[fState].getVal()
        n_zz_asimov[fState] = n_ggzz_asimov[fState]+n_qqzz_asimov[fState]
        n_trueH_asimov["4l"] += trueH_asimov[fState].getVal()
        n_trueZ_asimov["4l"] += trueZ_asimov[fState].getVal()
        n_zjets_asimov["4l"] += zjets_asimov[fState].getVal()
        n_ggzz_asimov["4l"] += ggzz_asimov[fState].getVal()
        n_fakeH_asimov["4l"] += fakeH_asimov[fState].getVal()
        n_out_trueH_asimov["4l"] += out_trueH_asimov[fState].getVal()
        n_out_trueZ_asimov["4l"] += out_trueZ_asimov[fState].getVal()
        n_qqzz_asimov["4l"] += qqzz_asimov[fState].getVal()
        n_zz_asimov["4l"] += n_ggzz_asimov[fState]+n_qqzz_asimov[fState]                                                                
        
    #f_modelfit = TFile(opt.resultFile,'READ')
    #w_modelfit = f_modelfit.Get("w")    
    w_modelfit = w_asimov #f_modelfit.Get("w")    
    sim = w_modelfit.pdf("model_s")
    #sim.Print("v")
    if (fstate=="4l"): pdfi = sim.getPdf("ch1")
    else: pdfi = sim.getPdf("ch"+channel[fstate])     
    CMS_zz4l_mass = w_modelfit.var("CMS_zz4l_mass")
    w_modelfit.loadSnapshot("MultiDimFit")
    #w_modelfit.loadSnapshot("clean")
    #pdfi.Print("v")

    trueH_modelfit = {}
    trueZ_modelfit = {}
    zjets_modelfit = {}
    ggzz_modelfit = {}
    fakeH_modelfit = {}
    out_trueH_modelfit = {}
    out_trueZ_modelfit = {}
    qqzz_modelfit = {}
    n_trueH_modelfit = {}
    n_trueH_modelfit["4l"] = 0.0
    n_trueZ_modelfit = {}
    n_trueZ_modelfit["4l"] = 0.0
    n_zjets_modelfit = {}
    n_zjets_modelfit["4l"] = 0.0
    n_ggzz_modelfit = {}
    n_ggzz_modelfit["4l"] = 0.0
    n_fakeH_modelfit = {}
    n_fakeH_modelfit["4l"] = 0.0
    n_out_trueH_modelfit = {}
    n_out_trueH_modelfit["4l"] = 0.0
    n_out_trueZ_modelfit = {}
    n_out_trueZ_modelfit["4l"] = 0.0
    n_qqzz_modelfit = {}
    n_qqzz_modelfit["4l"] = 0.0
    n_zz_modelfit = {}
    n_zz_modelfit["4l"] = 0.0
        
    for fState in fStates:
        trueH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_trueH"+fState)
        trueZ_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_trueZ"+fState)
        zjets_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_zjets")
        ggzz_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_ggzz")
        fakeH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_fakeH")
        out_trueH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueH")
        out_trueZ_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueZ")
        qqzz_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_qqzz")
        n_trueH_modelfit[fState] = trueH_modelfit[fState].getVal()
        n_trueZ_modelfit[fState] = trueZ_modelfit[fState].getVal()
        n_zjets_modelfit[fState] = zjets_modelfit[fState].getVal()
        n_ggzz_modelfit[fState] = ggzz_modelfit[fState].getVal()
        n_fakeH_modelfit[fState] = fakeH_modelfit[fState].getVal()
        n_out_trueH_modelfit[fState] = out_trueH_modelfit[fState].getVal()
        n_out_trueZ_modelfit[fState] = out_trueZ_modelfit[fState].getVal()
        n_qqzz_modelfit[fState] = qqzz_modelfit[fState].getVal()
        n_zz_modelfit[fState] = n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]
        n_trueH_modelfit["4l"] += trueH_modelfit[fState].getVal()
        n_trueZ_modelfit["4l"] += trueZ_modelfit[fState].getVal()
        n_zjets_modelfit["4l"] += zjets_modelfit[fState].getVal()
        n_ggzz_modelfit["4l"] += ggzz_modelfit[fState].getVal()
        n_fakeH_modelfit["4l"] += fakeH_modelfit[fState].getVal()
        n_out_trueH_modelfit["4l"] += out_trueH_modelfit[fState].getVal()
        n_out_trueZ_modelfit["4l"] += out_trueZ_modelfit[fState].getVal()
        n_qqzz_modelfit["4l"] += qqzz_modelfit[fState].getVal()
        n_zz_modelfit["4l"] += n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]
                                                    
    CMS_channel = w.cat("CMS_channel")
    mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(30))

    if (fstate=="4l"):
        data.plotOn(mass)
        sim.plotOn(mass,RooFit.LineColor(kRed), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3,shapeBkg_out_trueH_ch1,shapeBkg_out_trueH_ch2,shapeBkg_out_trueH_ch3,shapeSig_trueH4mu_ch1,shapeSig_trueH4e_ch2,shapeSig_trueH2e2mu_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(3), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3,shapeBkg_out_trueH_ch1,shapeBkg_out_trueH_ch2,shapeBkg_out_trueH_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kMagenta), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3,shapeBkg_out_trueZ_ch1,shapeBkg_out_trueZ_ch2,shapeBkg_out_trueZ_ch3,shapeSig_trueZ4mu_ch1,shapeSig_trueZ4e_ch2,shapeSig_trueZ2e2mu_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kMagenta), RooFit.LineWidth(2), RooFit.LineStyle(3), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3,shapeBkg_out_trueZ_ch1,shapeBkg_out_trueZ_ch2,shapeBkg_out_trueZ_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kOrange), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3"), RooFit.ProjWData(data,True))
    else:
        sbin = "ch"+channel[fstate]
        data = data.reduce(RooFit.Cut("CMS_channel==CMS_channel::"+sbin))
        data.plotOn(mass)
        pdfi.plotOn(mass, RooFit.Components("pdf_binch"+channel[fstate]+"_nuis"),RooFit.LineColor(kRed), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin+",shapeBkg_out_trueH_"+sbin+",shapeSig_trueH"+fstate+"_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin+",shapeBkg_out_trueH_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kMagenta),RooFit.LineWidth(2), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin+",shapeBkg_out_trueZ_"+sbin+",shapeSig_trueZ"+fstate+"_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kMagenta),RooFit.LineWidth(2), RooFit.LineStyle(3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin+",shapeBkg_out_trueZ_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))

        pdfi.plotOn(mass, RooFit.LineColor(kOrange), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        
    gStyle.SetOptStat(0)

    c = TCanvas("c","c",1000,800)
    c.cd()

    dummy = TH1D("","",1,50,140)
    dummy.SetBinContent(1,2)
    dummy.SetFillColor(0)
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.SetMarkerColor(0) 
    dummy.GetYaxis().SetTitle("Events / (2 GeV)")
    dummy.GetXaxis().SetTitle("m_{"+fstate.replace("mu","#mu")+"} [GeV]")
    dummy.SetMaximum(0.7*max(n_trueZ_asimov[fstate],n_trueZ_modelfit[fstate]))
    dummy.SetMinimum(0.0)
    dummy.Draw()
    
    mass.Draw("same")

    dummy_data = TH1D()
    dummy_data.SetMarkerColor(kBlack)
    dummy_data.SetMarkerStyle(20)
    dummy_fid = TH1D()
    dummy_fid.SetLineColor(kRed)
    dummy_fid.SetLineWidth(2)
    dummy_out = TH1D()
    dummy_out.SetLineColor(kRed)
    dummy_out.SetLineWidth(2)
    dummy_out.SetLineStyle(3)
    dummy_fidZ = TH1D()
    dummy_fidZ.SetLineColor(kMagenta)
    dummy_fidZ.SetLineWidth(2)
    dummy_outZ = TH1D()
    dummy_outZ.SetLineColor(kMagenta)
    dummy_outZ.SetLineWidth(2)
    dummy_outZ.SetLineStyle(3)
    dummy_fake = TH1D()
    dummy_fake.SetLineColor(kOrange)
    dummy_fake.SetLineWidth(2)
    dummy_zz = TH1D()
    dummy_zz.SetLineColor(kAzure-3)
    dummy_zz.SetLineWidth(2)
    dummy_zx = TH1D()
    dummy_zx.SetLineColor(kGreen+3)
    dummy_zx.SetLineWidth(2)

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
    latex2.SetTextSize(0.9*c.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.24, 0.85, "CMS")
    latex2.SetTextSize(0.7*c.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.22, 0.8, "Preliminary")
    latex2.SetTextFont(42)
    latex2.SetTextSize(0.45*c.GetTopMargin())
    latex2.DrawLatex(0.20, 0.73, 'Unfolding Model SM 125 GeV')
    
    lg1 = TLegend(0.6, 0.52,0.93,0.85)
    lg1.SetName("lg1")
    lg1.AddEntry(dummy_data,"Asimov Data","ep")
    lg1.AddEntry(dummy_data,"(SM m(H) = 125.0 GeV)","")
    lg1.AddEntry(dummy_fid, "Fiducial H#rightarrow 4l", "l")
    lg1.AddEntry(dummy_out, "Non-fiducial H#rightarrow 4l", "l")
    lg1.AddEntry(dummy_fake, "Non-resonant H#rightarrow 4l", "l")
    
    lg2 = TLegend(0.2, 0.5,0.5,0.7)
    lg2.SetName("lg2")
    lg2.AddEntry(dummy_fidZ, "Fiducial Z#rightarrow 4l", "l")
    lg2.AddEntry(dummy_outZ, "Non-fiducial Z#rightarrow 4l", "l")
    lg2.AddEntry(dummy_zz, "qqZZ(t-chan.) + ggZZ", "l")
    lg2.AddEntry(dummy_zx, "Z+X", "l")

    lg1.SetShadowColor(0);
    lg1.SetFillColor(0);
    lg1.SetLineColor(0);
    lg1.Draw()    
    lg2.SetShadowColor(0);
    lg2.SetFillColor(0);
    lg2.SetLineColor(0);
    lg2.Draw()

    plotFile = opt.resultFile.replace(".root","")             
    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".pdf")
    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".png")
    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".C")




for fState in ["4e","4mu","2e2mu","4l"]:
    plotAsimov(fState)
