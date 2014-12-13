import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *

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
    parser.add_option('',   '--resultTag',dest='resultTag',    type='string',default='',   help='Tag of results.')
    parser.add_option('',   '--setLog', action='store_true', dest='SETLOG', default=False, help='set plot to log scale y, default is False')
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
        

sys.path.append('./datacardInputs')


def plotRatio(obsName):    

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

    results_file = 'resultsXS'+opt.resultTag

    _temp = __import__(results_file, globals(), locals(), ['modelNames', 'resultsXS'], -1)
    modelNames = _temp.modelNames
    resultsXS = _temp.resultsXS
   
    print modelNames
    print resultsXS

    fidxs_data = [0.0,0.0,0.0,0.0]    
    fidxs_data_hi = [0.0,0.0,0.0,0.0]    
    fidxs_data_lo = [0.0,0.0,0.0,0.0]    
    ratio_data = [0.0,0.0,0.0,0.0]    
    ratio_data_hi = [0.0,0.0,0.0,0.0]    
    ratio_data_lo = [0.0,0.0,0.0,0.0]    
  
    chans = {'4l':0, '2e2mu':1, '4mu':2, '4e':3}
    # read data
    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        if (channel=='4l'): channel = '' 
        fidxs_data[chan] = resultsXS['SM_125_mass4l_SigmaH'+channel]['central']
        fidxs_data_hi[chan] = resultsXS['SM_125_mass4l_SigmaH'+channel]['uncerUp']
        fidxs_data_lo[chan] = fabs(resultsXS['SM_125_mass4l_SigmaH'+channel]['uncerDn'])
        ratio_data[chan] = resultsXS['SM_125_mass4l_RatioSigmaHoZ'+channel]['central']
        ratio_data_hi[chan] = resultsXS['SM_125_mass4l_RatioSigmaHoZ'+channel]['uncerUp']
        ratio_data_lo[chan] = fabs(resultsXS['SM_125_mass4l_RatioSigmaHoZ'+channel]['uncerDn'])

    print 'fidxs_data',fidxs_data
    print 'fidxs_data_hi',fidxs_data_hi
    print 'fidxs_data_lo',fidxs_data_lo
    print 'ratio_data',ratio_data
    print 'ratio_data_hi',ratio_data_hi
    print 'ratio_data_lo',ratio_data_lo    

    #calculate mc
    fidxs_ggh1 = [0.0,0.0,0.0,0.0]
    fidxs_ggh2 = [0.0,0.0,0.0,0.0]
    fidxs_xh = [0.0,0.0,0.0,0.0]
    fidxs_z = [0.0,0.0,0.0,0.0]
    ratio_ggh1 = [0.0,0.0,0.0,0.0]
    ratio_ggh2 = [0.0,0.0,0.0,0.0]
    ratio_xh = [0.0,0.0,0.0,0.0]

    fidxs_ggh1_hi = [0.0,0.0,0.0,0.0]
    fidxs_ggh2_hi = [0.0,0.0,0.0,0.0]
    fidxs_xh_hi = [0.0,0.0,0.0,0.0]
    fidxs_z_hi = [0.0,0.0,0.0,0.0]
    ratio_ggh1_hi = [0.0,0.0,0.0,0.0]
    ratio_ggh2_hi = [0.0,0.0,0.0,0.0]
    ratio_xh_hi = [0.0,0.0,0.0,0.0]

    fidxs_ggh1_lo = [0.0,0.0,0.0,0.0]
    fidxs_ggh2_lo = [0.0,0.0,0.0,0.0]
    fidxs_xh_lo = [0.0,0.0,0.0,0.0]
    fidxs_z_lo = [0.0,0.0,0.0,0.0]
    ratio_ggh1_lo = [0.0,0.0,0.0,0.0]
    ratio_ggh2_lo = [0.0,0.0,0.0,0.0]
    ratio_xh_lo = [0.0,0.0,0.0,0.0]

    for channel in ['2e2mu', '4mu', '4e']:
        chan = chans[channel]
        fidxs_xh[chan] = 0.0
        fidxs_xh[chan] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+channel]*acc['VBF_powheg_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_xh[chan] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+channel]*acc['WH_pythia_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_xh[chan] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+channel]*acc['ZH_pythia_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_xh[chan] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+channel]*acc['ttH_pythia_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_ggh1[chan] = higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+channel]*acc['ggH_powheg15_JHUgen_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_ggh1[chan] += fidxs_xh[chan]
        fidxs_ggh2[chan] = higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+channel]*acc['ggH_minloHJJ_125_'+channel+'_'+obsName+'_genbin0_recobin0']
        fidxs_ggh2[chan] += fidxs_xh[chan]
        fidxs_z[chan] = 1000.0*z4l_xsbr['SMZ4l_'+channel]*acc_z['SMZ4l_'+channel+'_'+obsName+'_genbin0_recobin0']
        ratio_xh[chan] = fidxs_xh[chan]/fidxs_z[chan]
        ratio_ggh1[chan] = fidxs_ggh1[chan]/fidxs_z[chan]
        ratio_ggh2[chan] = fidxs_ggh2[chan]/fidxs_z[chan]

    fidxs_xh[0] = fidxs_xh[1]+fidxs_xh[2]+fidxs_xh[3] 
    fidxs_ggh1[0] = fidxs_ggh1[1] + fidxs_ggh1[2] + fidxs_ggh1[3] 
    fidxs_ggh2[0] = fidxs_ggh2[1] + fidxs_ggh2[2] + fidxs_ggh2[3]
    fidxs_z[0] = fidxs_z[1]+fidxs_z[2]+fidxs_z[3]
    ratio_xh[0] = fidxs_xh[0]/fidxs_z[0]
    ratio_ggh1[0] = fidxs_ggh1[0]/fidxs_z[0]
    ratio_ggh2[0] = fidxs_ggh2[0]/fidxs_z[0]     




    #####
    #    Add theory uncertaities for MC

    # 4mu
    #pdf_qqbar lnN 1.0274 1.0274 -
    #pdf_hzz4l_accept lnN 1.02 - -
    # 4e
    #pdf_qqbar lnN 1.0274 1.0274 -
    #pdf_hzz4l_accept lnN 1.02 - -
    # 2e2mu
    #pdf_qqbar lnN 1.0274 1.0274 -
    #pdf_hzz4l_accept lnN 1.02 - -
    #QCDscale_VV lnN - 1.0234 -
    unc_theory_z_hi = sqrt(log(1.0+0.0274)**2+log(1.0+0.02)**2+log(1.0+0.0234)**2)
    unc_theory_z_lo = sqrt(log(1.0-0.0274)**2+log(1.0-0.02)**2+log(1.0-0.0234)**2)

    #process ggH qqH WH ZH ttH bkg_qqzz bkg_ggzz bkg_zjets
    #pdf_gg lnN 1.0720 - - - 1.0780 - 1.0710 -
    #pdf_qqbar lnN - 1.0270 1.0350 1.0350 - 1.0342 - -
    #pdf_hzz4l_accept lnN 1.02 1.02 1.02 1.02 1.02 - - -
    #QCDscale_ggH lnN 1.0750 - - - - - - -
    #QCDscale_qqH lnN - 1.0020 - - - - - -
    #QCDscale_VH lnN - - 1.0040 1.0155 - - - -
    #QCDscale_ttH lnN - - - - 1.0655 - - -
    #QCDscale_ggVV lnN - - - - - - 1.2435 -
    #BRhiggs_hzz4l lnN 1.02 1.02 1.02 1.02 1.02 - - -
    unc_theory_ggh_hi = sqrt(0.072**2+0.075**2+0.02**2+0.02**2)
    unc_theory_ggh_lo = sqrt(0.078**2+0.069**2+0.02**2+0.02**2)

    unc_theory_xh_hi  = sqrt(0.027**2+0.02**2+0.002**2+0.02**2)
    unc_theory_xh_lo  = unc_theory_xh_hi


    # for ratio, if we have 
    # z=x/y, 
    # +dx, -dx, +dy, -dy, 
    # +dtx = +dx/x, +dty = +dy/y
    # ask: +dz, +dtz, -dz, -dtz
    # we have:
    # z+dz = (x+dx)/(y-dy) 
    # z*(1+dtz) = x/y * (1+dtx)/(1-dty)
    # (1+dtz) = (1+dtx)/(1-dty)
    # +dtz = (1+dtx)/(1-dty)-1
    # similarly:
    # +dtz = (1+dtx)/(1-dty)-1
    # -dtz = (1-dtx)/(1+dty)-1

    unc_theory_ratio_ggh_hi = (1.0+unc_theory_ggh_hi)/(1.0-unc_theory_z_lo) - 1.0
    unc_theory_ratio_ggh_lo = -(1.0-unc_theory_ggh_lo)/(1.0+unc_theory_z_hi) + 1.0
    unc_theory_ratio_xh_hi = (1.0+unc_theory_xh_hi)/(1.0-unc_theory_z_lo) - 1.0
    unc_theory_ratio_xh_lo = -(1.0-unc_theory_xh_lo)/(1.0+unc_theory_z_hi) + 1.0

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]

        fidxs_ggh1_hi[chan] = unc_theory_ggh_hi*fidxs_ggh1[chan] 
        fidxs_ggh2_hi[chan] = unc_theory_ggh_hi*fidxs_ggh2[chan]
        fidxs_xh_hi[chan] = unc_theory_xh_hi*fidxs_xh[chan]
        fidxs_z_hi[chan] = unc_theory_z_hi*fidxs_z[chan]

        fidxs_ggh1_lo[chan] = unc_theory_ggh_lo*fidxs_ggh1[chan]
        fidxs_ggh2_lo[chan] = unc_theory_ggh_lo*fidxs_ggh2[chan]
        fidxs_xh_lo[chan] = unc_theory_xh_lo*fidxs_xh[chan]
        fidxs_z_lo[chan] = unc_theory_z_lo*fidxs_z[chan]
       
        ratio_ggh1_hi[chan] = unc_theory_ratio_ggh_hi*ratio_ggh1[chan]
        ratio_ggh2_hi[chan] = unc_theory_ratio_ggh_hi*ratio_ggh2[chan]
        ratio_xh_hi[chan] = unc_theory_ratio_xh_hi*ratio_xh[chan]

        ratio_ggh1_lo[chan] = unc_theory_ratio_ggh_lo*ratio_ggh1[chan]
        ratio_ggh2_lo[chan] = unc_theory_ratio_ggh_lo*ratio_ggh2[chan]
        ratio_xh_lo[chan] = unc_theory_ratio_xh_lo*ratio_xh[chan]

    print 'fidxs_ggh1',fidxs_ggh1
    print 'fidxs_ggh1_hi',fidxs_ggh1_hi
    print 'fidxs_ggh1_lo',fidxs_ggh1_lo
    print 'fidxs_ggh2',fidxs_ggh2
    print 'fidxs_ggh2_hi',fidxs_ggh2_hi
    print 'fidxs_ggh2_lo',fidxs_ggh2_lo
    print 'fidxs_xh',fidxs_xh
    print 'fidxs_xh_hi',fidxs_xh_hi
    print 'fidxs_xh_lo',fidxs_xh_lo
    print 'fidxs_z',fidxs_z
    print 'fidxs_z_hi',fidxs_z_hi
    print 'fidxs_z_lo',fidxs_z_lo
    print 'ratio_ggh1',ratio_ggh1
    print 'ratio_ggh1_hi',ratio_ggh1_hi
    print 'ratio_ggh1_lo',ratio_ggh1_lo
    print 'ratio_ggh2',ratio_ggh2
    print 'ratio_ggh2_hi',ratio_ggh2_hi
    print 'ratio_ggh2_lo',ratio_ggh2_lo
    print 'ratio_xh',ratio_xh
    print 'ratio_xh_hi',ratio_xh_hi
    print 'ratio_xh_lo',ratio_xh_lo


    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_data[chan],3))+'^{'+str(round(fidxs_data_hi[chan],3))+'}_{'+str(round(fidxs_data_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_ggh1[chan],3))+'^{'+str(round(fidxs_ggh1_hi[chan],3))+'}_{'+str(round(fidxs_ggh1_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_ggh2[chan],3))+'^{'+str(round(fidxs_ggh2_hi[chan],3))+'}_{'+str(round(fidxs_ggh2_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_z[chan],3))+'^{'+str(round(fidxs_z_hi[chan],3))+'}_{'+str(round(fidxs_z_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(ratio_data[chan],3))+'^{'+str(round(ratio_data_hi[chan],3))+'}_{'+str(round(ratio_data_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(ratio_ggh1[chan],3))+'^{'+str(round(ratio_ggh1_hi[chan],3))+'}_{'+str(round(ratio_ggh1_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(ratio_ggh2[chan],3))+'^{'+str(round(ratio_ggh2_hi[chan],3))+'}_{'+str(round(ratio_ggh2_lo[chan],3))+'}$'

    print " "

    a_observable  = array('d',[0.5+i for i in range(0,4)])
    v_observable    = TVectorD(len(a_observable),a_observable)

    a_dobservable  = array('d',[0.5 for i in range(0,4)])
    v_dobservable = TVectorD(len(a_dobservable),a_dobservable)

    a_zeros = array('d',[0.0 for i in range(0,4)])
    v_zeros = TVectorD(len(a_zeros),a_zeros)

    a_twos = array('d',[0.2*a_dobservable[i] for i in range(0,4)])
    v_twos = TVectorD(len(a_twos),a_twos)


    a_fidxs_data = array('d',[fidxs_data[i] for i in range(0,4)])
    v_fidxs_data = TVectorD(len(a_fidxs_data),a_fidxs_data)
    a_fidxs_data_hi = array('d',[fidxs_data_hi[i] for i in range(0,4)])
    v_fidxs_data_hi = TVectorD(len(a_fidxs_data_hi),a_fidxs_data_hi)
    a_fidxs_data_lo = array('d',[fidxs_data_lo[i] for i in range(0,4)])
    v_fidxs_data_lo = TVectorD(len(a_fidxs_data_lo),a_fidxs_data_lo)

    a_ratio_data = array('d',[ratio_data[i] for i in range(0,4)])
    v_ratio_data = TVectorD(len(a_ratio_data),a_ratio_data)
    a_ratio_data_hi = array('d',[ratio_data_hi[i] for i in range(0,4)])
    v_ratio_data_hi = TVectorD(len(a_ratio_data_hi),a_ratio_data_hi)
    a_ratio_data_lo = array('d',[ratio_data_lo[i] for i in range(0,4)])
    v_ratio_data_lo = TVectorD(len(a_ratio_data_lo),a_ratio_data_lo)

    a_fidxs_ggh1 = array('d',[fidxs_ggh1[i] for i in range(0,4)])
    v_fidxs_ggh1 = TVectorD(len(a_fidxs_ggh1),a_fidxs_ggh1)
    a_fidxs_ggh1_hi = array('d',[fidxs_ggh1_hi[i] for i in range(0,4)])
    v_fidxs_ggh1_hi = TVectorD(len(a_fidxs_ggh1_hi),a_fidxs_ggh1_hi)
    a_fidxs_ggh1_lo = array('d',[fidxs_ggh1_lo[i] for i in range(0,4)])
    v_fidxs_ggh1_lo = TVectorD(len(a_fidxs_ggh1_lo),a_fidxs_ggh1_lo)

    a_fidxs_ggh2 = array('d',[fidxs_ggh2[i] for i in range(0,4)])
    v_fidxs_ggh2 = TVectorD(len(a_fidxs_ggh2),a_fidxs_ggh2)
    a_fidxs_ggh2_hi = array('d',[fidxs_ggh2_hi[i] for i in range(0,4)])
    v_fidxs_ggh2_hi = TVectorD(len(a_fidxs_ggh2_hi),a_fidxs_ggh2_hi)
    a_fidxs_ggh2_lo = array('d',[fidxs_ggh2_lo[i] for i in range(0,4)])
    v_fidxs_ggh2_lo = TVectorD(len(a_fidxs_ggh2_lo),a_fidxs_ggh2_lo)

    a_fidxs_xh = array('d',[fidxs_xh[i] for i in range(0,4)])
    v_fidxs_xh = TVectorD(len(a_fidxs_xh),a_fidxs_xh)
    a_fidxs_xh_hi = array('d',[fidxs_xh_hi[i] for i in range(0,4)])
    v_fidxs_xh_hi = TVectorD(len(a_fidxs_xh_hi),a_fidxs_xh_hi)
    a_fidxs_xh_lo = array('d',[fidxs_xh_lo[i] for i in range(0,4)])
    v_fidxs_xh_lo = TVectorD(len(a_fidxs_xh_lo),a_fidxs_xh_lo)

    a_fidxs_z = array('d',[fidxs_z[i] for i in range(0,4)])
    v_fidxs_z = TVectorD(len(a_fidxs_z),a_fidxs_z)
    a_fidxs_z_hi = array('d',[fidxs_z_hi[i] for i in range(0,4)])
    v_fidxs_z_hi = TVectorD(len(a_fidxs_z_hi),a_fidxs_z_hi)
    a_fidxs_z_lo = array('d',[fidxs_z_lo[i] for i in range(0,4)])
    v_fidxs_z_lo = TVectorD(len(a_fidxs_z_lo),a_fidxs_z_lo)


    a_ratio_ggh1 = array('d',[ratio_ggh1[i] for i in range(0,4)])
    v_ratio_ggh1 = TVectorD(len(a_ratio_ggh1),a_ratio_ggh1)
    a_ratio_ggh1_hi = array('d',[ratio_ggh1_hi[i] for i in range(0,4)])
    v_ratio_ggh1_hi = TVectorD(len(a_ratio_ggh1_hi),a_ratio_ggh1_hi)
    a_ratio_ggh1_lo = array('d',[ratio_ggh1_lo[i] for i in range(0,4)])
    v_ratio_ggh1_lo = TVectorD(len(a_ratio_ggh1_lo),a_ratio_ggh1_lo)

    a_ratio_ggh2 = array('d',[ratio_ggh2[i] for i in range(0,4)])
    v_ratio_ggh2 = TVectorD(len(a_ratio_ggh2),a_ratio_ggh2)
    a_ratio_ggh2_hi = array('d',[ratio_ggh2_hi[i] for i in range(0,4)])
    v_ratio_ggh2_hi = TVectorD(len(a_ratio_ggh2_hi),a_ratio_ggh2_hi)
    a_ratio_ggh2_lo = array('d',[ratio_ggh2_lo[i] for i in range(0,4)])
    v_ratio_ggh2_lo = TVectorD(len(a_ratio_ggh2_lo),a_ratio_ggh2_lo)

    a_ratio_xh = array('d',[ratio_xh[i] for i in range(0,4)])
    v_ratio_xh = TVectorD(len(a_ratio_xh),a_ratio_xh)
    a_ratio_xh_hi = array('d',[ratio_xh_hi[i] for i in range(0,4)])
    v_ratio_xh_hi = TVectorD(len(a_ratio_xh_hi),a_ratio_xh_hi)
    a_ratio_xh_lo = array('d',[ratio_xh_lo[i] for i in range(0,4)])
    v_ratio_xh_lo = TVectorD(len(a_ratio_xh_lo),a_ratio_xh_lo)


    g_fidxs_data = TGraphAsymmErrors(v_observable,v_fidxs_data,v_zeros,v_zeros,v_fidxs_data_lo,v_fidxs_data_hi)
    g_fidxs_data.SetMarkerColor(ROOT.kBlack)
    g_fidxs_data.SetLineColor(ROOT.kBlack)
    g_fidxs_data.SetLineWidth(2)
    g_fidxs_data.SetMarkerStyle(20)
    g_fidxs_data.SetMarkerSize(1.2)

    g_ratio_data = TGraphAsymmErrors(v_observable,v_ratio_data,v_zeros,v_zeros,v_ratio_data_lo,v_ratio_data_hi)
    g_ratio_data.SetMarkerColor(ROOT.kBlack)
    g_ratio_data.SetLineColor(ROOT.kBlack)
    g_ratio_data.SetLineWidth(2)
    g_ratio_data.SetMarkerStyle(20)
    g_ratio_data.SetMarkerSize(1.2)


    g_fidxs_ggh1 = TGraphAsymmErrors(v_observable,v_fidxs_ggh1,v_dobservable,v_dobservable,v_fidxs_ggh1_lo,v_fidxs_ggh1_hi)
    g_fidxs_ggh1.SetFillStyle(3216);
    g_fidxs_ggh1.SetFillColor(ROOT.kAzure)

    g_fidxs_ggh2 = TGraphAsymmErrors(v_observable,v_fidxs_ggh2,v_dobservable,v_dobservable,v_fidxs_ggh2_lo,v_fidxs_ggh2_hi)
    g_fidxs_ggh2.SetFillStyle(3218);
    g_fidxs_ggh2.SetFillColor(ROOT.kOrange)

    g_fidxs_xh = TGraphAsymmErrors(v_observable,v_fidxs_xh,v_dobservable,v_dobservable,v_fidxs_xh_lo,v_fidxs_xh_hi)
    g_fidxs_xh.SetFillColor(ROOT.kGreen+3)
    g_fidxs_xh.SetLineColor(ROOT.kGreen+3)

    g_ratio_ggh1 = TGraphAsymmErrors(v_observable,v_ratio_ggh1,v_dobservable,v_dobservable,v_ratio_ggh1_lo,v_ratio_ggh1_hi)
    g_ratio_ggh1.SetFillStyle(3216);
    g_ratio_ggh1.SetFillColor(ROOT.kAzure)

    g_ratio_ggh2 = TGraphAsymmErrors(v_observable,v_ratio_ggh2,v_dobservable,v_dobservable,v_ratio_ggh2_lo,v_ratio_ggh2_hi)
    g_ratio_ggh2.SetFillStyle(3218);
    g_ratio_ggh2.SetFillColor(ROOT.kOrange)

    g_ratio_xh = TGraphAsymmErrors(v_observable,v_ratio_xh,v_dobservable,v_dobservable,v_ratio_xh_lo,v_ratio_xh_hi)
    g_ratio_xh.SetFillColor(ROOT.kGreen+3)
    g_ratio_xh.SetLineColor(ROOT.kGreen+3)


    # plotting
  
    # fidxs 
    c1 = TCanvas("c1",obsName, 1000, 800)
    if(opt.SETLOG): c1.SetLogy()
    c1.SetBottomMargin(0.15)
    c1.SetRightMargin(0.06)
    c1.SetLeftMargin(0.2)

    dummy1 = TH1D("dummy1","dummy1", 4, 0, 4)
    for i in range(1,5):
        dummy1.SetBinContent(i,2.5*max(a_fidxs_ggh1))
    dummy1.GetXaxis().SetBinLabel(1,'4l')
    dummy1.GetXaxis().SetBinLabel(2,'2e2#mu')
    dummy1.GetXaxis().SetBinLabel(3,'4#mu')
    dummy1.GetXaxis().SetBinLabel(4,'4e')

    dummy1.SetMaximum(2.5*max(a_fidxs_ggh1))
    dummy1.SetMinimum(0.0)
    dummy1.SetLineColor(0)
    dummy1.SetMarkerColor(0)
    dummy1.SetLineWidth(0)
    dummy1.SetMarkerSize(0)
    dummy1.GetXaxis().SetTitle("")
    dummy1.GetXaxis().SetTitleOffset(1.1)
    #dummy1.GetYaxis().SetTitle("#sigma^{H#rightarrow 4l}_{fid.}/#sigma^{Z#rightarrow 4l}_{fid.}")
    dummy1.GetYaxis().SetTitle("#sigma_{fid.} [fb]")
    dummy1.GetYaxis().SetTitleOffset(1.5)

    dummy1.Draw("hist")
    g_fidxs_ggh1.Draw("2same")
    g_fidxs_ggh2.Draw("2same")
    g_fidxs_xh.Draw("2same")
    g_fidxs_data.Draw("psameZ")
    dummy1.Draw("axissame")

    latex1 = TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.5*c1.GetTopMargin())
    latex1.SetTextFont(42)
    latex1.SetTextAlign(31) # align right
    latex1.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
    latex1.SetTextSize(0.9*c1.GetTopMargin())
    latex1.SetTextFont(62)
    latex1.SetTextAlign(11) # align right
    latex1.DrawLatex(0.27, 0.85, "CMS")
    latex1.SetTextSize(0.7*c1.GetTopMargin())
    latex1.SetTextFont(52)
    latex1.SetTextAlign(11)
    latex1.DrawLatex(0.25, 0.8, "Preliminary")

    legend1 = TLegend(0.48,0.60,0.9,0.88)
    if ("Asimov" in opt.resultTag):
        legend1.AddEntry(g_fidxs_data, "Asimov Data (stat. #oplus sys. unc.)", "ep")
    else: 
        legend1.AddEntry(g_fidxs_data, "Data (stat. #oplus sys. unc.)", "ep")
    legend1.AddEntry(g_fidxs_ggh1, "gg#rightarrowH (powheg+JHUgen) + XH", "f")
    legend1.AddEntry(g_fidxs_ggh2, "gg#rightarrowH (minlo HJJ) + XH", "f")
    legend1.AddEntry(g_fidxs_xh , "XH = VBF (powheg) + VH + ttH (pythia)", "l")

    legend1.SetShadowColor(0);
    legend1.SetFillColor(0);
    legend1.SetLineColor(0);
    legend1.Draw()

    if (opt.SETLOG): set_log = '_logscale'
    else: set_log = ''
    c1.SaveAs('plots_ratio/fidxs'+opt.resultTag+set_log+'.pdf')
    c1.SaveAs('plots_ratio/fidxs'+opt.resultTag+set_log+'.png')
    c1.SaveAs('plots_ratio/fidxs'+opt.resultTag+set_log+'.C')

    

    # ratio
    c2 = TCanvas("c2",obsName, 1000, 800)
    if(opt.SETLOG): c2.SetLogy()
    c2.SetBottomMargin(0.15)
    c2.SetRightMargin(0.06)
    c2.SetLeftMargin(0.2)

    dummy2 = TH1D("dummy2","dummy2", 4, 0, 4)
    for i in range(1,5):
        dummy2.SetBinContent(i,2.5*max(a_ratio_ggh1))
    dummy2.GetXaxis().SetBinLabel(1,'4l')
    dummy2.GetXaxis().SetBinLabel(2,'2e2#mu')
    dummy2.GetXaxis().SetBinLabel(3,'4#mu')
    dummy2.GetXaxis().SetBinLabel(4,'4e')

    dummy2.SetMaximum(2.5*max(a_ratio_ggh1))
    dummy2.SetMinimum(0.0)
    dummy2.SetLineColor(0)
    dummy2.SetMarkerColor(0)
    dummy2.SetLineWidth(0)
    dummy2.SetMarkerSize(0)
    dummy2.GetXaxis().SetTitle("")
    dummy2.GetXaxis().SetTitleOffset(1.1)
    dummy2.GetYaxis().SetTitle("#sigma^{H#rightarrow 4l}_{fid.}/#sigma^{Z#rightarrow 4l}_{fid.}")
    #dummy2.GetYaxis().SetTitle("#sigma_{fid.} [fb]")
    dummy2.GetYaxis().SetTitleOffset(1.5)

    dummy2.Draw("hist")
    g_ratio_ggh1.Draw("2same")
    g_ratio_ggh2.Draw("2same")
    g_ratio_xh.Draw("2same")
    g_ratio_data.Draw("psameZ")
    dummy2.Draw("axissame")

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c2.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
    #latex2.SetTextSize(0.6*c2.GetTopMargin())
    #latex2.SetTextFont(62)
    #latex2.SetTextAlign(11) # align right
    #latex2.DrawLatex(0.19, 0.95, "CMS")
    #latex2.SetTextSize(0.45*c2.GetTopMargin())
    #latex2.SetTextFont(52)
    #latex2.SetTextAlign(11)
    #latex2.DrawLatex(0.30, 0.95, "Preliminary")

    latex2.SetTextSize(0.9*c2.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.27, 0.85, "CMS")
    latex2.SetTextSize(0.7*c2.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.25, 0.8, "Preliminary")

    legend2 = TLegend(.48,0.60,0.9,0.88)
    if ("Asimov" in opt.resultTag):
        legend2.AddEntry(g_ratio_data, "Asimov Data (stat. #oplus sys. unc.)", "ep")
    else: 
        legend2.AddEntry(g_ratio_data, "Data (stat. #oplus sys. unc.)", "ep")
    legend2.AddEntry(g_ratio_ggh1, "gg#rightarrowH (powheg+JHUgen) + XH", "f")
    legend2.AddEntry(g_ratio_ggh2, "gg#rightarrowH (minlo HJJ) + XH", "f")
    legend2.AddEntry(g_ratio_xh , "XH = VBF (powheg) + VH + ttH (pythia)", "l")

    legend2.SetShadowColor(0);
    legend2.SetFillColor(0);
    legend2.SetLineColor(0);
    legend2.Draw()

    if (opt.SETLOG): set_log = '_logscale'
    else: set_log = ''
    c2.SaveAs('plots_ratio/ratio'+opt.resultTag+set_log+'.pdf')
    c2.SaveAs('plots_ratio/ratio'+opt.resultTag+set_log+'.png')
    c2.SaveAs('plots_ratio/ratio'+opt.resultTag+set_log+'.C')
            
   

plotRatio('mass4l')  

