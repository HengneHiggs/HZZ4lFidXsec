# this script is called once for each reco bin (obsBin)
# in each reco bin there are (nBins) signals (one for each gen bin)

from ROOT import *

def createXSworkspace(obsName, channel, nBins, obsBin, observableBins, usecfactor, addfakeH, modelName, physicalModel):

    obsBin_low = observableBins[obsBin]
    obsBin_high = observableBins[obsBin+1]

    obs_bin_lowest = observableBins[0]
    obs_bin_highest = observableBins[len(observableBins)-1]
    
    recobin = "recobin"+str(obsBin)

    doJES = 1
    
    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING) 

    #from inputs_sig import eff,inc_wrongfrac,binfrac_wrongfrac,inc_outfrac,binfrac_outfrac
    if (usecfactor):
        _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['cfactor','inc_wrongfrac','binfrac_wrongfrac','inc_outfrac','binfrac_outfrac','lambdajesup','lambdajesdn'], -1)
        cfactor = _temp.cfactor
        inc_outfrac = _temp.inc_outfrac
        binfrac_outfrac = _temp.binfrac_wrongfrac
    else:
        _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc','eff','inc_wrongfrac','binfrac_wrongfrac','outinratio','lambdajesup','lambdajesdn'], -1)
        acc = _temp.acc
        eff = _temp.eff
        outinratio = _temp.outinratio        

    lambdajesup = _temp.lambdajesup
    lambdajesdn = _temp.lambdajesdn        
    inc_wrongfrac = _temp.inc_wrongfrac
    binfrac_wrongfrac = _temp.binfrac_wrongfrac

    #from inputs_bkg_{obsName} import fractionsBackground
    _temp = __import__('inputs_bkg_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # Load the legacy workspace
    f_in = TFile("125.0/hzz4l_"+channel+"S_8TeV.input.root","READ")
    w = f_in.Get("w")
    #w.Print()

    # import h4l xs br
    _temp = __import__('higgs_xsbr', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
    higgs_xs = _temp.higgs_xs
    higgs4l_br = _temp.higgs4l_br

    # 4 lepton mass observable to perform the fit
    m = w.var("CMS_zz4l_mass")
    mass4e = RooRealVar("mass4e", "mass4e", 105.0, 140.0)
    mass4mu = RooRealVar("mass4mu", "mass4mu", 105.0, 140.0)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",105.0, 140.0)
    if (not obsName=="mass4l"):
        observable = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))
        observable.Print()

    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)
    
    # SM values of signal expectations (inclusive, reco level)
    ggH_norm = w.function("ggH_norm")
    qqH_norm = w.function("qqH_norm")
    WH_norm = w.function("WH_norm")
    ZH_norm = w.function("ZH_norm")
    ttH_norm = w.function("ttH_norm")

    n_allH = (ggH_norm.getVal()+qqH_norm.getVal()+WH_norm.getVal()+ZH_norm.getVal()+ttH_norm.getVal())
    print "n_allH",n_allH
    
    # true signal shape 
    trueH = w.pdf("ggH")
    
    # Wrong signal combination events

    if (channel=='4mu'):
        #p1_1_8 = RooRealVar("CMS_fakeH_p1_1_8","p1_1_8", 150.0, 135.0, 185.) 
        #p2_1_8 = RooRealVar("CMS_fakeH_p2_1_8","p2_1_8", 20.0, 10.0, 40.0) 
        p1_1_8 = RooRealVar("CMS_fakeH_p1_1_8","p1_1_8",165.0, 145.0, 185.0)       
        p3_1_8 = RooRealVar("CMS_fakeH_p3_1_8","p3_1_8",89.0, 84.0,94.0) 
        p2_1_8 = RooFormulaVar("CMS_fakeH_p2_1_8","p2_1_8","0.72*@0-@1",RooArgList(p1_1_8,p3_1_8))         
        fakeH = RooLandau("fakeH", "landau", m, p1_1_8, p2_1_8)
    if (channel=='4e'):
        #p1_2_8 = RooRealVar("CMS_fakeH_p1_2_8","p1_2_8", 150.0, 135.0, 185.)
        #p2_2_8 = RooRealVar("CMS_fakeH_p2_2_8","p2_2_8", 20.0, 10.0, 40.0) 
        p1_2_8 = RooRealVar("CMS_fakeH_p1_2_8","p1_2_8",165.0, 145.0, 185.0)       
        p3_2_8 = RooRealVar("CMS_fakeH_p3_2_8","p3_2_8",89.0, 84.0,94.0) 
        p2_2_8 = RooFormulaVar("CMS_fakeH_p2_2_8","p2_2_8","0.72*@0-@1",RooArgList(p1_2_8,p3_2_8))         
        fakeH = RooLandau("fakeH", "landau", m, p1_2_8, p2_2_8) 
    if (channel=='2e2mu'):
        #p1_3_8 = RooRealVar("CMS_fakeH_p1_3_8","p1_3_8", 150.0, 135.0, 185.) 
        #p2_3_8 = RooRealVar("CMS_fakeH_p2_3_8","p2_3_8", 20.0, 10.0, 40.0) 
        p1_3_8 = RooRealVar("CMS_fakeH_p1_3_8","p1_3_8",165.0, 145.0, 185.0)       
        p3_3_8 = RooRealVar("CMS_fakeH_p3_3_8","p3_3_8",89.0, 84.0,94.0) 
        p2_3_8 = RooFormulaVar("CMS_fakeH_p2_3_8","p2_3_8","0.72*@0-@1",RooArgList(p1_3_8,p3_3_8))         
        fakeH = RooLandau("fakeH", "landau", m, p1_3_8, p2_3_8) 

    if (addfakeH): 
        inc_wrongfrac_ggH=inc_wrongfrac["ggH_powheg15_JHUgen_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
        inc_wrongfrac_qqH=inc_wrongfrac["VBF_powheg_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
        inc_wrongfrac_WH=inc_wrongfrac["WH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
        inc_wrongfrac_ZH=inc_wrongfrac["ZH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
        inc_wrongfrac_ttH=inc_wrongfrac["ttH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    else:
        inc_wrongfrac_ggH=0.0
        inc_wrongfrac_qqH=0.0
        inc_wrongfrac_WH=0.0
        inc_wrongfrac_ZH=0.0
        inc_wrongfrac_ttH=0.0

    binfrac_wrongfrac_ggH=binfrac_wrongfrac["ggH_powheg15_JHUgen_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    binfrac_wrongfrac_qqH=binfrac_wrongfrac["VBF_powheg_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    binfrac_wrongfrac_WH=binfrac_wrongfrac["WH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    binfrac_wrongfrac_ZH=binfrac_wrongfrac["ZH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    binfrac_wrongfrac_ttH=binfrac_wrongfrac["ttH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]

    n_fakeH = binfrac_wrongfrac_ggH*inc_wrongfrac_ggH*ggH_norm.getVal()+binfrac_wrongfrac_qqH*inc_wrongfrac_qqH*qqH_norm.getVal()+binfrac_wrongfrac_WH*inc_wrongfrac_WH*WH_norm.getVal()+binfrac_wrongfrac_ZH*inc_wrongfrac_ZH*ZH_norm.getVal()+binfrac_wrongfrac_ttH*inc_wrongfrac_ttH*ttH_norm.getVal() 
    n_fakeH_var = RooRealVar("n_fakeH_var_"+recobin+"_"+channel,"n_fakeH_var_"+recobin+"_"+channel,n_fakeH);
    fakeH_norm = RooFormulaVar("fakeH_norm","@0",RooArgList(n_fakeH_var))


    # Out of acceptance events
    # (same shape as in acceptance shape)
    out_trueH = trueH.Clone()

    #if (not usecfactor):
    #    inc_outfrac_ggH=inc_outfrac["ggH_powheg15_JHUgen_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    inc_outfrac_qqH=inc_outfrac["VBF_powheg_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    inc_outfrac_WH=inc_outfrac["WH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    inc_outfrac_ZH=inc_outfrac["ZH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    inc_outfrac_ttH=inc_outfrac["ttH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]

    #    binfrac_outfrac_ggH=binfrac_outfrac["ggH_powheg15_JHUgen_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    binfrac_outfrac_qqH=binfrac_outfrac["VBF_powheg_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    binfrac_outfrac_WH=binfrac_outfrac["WH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    binfrac_outfrac_ZH=binfrac_outfrac["ZH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]
    #    binfrac_outfrac_ttH=binfrac_outfrac["ttH_pythia_125_"+channel+"_"+obsName+"_genbin0_"+recobin]

    #    n_out_trueH =  binfrac_outfrac_ggH*inc_outfrac_ggH*(1.0-inc_wrongfrac_ggH)*ggH_norm.getVal()
    #    n_out_trueH += binfrac_outfrac_qqH*inc_outfrac_qqH*(1.0-inc_wrongfrac_qqH)*qqH_norm.getVal()
    #    n_out_trueH += binfrac_outfrac_WH*inc_outfrac_WH*(1.0-inc_wrongfrac_WH)*WH_norm.getVal()
    #    n_out_trueH += binfrac_outfrac_ZH*inc_outfrac_ZH*(1.0-inc_wrongfrac_ZH)*ZH_norm.getVal()
    #    n_out_trueH += binfrac_outfrac_ttH*inc_outfrac_ttH*(1.0-inc_wrongfrac_ttH)*ttH_norm.getVal()
    #    n_out_trueH_var = RooRealVar("n_out_trueH_var_"+recobin+"_"+channel, "n_out_trueH_var_"+recobin+"_"+channel, n_out_trueH);
    
    #n_trueH = binfrac_true_ggH*(1.0-inc_outfrac_ggH)*(1.0-inc_wrongfrac_ggH)*ggH_norm.getVal() 
    #n_trueH_var = RooRealVar("n_fakeH_var_"+recobin+"_"+channel,"n_fakeH_var_"+recobin+"_"+channel,n_fakeH);
    #trueH_norm = RooFormulaVar("fakeH_norm","@0",RooArgList(n_fakeH_var))

    # true signal shape/norm
    trueH = w.pdf("ggH")
    
    # signal shape in different recobin
    trueH_shape = {}
    fideff = {}
    fideff_var = {}
    trueH_norm = {}

    # nuisance describes the jet energy scale uncertainty
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)
    if (obsName.startswith("njets")):
        lambda_JES_sig = lambdajesup[modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin, "lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin, lambda_JES_sig)    
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )

    for genbin in range(nBins-1):
        trueH_shape[genbin] = trueH.Clone();
        trueH_shape[genbin].SetName("trueH"+channel+"Bin"+str(genbin))
        if (usecfactor): fideff[genbin] = cfactor[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        else: fideff[genbin] = eff[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        fideff_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+channel,"effBin"+str(genbin)+"_"+recobin+"_"+channel, fideff[genbin]);

        if( not (obsName=='nJets' or obsName.startswith("njets")) or (not doJES)) :
            trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
        else :
            trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) ); 
 

    trueH_norm_final = {}
    fracBin = {}
    rBin = {}
    rBin_channel = {}
    fracSM4eBin = {}
    fracSM4muBin = {}
    K1Bin = {}
    K2Bin = {}
    SigmaBin = {}
    SigmaHBin = {}

    for genbin in range(nBins-1):
        if (physicalModel=="v3"):
            fidxs = {}
            for fState in ['4e','4mu', '2e2mu']:
                fidxs[fState] = 0
                fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']
                fidxs[fState] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']
                fidxs[fState] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']
                fidxs[fState] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']
                fidxs[fState] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']        
            fidxs['4l'] = fidxs['4e'] + fidxs['4mu'] + fidxs['2e2mu']
            
            fracSM4eBin[str(genbin)] = RooRealVar('fracSM4eBin'+str(genbin), 'fracSM4eBin'+str(genbin), fidxs['4e']/fidxs['4l'])
            fracSM4eBin[str(genbin)].setConstant(True)
            fracSM4muBin[str(genbin)] = RooRealVar('fracSM4muBin'+str(genbin), 'fracSM4muBin'+str(genbin), fidxs['4mu']/fidxs['4l'])
            fracSM4muBin[str(genbin)].setConstant(True)
            K1Bin[str(genbin)] = RooRealVar('K1Bin'+str(genbin), 'K1Bin'+str(genbin), 1.0, 0.0,  1.0/fracSM4eBin[str(genbin)].getVal())
            K2Bin[str(genbin)] = RooRealVar('K2Bin'+str(genbin), 'K2Bin'+str(genbin), 1.0, 0.0, (1.0-fracSM4eBin[str(genbin)].getVal())/fracSM4eBin[str(genbin)].getVal())
            SigmaBin[str(genbin)] = RooRealVar('SigmaBin'+str(genbin), 'SigmaBin'+str(genbin), fidxs['4l'], 0.0, 10.0)
            SigmaHBin['4e'+str(genbin)] = RooFormulaVar("Sigma4eBin"+str(genbin),"(@0*@1*@2)", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)]))
            SigmaHBin['4mu'+str(genbin)] = RooFormulaVar("Sigma4muBin"+str(genbin),"(@0*(1.0-@1*@2)*@3*@4/(1.0-@1))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))
            SigmaHBin['2e2mu'+str(genbin)] = RooFormulaVar("Sigma2e2muBin"+str(genbin),"(@0*(1.0-@1*@2)*(1.0-@3*@4/(1.0-@1)))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))
            if (("jets" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi))
        elif (physicalModel=="v1"):
            fracBin['4mu'+str(genbin)] = RooRealVar("frac4muBin"+str(genbin),"frac4muBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4mu
            fracBin['4e'+str(genbin)] = RooRealVar("frac4eBin"+str(genbin),"frac4eBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4e
            fracBin['2e2mu'+str(genbin)] = RooFormulaVar("frac2e2muBin"+str(genbin),"1-@0-@1", RooArgList(fracBin['4e'+str(genbin)],fracBin['4mu'+str(genbin)])) # frac 2e2mu
            fracBin['4mu'+str(genbin)].setConstant(True)            
            fracBin['4e'+str(genbin)].setConstant(True)
            rBin[str(genbin)] = RooRealVar("rBin"+str(genbin),"rBin"+str(genbin), 1.0, 0.0, 10.0)
            rBin[str(genbin)].setConstant(True)
            #trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1*@2", RooArgList(rBin[str(genbin)], fracBin[channel+str(genbin)], trueH_norm[genbin]) );
            if (("jets" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*@3*(1-@4)" ,RooArgList(rBin[str(genbin)],fracBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*@3" ,RooArgList(rBin[str(genbin)],fracBin[channel+str(genbin)],fideff_var[genbin],lumi))
        else:
            rBin_channel[str(genbin)] = RooRealVar("r"+channel+"Bin"+str(genbin),"r"+channel+"Bin"+str(genbin), 1.0, 0.0, 10.0)                
            rBin_channel[str(genbin)].setConstant(True)
            #trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1", RooArgList(rBin_channel[str(genbin)], trueH_norm[genbin]) );
            if (("jets" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi))
                                                                                                                                                            
    outin = outinratio[modelName+"_"+channel+"_"+obsName+"_genbin0_"+recobin]
    outin_var = RooRealVar("outfracBin_"+recobin+"_"+channel,"outfracBin_"+recobin+"_"+channel, outin);
    outin_var.setConstant(True)
    out_trueH_norm_args = RooArgList(outin_var)
    out_trueH_norm_func = "@0*(" 
    for i in range(nBins-1): 
        out_trueH_norm_args.add(trueH_norm_final[i]) 
        out_trueH_norm_func = out_trueH_norm_func+"@"+str(i+1)+"+" 
    out_trueH_norm_func = out_trueH_norm_func.replace(str(nBins-1)+"+",str(nBins-1)+")") 
    out_trueH_norm = RooFormulaVar("out_trueH_norm",out_trueH_norm_func,out_trueH_norm_args) 
                                                                                              
    # Backgrounds
    #ggZZ = w.pdf("bkg_ggzz")
    #qqZZ = w.pdf("bkg_qqzz")
    #zjets = w.pdf("bkg_zjetsB")
    
    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = {'qqzz':{'2e2mu':'ZZTo2e2mu_powheg', '4e':'ZZTo4e_powheg', '4mu':'ZZTo4mu_powheg'},'ggzz':{'2e2mu':'ggZZ_2e2mu_MCFM67', '4e':'ggZZ_4e_MCFM67', '4mu':'ggZZ_4mu_MCFM67'},'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}

    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsName+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+channel,"frac_qqzz_"+recobin+"_"+channel, frac_qqzz);

    frac_ggzz = fractionsBackground[bkg_sample_tags['ggzz'][channel]+'_'+channel+'_'+obsName+'_'+recobin]
    frac_ggzz_var = RooRealVar("frac_ggzz_"+recobin+"_"+channel,"frac_ggzz_"+recobin+"_"+channel, frac_ggzz);

    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsName+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+channel,"frac_zjet_"+recobin+"_"+channel, frac_zjets);

    if (obsName.startswith("njets")):
        #######
        lambda_JES_qqzz = 0.0 #lambda_qqzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_qqzz_var = RooRealVar("lambda_qqzz_"+recobin+"_"+channel,"lambda_"+recobin+"_"+channel, lambda_JES_qqzz)           
        JES_qqzz_rfv = RooFormulaVar("JES_rfv_qqzz_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_qqzz_var) )

        ####
        lambda_JES_ggzz = 0.0 #lambda_ggzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_ggzz_var = RooRealVar("lambda_ggzz_"+recobin+"_"+channel,"lambda_"+recobin+"_"+channel, lambda_JES_ggzz)
        JES_ggzz_rfv = RooFormulaVar("JES_rfv_ggzz_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_ggzz_var) )

        ####
        lambda_JES_zjets = 0.0 #lambda_zjets_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_zjets_var = RooRealVar("lambda_zjets_"+recobin+"_"+channel,"lambda_zjets_"+recobin+"_"+channel, lambda_JES_zjets)
        JES_zjets_rfv = RooFormulaVar("JES_rfv_zjets_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_zjets_var) )


    ## background shapes in each reco bin
#    ggzzTemplatePdf = w.pdf("bkg_ggzz")
#    qqzzTemplatePdf = w.pdf("bkg_qqzz")
#    zjetsTemplatePdf = ggzzTemplatePdf.Clone();
#    zjetsTemplatePdf.SetName("bkg_zjets");

    #template path : ./templates/templatesXS/DTreeXS_{obsName}/8TeV/
    #template name : XSBackground_{bkgTag}_{finalStateString}_{obsName}_recobin{binNum}.root

    template_qqzzName = "./templates/templatesXS/DTreeXS_"+obsName+"/8TeV/XSBackground_qqZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_ggzzName = "./templates/templatesXS/DTreeXS_"+obsName+"/8TeV/XSBackground_ggZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = "./templates/templatesXS/DTreeXS_"+obsName+"/8TeV/XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    ggzzTempFile = TFile(template_ggzzName,"READ")
    ggzzTemplate = ggzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    zjetsTempFile = TFile(template_zjetsName,"READ")
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    qqzzTemplateName = "qqzz_"+channel+recobin
    ggzzTemplateName = "ggzz_"+channel+recobin
    zjetsTemplateName = "zjets_"+channel+recobin

    qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplate)
    ggzzTempDataHist = RooDataHist(ggzzTemplateName,ggzzTemplateName,RooArgList(m),ggzzTemplate)
    zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplate)

    qqzzTemplatePdf = RooHistPdf("qqzz","qqzz",RooArgSet(m),qqzzTempDataHist)
    ggzzTemplatePdf = RooHistPdf("ggzz","ggzz",RooArgSet(m),ggzzTempDataHist)
    zjetsTemplatePdf = RooHistPdf("zjets","zjets",RooArgSet(m),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions

    if( not (obsName=='nJets' or obsName.startswith("njets") ) or (not doJES)) :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0*(1-@1)", RooArgList(frac_ggzz_var, JES_ggzz_rfv) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )
     

    #legacy_data = w.data("data_obs").reduce(RooArgSet(m))
    #for event in range(legacy_data.numEntries()):
    #     row = legacy_data.get(event)
    #     row.Print("v") 
    #legacy_data.Print("v")

    data_obs_file = TFile('data_8TeV.root')
    data_obs_tree = data_obs_file.Get('passedEvents')
    print obsName,obsBin_low,obsBin_high
    if (obsName == "nJets"): obsName = "njets_reco_pt30_eta4p7"
    if (channel=='4mu'):
        if (obsName=="mass4l"): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu),"(mass4mu>105.0 && mass4mu<140.0)")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>105.0 && mass4mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
    if (channel=='4e'):
        if (obsName=="mass4l"): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e),"(mass4e>105.0 && mass4e<140.0)")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>105.0 && mass4e<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
    if (channel=='2e2mu'):
        if (obsName=="mass4l"): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu),"(mass2e2mu>105.0 && mass2e2mu<140.0)")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>105.0 && mass2e2mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")") 
    #for event in range(data_obs.numEntries()):
    #    row = data_obs.get(event)
    #    row.Print("v")
    data_obs.Print("v")
    
    wout = RooWorkspace("w","w")
    
    for genbin in range(nBins-1):
        getattr(wout,'import')(trueH_shape[genbin],RooFit.RecycleConflictNodes(),RooFit.Silence())
        getattr(wout,'import')(trueH_norm[genbin],RooFit.RecycleConflictNodes(),RooFit.Silence())

    if (not usecfactor):
        out_trueH.SetName("out_trueH")  
        getattr(wout,'import')(out_trueH,RooFit.RecycleConflictNodes(),RooFit.Silence()) 
        getattr(wout,'import')(out_trueH_norm,RooFit.RecycleConflictNodes(),RooFit.Silence()) 
    

    getattr(wout,'import')(fakeH,RooFit.Silence()) 
    getattr(wout,'import')(fakeH_norm,RooFit.Silence())
    
    #print "trueH norm: ",n_trueH,"fakeH norm:",n_fakeH
    qqzzTemplatePdf.SetName("bkg_qqzz")
    getattr(wout,'import')(qqzzTemplatePdf,RooFit.Silence())
    getattr(wout,'import')(qqzz_norm,RooFit.Silence())

    ggzzTemplatePdf.SetName("bkg_ggzz")
    getattr(wout,'import')(ggzzTemplatePdf,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(ggzz_norm,RooFit.Silence())

    zjetsTemplatePdf.SetName("bkg_zjets")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes(), RooFit.Silence())
    getattr(wout,'import')(zjets_norm)

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m)),RooFit.Silence())

    if (addfakeH):
        if (usecfactor):
            fout = TFile("xs_125.0/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.root","RECREATE")
        else:
            fout = TFile("xs_125.0/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".root","RECREATE")
    else:
        if (usecfactor):
            fout = TFile("xs_125.0/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.NoFakeH.root","RECREATE")
        else:
            fout = TFile("xs_125.0/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".NoFakeH.root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(wout) 
    fout.Close()

    return data_obs.numEntries()

#createXSworkspace("pT4l", "2e2mu", 4, 0, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 1, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 2, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 3, False, True)
#createXSworkspace("mass4l", "2e2mu", 1, 0, ["105.0","140.0"], False, True, "SM_125", "v2")
