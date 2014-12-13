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
    m4l_hi = 160.0 #105.0

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

    # MZ
    name = "MZ"
    MZ = RooRealVar(name,"MZ", 91.1876, 10.0, 1000.0)

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
    elif (physicalModel=='v1' and chan=='2e2mu'):
        SigmaZ = RooRealVar('SigmaZ', 'SigmaZ', fidxs_z['4l'], 0.0, 10.0)
        SigmaZ4e = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
        SigmaZ4mu = RooRealVar('SigmaZ4mu', 'SigmaZ4mu', fidxs_z['4mu'], 0.0, 10.0)
        SigmaZ2e2mu = RooFormulaVar("SigmaZ2e2mu","(@0-@1-@2)", RooArgList(SigmaZ, SigmaZ4e, SigmaZ4mu))
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ2e2mu, trueZ_norm))
    else:
        name = "SigmaZ"+chan
        SigmaZ = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ, trueZ_norm))
   

    #int
    CMS_zz4l_mass.setRange("h4l", 105.0, 140.0)
    IntTrueZ = trueZ.createIntegral(RooArgSet(CMS_zz4l_mass), RooFit.Range("h4l"))
    print 'Int : ',IntTrueZ.getVal()





createXSworkspaceZ4lInclusive("mass4l", "4mu", "SMZ4l", "v2")
