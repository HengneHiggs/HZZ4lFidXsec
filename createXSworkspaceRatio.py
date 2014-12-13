#!/usr/bin/python

from ROOT import *


def createXSworkspaceRatioInclusive(obsName, chan, modelName, physicalModel):

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
    m4l_hi = 140.0

    # obs bin for tags
    obsBin_low = '50'
    obsBin_high = '140'
    
    # 8TeV
    sqrts = int(8)

    # luminosity
    lumi = RooRealVar("lumi_8","lumi_8", 19.712)

    # x-axis variable
    CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",m4l_lo, m4l_hi)
    CMS_zz4l_mass.setBins(3000)

    # MH
    name = "MH"
    MH = RooRealVar(name,"MH", 125.0, 100.0, 150.0)

    # DeltaMHmZ
    name = "DeltaMHmZ"
    DeltaMHmZ = RooRealVar(name, "DeltaMHmZ", 33.8124, 0.0, 100.0)

    # MZ
    name = "MZ"
    MZ = RooFormulaVar(name, "(@0-@1)",RooArgList(MH,DeltaMHmZ))   

    # import ws parameters
    _temp = __import__('inputs_ratio', globals(), locals(), ['inputs'], -1)
    inputs = _temp.inputs 
    #print inputs

    # import h4l fid acc eff outinratio wrong frac etc
    _temp = __import__('inputs_sig_ratio_h4l_'+obsName, globals(), locals(), ['acc', 'eff','inc_wrongfrac','binfrac_wrongfrac','outinratio'], -1)
    acc = _temp.acc
    eff = _temp.eff
    outinratio = _temp.outinratio
    inc_wrongfrac = _temp.inc_wrongfrac
    binfrac_wrongfrac = _temp.binfrac_wrongfrac

    # import z4l fid acc eff outinratio
    _temp = __import__('inputs_sig_ratio_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
    acc_z = _temp.acc
    eff_z = _temp.eff
    outinratio_z = _temp.outinratio

    # import h4l xs br
    _temp = __import__('higgs_xsbr', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
    higgs_xs = _temp.higgs_xs
    higgs4l_br = _temp.higgs4l_br

    # import z4l xsbr
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    # import background fractions
    _temp = __import__('inputs_bkg_ratio_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # Load the legacy workspace
    f_in = TFile("125/hzz4l_"+chan+"S_8TeV.input.root","READ")
    w_in = f_in.Get("w")

    # load background templates
    template_location = "./templates/templatesXSRatio/DTreeXS_"+obsName+"/8TeV/"
    template_qqzzName = template_location+"XSBackground_qqZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_ggzzName = template_location+"XSBackground_ggZZ_"+chan+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_zjetsName = template_location+"XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    ggzzTempFile = TFile(template_ggzzName,"READ")
    zjetsTempFile = TFile(template_zjetsName,"READ")



    #######################
    # everything about H
    #######################

    ###############
    # RooRealVar
    ###############
 
    name = "CMS_zz4l_mean_m_sig"
    CMS_zz4l_mean_m_sig = RooRealVar(name,"CMS_zz4l_mean_m_sig",0.0,-10.0,10.0)
    CMS_zz4l_mean_m_sig.setVal(0)
    CMS_zz4l_mean_m_sig.setConstant(kTRUE)

    name = "CMS_zz4l_mean_m_err_{0}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_mean_m_err = RooRealVar(name,"CMS_zz4l_mean_m_err",float(inputs['CMS_zz4l_mean_m_sig_'+chan]),-0.99,0.99)
    CMS_zz4l_mean_m_err.setConstant(kTRUE)

    name = "CMS_zz4l_mean_e_sig"
    CMS_zz4l_mean_e_sig = RooRealVar(name,"CMS_zz4l_mean_e_sig",0.0,-10.0,10.0)
    CMS_zz4l_mean_e_sig.setVal(0)
    CMS_zz4l_mean_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_mean_e_err_{0}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_mean_e_err = RooRealVar(name,"CMS_zz4l_mean_e_err",float(inputs['CMS_zz4l_mean_e_sig_'+chan]),-0.99,0.99)
    CMS_zz4l_mean_e_err.setConstant(kTRUE)

    name = "CMS_zz4l_sigma_m_sig"
    CMS_zz4l_sigma_m_sig = RooRealVar(name,"CMS_zz4l_sigma_m_sig",3.0,0.0,30.0)
    CMS_zz4l_sigma_m_sig.setVal(0)
    CMS_zz4l_sigma_m_sig.setConstant(kTRUE)
    
    name = "CMS_zz4l_sigma_e_sig"
    CMS_zz4l_sigma_e_sig = RooRealVar(name,"CMS_zz4l_sigma_e_sig",3.0,0.0,30.0)
    CMS_zz4l_sigma_e_sig.setVal(0)
    CMS_zz4l_sigma_e_sig.setConstant(kTRUE)

    name = "CMS_zz4l_n_sig_{0}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_n_sig = RooRealVar(name,"CMS_zz4l_n_sig",2.,-10.,10.)
    CMS_zz4l_n_sig.setVal(0)
    CMS_zz4l_n_sig.setConstant(kTRUE)


    #################
    # RooFormulaVar
    #################

    name = "CMS_zz4l_n_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    rfv_n_CB = RooFormulaVar(name,"("+inputs['n_CB_shape_'+chan]+")"+"*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig))

    name = "CMS_zz4l_alpha_{0:.0f}_centralValue".format(channel)
    rfv_alpha_CB = RooFormulaVar(name,inputs['alpha_CB_shape_'+chan], RooArgList(MH))

    name = "CMS_zz4l_n2_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    rfv_n2_CB = RooFormulaVar(name,"("+inputs['n2_CB_shape_'+chan]+")",RooArgList(MH))

    name = "CMS_zz4l_alpha2_{0:.0f}_centralValue".format(channel)
    rfv_alpha2_CB = RooFormulaVar(name,inputs['alpha2_CB_shape_'+chan], RooArgList(MH))

    name = "CMS_zz4l_mean_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_mean_CB = RooFormulaVar(name,"("+inputs['mean_CB_shape_'+chan]+")"+"+@0*@1*@2", RooArgList(MH, CMS_zz4l_mean_m_sig,CMS_zz4l_mean_m_err))
    elif (chan=="4e"):
        rfv_mean_CB = RooFormulaVar(name,"("+inputs['mean_CB_shape_'+chan]+")"+"+@0*@1*@2", RooArgList(MH, CMS_zz4l_mean_e_sig,CMS_zz4l_mean_e_err))
    elif (chan=="2e2mu"):
        rfv_mean_CB = RooFormulaVar(name,"("+inputs['mean_CB_shape_'+chan]+")"+"+ (@0*@1*@3 + @0*@2*@4)/2", RooArgList(MH, CMS_zz4l_mean_m_sig,CMS_zz4l_mean_e_sig,CMS_zz4l_mean_m_err,CMS_zz4l_mean_e_err))

    name = "CMS_zz4l_sigma_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_sigma_CB = RooFormulaVar(name,"("+inputs['sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_sigma_m_sig))
    elif (chan=="4e"):
        rfv_sigma_CB = RooFormulaVar(name,"("+inputs['sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MH, CMS_zz4l_sigma_e_sig))
    elif (chan=="2e2mu"):
        rfv_sigma_CB = RooFormulaVar(name,"("+inputs['sigma_CB_shape_'+chan]+")"+"*TMath::Sqrt((1+@1)*(1+@2))", RooArgList(MH, CMS_zz4l_sigma_m_sig,CMS_zz4l_sigma_e_sig))


    name = "CMS_zz4l_mean_sig_NoConv_{0:.0f}_{1:.0f}".format(channel,sqrts)
    CMS_zz4l_mean_sig_NoConv = RooFormulaVar(name,"@0+@1", RooArgList(rfv_mean_CB, MH))

    ################
    # trueH
    ################

    name = "trueH"+chan
    trueH = RooDoubleCB(name,name,CMS_zz4l_mass, CMS_zz4l_mean_sig_NoConv ,rfv_sigma_CB,rfv_alpha_CB,rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)


    #################
    # trueH_norm
    #################

    fideff = eff[modelName+"_"+chan+"_"+obsName+"_genbin0_recobin0"]
    fideff_var = RooRealVar("eff_"+chan,"eff_"+chan, fideff);
    trueH_norm = RooFormulaVar("trueH"+chan+"_norm","@0*@1", RooArgList(fideff_var, lumi) ); 

    #################
    # trueH_norm_final
    #################

    fidxs = {}
    for fState in ['4e','4mu', '2e2mu']:
        fidxs[fState] = 0
        fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs[fState] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs[fState] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs[fState] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs[fState] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #fidxs[fState] += higgs_xs['ggH_125.6']*higgs4l_br['125.6_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #fidxs[fState] += higgs_xs['VBF_125.6']*higgs4l_br['125.6_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #fidxs[fState] += higgs_xs['WH_125.6']*higgs4l_br['125.6_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #fidxs[fState] += higgs_xs['ZH_125.6']*higgs4l_br['125.6_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #fidxs[fState] += higgs_xs['ttH_125.6']*higgs4l_br['125.6_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']

    if (physicalModel=='v1' and chan=='2e2mu'):
        fidxs['4l'] = fidxs['4e']+fidxs['4mu']+fidxs['2e2mu']
        SigmaH = RooRealVar("SigmaH","SigmaH", fidxs['4l'], 0.0, 10.0)
        SigmaH4e = RooRealVar("SigmaH4e","SigmaH4e", fidxs['4e'], 0.0, 10.0)
        SigmaH4mu = RooRealVar("SigmaH4mu","SigmaH4mu", fidxs['4mu'], 0.0, 10.0)
        SigmaH2e2mu = RooFormulaVar("SigmaH2e2mu", "(@0-@1-@2)", RooArgList(SigmaH,SigmaH4e,SigmaH4mu))
        trueH_norm_final = RooFormulaVar("trueH"+chan+"_final_norm","@0*@1", RooArgList(SigmaH2e2mu, trueH_norm))
    else:
        SigmaH = RooRealVar("SigmaH"+chan,"SigmaH"+chan, fidxs[chan], 0.0, 10.0)
        trueH_norm_final = RooFormulaVar("trueH"+chan+"_final_norm","@0*@1", RooArgList(SigmaH, trueH_norm))
           


    #################
    #  out_trueH
    #################
    out_trueH = trueH.Clone()
    out_trueH.SetName("out_trueH");
    out_trueH.SetTitle("out_trueH");
 
    outin = outinratio[modelName+"_"+chan+"_"+obsName+"_genbin0_recobin0"]
    outin_var = RooRealVar("outinratio_"+chan,"outinratio_"+chan, outin);
    outin_var.setConstant(True)
    out_trueH_norm = RooFormulaVar("out_trueH_norm","@0*@1",RooArgList(outin_var,trueH_norm_final))

    #################
    #  fakeH
    #################    

    # fake fraction
    if (chan=='4mu'):
        p1_1_8 = RooRealVar("CMS_fakeH_p1_1_8","p1_1_8",165.0, 145.0, 185.0)
        p3_1_8 = RooRealVar("CMS_fakeH_p3_1_8","p3_1_8",89.0, 84.0,94.0)
        p2_1_8 = RooFormulaVar("CMS_fakeH_p2_1_8","p2_1_8","0.72*@0-@1",RooArgList(p1_1_8,p3_1_8))
        fakeH = RooLandau("fakeH", "landau", CMS_zz4l_mass, p1_1_8, p2_1_8)
    elif (chan=='4e'):
        p1_2_8 = RooRealVar("CMS_fakeH_p1_2_8","p1_2_8",165.0, 145.0, 185.0)
        p3_2_8 = RooRealVar("CMS_fakeH_p3_2_8","p3_2_8",89.0, 84.0,94.0)
        p2_2_8 = RooFormulaVar("CMS_fakeH_p2_2_8","p2_2_8","0.72*@0-@1",RooArgList(p1_2_8,p3_2_8))
        fakeH = RooLandau("fakeH", "landau", CMS_zz4l_mass, p1_2_8, p2_2_8)
    elif (chan=='2e2mu'):
        p1_3_8 = RooRealVar("CMS_fakeH_p1_3_8","p1_3_8",165.0, 145.0, 185.0)
        p3_3_8 = RooRealVar("CMS_fakeH_p3_3_8","p3_3_8",89.0, 84.0,94.0)
        p2_3_8 = RooFormulaVar("CMS_fakeH_p2_3_8","p2_3_8","0.72*@0-@1",RooArgList(p1_3_8,p3_3_8))
        fakeH = RooLandau("fakeH", "landau", CMS_zz4l_mass, p1_3_8, p2_3_8)

    inc_wrongfrac_ggH=inc_wrongfrac["ggH_powheg15_JHUgen_125_"+chan+"_"+obsName+"_genbin0_recobin0"]
    inc_wrongfrac_qqH=inc_wrongfrac["VBF_powheg_125_"+chan+"_"+obsName+"_genbin0_recobin0"]
    inc_wrongfrac_WH=inc_wrongfrac["WH_pythia_125_"+chan+"_"+obsName+"_genbin0_recobin0"]
    inc_wrongfrac_ZH=inc_wrongfrac["ZH_pythia_125_"+chan+"_"+obsName+"_genbin0_recobin0"]
    inc_wrongfrac_ttH=inc_wrongfrac["ttH_pythia_125_"+chan+"_"+obsName+"_genbin0_recobin0"]

    # SM values of signal expectations (inclusive, reco level)
    ggH_norm = w_in.function("ggH_norm")
    qqH_norm = w_in.function("qqH_norm")
    WH_norm = w_in.function("WH_norm")
    ZH_norm = w_in.function("ZH_norm")
    ttH_norm = w_in.function("ttH_norm")

    # 
    wrongfrac_ggH = RooRealVar("wrongfrac_ggH"+chan, "wrongfrac_ggH"+chan, inc_wrongfrac_ggH)
    wrongfrac_qqH = RooRealVar("wrongfrac_qqH"+chan, "wrongfrac_qqH"+chan, inc_wrongfrac_qqH)
    wrongfrac_WH = RooRealVar("wrongfrac_WH"+chan, "wrongfrac_WH"+chan, inc_wrongfrac_WH)
    wrongfrac_ZH = RooRealVar("wrongfrac_ZH"+chan, "wrongfrac_ZH"+chan, inc_wrongfrac_ZH)
    wrongfrac_ttH = RooRealVar("wrongfrac_ttH"+chan, "wrongfrac_ttH"+chan, inc_wrongfrac_ttH)

    fakeH_norm_ggH = RooFormulaVar("fakeH_norm_ggH"+chan,"(@0*@1)", RooArgList(wrongfrac_ggH, ggH_norm))
    fakeH_norm_qqH = RooFormulaVar("fakeH_norm_qqH"+chan,"(@0*@1)", RooArgList(wrongfrac_qqH, qqH_norm))
    fakeH_norm_WH = RooFormulaVar("fakeH_norm_WH"+chan,"(@0*@1)", RooArgList(wrongfrac_WH, WH_norm))
    fakeH_norm_ZH = RooFormulaVar("fakeH_norm_ZH"+chan,"(@0*@1)", RooArgList(wrongfrac_ZH, ZH_norm))
    fakeH_norm_ttH = RooFormulaVar("fakeH_norm_ttH"+chan,"(@0*@1)", RooArgList(wrongfrac_ttH, ttH_norm))

    fakeH_norm = RooFormulaVar("fakeH_norm","(@0+@1+@2+@3+@4)",RooArgList(fakeH_norm_ggH, fakeH_norm_qqH, fakeH_norm_WH, fakeH_norm_ZH, fakeH_norm_ttH))

    #
    #n_fakeH = inc_wrongfrac_ggH*ggH_norm.getVal()+inc_wrongfrac_qqH*qqH_norm.getVal()+inc_wrongfrac_WH*WH_norm.getVal()+inc_wrongfrac_ZH*ZH_norm.getVal()+inc_wrongfrac_ttH*ttH_norm.getVal()
    #n_fakeH_var = RooRealVar("n_fakeH_var_"+chan,"n_fakeH_var_"+chan,n_fakeH);
    #fakeH_norm = RooFormulaVar("fakeH_norm","@0",RooArgList(n_fakeH_var)) 

    #######################
    # everything about Z
    #######################

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
    rfv_Z_n_CB = RooFormulaVar(name,"("+inputs['Z_n_CB_shape_'+chan]+")"+"*(1+@1)",RooArgList(MZ,CMS_zz4l_Z_n_sig))

    name = "CMS_zz4l_Z_alpha_{0:.0f}_centralValue".format(channel)
    rfv_Z_alpha_CB = RooFormulaVar(name,inputs['Z_alpha_CB_shape_'+chan], RooArgList(MZ))

    name = "CMS_zz4l_Z_sigma_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MZ, CMS_zz4l_Z_sigma_m_sig))
    elif (chan=="4e"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*(1+@1)", RooArgList(MZ, CMS_zz4l_Z_sigma_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_sigma_CB = RooFormulaVar(name,"("+inputs['Z_sigma_CB_shape_'+chan]+")"+"*TMath::Sqrt((1+@1)*(1+@2))", RooArgList(MZ, CMS_zz4l_Z_sigma_m_sig,CMS_zz4l_Z_sigma_e_sig))

    name = "CMS_zz4l_Z_mean_sig_{0:.0f}_{1:.0f}_centralValue".format(channel,sqrts)
    if (chan=="4mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MZ, CMS_zz4l_Z_mean_m_sig))
    elif (chan=="4e"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+@0*@1", RooArgList(MZ, CMS_zz4l_Z_mean_e_sig))
    elif (chan=="2e2mu"):
        rfv_Z_mean_CB = RooFormulaVar(name,"("+inputs['Z_mean_CB_shape_'+chan]+")"+"+ (@0*@1 + @0*@2)/2", RooArgList(MZ, CMS_zz4l_Z_mean_m_sig,CMS_zz4l_Z_mean_e_sig))


    ################
    # trueZ
    ################

    name = "signalCB_trueZ"
    signalCB_trueZ = RooCBShape(name, name, CMS_zz4l_mass, rfv_Z_mean_CB, rfv_Z_sigma_CB,rfv_Z_alpha_CB,rfv_Z_n_CB)

    name = "signalBW_trueZ"
    signalBW_trueZ = RooBreitWigner(name,name, CMS_zz4l_mass,MZ,ZDecayWidth)

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


    if (physicalModel=='v1' and chan=='2e2mu'):
        fidxs_z['4l'] = fidxs_z['4e']+fidxs_z['4mu']+fidxs_z['2e2mu']
        RatioSigmaHoZ = RooRealVar('RatioSigmaHoZ', 'RatioSigmaHoZ', fidxs['4l']/fidxs_z['4l'], 0.0, 10.0)
        RatioSigmaHoZ4e = RooRealVar('RatioSigmaHoZ4e', 'RatioSigmaHoZ4e', fidxs['4e']/fidxs_z['4e'], 0.0, 10.0)
        RatioSigmaHoZ4mu = RooRealVar('RatioSigmaHoZ4mu', 'RatioSigmaHoZ4mu', fidxs['4mu']/fidxs_z['4mu'], 0.0, 10.0)
        SigmaZ2e2mu = RooFormulaVar("SigmaZ2e2mu","(@0/@1-@2/@3-@4/@5)", RooArgList(SigmaH, RatioSigmaHoZ, SigmaH4e, RatioSigmaHoZ4e, SigmaH4mu, RatioSigmaHoZ4mu))
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ2e2mu, trueZ_norm))
    else:
        name = "RatioSigmaHoZ"+chan
        RatioSigmaHoZ = RooRealVar(name, name, fidxs[chan]/fidxs_z[chan], 0.0, 10.0)
        name = "SigmaZ"+chan
        SigmaZ = RooFormulaVar(name,"(@0/@1)", RooArgList(SigmaH, RatioSigmaHoZ))
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ, trueZ_norm))


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

    data_obs_file = TFile('data_8TeV.root')
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

    # trueH
    getattr(w,'import')(trueH,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueH_norm,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueH_norm_final,RooFit.RecycleConflictNodes())

    # trueZ
    getattr(w,'import')(trueZ,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueZ_norm,RooFit.RecycleConflictNodes())
    getattr(w,'import')(trueZ_norm_final,RooFit.RecycleConflictNodes())

    # out_trueH
    getattr(w,'import')(out_trueH,RooFit.RecycleConflictNodes())
    getattr(w,'import')(out_trueH_norm,RooFit.RecycleConflictNodes())

    # out_trueZ
    getattr(w,'import')(out_trueZ,RooFit.RecycleConflictNodes())
    getattr(w,'import')(out_trueZ_norm,RooFit.RecycleConflictNodes())
    
    # fakeH
    getattr(w,'import')(fakeH,RooFit.RecycleConflictNodes())
    getattr(w,'import')(fakeH_norm,RooFit.RecycleConflictNodes())

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
    fout = TFile("xs_ratio/hzz4l_"+chan+"S_8TeV_xs_Ratio_"+modelName+"_"+physicalModel+".input.root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(w)
    fout.Close()

    return data_obs.numEntries()





