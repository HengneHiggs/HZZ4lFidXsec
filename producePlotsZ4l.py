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
    parser.add_option('',   '--resultTag',dest='resultTag',    type='string',default='',   help='Tag of results.')
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--unfoldModel',dest='UNFOLD',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the unfolding model for central value')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--useAsimov',action='store_true', dest='useAsimov',default=False, help='Use Asimov Data set, default is False')
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
        
datamodel = opt.UNFOLD

sys.path.append('./datacardInputs')


def plotXS(obsName, obs_bins):    

    _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc 
    _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
    z4l_xsbr = _temp.z4l_xsbr

    results_file = 'resultsXS'+opt.resultTag

    _temp = __import__(results_file, globals(), locals(), ['modelNames', 'resultsXS'], -1)
    modelNames = _temp.modelNames
    resultsXS = _temp.resultsXS
    
    SMZ4l = []
    SMZ4l_hi = []
    SMZ4l_lo = []
    data = []
    data_hi = []
    data_lo = []
    modeldep_hi = []
    modeldep_lo = []
    data_hi_allunc = []
    data_lo_allunc = []
    
    #process ggH bkg_qqzz bkg_zjets
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
    unc_theory_SMZ4l_hi = sqrt(log(1.0+0.0274)**2+log(1.0+0.02)**2+log(1.0+0.0234)**2)
    unc_theory_SMZ4l_lo = sqrt(log(1.0-0.0274)**2+log(1.0-0.02)**2+log(1.0-0.0234)**2)
    
    print "unc_theory_SMZ4l_hi=",unc_theory_SMZ4l_hi
    print "unc_theory_SMZ4l_lo=",unc_theory_SMZ4l_lo 

    if (not obsName=="mass4l"):    
        nBins=len(obs_bins)
        for obsBin in range(nBins-1):

            SMZ4l.append(0.0)
            SMZ4l_hi.append(0.0)
            SMZ4l_lo.append(0.0)
            data.append(0.0)
            data_hi.append(0.0)
            data_lo.append(0.0)
        
            for channel in ['4e','4mu','2e2mu']:
                SMZ4l[obsBin]+=1000.0*z4l_xsbr['SMZ4l_'+channel]*acc['SMZ4l_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']                        

            data[obsBin] = resultsXS[datamodel+"_"+obsName+"_genbin"+str(obsBin)]["central"]
            data_hi[obsBin] = resultsXS[datamodel+"_"+obsName+"_genbin"+str(obsBin)]["uncerUp"]
            data_lo[obsBin] = -1.0*resultsXS[datamodel+"_"+obsName+"_genbin"+str(obsBin)]["uncerDn"]

            SMZ4l_hi[obsBin] = unc_theory_SMZ4l_hi*SMZ4l[obsBin]
            SMZ4l_lo[obsBin] = unc_theory_SMZ4l_lo*SMZ4l[obsBin]   
 
    elif (obsName=="mass4l"):
        # binning 4l:0 2e2mu:1 4mu:2 4e:3 
        SMZ4l = [0.0,0.0,0.0,0.0]
        SMZ4l_hi = [0.0,0.0,0.0,0.0]
        SMZ4l_lo = [0.0,0.0,0.0,0.0]
        data = [0.0,0.0,0.0,0.0]
        data_hi = [0.0,0.0,0.0,0.0]
        data_lo = [0.0,0.0,0.0,0.0]
        SMZ4l[1] = 1000.0*z4l_xsbr['SMZ4l_2e2mu']*acc['SMZ4l_2e2mu_'+obsName+'_genbin0_recobin0']
        SMZ4l[2] = 1000.0*z4l_xsbr['SMZ4l_4mu']*acc['SMZ4l_4mu_'+obsName+'_genbin0_recobin0']
        SMZ4l[3] = 1000.0*z4l_xsbr['SMZ4l_4e']*acc['SMZ4l_4e_'+obsName+'_genbin0_recobin0']
        SMZ4l[0] = SMZ4l[1]+SMZ4l[2]+SMZ4l[3]
        for ch in range(0,4):
            SMZ4l_hi[ch] = unc_theory_SMZ4l_hi*SMZ4l[ch] 
            SMZ4l_lo[ch] = unc_theory_SMZ4l_lo*SMZ4l[ch] 
        #data
        Z4lr = resultsXS['SMZ4l_mass4l_Z4lr']["central"]
        Z4lr_hi = resultsXS['SMZ4l_mass4l_Z4lr']["uncerUp"]
        Z4lr_lo = resultsXS['SMZ4l_mass4l_Z4lr']["uncerDn"]
        Z4lfrac4e = resultsXS['SMZ4l_mass4l_Z4lfrac4e']["central"]
        Z4lfrac4e_hi = resultsXS['SMZ4l_mass4l_Z4lfrac4e']["uncerUp"]
        Z4lfrac4e_lo = resultsXS['SMZ4l_mass4l_Z4lfrac4e']["uncerDn"]
        Z4lfrac4mu = resultsXS['SMZ4l_mass4l_Z4lfrac4mu']["central"]
        Z4lfrac4mu_hi = resultsXS['SMZ4l_mass4l_Z4lfrac4mu']["uncerUp"]
        Z4lfrac4mu_lo = resultsXS['SMZ4l_mass4l_Z4lfrac4mu']["uncerDn"]
        data[0] = Z4lr
        data_hi[0] = Z4lr_hi 
        data_lo[0] = -1.0*Z4lr_lo
        data[1] = Z4lr*(1.0-Z4lfrac4mu-Z4lfrac4e)
        data_hi[1] = sqrt((1.0-Z4lfrac4mu-Z4lfrac4e)*(1.0-Z4lfrac4mu-Z4lfrac4e)*Z4lr_hi*Z4lr_hi+Z4lr*Z4lr*Z4lfrac4mu_hi*Z4lfrac4mu_hi+Z4lr*Z4lr*Z4lfrac4e_hi*Z4lfrac4e_hi)
        data_lo[1] = sqrt((1.0-Z4lfrac4mu-Z4lfrac4e)*(1.0-Z4lfrac4mu-Z4lfrac4e)*Z4lr_lo*Z4lr_lo+Z4lr*Z4lr*Z4lfrac4mu_lo*Z4lfrac4mu_lo+Z4lr*Z4lr*Z4lfrac4e_lo*Z4lfrac4e_lo)
        data[2] = Z4lr*Z4lfrac4mu
        data_hi[2] = sqrt(Z4lfrac4mu*Z4lfrac4mu*Z4lr_hi*Z4lr_hi+Z4lr*Z4lr*Z4lfrac4mu_hi*Z4lfrac4mu_hi)
        data_lo[2] = sqrt(Z4lfrac4mu*Z4lfrac4mu*Z4lr_lo*Z4lr_lo+Z4lr*Z4lr*Z4lfrac4mu_lo*Z4lfrac4mu_lo)
        data[3] = Z4lr*Z4lfrac4e
        data_hi[3] = sqrt(Z4lfrac4e*Z4lfrac4e*Z4lr_hi*Z4lr_hi+Z4lr*Z4lr*Z4lfrac4e_hi*Z4lfrac4e_hi)
        data_lo[3] = sqrt(Z4lfrac4e*Z4lfrac4e*Z4lr_lo*Z4lr_lo+Z4lr*Z4lr*Z4lfrac4e_lo*Z4lfrac4e_lo)
         

    data_hi_allunc = data_hi                                        
    data_lo_allunc = data_lo                                       

    
        
    print 'data',data
    print 'data_hi',data_hi
    print 'data_lo',data_lo
    print 'SMZ4l', SMZ4l
    print 'SMZ4l_hi', SMZ4l_hi
    print 'SMZ4l_lo', SMZ4l_lo

    if (obsName=="mass4l"):
        a_observable  = array('d',[0.5+i for i in range(0,4)])
        v_observable    = TVectorD(len(a_observable),a_observable)

        a_dobservable  = array('d',[0.5 for i in range(0,4)])
        v_dobservable = TVectorD(len(a_dobservable),a_dobservable)

        a_zeros = array('d',[0.0 for i in range(0,4)])
        v_zeros = TVectorD(len(a_zeros),a_zeros)
        a_twos = array('d',[0.2*a_dobservable[i] for i in range(0,4)])
        v_twos = TVectorD(len(a_twos),a_twos)

        a_SMZ4l = array('d',[SMZ4l[i] for i in range(0,4)])
        v_SMZ4l = TVectorD(len(a_SMZ4l),a_SMZ4l)
        print a_SMZ4l

        a_SMZ4l_hi = array('d',[unc_theory_SMZ4l_hi*SMZ4l[i] for i in range(0,4)])
        v_SMZ4l_hi = TVectorD(len(a_SMZ4l_hi),a_SMZ4l_hi)
        a_SMZ4l_lo = array('d',[unc_theory_SMZ4l_lo*SMZ4l[i] for i in range(0,4)])
        v_SMZ4l_lo = TVectorD(len(a_SMZ4l_lo),a_SMZ4l_lo)

        print data
        a_data = array('d',[data[i] for i in range(0,4)])
        print a_data
        v_data = TVectorD(len(a_data),a_data)
        a_data_hi = array('d',[data_hi[i] for i in range(0,4)])
        v_data_hi = TVectorD(len(a_data_hi),a_data_hi)
        a_data_lo = array('d',[data_lo[i] for i in range(0,4)])
        v_data_lo = TVectorD(len(a_data_lo),a_data_lo)

        v_data_hi_allunc = TVectorD(len(data_hi_allunc), array('d',[data_hi_allunc[i] for i in range(len(data_hi_allunc))]))
        v_data_lo_allunc = TVectorD(len(data_lo_allunc), array('d',[data_lo_allunc[i] for i in range(len(data_lo_allunc))]))
    else:
        a_observable  = array('d',[0.5*(float(obs_bins[i])+float(obs_bins[i+1])) for i in range(len(obs_bins)-1)])
        v_observable    = TVectorD(len(a_observable),a_observable)

        a_dobservable = array('d',[0.5*(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(obs_bins)-1)])
        v_dobservable = TVectorD(len(a_dobservable),a_dobservable)

        a_zeros = array('d',[0.0 for i in range(len(obs_bins)-1)])
        v_zeros = TVectorD(len(a_zeros),a_zeros)

        a_twos = array('d',[0.2*a_dobservable[i] for i in range(len(obs_bins)-1)])
        v_twos = TVectorD(len(a_twos),a_twos)
             
        a_SMZ4l = array('d',[SMZ4l[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(SMZ4l))])
        v_SMZ4l = TVectorD(len(a_SMZ4l),a_SMZ4l)
        print a_SMZ4l
        a_SMZ4l_hi = array('d',[unc_theory_SMZ4l_hi*SMZ4l[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(SMZ4l))])
        v_SMZ4l_hi = TVectorD(len(a_SMZ4l_hi),a_SMZ4l_hi)
        a_SMZ4l_lo = array('d',[unc_theory_SMZ4l_lo*SMZ4l[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(SMZ4l))])
        v_SMZ4l_lo = TVectorD(len(a_SMZ4l_lo),a_SMZ4l_lo)

        print data
        a_data = array('d',[data[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(data))])
        print a_data
        v_data = TVectorD(len(a_data),a_data)
        a_data_hi = array('d',[data_hi[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(data_hi))])
        v_data_hi = TVectorD(len(a_data_hi),a_data_hi)
        a_data_lo = array('d',[data_lo[i]/(float(obs_bins[i+1])-float(obs_bins[i])) for i in range(len(data_lo))])
        v_data_lo = TVectorD(len(a_data_lo),a_data_lo)

        v_data_hi_allunc = TVectorD(len(data_hi_allunc), array('d',[data_hi_allunc[i] for i in range(len(data_hi_allunc))]))
        v_data_lo_allunc = TVectorD(len(data_lo_allunc), array('d',[data_lo_allunc[i] for i in range(len(data_lo_allunc))]))                                        

    g_SMZ4l = TGraphAsymmErrors(v_observable,v_SMZ4l,v_dobservable,v_dobservable,v_SMZ4l_lo,v_SMZ4l_hi)
    g_SMZ4l.SetFillStyle(3145);
    g_SMZ4l.SetFillColor(ROOT.kAzure)

    g_data = TGraphAsymmErrors(v_observable,v_data,v_zeros,v_zeros,v_data_lo,v_data_hi)
    g_data.SetMarkerColor(ROOT.kBlack)
    g_data.SetLineColor(ROOT.kBlack)
    g_data.SetLineWidth(2)
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(1.2)

    g_data_allunc = TGraphAsymmErrors(v_observable,v_data,v_zeros,v_zeros,v_data_lo_allunc,v_data_hi_allunc)
    g_data_allunc.SetMarkerColor(ROOT.kBlack)
    g_data_allunc.SetLineColor(ROOT.kBlack)
    g_data_allunc.SetLineWidth(1)
    g_data_allunc.SetMarkerStyle(20)
    g_data_allunc.SetMarkerSize(1.2)
                
    if (obsName=="pT4l"):
        label="p_{T}^{Z}"
        unit="GeV"
    elif (obsName=="massZ1"):
        label = "m(Z_{1})"
        unit = "GeV"
    elif (obsName=="massZ2"):
        label = "m(Z_{2})"
        unit = "GeV"
    elif (obsName=="nJets" or obsName.startswith("njets")):
        label = "N(jets)"
        unit = ""
    elif (obsName=="rapidity4l"):
        label = "|y^{Z}|"
        unit = ""
    elif (obsName=="cosThetaStar"):
        label = "|cos#theta*|"
        unit = ""
    elif (obsName=="cosTheta1"):
        label = "|cos#theta_{1}|"
        unit = ""
    elif (obsName=="cosTheta2"):
        label = "|cos#theta_{2}|"
        unit = ""
    elif (obsName=="Phi"):
        label = "|#Phi|"
        unit = ""
    elif (obsName=="Phi1"):
        label = "|#Phi_{1}|"
        unit = ""
    elif (obsName=="mass4l"):
        label = "inclusive"
        unit = ""
    else:
        label = obsName
        unit = ""
    
    c = TCanvas("c",obsName, 1000, 800)
    if(opt.SETLOG): c.SetLogy()
    c.SetBottomMargin(0.15)
    c.SetRightMargin(0.06)
    c.SetLeftMargin(0.2)
   
    if (obsName=="mass4l"):
        dummy = TH1D("dummy","dummy", 4, 0, 4)
        for i in range(1,5):
            dummy.SetBinContent(i,2.5*max(a_SMZ4l))
        dummy.GetXaxis().SetBinLabel(1,'4l')
        dummy.GetXaxis().SetBinLabel(2,'2e2#mu')
        dummy.GetXaxis().SetBinLabel(3,'4#mu')
        dummy.GetXaxis().SetBinLabel(4,'4e')
    else: 
        dummy = TH1D("dummy","dummy", int(float(obs_bins[nBins-1])-float(obs_bins[0])), float(obs_bins[0]), float(obs_bins[nBins-1]))
        for i in range(int(float(obs_bins[nBins-1])-float(obs_bins[0]))):
            dummy.SetBinContent(i,2.5*max(a_SMZ4l))
    if (opt.SETLOG): dummy.SetMaximum(25.0*max(a_SMZ4l))
    else: dummy.SetMaximum(2.5*max(a_SMZ4l))
    if (opt.SETLOG): dummy.SetMinimum(min(0.1*min(a_SMZ4l),0.9*min(a_data)))
    else: dummy.SetMinimum(0.0)
    dummy.SetLineColor(0)
    dummy.SetMarkerColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    if (label=="inclusive"):
        dummy.GetXaxis().SetTitle("")
    elif (unit==""):
        dummy.GetXaxis().SetTitle(label)
    else:
        dummy.GetXaxis().SetTitle(label+" ["+unit+"]")
    dummy.GetXaxis().SetTitleOffset(1.1)
    if (label=="inclusive"):
        dummy.GetYaxis().SetTitle("#sigma_{fid.} [fb]")
    elif (unit==""):
        dummy.GetYaxis().SetTitle("d#sigma_{fid.}/d"+label+" [fb]")
    else:
        dummy.GetYaxis().SetTitle("d#sigma_{fid.}/d"+label+" [fb/"+unit+"]") 
    dummy.GetYaxis().SetTitleOffset(1.5)
    dummy.Draw("hist")
    g_SMZ4l.Draw("2same")
    g_data.Draw("psameZ")
    #g_data_allunc.Draw("psame")
    #g_data_allunc.Draw("psame[]")
    dummy.Draw("axissame")


    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
    latex2.SetTextSize(0.9*c.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.27, 0.85, "CMS")
    latex2.SetTextSize(0.7*c.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.25, 0.8, "Preliminary")
    
    legend = TLegend(.5,.68,.9,.88)
    if (opt.useAsimov):
        legend.AddEntry(g_data,"Asimov Data (stat. #oplus sys. unc.)","ep")
    else:
        legend.AddEntry(g_data,"Data (stat. #oplus sys. unc.)","ep")
    legend . AddEntry(g_SMZ4l , "Z #rightarrow 4l (powheg)", "f") 
    
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()
    
    if (opt.SETLOG): set_log = '_logscale'
    else: set_log = ''
    c.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.pdf')
    c.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.png')
    c.SaveAs('plots_z4l/fidxs'+opt.resultTag+set_log+'.C')

   
    for chan in range(0,4):
        print '&$'+str(round(data[chan],3))+'^{+'+str(round(data_hi[chan],3))+'}_{-'+str(round(data_lo[chan],3))+'}$'

    for chan in range(0,4):
        print '&$'+str(round(SMZ4l[chan],3))+'^{+'+str(round(SMZ4l_hi[chan],3))+'}_{-'+str(round(SMZ4l_lo[chan],3))+'}$'

    print " "

 
obs_bins = opt.OBSBINS.split("|")
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins.pop()
obs_bins.pop(0)

if float(obs_bins[len(obs_bins)-1])>200.0:
    obs_bins[len(obs_bins)-1]='200.0'
if (opt.OBSNAME=="nJets" or opt.OBSNAME.startswith("njets")):
    obs_bins[len(obs_bins)-1]='4'

plotXS(opt.OBSNAME, obs_bins)  

