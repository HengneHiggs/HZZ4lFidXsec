# this script is called once for each reco bin (obsBin)
# in each reco bin there are (nBins) signals (one for each gen bin)

from ROOT import *


def createXSworkspaceZ4lInclusive(obsName, channel, modelName):

    obs_low = 50.0
    obs_high = 110.0
    obsBin_low = "50"
    obsBin_high = "110"
    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    #from inputs_sig import eff, outinratio
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['eff','outinratio'], -1)
    eff = _temp.eff
    outinratio = _temp.outinratio

    #from inputs_bkg_{obsName} import fractionsBackground
    _temp = __import__('inputs_bkg_z4l_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # Load the legacy workspace
    f_in = TFile("91.1876/hzz4l_"+channel+"S_8TeV.input.root","READ")
    w = f_in.Get("w")
    #w.Print()

    # 4 lepton mass observable to perform the fit
    m = w.var("CMS_zz4l_mass")
    mass4e = RooRealVar("mass4e", "mass4e", obs_low, obs_high)
    mass4mu = RooRealVar("mass4mu", "mass4mu", obs_low, obs_high)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",obs_low, obs_high)
    observable = RooRealVar(obsName,obsName, obs_low, obs_high)
    observable.Print()
    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)

    # true signal shape
    trueZ = w.pdf("ggH")
    trueZ.SetName("trueZ");

    # Out of acceptance events
    # (same shape as in acceptance shape)
    out_trueZ = trueZ.Clone()
    out_trueZ.SetName("out_trueZ");

    # signal shape in different recobin
    trueZ_shape = trueZ.Clone()
    trueZ_shape.SetName("trueZ"+channel)
    fideff = eff[modelName+"_"+channel+"_"+obsName+"_genbin0_recobin0"]
    fideff_var = RooRealVar("eff_"+channel,"eff_"+channel, fideff)
    trueZ_norm = RooFormulaVar("trueZ"+channel+"_norm","@0*@1", RooArgList(fideff_var, lumi) );

    # pre-set fidxs
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    fracBin = {}

    fidxs_4e = 1000.0*z4l_xsbr['SMZ4l_4e']*acc['SMZ4l_4e_'+obsName+'_genbin0_recobin0']
    fidxs_4mu = 1000.0*z4l_xsbr['SMZ4l_4mu']*acc['SMZ4l_4mu_'+obsName+'_genbin0_recobin0']
    fidxs_2e2mu = 1000.0*z4l_xsbr['SMZ4l_2e2mu']*acc['SMZ4l_2e2mu_'+obsName+'_genbin0_recobin0']
    fidxs_4l = fidxs_4e+fidxs_4mu+fidxs_2e2mu
    fidxs_frac_4mu = fidxs_4mu/fidxs_4l;
    fidxs_frac_4e = fidxs_4e/fidxs_4l;
    fracBin["4mu"] = RooRealVar("Z4lfrac4mu", "Z4lfrac4mu", fidxs_frac_4mu, 0.0, 0.5) # frac 4mu
    fracBin["4e"] = RooRealVar("Z4lfrac4e","Z4lfrac4e", fidxs_frac_4e, 0.0, 0.5) # frac 4e
    fracBin["2e2mu"] = RooFormulaVar("Z4lfrac2e2mu","1-@0-@1", RooArgList(fracBin["4e"],fracBin["4mu"])) # frac 2e2mu
    fracBin["4mu"].setConstant(True)
    fracBin["4e"].setConstant(True)
    Z4lr = RooRealVar("Z4lr","Z4lr", fidxs_4l, 0.0, 10.0)
    Z4lr.setConstant(True)
    trueZ_norm_final = RooFormulaVar("trueZ"+channel+"_final_norm","@0*@1*@2", RooArgList(Z4lr, fracBin[channel], trueZ_norm) );

    outin = outinratio[modelName+"_"+channel+"_"+obsName+"_genbin0_recobin0"]
    outin_var = RooRealVar("Z4loutfrac_"+channel,"Z4loutfracBin_"+channel, outin);
    outin_var.setConstant(True)
    out_trueZ_norm = RooFormulaVar("Z4lout_trueZ_norm","@0*@1",RooArgList(outin_var,trueZ_norm_final))

    # Backgrounds

    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = {'qqzz':{'2e2mu':'ZZTo2e2mu_powheg_tchan', '4e':'ZZTo4e_powheg_tchan', '4mu':'ZZTo4mu_powheg_tchan'}, 'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}

    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsName+'_recobin0']
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+channel,"frac_qqzz_"+channel, frac_qqzz);

    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsName+'_recobin0']
    frac_zjets_var = RooRealVar("frac_zjet_"+channel,"frac_zjet_"+channel, frac_zjets);

    ## background shapes in each reco bin

    #template path : ./templates/templatesXSZ4l/DTreeXS_{obsName}/8TeV/
    #template name : XSBackground_{bkgTag}_{finalStateString}_{obsName}_recobin{binNum}.root

    template_qqzzName = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/XSBackground_qqZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    zjetsTempFile = TFile(template_zjetsName,"READ")
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    qqzzTemplateName = "qqzz_"+channel
    zjetsTemplateName = "zjets_"+channel

    qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplate)
    zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplate)

    qqzzTemplatePdf = RooHistPdf("qqzz","qqzz",RooArgSet(m),qqzzTempDataHist)
    zjetsTemplatePdf = RooHistPdf("zjets","zjets",RooArgSet(m),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions
    qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
    zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )

    data_obs_file = TFile('data_8TeV.root')
    data_obs_tree = data_obs_file.Get('passedEvents')
    all_vars = RooArgSet(m,mass4mu,mass4e,mass2e2mu,observable)
    print obsName,obs_low,obs_high

    if (channel=='4mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>50.0 && mass4mu<110.0 && "+obsName+">="+str(obs_low)+" && "+obsName+"<"+str(obs_high)+")")
    if (channel=='4e'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>50.0 && mass4e<110.0 && "+obsName+">="+str(obs_low)+" && "+obsName+"<"+str(obs_high)+")")
    if (channel=='2e2mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>50.0 && mass2e2mu<110.0 && "+obsName+">="+str(obs_low)+" && "+obsName+"<"+str(obs_high)+")")
    #for event in range(data_obs.numEntries()):
    #    row = data_obs.get(event)
    #    row.Print("v")
    data_obs.Print("v")

    wout = RooWorkspace("w","w")

    getattr(wout,'import')(trueZ_shape,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(trueZ_norm,RooFit.RecycleConflictNodes())

    out_trueZ.SetName("out_trueZ")
    getattr(wout,'import')(out_trueZ,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(out_trueZ_norm,RooFit.RecycleConflictNodes())


    #print "trueZ norm: ",n_trueZ
    qqzzTemplatePdf.SetName("bkg_qqzz")
    getattr(wout,'import')(qqzzTemplatePdf)
    getattr(wout,'import')(qqzz_norm)

    zjetsTemplatePdf.SetName("bkg_zjets")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes())
    getattr(wout,'import')(zjets_norm)

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m)))

    fout = TFile("xs_91.1876/hzz4l_"+channel+"S_8TeV_xs_"+modelName+".input.root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(wout)
    fout.Close()

    return data_obs.numEntries()



def createXSworkspaceZ4l(obsName, channel, nBins, obsBin, observableBins, usecfactor, modelName, physicalModel):

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
        _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['cfactor','inc_wrongfrac','binfrac_wrongfrac','inc_outfrac','binfrac_outfrac','lambdajesup','lambdajesdn'], -1)
        cfactor = _temp.cfactor
        inc_outfrac = _temp.inc_outfrac
        binfrac_outfrac = _temp.binfrac_wrongfrac
    else:
        _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['eff','inc_wrongfrac','binfrac_wrongfrac','outinratio','lambdajesup','lambdajesdn'], -1)
        eff = _temp.eff
        outinratio = _temp.outinratio        

    lambdajesup = _temp.lambdajesup
    lambdajesdn = _temp.lambdajesdn        
    inc_wrongfrac = _temp.inc_wrongfrac
    binfrac_wrongfrac = _temp.binfrac_wrongfrac

    #from inputs_bkg_{obsName} import fractionsBackground
    _temp = __import__('inputs_bkg_z4l_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # Load the legacy workspace
    f_in = TFile("91.1876/hzz4l_"+channel+"S_8TeV.input.root","READ")
    w = f_in.Get("w")
    #w.Print()

    # 4 lepton mass observable to perform the fit
    m = w.var("CMS_zz4l_mass")
    mass4e = RooRealVar("mass4e", "mass4e", 50.0, 110.0)
    mass4mu = RooRealVar("mass4mu", "mass4mu", 50.0, 110.0)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",50.0, 110.0)
    if ("jets" in obsName or "Jets" in obsName):
        observable = RooRealVar("njets_reco_pt30_eta4p7","njets_reco_pt30_eta4p7",int(obs_bin_lowest),int(obs_bin_highest))
    elif (obsName=="rapidity4l"):
       observable = RooRealVar("absrapidity4l", "absrapidity4l", float(obs_bin_lowest),float(obs_bin_highest))
    elif (obsName=="cosThetaStar"):
       observable = RooRealVar("abscosThetaStar", "abscosThetaStar", float(obs_bin_lowest),float(obs_bin_highest))
    else:
        observable = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))
    observable.Print()
    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)
    
    # true signal shape
    trueZ = w.pdf("ggH")
    trueZ.SetName("trueZ");
    
    # Out of acceptance events
    # (same shape as in acceptance shape)
    out_trueZ = trueZ.Clone()
    out_trueZ.SetName("out_trueZ");
    
    # signal shape in different recobin
    trueZ_shape = {}
    fideff = {}
    fideff_var = {}
    trueZ_norm = {}

    # nuisance describes the jet energy scale uncertainty
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)
    if (obsName.startswith("njets")):
        lambda_JES_sig = lambdajesup[modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin, "lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin0"+"_"+recobin, lambda_JES_sig)    
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )

    for genbin in range(nBins-1):
        trueZ_shape[genbin] = trueZ.Clone();
        trueZ_shape[genbin].SetName("trueZ"+channel+"Bin"+str(genbin))
        if (usecfactor): fideff[genbin] = cfactor[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        else: fideff[genbin] = eff[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        fideff_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+channel,"effBin"+str(genbin)+"_"+recobin+"_"+channel, fideff[genbin]);

        if( not (obsName=='nJets' or obsName.startswith("njets")) or (not doJES)) :
            trueZ_norm[genbin] = RooFormulaVar("trueZ"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
        else :
            trueZ_norm[genbin] = RooFormulaVar("trueZ"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) ); 
 

    # pre-set fidxs
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    trueZ_norm_final = {}
    fracBin = {}
    rBin = {}
    rBin_channel = {}
    for genbin in range(nBins-1):
        if (physicalModel=="v1"):
            fidxs_4e = 1000.0*z4l_xsbr['SMZ4l_4e']*acc['SMZ4l_4e_'+obsName+'_genbin'+str(genbin)+'_recobin0']
            fidxs_4mu = 1000.0*z4l_xsbr['SMZ4l_4mu']*acc['SMZ4l_4mu_'+obsName+'_genbin'+str(genbin)+'_recobin0']
            fidxs_2e2mu = 1000.0*z4l_xsbr['SMZ4l_2e2mu']*acc['SMZ4l_2e2mu_'+obsName+'_genbin'+str(genbin)+'_recobin0']
            fidxs_4l = fidxs_4e+fidxs_4mu+fidxs_2e2mu
            fidxs_frac_4mu = fidxs_4mu/fidxs_4l;
            fidxs_frac_4e = fidxs_4e/fidxs_4l;
            #fracBin['4mu'+str(genbin)] = RooRealVar("Z4lfrac4muBin"+str(genbin),"Z4lfrac4muBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4mu
            #fracBin['4e'+str(genbin)] = RooRealVar("Z4lfrac4eBin"+str(genbin),"Z4lfrac4eBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4e
            fracBin['4mu'+str(genbin)] = RooRealVar("Z4lfrac4muBin"+str(genbin),"Z4lfrac4muBin"+str(genbin), fidxs_frac_4mu, 0.0, 0.5) # frac 4mu
            fracBin['4e'+str(genbin)] = RooRealVar("Z4lfrac4eBin"+str(genbin),"Z4lfrac4eBin"+str(genbin), fidxs_frac_4e, 0.0, 0.5) # frac 4e
            fracBin['2e2mu'+str(genbin)] = RooFormulaVar("Z4lfrac2e2muBin"+str(genbin),"1-@0-@1", RooArgList(fracBin['4e'+str(genbin)],fracBin['4mu'+str(genbin)])) # frac 2e2mu
            fracBin['4mu'+str(genbin)].setConstant(True)            
            fracBin['4e'+str(genbin)].setConstant(True)
            #rBin[str(genbin)] = RooRealVar("Z4lrBin"+str(genbin),"Z4lrBin"+str(genbin), 1.0, 0.0, 10.0)
            rBin[str(genbin)] = RooRealVar("Z4lrBin"+str(genbin),"Z4lrBin"+str(genbin), fidxs_4l, 0.0, 10.0)
            rBin[str(genbin)].setConstant(True)
            trueZ_norm_final[genbin] = RooFormulaVar("trueZ"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1*@2", RooArgList(rBin[str(genbin)], fracBin[channel+str(genbin)], trueZ_norm[genbin]) );
        else:
            rBin_channel[str(genbin)] = RooRealVar("Z4lr"+channel+"Bin"+str(genbin),"Z4lr"+channel+"Bin"+str(genbin), 1.0, 0.0, 10.0)                
            rBin_channel[str(genbin)].setConstant(True)
            trueZ_norm_final[genbin] = RooFormulaVar("trueZ"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1", RooArgList(rBin_channel[str(genbin)], trueZ_norm[genbin]) );
            
    outin = outinratio[modelName+"_"+channel+"_"+obsName+"_genbin0_"+recobin]
    outin_var = RooRealVar("Z4loutfracBin_"+recobin+"_"+channel,"Z4loutfracBin_"+recobin+"_"+channel, outin);
    outin_var.setConstant(True)
    out_trueZ_norm_args = RooArgList(outin_var)
    out_trueZ_norm_func = "@0*(" 
    for i in range(nBins-1): 
        out_trueZ_norm_args.add(trueZ_norm_final[i]) 
        out_trueZ_norm_func = out_trueZ_norm_func+"@"+str(i+1)+"+" 
    out_trueZ_norm_func = out_trueZ_norm_func.replace(str(nBins-1)+"+",str(nBins-1)+")") 
    out_trueZ_norm = RooFormulaVar("Z4lout_trueZ_norm",out_trueZ_norm_func,out_trueZ_norm_args) 
                                                                                              
    # Backgrounds
    
    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = {'qqzz':{'2e2mu':'ZZTo2e2mu_powheg_tchan', '4e':'ZZTo4e_powheg_tchan', '4mu':'ZZTo4mu_powheg_tchan'}, 'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}

    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsName+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+channel,"frac_qqzz_"+recobin+"_"+channel, frac_qqzz);

    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsName+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+channel,"frac_zjet_"+recobin+"_"+channel, frac_zjets);

    if (obsName=='nJets' or obsName.startswith("njets")):
        #######
        lambda_JES_qqzz = 0.0 #lambda_qqzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_qqzz_var = RooRealVar("lambda_qqzz_"+recobin+"_"+channel,"lambda_"+recobin+"_"+channel, lambda_JES_qqzz)           
        JES_qqzz_rfv = RooFormulaVar("JES_rfv_qqzz_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_qqzz_var) )

        ####
        lambda_JES_zjets = 0.0 #lambda_zjets_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_zjets_var = RooRealVar("lambda_zjets_"+recobin+"_"+channel,"lambda_zjets_"+recobin+"_"+channel, lambda_JES_zjets)
        JES_zjets_rfv = RooFormulaVar("JES_rfv_zjets_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_zjets_var) )


    ## background shapes in each reco bin

    #template path : ./templates/templatesXSZ4l/DTreeXS_{obsName}/8TeV/
    #template name : XSBackground_{bkgTag}_{finalStateString}_{obsName}_recobin{binNum}.root

    template_qqzzName = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/XSBackground_qqZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    zjetsTempFile = TFile(template_zjetsName,"READ")
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)

    qqzzTemplateName = "qqzz_"+channel+recobin
    zjetsTemplateName = "zjets_"+channel+recobin

    qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplate)
    zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplate)

    qqzzTemplatePdf = RooHistPdf("qqzz","qqzz",RooArgSet(m),qqzzTempDataHist)
    zjetsTemplatePdf = RooHistPdf("zjets","zjets",RooArgSet(m),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions
    if( not (obsName=='nJets' or obsName.startswith("njets") ) or (not doJES)) :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )
     

    data_obs_file = TFile('data_8TeV.root')
    data_obs_tree = data_obs_file.Get('passedEvents')
    all_vars = RooArgSet(m,mass4mu,mass4e,mass2e2mu,observable)
    print obsName,obsBin_low,obsBin_high
    if (obsName == "nJets"): obsName = "njets_reco_pt30_eta4p7"

    tempObsName = obsName
    if (obsName=="rapidity4l"): 
        tempObsName = "absrapidity4l"
    elif (obsName=="cosThetaStar"):
        tempObsName = "abscosThetaStar"

    if (channel=='4mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>50.0 && mass4mu<110.0 && "+tempObsName+">="+obsBin_low+" && "+tempObsName+"<"+obsBin_high+")")
    if (channel=='4e'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>50.0 && mass4e<110.0 && "+tempObsName+">="+obsBin_low+" && "+tempObsName+"<"+obsBin_high+")")
    if (channel=='2e2mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>50.0 && mass2e2mu<110.0 && "+tempObsName+">="+obsBin_low+" && "+tempObsName+"<"+obsBin_high+")")
    #for event in range(data_obs.numEntries()):
    #    row = data_obs.get(event)
    #    row.Print("v")
    data_obs.Print("v")
    
    wout = RooWorkspace("w","w")
    
    for genbin in range(nBins-1):
        getattr(wout,'import')(trueZ_shape[genbin],RooFit.RecycleConflictNodes())
        getattr(wout,'import')(trueZ_norm[genbin],RooFit.RecycleConflictNodes())

    if (not usecfactor):
        out_trueZ.SetName("out_trueZ")  
        getattr(wout,'import')(out_trueZ,RooFit.RecycleConflictNodes()) 
        getattr(wout,'import')(out_trueZ_norm,RooFit.RecycleConflictNodes()) 
    

    #print "trueZ norm: ",n_trueZ
    qqzzTemplatePdf.SetName("bkg_qqzz")
    getattr(wout,'import')(qqzzTemplatePdf)
    getattr(wout,'import')(qqzz_norm)

    zjetsTemplatePdf.SetName("bkg_zjets")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes())
    getattr(wout,'import')(zjets_norm)

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m)))

    if (usecfactor):
        fout = TFile("xs_91.1876/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.root","RECREATE")
    else:
        fout = TFile("xs_91.1876/hzz4l_"+channel+"S_8TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(wout) 
    fout.Close()

    return data_obs.numEntries()


