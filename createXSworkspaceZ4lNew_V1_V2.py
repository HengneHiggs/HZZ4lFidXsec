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

    # MZ
    name = "MZ"
    MZ = RooRealVar(name,"MZ", 91.1876, 70.0, 150.0)

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
        SigmaZ = RooRealVar('SigmaZ', 'SigmaZ', fidxs_z['4l'], 0.0, 10.0)
        SigmaZ4e = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
        SigmaZ4mu = RooRealVar('SigmaZ4mu', 'SigmaZ4mu', fidxs_z['4mu'], 0.0, 10.0)
        SigmaZ2e2mu = RooFormulaVar("SigmaZ2e2mu","(@0-@1-@2)", RooArgList(SigmaZ, SigmaZ4e, SigmaZ4mu))
        trueZ_norm_final = RooFormulaVar("trueZ"+chan+"_final_norm","@0*@1", RooArgList(SigmaZ2e2mu, trueZ_norm))
    else:
        name = "SigmaZ"+chan
        SigmaZ = RooRealVar('SigmaZ4e', 'SigmaZ4e', fidxs_z['4e'], 0.0, 10.0)
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

    frac_ggzz = fractionsBackground['ggZZ_'+chan+'_MCFM67_'+chan+'_'+obsName+'_recobin0']
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





