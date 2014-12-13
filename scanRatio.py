import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames import *

from ROOT import *
from tdrStyle import *

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
    #parser.add_option('',   '--resultFile',dest='resultFile',type='string',default='resultFile.root', help='result root file from the combine fit.')
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
    
setTDRStyle()

### Define function for processing of os command
def processCmd(cmd, quiet = 0):
    output = '\n'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        print line, 
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))
    return output

def scanRatio():
    # Load some libraries                                 
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")
    
    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

#    HistsRatio = {}
    #poi = 'RatioSigmaHoZ'
    for poi in ['RatioSigmaHoZ','RatioSigmaHoZ4e','RatioSigmaHoZ4mu', 'RatioSigmaHoZ2e2mu', 'SigmaH', 'SigmaH4e', 'SigmaH4mu','SigmaH2e2mu']:
        if (poi=='RatioSigmaHoZ' or poi=='SigmaH'): 
           tag = '_Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1_'+poi
        else: 
           tag = '_Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v2_'+poi 
        
        cmd =  'combine -n '+tag
        cmd += ' -M MultiDimFit -m 125.0 --saveWorkspace  -D data_obs '
        cmd += ' --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124 '
        cmd += ' -P '+poi+' --setPhysicsModelParameterRanges '+poi+'=0.0,3.0 '
        cmd += ' --floatOtherPOIs=1 --algo=grid --points=100 '
        print cmd
        output=processCmd(cmd)       

#        rootfile = TFile('higgsCombine'+tag+'.MultiDimFit.mH125.root')
#        HistsRatio[poi] = TH1D("
        

  


    #print cmd
    #output=processCmd(cmd)

#    plotFile = opt.resultFile.replace(".root","")             
#    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".pdf")
#    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".png")
#    c.SaveAs("plots_ratio/Result_"+plotFile+"_"+fstate+".C")




scanRatio()

