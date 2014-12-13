#!/usr/bin/python

import sys, os, pwd, commands

from ROOT import *


sys.path.append('./datacardInputs')

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
    DeltaMHmZ = RooRealVar(name, "DeltaMHmZ", 125.0-91.1876, 0.0, 100.0)

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
           


    CMS_zz4l_mass.setRange("small", 105., 140.)
    CMS_zz4l_mass.setRange("big", 50., 140.)
    CMS_zz4l_mass.setRange("tail", 50., 105.)

    intSmall = trueH.createIntegral(RooArgSet(CMS_zz4l_mass), RooFit.NormSet(RooArgSet(CMS_zz4l_mass)), RooFit.Range("small"))
    intBig = trueH.createIntegral(RooArgSet(CMS_zz4l_mass), RooFit.NormSet(RooArgSet(CMS_zz4l_mass)), RooFit.Range("big"))
    intTail = trueH.createIntegral(RooArgSet(CMS_zz4l_mass), RooFit.NormSet(RooArgSet(CMS_zz4l_mass)), RooFit.Range("tail"))

    intS = intSmall.getVal()
    intB = intBig.getVal()
    intT = intTail.getVal()
    print "intS = ", intS
    print "intB = ", intB
    print "intT = ", intT
    print "tail/big ratio "+chan+" = ",intT/intB

createXSworkspaceZ4lInclusive("mass4l", "4e", "SM_125", "v2")
createXSworkspaceZ4lInclusive("mass4l", "4mu", "SM_125", "v2")
createXSworkspaceZ4lInclusive("mass4l", "2e2mu", "SM_125", "v2")

