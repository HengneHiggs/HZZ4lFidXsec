#!/usr/bin/python

from ROOT import *


def createXSworkspaceZ4lInclusive(obsName, chan, modelName, physicalModel):

    #######################
    # general items
    #######################   

    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    # channel map
    channels = {'4mu':1,'4e':2,'2e2mu':3}
    channel = channels[chan]

    # mass window
    m4l_lo = 50.0
    m4l_hi = 105.0

    # obs bin for tags
    obsBin_low = '50'
    obsBin_high = '105'
    
    # 8TeV
    sqrts = int(8)

    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)

    # x-axis variable
    CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",m4l_lo, m4l_hi)
    CMS_zz4l_mass.setBins(3000)

    # MH, to describe for MZ
    name = "MH"
    MH = RooRealVar(name,"MH", 91.1876, 70.0, 150.0)

    # import ws parameters
    _temp = __import__('inputs_ratio', globals(), locals(), ['inputs'], -1)
    inputs = _temp.inputs 
    #print inputs

    # import z4l fid acc eff outinratio
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
    acc_z = _temp.acc
    eff_z = _temp.eff
    outinratio_z = _temp.outinratio

    # import z4l xsbr
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    # import background fractions
    _temp = __import__('inputs_bkg_z4l_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # load background templates
    template_location = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/"
    template_qqzzName = template_location+"XSBackground_qqZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_ggzzName = template_location+"XSBackground_ggZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = template_location+"XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    ggzzTempFile = TFile(template_ggzzName,"READ")
    zjetsTempFile = TFile(template_zjetsName,"READ")


    ###############
    # RooRealVar
    ###############

    name = "CMS_zz4l_Z_mean_m_sig"
    CMS_zz4l_Z_mean_m_sig = RooRealVar(name,name,0.0,-10.0,10.0)
    CMS_zz4l_Z_mean_m_sig.setVal(0)
    CMS_zz4l_Z_mean_m_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_mean_e_sig"
    CMS_zz4l_Z_mean_e_sig = RooRealVar(name,name,0.0,-10.0,10.0)
    CMS_zz4l_Z_mean_e_sig.setVal(0)
    CMS_zz4l_Z_mean_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_sigma_m_sig"
    CMS_zz4l_Z_sigma_m_sig = RooRealVar(name, name,3.0,0.0,30.0)
    CMS_zz4l_Z_sigma_m_sig.setVal(0)
    CMS_zz4l_Z_sigma_m_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_sigma_e_sig"
    CMS_zz4l_Z_sigma_e_sig = RooRealVar(name, name,3.0,0.0,30.0)
    CMS_zz4l_Z_sigma_e_sig.setVal(0)
    CMS_zz4l_Z_sigma_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_n_sig_{0}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_Z_n_sig = RooRealVar(name,name,2.,-10.,10.)
    CMS_zz4l_Z_n_sig.setVal(0)
    CMS_zz4l_Z_n_sig.setConstant(kTRUE)

    name = "ZDecayWidth"
    ZDecayWidth = RooRealVar(name,name,2.4952)
    ZDecayWidth.setConstant(kTRUE)

    #################
    # RooFormulaVar
    #################

    name = "CMS_zz4l_Z_n_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    rfv_Z_n_CB = RooFormulaVar(name,"("+inputs['Z_n_CB_shape_'+chan]+")"+"*(1+@1)",RooArgList(MH,CMS_zz4l_Z_n_sig))

    name = "CMS_zz4l_Z_alpha_{0:.0f}_centralValue".format(channel)
    rfv_Z_alpha_CB = RooFormulaVar(name,inputs['Z_alpha_CB_shape_'+chan], RooArgList(MH))

    name = "CMS_zz4l_Z_sigma_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_Z_sigma_m_sig))
    elif (chan=="4e"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_Z_sigma_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*TMath::Sqrt((1+@1)*(1+@2))", RooArgList(MH, CMS_zz4l_Z_sigma_m_sig,CMS_zz4l_Z_sigma_e_sig))

    name = "CMS_zz4l_Z_mean_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MH, CMS_zz4l_Z_mean_m_sig))
    elif (chan=="4e"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MH, CMS_zz4l_Z_mean_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+ (@0*@1 + @0*@2)/2", RooArgList(MH, CMS_zz4l_Z_mean_m_sig,CMS_zz4l_Z_mean_e_sig))


    ################
    # trueZ
    ################

    name = "signalCB_trueZ"
    signalCB_trueZ = RooCBShape(name, name, CMS_zz4l_mass, rfv_Z_mean_CB, rfv_Z_sigma_CB,rfv_Z_alpha_CB,rfv_Z_n_CB)

    name = "signalBW_trueZ"
    signalBW_trueZ = RooBreitWigner(name,name, CMS_zz4l_mass,MH,ZDecayWidth)

    name = "trueZ"+chan
    trueZ = RooFFTConvPdf(name,"BW (X) CB",CMS_zz4l_mass,signalBW_trueZ,signalCB_trueZ,2)


    #################
    # trueZ_norm
    #################

    fideff_z = eff_z["SMZ4l_"+chan+"_"+obsName+"_genbin0_recobin0"]
    fideff_z_var = RooRealVar("eff_z_"+chan,"eff_z_"+chan, fideff_z);
    trueZ_norm = RooFormulaVar("trueZ"+chan+"_norm","@0*@1", RooArgList(fideff_z_var, lumi) );

    #################
    # trueZ_norm_final
    #################

    fidxs_z = {}
    for fState in ['4e','4mu', '2e2mu']:
        fidxs_z[fState] = 1000.0*z4l_xsbr['SMZ4l_'+fState]*acc_z['SMZ4l_'+fState+'_'+obsName+'_genbin0_recobin0']

    fidxs_z['4l'] = fidxs_z['4e']+fidxs_z['4mu']+fidxs_z['2e2mu']

    if (physicalModel=='v3'):
        fracSM4e = RooRealVar('fracSM4e', 'fracSM4e', fidxs_z['4e']/fidxs_z['4l']) 
        fracSM4e.setConstant(True)
        fracSM4mu = RooRealVar('fracSM4mu', 'fracSM4mu', fidxs_z['4mu']/fidxs_z['4l']) 
        fracSM4mu.setConstant(True)
        K1 = RooRealVar('K1', 'K1', 1.0, 0.0,  1.0/fracSM4e.getVal())
        K2 = RooRealVar('K2', 'K2', 1.0, 0.0, (1.0-fracSM4e.getVal())/fracSM4mu.getVal())
        Sigma = RooRealVar('Sigma', 'Sigma', fidxs_z['4l'], 0.0, 10.0)
        if (chan=='4e'): 
            SigmaZ = RooFormulaVar("Sigma4e","(@0*@1*@2)", RooArgList(Sigma, fracSM4e, K1)) 
        elif (chan=='4mu'): 
            SigmaZ = RooFormulaVar("Sigma4mu","(@0*(1.0-@1*@2)*@3*@4/(1.0-@1))", RooArgList(Sigma, fracSM4e, K1, K2, fracSM4mu))
        elif (chan=='2e2mu'): 
            SigmaZ = RooFormulaVar("Sigma2e2mu","(@0*(1.0-@1*@2)*(1.0-@3*@4/(1.0-@1)))", RooArgList(Sigma, fracSM4e, K1, K2, fracSM4mu))
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ, trueZ_norm)) 
    elif (physicalModel=='v1'):
        if (chan=='2e2mu'):
            SigmaZ = RooRealVar('SigmaZ', 'SigmaZ', fidxs_z['4l'], 0.0, 10.0)
            SigmaZ4e = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
            SigmaZ4mu = RooRealVar('SigmaZ4mu', 'SigmaZ4mu', fidxs_z['4mu'], 0.0, 10.0)
            SigmaZ2e2mu = RooFormulaVar("SigmaZ2e2mu","(@0-@1-@2)", RooArgList(SigmaZ, SigmaZ4e, SigmaZ4mu))
            trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ2e2mu, trueZ_norm))
        else:
            name = "SigmaZ"+chan
            SigmaZ = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
            trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ, trueZ_norm))
    elif (physicalModel=='v2'):
        name = "Sigma"+chan
        SigmaZ = RooRealVar('Sigma4e', 'Sigma4e', fidxs_z['4e'], 0.0, 10.0)
        trueZ_norm_final = RooFormulaVar("true"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ, trueZ_norm))
   

    #################
    #  out_trueZ
    #################
    out_trueZ = trueZ.Clone()
    out_trueZ.SetName("out_trueZ");
    out_trueZ.SetTitle("out_trueZ");

    outin_z = outinratio_z["SMZ4l_"+chan+"_"+obsName+"_genbin0_recobin0"]
    outin_z_var = RooRealVar("outinratio_z_"+chan,"outinratio_z_"+chan, outin_z);
    outin_z_var.setConstant(True)
    out_trueZ_norm = RooFormulaVar("out_trueZ_norm","@0*@1",RooArgList(outin_z_var,trueZ_norm_final))


    #######################
    # backgrounds
    #######################

    # fractions
    frac_qqzz = fractionsBackground['ZZTo'+chan+'_powheg_tchan_'+chan+'_'+obsName+'_recobin0']
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+chan,"frac_qqzz_"+chan, frac_qqzz);

    frac_ggzz = fractionsBackground['ggZZ_'+chan+'_'+chan+'_'+obsName+'_recobin0']
    frac_ggzz_var = RooRealVar("frac_ggzz_"+chan,"frac_ggzz_"+chan, frac_ggzz);

    frac_zjets = fractionsBackground['ZX4l_CR_AllChans_'+obsName+'_recobin0']
    frac_zjets_var = RooRealVar("frac_zjet_"+chan,"frac_zjet_"+chan, frac_zjets);

    # templates
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    ggzzTemplate = ggzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)


    # make pdfs

    # qqzz
    qqzzTempDataHist = RooDataHist("qqzz_"+chan, "qqzz_"+chan,RooArgList(CMS_zz4l_mass),qqzzTemplate)
    bkg_qqzz = RooHistPdf("bkg_qqzz","bkg_qqzz",RooArgSet(CMS_zz4l_mass),qqzzTempDataHist)
    bkg_qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )

    # ggzz
    ggzzTempDataHist = RooDataHist("ggzz_"+chan,"ggzz_"+chan,RooArgList(CMS_zz4l_mass),ggzzTemplate)
    bkg_ggzz = RooHistPdf("bkg_ggzz","bkg_ggzz",RooArgSet(CMS_zz4l_mass),ggzzTempDataHist)
    bkg_ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )

    # zjets
    zjetsTempDataHist = RooDataHist("zjets_"+chan, "zjets_"+chan, RooArgList(CMS_zz4l_mass),zjetsTemplate)
    bkg_zjets = RooHistPdf("bkg_zjets","bkg_zjets",RooArgSet(CMS_zz4l_mass),zjetsTempDataHist)
    bkg_zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )




    #######################
    # data
    #######################

    data_obs_file = TFile('data_8TeV_new.root')
    data_obs_tree = data_obs_file.Get('passedEvents')

    mass4e = RooRealVar("mass4e", "mass4e", m4l_lo, m4l_hi)
    mass4mu = RooRealVar("mass4mu", "mass4mu", m4l_lo, m4l_hi)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",m4l_lo, m4l_hi)

    if (chan=='4mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass4mu),"(mass4mu>"+str(m4l_lo)+"&&mass4mu<"+str(m4l_hi)+")")
    elif (chan=='4e'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass4e),"(mass4e>"+str(m4l_lo)+"&&mass4e<"+str(m4l_hi)+")")
    elif (chan=='2e2mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass2e2mu),"(mass2e2mu>"+str(m4l_lo)+"&&mass2e2mu<"+str(m4l_hi)+")")


    #######################
    #   Import to ws
    #######################

    # output workspace
    w = RooWorkspace("w","w")

    # trueZ
    getattr(w,'import')(trueZ,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueZ_norm,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueZ_norm_final,RooFit.RecycleConflictNodes())

    # out_trueZ
    getattr(w,'import')(out_trueZ,RooFit.RecycleConflictNodes())
    getattr(w,'import')(out_trueZ_norm,RooFit.RecycleConflictNodes())
    
    # bkg_qqzz
    getattr(w,'import')(bkg_qqzz,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_qqzz_norm,RooFit.RecycleConflictNodes())

    # bkg_ggzz
    getattr(w,'import')(bkg_ggzz,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_ggzz_norm,RooFit.RecycleConflictNodes())

    # bkg_zjets
    getattr(w,'import')(bkg_zjets,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_zjets_norm,RooFit.RecycleConflictNodes())

    ## data
    getattr(w,'import')(data_obs.reduce(RooArgSet(CMS_zz4l_mass)))

    # output file
    fout = TFile("xs_z4l/hzz4l_"+chan+"S_8TeV_xs_Z4l_"+modelName+"_"+physicalModel+".input.root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(w)
    fout.Close()

    return data_obs.numEntries()



def createXSworkspaceZ4lDifferential(obsName, chan, nBins, obsBin, observableBins, modelName, physicalModel):

    #######################
    # general items
    #######################   

    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    # channel map
    channels = {'4mu':1,'4e':2,'2e2mu':3}
    channel = channels[chan]

    # mass window
    m4l_lo = 50.0
    m4l_hi = 105.0

    # obs bin for tags
    obsBin_low = observableBins[obsBin]
    obsBin_high = observableBins[obsBin+1]

    obs_bin_lowest = observableBins[0]
    obs_bin_highest = observableBins[len(observableBins)-1]

    recobin = "recobin"+str(obsBin)

    #observable
    observable = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))

    # 8TeV
    sqrts = int(8)

    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)

    # x-axis variable
    CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",10.0, 1000.0)
    CMS_zz4l_mass.setBins(3000)

    # MH, to describe for MZ
    name = "MH"
    MH = RooRealVar(name,"MH", 91.1876, 70.0, 150.0)

    # import ws parameters
    _temp = __import__('inputs_ratio', globals(), locals(), ['inputs'], -1)
    inputs = _temp.inputs 
    #print inputs

    # import z4l fid acc eff outinratio
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
    acc_z = _temp.acc
    eff_z = _temp.eff
    outinratio_z = _temp.outinratio
    if (obsName.startswith("njets")):
        _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['lambdajesup','lambdajesdn'], -1)
        lambdajesup = _temp.lambdajesup
        lambdajesdn = _temp.lambdajesdn

    # import z4l xsbr
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    # import background fractions
    _temp = __import__('inputs_bkg_z4l_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # load background templates
    template_location = "./templates/templatesXSZ4l/DTreeXS_"+obsName+"/8TeV/"
    template_qqzzName = template_location+"XSBackground_qqZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_ggzzName = template_location+"XSBackground_ggZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = template_location+"XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    ggzzTempFile = TFile(template_ggzzName,"READ")
    zjetsTempFile = TFile(template_zjetsName,"READ")

    ###############
    # RooRealVar
    ###############

    name = "CMS_zz4l_Z_mean_m_sig"
    CMS_zz4l_Z_mean_m_sig = RooRealVar(name,name,0.0,-10.0,10.0)
    CMS_zz4l_Z_mean_m_sig.setVal(0)
    CMS_zz4l_Z_mean_m_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_mean_e_sig"
    CMS_zz4l_Z_mean_e_sig = RooRealVar(name,name,0.0,-10.0,10.0)
    CMS_zz4l_Z_mean_e_sig.setVal(0)
    CMS_zz4l_Z_mean_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_sigma_m_sig"
    CMS_zz4l_Z_sigma_m_sig = RooRealVar(name, name,3.0,0.0,30.0)
    CMS_zz4l_Z_sigma_m_sig.setVal(0)
    CMS_zz4l_Z_sigma_m_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_sigma_e_sig"
    CMS_zz4l_Z_sigma_e_sig = RooRealVar(name, name,3.0,0.0,30.0)
    CMS_zz4l_Z_sigma_e_sig.setVal(0)
    CMS_zz4l_Z_sigma_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_Z_n_sig_{0}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_Z_n_sig = RooRealVar(name,name,2.,-10.,10.)
    CMS_zz4l_Z_n_sig.setVal(0)
    CMS_zz4l_Z_n_sig.setConstant(kTRUE)

    name = "ZDecayWidth"
    ZDecayWidth = RooRealVar(name,name,2.4952)
    ZDecayWidth.setConstant(kTRUE)

    #################
    # RooFormulaVar
    #################

    name = "CMS_zz4l_Z_n_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    rfv_Z_n_CB = RooFormulaVar(name,"("+inputs['Z_n_CB_shape_'+chan]+")"+"*(1+@1)",RooArgList(MH,CMS_zz4l_Z_n_sig))

    name = "CMS_zz4l_Z_alpha_{0:.0f}_centralValue".format(channel)
    rfv_Z_alpha_CB = RooFormulaVar(name,inputs['Z_alpha_CB_shape_'+chan], RooArgList(MH))

    name = "CMS_zz4l_Z_sigma_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_Z_sigma_m_sig))
    elif (chan=="4e"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_Z_sigma_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*TMath::Sqrt((1+@1)*(1+@2))", RooArgList(MH, CMS_zz4l_Z_sigma_m_sig,CMS_zz4l_Z_sigma_e_sig))

    name = "CMS_zz4l_Z_mean_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MH, CMS_zz4l_Z_mean_m_sig))
    elif (chan=="4e"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MH, CMS_zz4l_Z_mean_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+ (@0*@1 + @0*@2)/2", RooArgList(MH, CMS_zz4l_Z_mean_m_sig,CMS_zz4l_Z_mean_e_sig))


    ################
    # trueZ
    ################

    name = "signalCB_trueZ"
    signalCB_trueZ = RooCBShape(name, name, CMS_zz4l_mass, rfv_Z_mean_CB, rfv_Z_sigma_CB,rfv_Z_alpha_CB,rfv_Z_n_CB)

    name = "signalBW_trueZ"
    signalBW_trueZ = RooBreitWigner(name,name, CMS_zz4l_mass,MH,ZDecayWidth)

    name = "trueZ"+chan
    trueZ = RooFFTConvPdf(name,"BW (X) CB",CMS_zz4l_mass,signalBW_trueZ,signalCB_trueZ,2)

    # nuisance describes the jet energy scale uncertainty
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)
    if (obsName.startswith("njets")):
        lambda_JES_sig = lambdajesup[modelName+"_"+chan+"_"+obsName+"_genbin0"+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+chan+"_"+obsName+"_genbin0"+"_"+recobin, "lambda_sig_"+modelName+"_"+chan+"_"+obsName+"_genbin0"+"_"+recobin, lambda_JES_sig)
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+chan,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )


    # signal shape in different recobin
    trueZ_shape = {}
    fideff_z = {}
    fideff_z_var = {}
    trueZ_norm = {}

    for genbin in range(nBins-1):
        trueZ_shape[genbin] = trueZ.Clone();
        trueZ_shape[genbin].SetName("trueZ"+chan+"Bin"+str(genbin))
        fideff_z[genbin] = eff_z[modelName+"_"+chan+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        fideff_z_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+chan,"effBin"+str(genbin)+"_"+recobin+"_"+chan, fideff_z[genbin]);

        if( not (obsName.startswith("njets"))) :
            trueZ_norm[genbin] = RooFormulaVar("trueZ"+chan+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_z_var[genbin], lumi) );
        else :
            trueZ_norm[genbin] = RooFormulaVar("trueZ"+chan+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_z_var[genbin], lumi, JES_sig_rfv) );


    #################
    # trueZ_norm_final
    #################
    trueZ_norm_final = {}
    fracSM4eBin = {}
    fracSM4muBin = {}
    K1Bin = {}
    K2Bin = {}
    SigmaBin = {}
    SigmaZBin = {}
    rBin_channel = {}

    for genbin in range(nBins-1):
        fidxs_z = {}
        for fState in ['4e','4mu', '2e2mu']:
            fidxs_z[fState] = 1000.0*z4l_xsbr['SMZ4l_'+fState]*acc_z['SMZ4l_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin0']  
        fidxs_z['4l'] = fidxs_z['4e']+fidxs_z['4mu']+fidxs_z['2e2mu']
        if (physicalModel=="v3"):
            frac4e = 0.0
            frac4mu = 0.0
            if (fidxs_z['4l']>0.0): 
                frac4e = fidxs_z['4e']/fidxs_z['4l']
                frac4mu = fidxs_z['4mu']/fidxs_z['4l']
            fracSM4eBin[str(genbin)] = RooRealVar('fracSM4eBin'+str(genbin), 'fracSM4eBin'+str(genbin), frac4e)
            fracSM4eBin[str(genbin)].setConstant(True)
            fracSM4muBin[str(genbin)] = RooRealVar('fracSM4muBin'+str(genbin), 'fracSM4muBin'+str(genbin), frac4mu)
            fracSM4muBin[str(genbin)].setConstant(True)
            K1Bin[str(genbin)] = RooRealVar('K1Bin'+str(genbin), 'K1Bin'+str(genbin), 1.0, 0.0,  1.0/fracSM4eBin[str(genbin)].getVal())
            K2Bin[str(genbin)] = RooRealVar('K2Bin'+str(genbin), 'K2Bin'+str(genbin), 1.0, 0.0, (1.0-fracSM4eBin[str(genbin)].getVal())/fracSM4eBin[str(genbin)].getVal())
            SigmaBin[str(genbin)] = RooRealVar('SigmaBin'+str(genbin), 'SigmaBin'+str(genbin), fidxs_z['4l'], 0.0, 10.0)
            SigmaZBin['4e'+str(genbin)] = RooFormulaVar("Sigma4eBin"+str(genbin),"(@0*@1*@2)", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)]))
            SigmaZBin['4mu'+str(genbin)] = RooFormulaVar("Sigma4muBin"+str(genbin),"(@0*(1.0-@1*@2)*@3*@4/(1.0-@1))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))
            SigmaZBin['2e2mu'+str(genbin)] = RooFormulaVar("Sigma2e2muBin"+str(genbin),"(@0*(1.0-@1*@2)*(1.0-@3*@4/(1.0-@1)))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))
            if (("jets" in obsName)):
                trueZ_norm_final[genbin] = RooFormulaVar("trueZ"+chan+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)" ,RooArgList(SigmaZBin[chan+str(genbin)],fideff_z_var[genbin],lumi,JES_sig_rfv))
            else:
                trueZ_norm_final[genbin] = RooFormulaVar("trueZ"+chan+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2" ,RooArgList(SigmaZBin[chan+str(genbin)],fideff_z_var[genbin],lumi))
        elif (physicalModel=="v2"):
            rBin_channel[str(genbin)] = RooRealVar("r"+chan+"Bin"+str(genbin),"r"+chan+"Bin"+str(genbin), fidxs_z[chan], 0.0, 10.0)
            rBin_channel[str(genbin)].setConstant(True)
            if (("jets" in obsName)):
                trueZ_norm_final[genbin] = RooFormulaVar("trueH"+chan+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)", RooArgList(rBin_channel[str(genbin)], fideff_z_var[genbin],lumi,JES_sig_rfv))
            else:
                trueZ_norm_final[genbin] = RooFormulaVar("trueH"+chan+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2", RooArgList(rBin_channel[str(genbin)], fideff_z_var[genbin],lumi))



    #################
    #  out_trueZ
    #################
    out_trueZ = trueZ.Clone()
    out_trueZ.SetName("out_trueZ");
    out_trueZ.SetTitle("out_trueZ");

    outin_z = outinratio_z[modelName+"_"+chan+"_"+obsName+"_genbin0_"+recobin]
    outin_z_var = RooRealVar("outinratio_z_Bin_"+recobin+"_"+chan,"outinratio_z_Bin_"+recobin+"_"+chan, outin_z);
    outin_z_var.setConstant(True)
    out_trueZ_norm_args = RooArgList(outin_z_var)
    out_trueZ_norm_func = "@0*("
    for i in range(nBins-1):
        out_trueZ_norm_args.add(trueZ_norm_final[i])
        out_trueZ_norm_func = out_trueZ_norm_func+"@"+str(i+1)+"+"
    out_trueZ_norm_func = out_trueZ_norm_func.replace(str(nBins-1)+"+",str(nBins-1)+")")
    out_trueZ_norm = RooFormulaVar("out_trueZ_norm",out_trueZ_norm_func,out_trueZ_norm_args)


    #######################
    # backgrounds
    #######################

    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = {'qqzz':{'2e2mu':'ZZTo2e2mu_powheg_tchan', '4e':'ZZTo4e_powheg_tchan', '4mu':'ZZTo4mu_powheg_tchan'},'ggzz':{'2e2mu':'ggZZ_2e2mu', '4e':'ggZZ_4e', '4mu':'ggZZ_4mu'},'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}

    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][chan]+'_'+chan+'_'+obsName+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+chan,"frac_qqzz_"+recobin+"_"+chan, frac_qqzz);

    frac_ggzz = fractionsBackground[bkg_sample_tags['ggzz'][chan]+'_'+chan+'_'+obsName+'_'+recobin]
    frac_ggzz_var = RooRealVar("frac_ggzz_"+recobin+"_"+chan,"frac_ggzz_"+recobin+"_"+chan, frac_ggzz);

    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][chan]+"_AllChans_"+obsName+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+chan,"frac_zjet_"+recobin+"_"+chan, frac_zjets);

    if (obsName.startswith("njets")):
        #######
        lambda_JES_qqzz = 0.0 #lambda_qqzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_qqzz_var = RooRealVar("lambda_qqzz_"+recobin+"_"+chan,"lambda_"+recobin+"_"+chan, lambda_JES_qqzz)
        JES_qqzz_rfv = RooFormulaVar("JES_rfv_qqzz_"+recobin+"_"+chan,"@0*@1", RooArgList(JES, lambda_JES_qqzz_var) )

        ####
        lambda_JES_ggzz = 0.0 #lambda_ggzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_ggzz_var = RooRealVar("lambda_ggzz_"+recobin+"_"+chan,"lambda_"+recobin+"_"+chan, lambda_JES_ggzz)
        JES_ggzz_rfv = RooFormulaVar("JES_rfv_ggzz_"+recobin+"_"+chan,"@0*@1", RooArgList(JES, lambda_JES_ggzz_var) )

        ####
        lambda_JES_zjets = 0.0 #lambda_zjets_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_zjets_var = RooRealVar("lambda_zjets_"+recobin+"_"+chan,"lambda_zjets_"+recobin+"_"+chan, lambda_JES_zjets)
        JES_zjets_rfv = RooFormulaVar("JES_rfv_zjets_"+recobin+"_"+chan,"@0*@1", RooArgList(JES, lambda_JES_zjets_var) )




    # templates
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    ggzzTemplate = ggzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)


    # make pdfs

    # qqzz
    qqzzTemplateName = "qqzz_"+chan+recobin
    qqzzTempDataHist = RooDataHist(qqzzTemplateName, qqzzTemplateName, RooArgList(CMS_zz4l_mass),qqzzTemplate)
    bkg_qqzz = RooHistPdf("bkg_qqzz","bkg_qqzz",RooArgSet(CMS_zz4l_mass),qqzzTempDataHist)

    # ggzz
    ggzzTemplateName = "ggzz_"+chan+recobin
    ggzzTempDataHist = RooDataHist(ggzzTemplateName, ggzzTemplateName, RooArgList(CMS_zz4l_mass),ggzzTemplate)
    bkg_ggzz = RooHistPdf("bkg_ggzz","bkg_ggzz",RooArgSet(CMS_zz4l_mass),ggzzTempDataHist)

    # zjets
    zjetsTemplateName = "zjets_"+chan+recobin
    zjetsTempDataHist = RooDataHist(zjetsTemplateName, zjetsTemplateName, RooArgList(CMS_zz4l_mass),zjetsTemplate)
    bkg_zjets = RooHistPdf("bkg_zjets","bkg_zjets",RooArgSet(CMS_zz4l_mass),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions
    if ( not (obsName=='nJets' or obsName.startswith("njets") )) :
        bkg_qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
        bkg_ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )
        bkg_zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else:
        bkg_qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
        bkg_ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0*(1-@1)", RooArgList(frac_ggzz_var, JES_ggzz_rfv) )
        bkg_zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )


    #######################
    # data
    #######################

    data_obs_file = TFile('data_8TeV_new.root')
    data_obs_tree = data_obs_file.Get('passedEvents')

    mass4e = RooRealVar("mass4e", "mass4e", m4l_lo, m4l_hi)
    mass4mu = RooRealVar("mass4mu", "mass4mu", m4l_lo, m4l_hi)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",m4l_lo, m4l_hi)

    if (chan=='4mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass4mu,observable),"(mass4mu>"+str(m4l_lo)+"&&mass4mu<"+str(m4l_hi)+"&&"+obsName+">="+obsBin_low+"&&"+obsName+"<"+obsBin_high+")")
    elif (chan=='4e'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass4e,observable),"(mass4e>"+str(m4l_lo)+"&&mass4e<"+str(m4l_hi)+"&&"+obsName+">="+obsBin_low+"&&"+obsName+"<"+obsBin_high+")")
    elif (chan=='2e2mu'):
        data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(CMS_zz4l_mass,mass2e2mu,observable),"(mass2e2mu>"+str(m4l_lo)+"&&mass2e2mu<"+str(m4l_hi)+"&&"+obsName+">="+obsBin_low+"&&"+obsName+"<"+obsBin_high+")")


    #######################
    #   Import to ws
    #######################

    # output workspace
    w = RooWorkspace("w","w")
    # trueZ
    for genbin in range(nBins-1):
        getattr(w,'import')(trueZ_shape[genbin],RooFit.RecycleConflictNodes())
        getattr(w,'import')(trueZ_norm[genbin],RooFit.RecycleConflictNodes())

    # out_trueZ
    getattr(w,'import')(out_trueZ,RooFit.RecycleConflictNodes())
    getattr(w,'import')(out_trueZ_norm,RooFit.RecycleConflictNodes())
    
    # bkg_qqzz
    getattr(w,'import')(bkg_qqzz,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_qqzz_norm,RooFit.RecycleConflictNodes())

    # bkg_ggzz
    getattr(w,'import')(bkg_ggzz,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_ggzz_norm,RooFit.RecycleConflictNodes())

    # bkg_zjets
    getattr(w,'import')(bkg_zjets,RooFit.RecycleConflictNodes())
    getattr(w,'import')(bkg_zjets_norm,RooFit.RecycleConflictNodes())

    ## data
    getattr(w,'import')(data_obs.reduce(RooArgSet(CMS_zz4l_mass)))

    # output file
    fout = TFile("xs_z4l/hzz4l_"+chan+"S_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".input.root","RECREATE")
    print "write ws to fout"
    fout.WriteTObject(w)
    fout.Close()

    return data_obs.numEntries()






