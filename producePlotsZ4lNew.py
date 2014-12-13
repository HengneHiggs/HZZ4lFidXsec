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

if (not os.path.exists("plots_z4l")):
    os.system("mkdir plots_z4l")

from ROOT import *

from tdrStyle import *
setTDRStyle()
        

sys.path.append('./datacardInputs')


def plotZ4l(obsName):    

    # import z4l fid acc eff outinratio
    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
    acc_z = _temp.acc
    eff_z = _temp.eff
    outinratio_z = _temp.outinratio

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
  
    chans = {'4l':0, '2e2mu':1, '4mu':2, '4e':3}
    # read data
    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        if (channel=='4l'): channel = '' 
        fidxs_data[chan] = resultsXS['SMZ4l_mass4l_SigmaZ'+channel]['central']
        fidxs_data_hi[chan] = resultsXS['SMZ4l_mass4l_SigmaZ'+channel]['uncerUp']
        fidxs_data_lo[chan] = fabs(resultsXS['SMZ4l_mass4l_SigmaZ'+channel]['uncerDn'])

    print 'fidxs_data',fidxs_data
    print 'fidxs_data_hi',fidxs_data_hi
    print 'fidxs_data_lo',fidxs_data_lo

    #calculate mc
    fidxs_z = [0.0,0.0,0.0,0.0]
    fidxs_z_hi = [0.0,0.0,0.0,0.0]
    fidxs_z_lo = [0.0,0.0,0.0,0.0]

    for channel in ['2e2mu', '4mu', '4e']:
        chan = chans[channel]
        fidxs_z[chan] = 1000.0*z4l_xsbr['SMZ4l_'+channel]*acc_z['SMZ4l_'+channel+'_'+obsName+'_genbin0_recobin0']

    fidxs_z[0] = fidxs_z[1]+fidxs_z[2]+fidxs_z[3]




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

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        fidxs_z_hi[chan] = unc_theory_z_hi*fidxs_z[chan]
        fidxs_z_lo[chan] = unc_theory_z_lo*fidxs_z[chan]

    print 'fidxs_z',fidxs_z
    print 'fidxs_z_hi',fidxs_z_hi
    print 'fidxs_z_lo',fidxs_z_lo


    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_data[chan],3))+'^{+'+str(round(fidxs_data_hi[chan],3))+'}_{-'+str(round(fidxs_data_lo[chan],3))+'}$'

    for channel in ['4l', '2e2mu', '4mu', '4e']:
        chan = chans[channel]
        print '&$'+str(round(fidxs_z[chan],3))+'^{+'+str(round(fidxs_z_hi[chan],3))+'}_{-'+str(round(fidxs_z_lo[chan],3))+'}$'

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

    a_fidxs_z = array('d',[fidxs_z[i] for i in range(0,4)])
    v_fidxs_z = TVectorD(len(a_fidxs_z),a_fidxs_z)
    a_fidxs_z_hi = array('d',[fidxs_z_hi[i] for i in range(0,4)])
    v_fidxs_z_hi = TVectorD(len(a_fidxs_z_hi),a_fidxs_z_hi)
    a_fidxs_z_lo = array('d',[fidxs_z_lo[i] for i in range(0,4)])
    v_fidxs_z_lo = TVectorD(len(a_fidxs_z_lo),a_fidxs_z_lo)

    g_fidxs_data = TGraphAsymmErrors(v_observable,v_fidxs_data,v_zeros,v_zeros,v_fidxs_data_lo,v_fidxs_data_hi)
    g_fidxs_data.SetMarkerColor(ROOT.kBlack)
    g_fidxs_data.SetLineColor(ROOT.kBlack)
    g_fidxs_data.SetLineWidth(2)
    g_fidxs_data.SetMarkerStyle(20)
    g_fidxs_data.SetMarkerSize(1.2)


    g_fidxs_z = TGraphAsymmErrors(v_observable,v_fidxs_z,v_dobservable,v_dobservable,v_fidxs_z_lo,v_fidxs_z_hi)
    g_fidxs_z.SetFillStyle(3116);
    g_fidxs_z.SetFillColor(ROOT.kAzure)

    # plotting
  
    # fidxs 
    c1 = TCanvas("c1",obsName, 1000, 800)
    if(opt.SETLOG): c1.SetLogy()
    c1.SetBottomMargin(0.15)
    c1.SetRightMargin(0.06)
    c1.SetLeftMargin(0.2)

    dummy1 = TH1D("dummy1","dummy1", 4, 0, 4)
    for i in range(1,5):
        dummy1.SetBinContent(i,2.5*max(a_fidxs_z))
    dummy1.GetXaxis().SetBinLabel(1,'4l')
    dummy1.GetXaxis().SetBinLabel(2,'2e2#mu')
    dummy1.GetXaxis().SetBinLabel(3,'4#mu')
    dummy1.GetXaxis().SetBinLabel(4,'4e')

    dummy1.SetMaximum(2.5*max(a_fidxs_z))
    dummy1.SetMinimum(0.0)
    dummy1.SetLineColor(0)
    dummy1.SetMarkerColor(0)
    dummy1.SetLineWidth(0)
    dummy1.SetMarkerSize(0)
    dummy1.GetXaxis().SetTitle("")
    dummy1.GetXaxis().SetTitleOffset(1.1)
    dummy1.GetYaxis().SetTitle("#sigma_{fid.} [fb]")
    dummy1.GetYaxis().SetTitleOffset(1.5)

    dummy1.Draw("hist")
    g_fidxs_z.Draw("2same")
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
    legend1.AddEntry(g_fidxs_z, "Z #rightarrow 4l (powheg)", "f")

    legend1.SetShadowColor(0);
    legend1.SetFillColor(0);
    legend1.SetLineColor(0);
    legend1.Draw()

    if (opt.SETLOG): set_log = '_logscale'
    else: set_log = ''
    c1.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.pdf')
    c1.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.png')
    c1.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.C')

    

   

plotZ4l('mass4l')  

