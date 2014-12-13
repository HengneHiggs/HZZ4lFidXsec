
#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.10.18
#-----------------------------------------------
import sys, os, pwd, commands
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *
import json
from ROOT import *

# load XS-specific modules
sys.path.append('./datacardInputs')

from sample_shortnames_bkg import *
from createXSworkspace import createXSworkspace
#from createXSworkspaceZ4l import *
from createXSworkspaceZ4lNew2 import *
from createXSworkspaceRatio import *
from higgs_xsbr import *

### Define function for parsing options
def parseOptions():
    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--modelName',dest='MODELNAME',type='string',default='all', help='Name of the Higgs production or spin-parity model, default is "SM", supported: "SM", "ggH", "VBF", "WH", "ZH", "ttH", "exotic","all", "SMZ4l"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    # action options - "redo"
    parser.add_option('',   '--redoEff',       action='store_true', dest='redoEff',      default=False, help='Redo the eff. factors, default is False')
    parser.add_option('',   '--redoTemplates', action='store_true', dest='redoTemplates',default=False, help='Redo the bkg shapes and fractions, default is False')
    # action options - "only"
    parser.add_option('',   '--effOnly',       action='store_true', dest='effOnly',       default=False, help='Extract the eff. factors only, default is False')
    parser.add_option('',   '--templatesOnly', action='store_true', dest='templatesOnly', default=False, help='Prepare the bkg shapes and fractions only, default is False')
    parser.add_option('',   '--uncertOnly',    action='store_true', dest='uncertOnly',    default=False, help='Extract the uncertanties only, default is False')
    parser.add_option('',   '--resultsOnly',   action='store_true', dest='resultsOnly',   default=False, help='Run the measurement only, default is False')
    parser.add_option('',   '--finalplotsOnly',action='store_true', dest='finalplotsOnly',default=False, help='Make the final plots only, default is False')
    parser.add_option('',   '--useAsimov',action='store_true', dest='useAsimov',default=False, help='Use Asimov Data set, default is False')
    parser.add_option('',   '--doRatio',action='store_true', dest='doRatio',default=False, help='Do H4l/Z4l ratio, default is False')
    parser.add_option('',   '--floatPOIs',action='store_true', dest='floatPOIs',default=False, help='Float other POIs')
    parser.add_option('',   '--fixMH',action='store_true', dest='fixMH',default=False, help='Fix MH')
    parser.add_option('',   '--fixMZ',action='store_true', dest='fixMZ',default=False, help='Fix MZ')
    parser.add_option('',   '--fixDeltaMHmZ',action='store_true', dest='fixDeltaMHmZ',default=False, help='Fix DeltaMHmZ')
        
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    # prepare the global flag if all the step should be run
    runAllSteps = not(opt.effOnly or opt.templatesOnly or opt.uncertOnly or opt.resultsOnly or opt.finalplotsOnly)

    if (opt.OBSBINS=='' and opt.OBSNAME!='inclusive'):
        parser.error('Bin boundaries not specified for differential measurement. Exiting...')
        sys.exit()

    #dirToExist = ['templates','datacardInputs','125.6','xs_125.6', 'xs_91.1876']
    #for dir in dirToExist:
    #    if not os.path.isdir(os.getcwd()+'/'+dir+'/'):
    #        parser.error(os.getcwd()+'/'+dir+'/ is not a directory. Exiting...')
    #        sys.exit()

### Define function for processing of os command
def processCmd(cmd, quiet = 0):
    #print cmd
    #status, output = commands.getstatusoutput(cmd)
    #output = subprocess.check_output(cmd, shell=True)

    output = '\n'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        print line, 
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))
    
    #if (status !=0 and not quiet):
    #    print 'Error in processing command:\n   ['+cmd+']'
    #    print 'Output:\n   ['+output+'] \n'
    #if (not quiet):
    #    print 'Output:\n   ['+output+'] \n'
    return output

### Extract the all efficiency factors (inclusive/differential, all bins, all final states)
def extractFiducialEfficiencies(obsName, observableBins, modelName):

    #from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if (not opt.redoEff):
        print '[Skipping eff. and out.factors for '+str(obsName)+']'
        return

    print '[Extracting eff. and out.factors]'
    # determine the ntuples/scipts to use from the path to ntuples [must contain only "sperka" or only "tchen"]
    # need a better way to handle this...
    if ((opt.SOURCEDIR.find("dsperka")!=-1) and (opt.SOURCEDIR.find("tcheng")==-1)):
        #cmd = 'python efficiencyFactors_dsperka.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --modelName='+modelName
        cmd = 'python efficiencyFactors_dsperka.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --modelName='+modelName+' --doPlots --doFit'
        print cmd
        output = processCmd(cmd)
        #print output
        cmd = 'python plot2dsigeffs.py -l -q -b --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'"'
        output = processCmd(cmd)
    elif ((opt.SOURCEDIR.find("dsperka")==-1) and (opt.SOURCEDIR.find("tcheng")!=-1)):
        cmd = 'root -l -q -b "efficiencyFactors_tcheng.C"' # need to pass parameters on opt.SOURCEDIR, obsName, observableBins, modelName...
        #processCmd(cmd)
    else:
        print 'Ambigious type of ntuples/scipts to use ["dsperka" or "tcheng"]. Exiting...'
        sys.exit()

### Extract the all efficiency factors (inclusive/differential, all bins, all final states), Z4l
def extractFiducialEfficienciesZ4l(obsName, observableBins, modelName):

    #from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if (not opt.redoEff):
        print '[Skipping eff. and out.factors for '+str(obsName)+']'
        return

    print '[Extracting eff. and out.factors]'
    if (opt.OBSNAME=="mass4l"):
        cmd = 'python efficiencyFactors_z4l.py --dir='+opt.SOURCEDIR+' -l -q -b --modelName='+modelName+' --doPlots '
        print cmd
        output = processCmd(cmd)
    else:
        cmd = 'python efficiencyFactors_z4l_diff.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --modelName='+modelName
        print cmd
        output = processCmd(cmd)
        #cmd = 'python plot2dsigeffsZ4l.py -l -q -b --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'"' 
        #print cmd
        #output = processCmd(cmd)



### Extract the all efficiency factors (inclusive/differential, all bins, all final states), Ratio H/Z
def extractFiducialEfficienciesRatio(obsName, observableBins, modelName):

    #from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if (not opt.redoEff):
        print '[Skipping eff. and out.factors for '+str(obsName)+']'
        return

    print '[Extracting eff. and out.factors for Z4l]'
    cmd = 'python efficiencyFactors_ratio.py --dir='+opt.SOURCEDIR+' -l -q -b --doPlots '
    print cmd
    output = processCmd(cmd)

    #print '[Extracting eff. and out.factors for H4l]'
    #cmd = 'python efficiencyFactors_ratio_h4l.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --modelName=SM --doPlots'
    #print cmd
    #output = processCmd(cmd)

    #print '[Combining ggH, VBF, WH, ZH, ttH, eff. and out.factors to SM ]'
    #cmd = 'python addConstrainedModel_ratio_h4l.py -l -q -b --obsName="'+opt.OBSNAME+'" --obsBins="'+opt.OBSBINS+'"'
    #print cmd
    #output = processCmd(cmd)


### Extract the templates for given obs, for all bins and final states (differential)
def extractBackgroundTemplatesAndFractions(obsName, observableBins):
    global opt

    fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}
    #if exists, from inputs_bkg_{obsName} import observableBins, fractionsBackground, jesLambdaBkgUp, jesLambdaBkgDn
    if os.path.isfile('datacardInputs/inputs_bkg_'+obsName+'.py'):
        _temp = __import__('inputs_bkg_'+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            print '[Fractions already exist for the given binning. Skipping templates/shapes... ]'
            return
        if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
            fractionBkg = _temp.fractionsBackground
            lambdajesupBkg = _temp.lambdajesupBkg
            lambdajesdnBkg = _temp.lambdajesdnBkg

    print '[Preparing bkg shapes and fractions, for bins with boundaries ', observableBins
    # save/create/prepare directories and compile templates script
    currentDir = os.getcwd(); os.chdir('./templates/')
    #    cmd = 'rm main_fiducialXSTemplates; make'; processCmd(cmd)
    cmd = 'mkdir -p templatesXS/DTreeXS_'+opt.OBSNAME+'/8TeV/'; processCmd(cmd,1)

    # extract bkg templates and bin fractions
    bkg_sample_tags = ['ZZTo2e2mu_powheg', 'ZZTo4e_powheg', 'ZZTo4mu_powheg','ggZZ_2e2mu_MCFM67', 'ggZZ_4e_MCFM67', 'ggZZ_4mu_MCFM67', 'ZX4l_CR']
    bkg_samples_shorttags = {'ZZTo2e2mu_powheg':'qqZZ', 'ZZTo4e_powheg':'qqZZ', 'ZZTo4mu_powheg':'qqZZ', 'ggZZ_2e2mu_MCFM67':'ggZZ', 'ggZZ_4e_MCFM67':'ggZZ', 'ggZZ_4mu_MCFM67':'ggZZ', 'ZX4l_CR':'ZJetsCR'}
    bkg_samples_fStates = {'ZZTo2e2mu_powheg':'2e2mu', 'ZZTo4e_powheg':'4e', 'ZZTo4mu_powheg':'4mu','ggZZ_2e2mu_MCFM67':'2e2mu', 'ggZZ_4e_MCFM67':'4e', 'ggZZ_4mu_MCFM67':'4mu', 'ZX4l_CR':'AllChans'}
    for sample_tag in bkg_sample_tags:
        tmpObsName = obsName
        tmpSrcDir = opt.SOURCEDIR
        if (sample_tag=='ZX4l_CR'):
            tmpSrcDir = '/scratch/osg/predragm/Histogramming_8TeV/rootFiles_dsperka_XS/'
        cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 8TeV templatesXS DTreeXS'
        print cmd
        output = processCmd(cmd)
        #print output
        tmp_fracs = output.split("[Bin fraction: ")
        for obsBin in range(0,len(observableBins)-1):
            fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            tmpFrac = float(tmp_fracs[obsBin+1].split("][end fraction]")[0])
            if not math.isnan(tmpFrac):
                fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac
            if (obsName=='njets_reco_pt30_eta4p7' and tmpFrac!=0 and not math.isnan(tmpFrac)):
                tmpFrac_up =float(tmp_fracs[obsBin+1].split("Bin fraction (JESup): ")[1].split("]")[0])
                tmpFrac_dn =float(tmp_fracs[obsBin+1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                if not math.isnan(tmpFrac_up):
                    lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_up/tmpFrac - 1
                if not math.isnan(tmpFrac_dn):
                    lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_dn/tmpFrac - 1

    os.chdir(currentDir)
    with open('datacardInputs/inputs_bkg_'+obsName+'.py', 'w') as f:
        f.write('observableBins = '     +json.dumps(observableBins)+';\n')
        f.write('fractionsBackground = '+json.dumps(fractionBkg)   +';\n')
        f.write('lambdajesupBkg = '     +json.dumps(lambdajesupBkg)+';\n')
        f.write('lambdajesdnBkg = '     +json.dumps(lambdajesdnBkg)+';\n')


### Extract the templates for given obs, for all bins and final states (differential), Z4l
def extractBackgroundTemplatesAndFractionsZ4l(obsName, observableBins):
    global opt

    fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}
    #if exists, from inputs_bkg_{obsName} import observableBins, fractionsBackground, jesLambdaBkgUp, jesLambdaBkgDn
    if os.path.isfile('datacardInputs/inputs_bkg_z4l_'+obsName+'.py'):
        _temp = __import__('inputs_bkg_z4l_'+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            print '[Fractions already exist for the given binning. Skipping templates/shapes... ]'
            return
        if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
            fractionBkg = _temp.fractionsBackground
            lambdajesupBkg = _temp.lambdajesupBkg
            lambdajesdnBkg = _temp.lambdajesdnBkg

    print '[Preparing bkg shapes and fractions, for bins with boundaries ', observableBins
    # save/create/prepare directories and compile templates script
    currentDir = os.getcwd(); os.chdir('./templates/')
    #    cmd = 'rm main_fiducialXSTemplates; make'; processCmd(cmd)
    cmd = 'mkdir -p templatesXSZ4l/DTreeXS_'+opt.OBSNAME+'/8TeV/'; processCmd(cmd,1)

    # extract bkg templates and bin fractions
    sZZname2e2mu = 'ZZTo2e2mu_powheg_tchan'; sZZname4mu = 'ZZTo4mu_powheg_tchan'; sZZname4e = 'ZZTo4e_powheg_tchan'
    bkg_sample_tags = [sZZname2e2mu, sZZname4e, sZZname4mu, 'ggZZ_2e2mu', 'ggZZ_4e', 'ggZZ_4mu', 'ZX4l_CR']
    bkg_samples_shorttags = {sZZname2e2mu:'qqZZ', sZZname4e:'qqZZ', sZZname4mu:'qqZZ', 'ggZZ_2e2mu':'ggZZ', 'ggZZ_4e':'ggZZ', 'ggZZ_4mu':'ggZZ', 'ZX4l_CR':'ZJetsCR'}
    bkg_samples_fStates = {sZZname2e2mu:'2e2mu', sZZname4e:'4e', sZZname4mu:'4mu', 'ggZZ_2e2mu':'2e2mu', 'ggZZ_4e':'4e', 'ggZZ_4mu':'4mu', 'ZX4l_CR':'AllChans'}
    for sample_tag in bkg_sample_tags:
        tmpObsName = obsName
        tmpSrcDir = opt.SOURCEDIR
        if (sample_tag=='ZX4l_CR'):
            tmpSrcDir = '/scratch/osg/predragm/Histogramming_8TeV/rootFiles_dsperka_XS/'
        cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 8TeV templatesXSZ4l DTreeXS true false'
        #cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' '+observableBins[obsBin]+' '+observableBins[obsBin+1]+' 8TeV templatesXSRatio DTreeXS false true'
        print cmd
        output = processCmd(cmd)
        #print output
        tmp_fracs = output.split("[Bin fraction: ")
        for obsBin in range(0,len(observableBins)-1):
            fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            tmpFrac = float(tmp_fracs[obsBin+1].split("][end fraction]")[0])
            if not math.isnan(tmpFrac):
                fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac
            if (obsName=='njets_reco_pt30_eta4p7' and tmpFrac!=0 and not math.isnan(tmpFrac)):
                tmpFrac_up =float(tmp_fracs[obsBin+1].split("Bin fraction (JESup): ")[1].split("]")[0])
                tmpFrac_dn =float(tmp_fracs[obsBin+1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                if not math.isnan(tmpFrac_up):
                    lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_up/tmpFrac - 1
                if not math.isnan(tmpFrac_dn):
                    lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_dn/tmpFrac - 1

    os.chdir(currentDir)
    with open('datacardInputs/inputs_bkg_z4l_'+obsName+'.py', 'w') as f:
        f.write('observableBins = '     +json.dumps(observableBins)+';\n')
        f.write('fractionsBackground = '+json.dumps(fractionBkg)   +';\n')
        f.write('lambdajesupBkg = '     +json.dumps(lambdajesupBkg)+';\n')
        f.write('lambdajesdnBkg = '     +json.dumps(lambdajesdnBkg)+';\n')


### Extract the templates for given obs, for all bins and final states (differential), inclusive Ratio H/Z
def extractBackgroundTemplatesAndFractionsRatio(obsName, observableBins):
    global opt

    fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}
    #if exists, from inputs_bkg_{obsName} import observableBins, fractionsBackground, jesLambdaBkgUp, jesLambdaBkgDn
    if os.path.isfile('datacardInputs/inputs_bkg_ratio_'+obsName+'.py'):
        _temp = __import__('inputs_bkg_ratio_'+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            print '[Fractions already exist for the given binning. Skipping templates/shapes... ]'
            return
        if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
            fractionBkg = _temp.fractionsBackground
            lambdajesupBkg = _temp.lambdajesupBkg
            lambdajesdnBkg = _temp.lambdajesdnBkg

    print '[Preparing bkg shapes and fractions, for bins with boundaries ', observableBins
    # save/create/prepare directories and compile templates script
    currentDir = os.getcwd(); os.chdir('./templates/')
    #    cmd = 'rm main_fiducialXSTemplates; make'; processCmd(cmd)
    cmd = 'mkdir -p templatesXSRatio/DTreeXS_'+opt.OBSNAME+'/8TeV/'; 
    processCmd(cmd)

    # extract bkg templates and bin fractions
    sZZname2e2mu = 'ZZTo2e2mu_powheg_tchan'; sZZname4mu = 'ZZTo4mu_powheg_tchan'; sZZname4e = 'ZZTo4e_powheg_tchan'
    bkg_sample_tags = [sZZname2e2mu, sZZname4e, sZZname4mu, 'ggZZ_2e2mu', 'ggZZ_4e', 'ggZZ_4mu', 'ZX4l_CR']
    bkg_samples_shorttags = {sZZname2e2mu:'qqZZ', sZZname4e:'qqZZ', sZZname4mu:'qqZZ', 'ggZZ_2e2mu':'ggZZ', 'ggZZ_4e':'ggZZ', 'ggZZ_4mu':'ggZZ', 'ZX4l_CR':'ZJetsCR'}
    bkg_samples_fStates = {sZZname2e2mu:'2e2mu', sZZname4e:'4e', sZZname4mu:'4mu', 'ggZZ_2e2mu':'2e2mu', 'ggZZ_4e':'4e', 'ggZZ_4mu':'4mu', 'ZX4l_CR':'AllChans'}
    for sample_tag in bkg_sample_tags:
        tmpObsName = obsName
        tmpSrcDir = opt.SOURCEDIR
        if (sample_tag=='ZX4l_CR'):
            tmpSrcDir = '/scratch/osg/predragm/Histogramming_8TeV/rootFiles_dsperka_XS/'
        cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 8TeV templatesXSRatio DTreeXS false true'
        #cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' '+observableBins[obsBin]+' '+observableBins[obsBin+1]+' 8TeV templatesXSRatio DTreeXS false true'
        print cmd
        output = processCmd(cmd)
        #print output
        tmp_fracs = output.split("[Bin fraction: ")
        for obsBin in range(0,len(observableBins)-1):
            fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            tmpFrac = float(tmp_fracs[obsBin+1].split("][end fraction]")[0])
            if not math.isnan(tmpFrac):
                fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac
            if (obsName=='njets_reco_pt30_eta4p7' and tmpFrac!=0 and not math.isnan(tmpFrac)):
                tmpFrac_up =float(tmp_fracs[obsBin+1].split("Bin fraction (JESup): ")[1].split("]")[0])
                tmpFrac_dn =float(tmp_fracs[obsBin+1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                if not math.isnan(tmpFrac_up):
                    lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_up/tmpFrac - 1
                if not math.isnan(tmpFrac_dn):
                    lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_dn/tmpFrac - 1

    os.chdir(currentDir)
    with open('datacardInputs/inputs_bkg_ratio_'+obsName+'.py', 'w') as f:
        f.write('observableBins = '     +json.dumps(observableBins)+';\n')
        f.write('fractionsBackground = '+json.dumps(fractionBkg)   +';\n')
        f.write('lambdajesupBkg = '     +json.dumps(lambdajesupBkg)+';\n')
        f.write('lambdajesdnBkg = '     +json.dumps(lambdajesdnBkg)+';\n')


### Extract the XS-specific uncertainties for given obs and bin, for all final states (differential)
def extractUncertainties(obsName, observableBinDn, observableBinUp):
    print '[Extracting uncertainties  -  range ('+observableBinDn+', '+observableBinUp+')]'
    cmd = 'some command...with some parameters...'
    #processCmd(cmd)

### Produce datacards for given obs and bin, for all final states
def produceDatacards(obsName, observableBins, modelName, physicalModel):
 
    print '[Producing workspace/datacards for obsName '+obsName+', bins '+str(observableBins)+']'
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        if (not obsName=="inclusive"):
            for obsBin in range(nBins-1):
                # first bool = cfactor second bool = add fake H
                ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel)
                os.system("cp xs_125.6/hzz4l_"+fState+"S_8TeV_xs_bin"+str(obsBin)+".txt xs_125.6/hzz4l_"+fState+"S_8TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' xs_125.6/hzz4l_"+fState+"S_8TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                os.system("sed -i 's~_xs.Databin"+str(obsBin)+"~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+"~g' xs_125.6/hzz4l_"+fState+"S_8TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
        else:
            ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel)
            os.system("cp xs_125.6/hzz4l_"+fState+"S_8TeV_xs_bin_inclusive_bin0.txt xs_125.6/hzz4l_"+fState+"S_8TeV_xs_inclusive_bin0_"+physicalModel+".txt")
            os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' xs_125.6/hzz4l_"+fState+"S_8TeV_xs_inclusive_bin0_"+physicalModel+".txt")
            os.system("sed -i 's~_xs.Databin0~_xs_"+modelName+"_inclusive_bin0_"+physicalModel+".Databin0~g' xs_125.6/hzz4l_"+fState+"S_8TeV_xs_inclusive_bin0_"+physicalModel+".txt")   


### Produce datacards for given obs and bin, for all final states, for Z4l
def produceDatacardsZ4l(obsName, observableBins, modelName, physicalModel):

    print '[Producing workspace/datacards for obsName '+obsName+', bins '+str(observableBins)+']'
    fStates = ['4e','4mu','2e2mu']
    nBins = len(observableBins)
    for fState in fStates:
        if (not obsName=="mass4l"):
            for obsBin in range(nBins-1):
                ndata = createXSworkspaceZ4lDifferential(obsName,fState, nBins, obsBin, observableBins, modelName, physicalModel)
                cardfile1 = "xs_z4l/hzz4l_"+fState+"S_8TeV_xs_Z4l_bin0.txt"
                cardfile2 = "xs_z4l/hzz4l_"+fState+"S_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                cmd = "cp "+cardfile1+" "+cardfile2
                print cmd
                os.system(cmd)
                cmd = "sed -i 's~bin0~bin"+str(obsBin)+"~g' "+cardfile2
                print cmd
                os.system(cmd)
                cmd = "sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' "+cardfile2
                print cmd
                os.system(cmd)
                cmd = "sed -i 's~_xs_Z4l_bin"+str(obsBin)+".input.root~_xs_Z4l_"+modelName+"_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".input.root~g' "+cardfile2
                print cmd
                os.system(cmd)
                if ("jets" in obsName):
                    cmd = "sed -i 's~\#JES param~JES param~g' "+cardfile2
                    print cmd
                    os.system(cmd)
        else:
            ndata = createXSworkspaceZ4lInclusive(obsName,fState, modelName, physicalModel)


### Produce datacards for given obs and bin, for all final states, for Ratio Inclusive
def produceDatacardsRatioInclusive(obsName, modelName, physicalModel):

    print '[Producing workspace/datacards for obsName '+obsName+', modelName'+str(modelName)+']'
    fStates = ['2e2mu','4mu','4e']
    for fState in fStates:
        ndata = createXSworkspaceRatioInclusive(obsName,fState, modelName,physicalModel)

### Create the asimov dataset and return fit results
def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel):
    print '[Producing/merging workspaces and datacards for obsName '+obsName+' using '+modelName+']'

    # Run combineCards and text2workspace
    currentDir = os.getcwd(); os.chdir('./xs_125.6/')
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        if (nBins>1):
            cmd = 'combineCards.py '
            for obsBin in range(nBins-1):
                cmd = cmd + 'hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
            cmd = cmd + '> hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt' 
            print cmd
            processCmd(cmd,1)
        else:
            cmd = 'cp hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin0_'+physicalModel+'.txt hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
            
    # combine 3 final states
    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_4eS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_2e2muS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt > hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
    print cmd 
    processCmd(cmd,1)

    # text-to-workspace
    if (physicalModel=="v2"):
        cmd = 'text2workspace.py hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 -o hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        print cmd
        processCmd(cmd)

    cmd = 'cp hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root ../'+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    print cmd 
    processCmd(cmd,1)
    
    os.chdir(currentDir)
        
    # import acc factors
    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc
    
    # Run the Combine
    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName+' -M MultiDimFit  '+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root -m 125.6 --setPhysicsModelParameters '
        for fState in fStates:
            nBins = len(observableBins)
            for obsBin in range(nBins-1):
                fidxs = 0
                fidxs += higgs_xs['ggH_125.6']*higgs4l_br['125.6_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
                fidxs += higgs_xs['VBF_125.6']*higgs4l_br['125.6_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
                fidxs += higgs_xs['WH_125.6']*higgs4l_br['125.6_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
                fidxs += higgs_xs['ZH_125.6']*higgs4l_br['125.6_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
                fidxs += higgs_xs['ttH_125.6']*higgs4l_br['125.6_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
                cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs)+','
        cmd = cmd+'MH=125.6 -t -1 --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace --saveToys'
        #cmd = cmd+'MH=125.6 -t -1 --algo=singles --cl=0.68 --saveWorkspace --saveToys'
        print cmd
        output=processCmd(cmd)

    # parse the results for all the bins and the given final state
    tmp_resultsXS = {}
    for fState in fStates:
        rTags = {'0':'r'+fState+'Bin0 :','1':'r'+fState+'Bin1 :','2':'r'+fState+'Bin2 :','3':'r'+fState+'Bin3 :'}
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag] = parseXSResults(output,rTags[binTag])

    cmd = 'mv higgsCombine'+obsName+'.MultiDimFit.mH125.6.123456.root '+modelName+'_all_'+obsName+'_8TeV_Asimov_'+physicalModel+'.root' 
    processCmd(cmd,1) 

    # merge the results for 3 final states, for the given bins
    for obsBin in range(len(observableBins)-1):
        binTag = str(obsBin)
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        tmp_central = 0.0
        tmp_uncerDn = 0.0
        tmp_uncerUp = 0.0
        for fState in fStates:
            tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['central']
            tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerDn']**2
            tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerUp']**2
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_central))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    return resultsXS

# parse the fit results from the MultiDim fit output "resultLog", for the bin and final state designated by "rTag"
def parseXSResults(resultLog, rTag):
    try:
        fXS_c = float(resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" ")[0])
        fXS_d = float('-'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[0])
        fXS_u = float('+'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[1])
        fXS = {'central':fXS_c, 'uncerDn':fXS_d, 'uncerUp':fXS_u}
        return fXS
    except IndexError:
        print "Parsing Failed!!! Inserting dummy values!!! check log!!!"
        fXS = {'central':-1.0, 'uncerDn':0.0, 'uncerUp':0.0}
        return fXS

### Extract the results and do plotting
def extractResults(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    currentDir = os.getcwd(); os.chdir('./xs_125.6/')
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        cmd = 'combineCards.py '
        for bin in range(nBins-1):
            cmd = cmd+'hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin'+str(bin)+'_'+physicalModel+'.txt '
        cmd = cmd + '> hzz4l_'+fState+'S_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
        print cmd
        processCmd(cmd,1)

    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_4eS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_2e2muS_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt > hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
    print cmd
    processCmd(cmd,1)

    if (physicalModel=="v1"):
        cmd = 'text2workspace.py hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducial --PO higgsMassRange=115,135 -o hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        print cmd
        processCmd(cmd)

    cmd = 'cp hzz4l_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root ../'+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    print cmd
    processCmd(cmd,1)

    os.chdir(currentDir)

    cmd = 'root -l -b -q "addToyDataset.C(\\"'+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'.root\\",\\"'+asimovModelName+'_all_'+obsName+'_8TeV_Asimov_'+asimovPhysicalModel+'.root\\",\\"toy_asimov\\",\\"'+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root\\")"'
    print cmd
    processCmd(cmd)

    # Run the Combine
    cmd =  'combine -M MultiDimFit '+modelName+'_all_8TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m 125.6 -D toy_asimov --algo=singles --cl=0.68 --robustFit=1'
    if (physicalModel=="v1"):
        # you can comment this out if you want the uncertainties on frac4e, frac4mu
        for bin in range(nBins-1):
            cmd = cmd + ' -P rBin'+str(bin)
        cmd = cmd + ' --floatOtherPOIs=1'
        print cmd
        output=processCmd(cmd)

    # parse the results for all the bins
    for obsBin in range(len(observableBins)-1):
        resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'rBin'+str(obsBin)+' :')

    return resultsXS


### Extract the results and do plotting, Z4l
def extractResultsZ4l(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS, doUncertainty):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    currentDir = os.getcwd(); os.chdir('./xs_z4l/')
    fStates = ['4e','4mu','2e2mu']
    nBins = len(observableBins)
    for fState in fStates:
        cmd = 'combineCards.py '
        for bin in range(nBins-1):
            cardfile = "hzz4l_"+fState+"S_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin"+str(bin)+"_"+physicalModel+".txt"
            cmd += ' '+cardfile+' '
        cardfile = "hzz4l_"+fState+"S_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin_"+physicalModel+".txt"
        cmd += '> '+cardfile 
        print cmd
        processCmd(cmd)

    cmd = 'combineCards.py '
    for fState in fStates:
        cardfile = "hzz4l_"+fState+"S_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin_"+physicalModel+".txt"
        cmd += ' '+cardfile+' '
    cardfile = "hzz4l_all_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin_"+physicalModel+".txt"
    cmd += '> '+cardfile      
    print cmd 
    processCmd(cmd)

    wsfile = "hzz4l_all_8TeV_xs_Z4l_"+modelName+"_"+obsName+"_bin_"+physicalModel+".root"
    if (physicalModel=="v3"):
        cmd = 'text2workspace.py '+cardfile+' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducialV3 --PO higgsMassRange=89,93 -o '+wsfile
        print cmd
        processCmd(cmd)

    nameTag = '_Z4l_'+modelName+'_'+obsName
    if ( opt.useAsimov ):
        nameTag += '_Asimov' 
    if ( opt.floatPOIs ): 
        nameTag += '_floatPOIs'
    if ( opt.fixMZ):
        nameTag += '_fixMZ'
    nameTag = nameTag+'_all_8TeV_xs'+'_'+physicalModel

    cmd = 'cp '+wsfile+' ../Combine'+nameTag+'.root'
    print cmd
    processCmd(cmd)

    os.chdir(currentDir)

    wsfile = 'Combine'+nameTag+'.root'

    # Run the Combine
    cmd = 'combine -n '+nameTag+' -M MultiDimFit '+wsfile+' -m 91.1876 '
    if (doUncertainty):
        cmd += ' --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    else:
        cmd += ' --saveWorkspace '
    if ( opt.useAsimov ):
        cmd += ' -t -1 --saveToys --setPhysicsModelParameters MH=91.1876'
    else:
        cmd += ' -D data_obs --setPhysicsModelParameters MH=91.1876 '

    if (opt.fixMZ):
        cmd += ' --freezeNuisances MH '

    if (doUncertainty):
        if (physicalModel=="v3"):
            for bin in range(nBins-1):
                cmd += ' -P SigmaBin'+str(bin)
        if ( opt.floatPOIs ):
            cmd += ' --floatOtherPOIs=1'

    print cmd
    output=processCmd(cmd)

    # parse the results for all the bins
    for obsBin in range(len(observableBins)-1):
        resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')

    tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH91.1876.root'
    if(opt.useAsimov): tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH91.1876.123456.root'
    if (doUncertainty):
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result.root'
    else:
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result_plot.root'

    print cmd
    output=processCmd(cmd)
        


    return resultsXS


### Extract the results and do plotting, Ratio, Inclusive
def extractResultsRatioInclusive(obsName, modelName, physicalModel, resultsXS, doUncertainty):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    currentDir = os.getcwd(); os.chdir('./xs_ratio/')

    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_Ratio.txt hzz4l_4eS_8TeV_xs_Ratio.txt  hzz4l_2e2muS_8TeV_xs_Ratio.txt > hzz4l_all_8TeV_xs_Ratio_'+modelName+'_'+physicalModel+'.txt '
    print cmd
    processCmd(cmd)

    #os.system("sed -i 's~_Ratio.input.root~_Ratio_"+modelName+"_"+physicalModel+".input.root~g' hzz4l_all_8TeV_xs_Ratio_"+modelName+"_"+physicalModel+".txt")
    cmd = "sed -i 's~_Ratio.input.root~_Ratio_"+modelName+"_"+physicalModel+".input.root~g' hzz4l_all_8TeV_xs_Ratio_"+modelName+"_"+physicalModel+".txt"
    print cmd
    processCmd(cmd)


    cmd = 'text2workspace.py hzz4l_all_8TeV_xs_Ratio_'+modelName+'_'+physicalModel+'.txt '
    if (physicalModel=='v1'):
        cmd += ' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:h4lZ4lInclusiveFiducialRatio '
    else:
        cmd += ' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:h4lZ4lInclusiveFiducialRatioV2 '
    if (opt.fixMH): 
        cmd += ' --PO defaultMH=125.0 '
        cmd += ' --PO fixMH '
    else: 
        cmd += ' --PO MHRange=115,135 '
    if (opt.fixDeltaMHmZ):
        cmd += ' --PO defaultDeltaMHmZ=33.8124 '
        cmd += ' --PO fixDeltaMHmZ '
    else:
        cmd += ' --PO DeltaMHmZRange=30,40 '
   
    cmd += ' -o hzz4l_all_8TeV_xs_Ratio_'+modelName+'_'+physicalModel+'.root'
    print cmd
    processCmd(cmd)

    nameTag = '_Ratio_'+modelName+'_'+obsName
    if ( opt.useAsimov ):
        nameTag += '_Asimov'
    if ( opt.floatPOIs ):
        nameTag += '_floatPOIs'
    if ( opt.fixMH):
        nameTag += '_fixMH'
    if ( opt.fixDeltaMHmZ):
        nameTag += '_fixDeltaMHmZ'
    nameTag = nameTag+'_all_8TeV_xs'+'_'+physicalModel


    cmd = 'cp hzz4l_all_8TeV_xs_Ratio_'+modelName+'_'+physicalModel+'.root ../Combine'+nameTag+'.root'
    print cmd
    processCmd(cmd)

    os.chdir(currentDir)

    # Run the Combine
    cmd = 'combine -n '+nameTag+' -M MultiDimFit Combine'+nameTag+'.root -m 125.0 '
    #cmd = cmd + ' -D data_obs --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    #cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    if (doUncertainty): 
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    else:
        cmd = cmd + ' --saveWorkspace '
    if ( opt.useAsimov ):
        #cmd = cmd + '-t -1 --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124'
        cmd += '-t -1 --setPhysicsModelParameters '
        if (not opt.fixMH):
            cmd += 'MH=125.0,'
        if (not opt.fixDeltaMHmZ):
            cmd += 'DeltaMHmZ=33.8124,'
        if (doUncertainty):
            cmd += 'MH=125.0,'
            cmd += 'DeltaMHmZ=33.8124,'
        # import h4l fid acc eff outinratio wrong frac etc
        _temp = __import__('inputs_sig_ratio_h4l_'+obsName, globals(), locals(), ['acc', 'eff','inc_wrongfrac','binfrac_wrongfrac','outinratio'], -1)
        acc = _temp.acc
        eff = _temp.eff
        outinratio = _temp.outinratio
        # import h4l xs br
        _temp = __import__('higgs_xsbr', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
        higgs_xs = _temp.higgs_xs
        higgs4l_br = _temp.higgs4l_br
        # import z4l fid acc eff outinratio
        _temp = __import__('inputs_sig_ratio_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
        acc_z = _temp.acc
        eff_z = _temp.eff
        outinratio_z = _temp.outinratio
        # import z4l xsbr
        _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
        z4l_xsbr = _temp.z4l_xsbr

        # fidxs for h4l
        fidxs = {}
        for fState in ['4e','4mu', '2e2mu']:
            fidxs[fState] = 0
            fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
            fidxs[fState] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin0_recobin0']
            fidxs[fState] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
            fidxs[fState] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
            fidxs[fState] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs['4l'] = fidxs['4e']+fidxs['4mu']+fidxs['2e2mu']

        # fidxs for z4l
        fidxs_z = {}
        for fState in ['4e','4mu', '2e2mu']:
            fidxs_z[fState] = 1000.0*z4l_xsbr['SMZ4l_'+fState]*acc_z['SMZ4l_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs_z['4l'] = fidxs_z['4e']+fidxs_z['4mu']+fidxs_z['2e2mu']

        # fidxs ratio h/z
        fidxs_ratio = {}
        for fState in ['4e','4mu', '2e2mu']:
            fidxs_ratio[fState] = fidxs[fState]/fidxs_z[fState]
        fidxs_ratio['4l'] = fidxs['4l']/fidxs_z['4l']

        #####
        if (physicalModel=='v1'):
            cmd = cmd+'SigmaH='+str(fidxs['4l'])+','
            cmd = cmd+'SigmaH4e='+str(fidxs['4e'])+','
            cmd = cmd+'SigmaH4mu='+str(fidxs['4mu'])+','
            cmd = cmd+'RatioSigmaHoZ='+str(fidxs_ratio['4l'])+','
            cmd = cmd+'RatioSigmaHoZ4e='+str(fidxs_ratio['4e'])+','
            cmd = cmd+'RatioSigmaHoZ4mu='+str(fidxs_ratio['4mu'])
        else:
            cmd = cmd+'SigmaH4e='+str(fidxs['4e'])+','
            cmd = cmd+'SigmaH4mu='+str(fidxs['4mu'])+','
            cmd = cmd+'SigmaH2e2mu='+str(fidxs['2e2mu'])+','
            cmd = cmd+'RatioSigmaHoZ4e='+str(fidxs_ratio['4e'])+','
            cmd = cmd+'RatioSigmaHoZ4mu='+str(fidxs_ratio['4mu'])+','
            cmd = cmd+'RatioSigmaHoZ2e2mu='+str(fidxs_ratio['2e2mu'])
    else:
        cmd = cmd + ' -D data_obs --setPhysicsModelParameters MH=125.0,DeltaMHmZ=33.8124 '

    # you can comment this out if you want the uncertainties
    if ( opt.floatPOIs ):
        cmd = cmd + ' --floatOtherPOIs=1 '
    else:
        cmd = cmd + ' --floatOtherPOIs=0 '
    if (doUncertainty):
        if (physicalModel=='v1'):
            cmd = cmd + '-P SigmaH '
            cmd = cmd + '-P RatioSigmaHoZ '
        else:
            cmd = cmd + '-P SigmaH4e '
            cmd = cmd + '-P SigmaH4mu '
            cmd = cmd + '-P SigmaH2e2mu '
            cmd = cmd + '-P RatioSigmaHoZ4e '
            cmd = cmd + '-P RatioSigmaHoZ4mu '
            cmd = cmd + '-P RatioSigmaHoZ2e2mu '
    
    #if(opt.useAsimov): cmd += ' --unbinned --saveToys '
    if(opt.useAsimov): cmd += ' --saveToys '

    print cmd
    output=processCmd(cmd)

    # parse the results for all the bins
    if (doUncertainty):
        if (physicalModel=='v1'):
            resultsXS[modelName+'_'+obsName+'_SigmaH'] = parseXSResults(output,'SigmaH :')
            resultsXS[modelName+'_'+obsName+'_RatioSigmaHoZ'] = parseXSResults(output,'RatioSigmaHoZ :')
        else:
            resultsXS[modelName+'_'+obsName+'_SigmaH4e'] = parseXSResults(output,'SigmaH4e :')
            resultsXS[modelName+'_'+obsName+'_SigmaH4mu'] = parseXSResults(output,'SigmaH4mu :')
            resultsXS[modelName+'_'+obsName+'_SigmaH2e2mu'] = parseXSResults(output,'SigmaH2e2mu :')
            resultsXS[modelName+'_'+obsName+'_RatioSigmaHoZ4e'] = parseXSResults(output,'RatioSigmaHoZ4e :')
            resultsXS[modelName+'_'+obsName+'_RatioSigmaHoZ4mu'] = parseXSResults(output,'RatioSigmaHoZ4mu :')
            resultsXS[modelName+'_'+obsName+'_RatioSigmaHoZ2e2mu'] = parseXSResults(output,'RatioSigmaHoZ2e2mu :')

    tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH125.root'
    if(opt.useAsimov): tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH125.123456.root'
    if (doUncertainty):
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result.root'
    else: 
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result_plot.root'
    output=processCmd(cmd)

    return resultsXS




### Extract the results and do plotting, Z4l, Inclusive
def extractResultsZ4lInclusive(obsName, modelName, physicalModel, resultsXS, doUncertainty):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    currentDir = os.getcwd(); os.chdir('./xs_z4l/')

    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_Z4l.txt hzz4l_4eS_8TeV_xs_Z4l.txt  hzz4l_2e2muS_8TeV_xs_Z4l.txt > hzz4l_all_8TeV_xs_Z4l_'+modelName+'_'+physicalModel+'.txt '
    print cmd
    processCmd(cmd)

    os.system("sed -i 's~_Z4l.input.root~_Z4l_"+modelName+"_"+physicalModel+".input.root~g' hzz4l_all_8TeV_xs_Z4l_"+modelName+"_"+physicalModel+".txt")

    cmd = 'text2workspace.py hzz4l_all_8TeV_xs_Z4l_'+modelName+'_'+physicalModel+'.txt '
    if (physicalModel=='v3'):
        cmd += ' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:inclusiveFiducialV3 '
    elif (physicalModel=='v1'):
        cmd += ' -P HiggsAnalysis.CombinedLimit.Z4L_Fiducial:Z4linclusiveFiducial '
    else:
        cmd += ' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:inclusiveFiducialV2 '
    if (opt.fixMZ):
        cmd += ' --PO mass=91.1876 '
    else:
        cmd += ' --PO higgsMassRange=80,100 '

    cmd += ' -o hzz4l_all_8TeV_xs_Z4l_'+modelName+'_'+physicalModel+'.root'
    print cmd
    processCmd(cmd)

    nameTag = '_Z4l_'+modelName+'_'+obsName
    if ( opt.useAsimov ):
        nameTag += '_Asimov'
    if ( opt.floatPOIs ):
        nameTag += '_floatPOIs'
    if ( opt.fixMZ):
        nameTag += '_fixMZ'
    nameTag = nameTag+'_all_8TeV_xs'+'_'+physicalModel


    cmd = 'cp hzz4l_all_8TeV_xs_Z4l_'+modelName+'_'+physicalModel+'.root ../Combine'+nameTag+'.root'
    print cmd
    processCmd(cmd)

    os.chdir(currentDir)

    # Run the Combine
    cmd = 'combine -n '+nameTag+' -M MultiDimFit Combine'+nameTag+'.root -m 91 '
    #cmd = cmd + ' -D data_obs --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    #cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    if (doUncertainty):
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace '
    else:
        cmd = cmd + ' --saveWorkspace '
    if (opt.fixMZ):
        cmd += ' --freezeNuisances MH '
    if ( opt.useAsimov ):
        cmd += '-t -1 --setPhysicsModelParameters '
        if (not opt.fixMZ):
            cmd += 'MH=91.1876,'
        
        # import z4l fid acc eff outinratio
        _temp = __import__('inputs_sig_z4l_'+obsName, globals(), locals(), ['acc','eff','outinratio'], -1)
        acc_z = _temp.acc
        eff_z = _temp.eff
        outinratio_z = _temp.outinratio
        # import z4l xsbr
        _temp = __import__('z4l_xsbr', globals(), locals(), ['z4l_xsbr'], -1)
        z4l_xsbr = _temp.z4l_xsbr

        # fidxs for z4l
        fidxs_z = {}
        for fState in ['4e','4mu', '2e2mu']:
            fidxs_z[fState] = 1000.0*z4l_xsbr['SMZ4l_'+fState]*acc_z['SMZ4l_'+fState+'_'+obsName+'_genbin0_recobin0']
        fidxs_z['4l'] = fidxs_z['4e']+fidxs_z['4mu']+fidxs_z['2e2mu']
        if (physicalModel=='v3'):
            cmd += 'Sigma='+str(fidxs_z['4l'])+','
            cmd += 'K1=1.0,'
            cmd += 'K2=1.0'
        elif (physicalModel=='v1'):
            cmd = cmd+'SigmaZ='+str(fidxs_z['4l'])+','
            cmd = cmd+'SigmaZ4e='+str(fidxs_z['4e'])+','
            cmd = cmd+'SigmaZ4mu='+str(fidxs_z['4mu'])
        else:
            cmd = cmd+'Sigma4e='+str(fidxs_z['4e'])+','
            cmd = cmd+'Sigma4mu='+str(fidxs_z['4mu'])+','
            cmd = cmd+'Sigma2e2mu='+str(fidxs_z['2e2mu'])
    else:
        cmd = cmd + ' -D data_obs --setPhysicsModelParameters MH=91.1876 '

    # you can comment this out if you want the uncertainties
    if ( opt.floatPOIs ):
        cmd = cmd + ' --floatOtherPOIs=1 '
    else:
        cmd = cmd + ' --floatOtherPOIs=0 '
    if (doUncertainty):
        if (physicalModel=='v3'):
            cmd += '-P Sigma '
            cmd += '-P K1 '
            cmd += '-P K2 '
        elif (physicalModel=='v1'):
            cmd += '-P SigmaZ '
        else:
            cmd += '-P Sigma4e '
            cmd += '-P Sigma4mu '
            cmd += '-P Sigma2e2mu '

    if(opt.useAsimov): cmd += ' --saveToys '

    print cmd
    output=processCmd(cmd)

    # parse the results for all the bins
    if (doUncertainty):
        if (physicalModel=='v3'):
            resultsXS[modelName+'_'+obsName+'_SigmaZ'] = parseXSResults(output,'Sigma :')
            resultsXS[modelName+'_'+obsName+'_K1'] = parseXSResults(output,'K1 :')
            resultsXS[modelName+'_'+obsName+'_K2'] = parseXSResults(output,'K2 :')
        elif (physicalModel=='v1'):
            resultsXS[modelName+'_'+obsName+'_SigmaZ'] = parseXSResults(output,'SigmaZ :')
        else:
            resultsXS[modelName+'_'+obsName+'_SigmaZ4e'] = parseXSResults(output,'Sigma4e :')
            resultsXS[modelName+'_'+obsName+'_SigmaZ4mu'] = parseXSResults(output,'Sigma4mu :')
            resultsXS[modelName+'_'+obsName+'_SigmaZ2e2mu'] = parseXSResults(output,'Sigma2e2mu :')

    tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH91.root'
    if(opt.useAsimov): tempCombOutFile='higgsCombine'+nameTag+'.MultiDimFit.mH91.123456.root'

    if (doUncertainty):
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result.root'
    else:
        cmd = 'cp '+tempCombOutFile+' Combine'+nameTag+'_result_plot.root'
    output=processCmd(cmd)

    return resultsXS



### Extract model dependance uncertnaities from the fit results
def addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName):
    modelIndependenceUncert = {'AsimovData_' + obsName + '_genbin0':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin1':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin2':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin3':{'uncerDn':0.0, 'uncerUp':0.0}}
    for key, value in resultsXS.iteritems():
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            if ('genbin'+binTag) in key:
                asimCent = resultsXS['AsimovData_' + obsName + '_genbin'+binTag]['central']
                keyCent = resultsXS[key]['central']
                diff = keyCent - asimCent
                if (diff<0) and (abs(diff) > abs(modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerDn'])):
                    modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                if (diff>0) and (abs(diff) > abs(modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerUp'])):
                    modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))
    return modelIndependenceUncert

### run all the steps towards the fiducial XS measurement
def runFiducialXS():

    # parse the arguments and options
    global opt, args, runAllSteps
    parseOptions()
    
    # save working dir
    jcpDir = os.getcwd()
    
    # prepare the set of bin boundaries to run over, only 1 bin in case of the inclusive measurement
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']

    ### Run for the given observable
    obsName = opt.OBSNAME
    print '[Running fiducial XS computation - '+obsName+' - bin boundaries: ', observableBins, ']'
    ## Extract the efficiency factors for all reco/gen bins and final states
    if (runAllSteps or opt.effOnly):
        if (opt.doRatio):
            extractFiducialEfficienciesRatio(obsName, observableBins, opt.MODELNAME)
        elif (opt.MODELNAME=="SMZ4l"):
            extractFiducialEfficienciesZ4l(obsName, observableBins, opt.MODELNAME)
        else: 
            extractFiducialEfficiencies(obsName, observableBins, opt.MODELNAME)

    ## Prepare templates and uncertaincies for each reco bin and final states
    for obsBin in range(0,len(observableBins)-1):
        # extract the uncertainties
        if (runAllSteps or opt.uncertOnly):
            extractUncertainties(obsName, observableBins[obsBin], observableBins[obsBin+1])

    ## Prepare templates for all reco bins and final states
    if (runAllSteps or opt.templatesOnly):
        if (opt.doRatio):
            extractBackgroundTemplatesAndFractionsRatio(obsName, observableBins)
        elif (opt.MODELNAME=="SMZ4l"):
            extractBackgroundTemplatesAndFractionsZ4l(obsName, observableBins)
        else:
            extractBackgroundTemplatesAndFractions(obsName, observableBins)

    ## Create the asimov dataset
    resultsXS = {}
        
    # create AsimovData for H4l
    if ((not opt.MODELNAME=="SMZ4l") and (not opt.doRatio) ):
        asimovPhysicalModel = "v2"
        asimovDataModelName = "ggH_powheg15_JHUgen_125"
        produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel)
        resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel)
        print "resultsXS: \n", resultsXS

    # plot the asimov predictions for data, signal, and backround in differential bins for H4l
    if ( (not obsName=="mass4l") and (not opt.MODELNAME=="SMZ4l") and (not opt.doRatio) ):
        cmd = 'python plotDifferentialBins.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'"'
        print cmd
        output = processCmd(cmd)


    ## Extract the results
    if (opt.doRatio):
        #modelNames = ['SM_125','SMup_125','SMdn_125'] 
        modelNames = ['SM_125']
        for modelName in modelNames:
            if (runAllSteps or opt.resultsOnly):
                produceDatacardsRatioInclusive(obsName, modelName, 'v1')
                resultsXS = extractResultsRatioInclusive(obsName, modelName, 'v1', resultsXS, True)
                print "resultsXS: \n", resultsXS
                produceDatacardsRatioInclusive(obsName, modelName, 'v2')
                resultsXS = extractResultsRatioInclusive(obsName, modelName, 'v2', resultsXS, True)
                print "resultsXS: \n", resultsXS
                produceDatacardsRatioInclusive(obsName, modelName, 'v2')
                resultsXS = extractResultsRatioInclusive(obsName, modelName, 'v2', resultsXS, False)
    elif (opt.MODELNAME=="SMZ4l"):
        if (runAllSteps or opt.resultsOnly):
            modelName = "SMZ4l"
            modelNames = ['SMZ4l']
            if (obsName=='mass4l'):
                produceDatacardsZ4l(obsName, observableBins, modelName, 'v3')
                resultsXS = extractResultsZ4lInclusive(obsName, modelName, 'v3', resultsXS, True)
                print "resultsXS: \n", resultsXS
                produceDatacardsZ4l(obsName, observableBins, modelName, 'v2')
                resultsXS = extractResultsZ4lInclusive(obsName, modelName, 'v2', resultsXS, True)
                print "resultsXS: \n", resultsXS
            else:
                asimovDataModelName = modelName
                asimovPhysicalModel = 'v3'
                produceDatacardsZ4l(obsName, observableBins, modelName, 'v3')
                resultsXS = extractResultsZ4l(obsName, observableBins, modelName, 'v3', asimovDataModelName, asimovPhysicalModel, resultsXS, True)
                print "resultsXS: \n", resultsXS
    else:
        if (opt.MODELNAME=="all"): 
            physicalModel="v1"
            if (obsName.startswith("njets")):
                modelNames = ['ggH_powheg15_JHUgen_125', 'VBF_powheg_125', 'WH_pythia_125', 'ZH_pythia_125']
            else:
                modelNames = ['ggH_powheg15_JHUgen_125', 'VBF_powheg_125', 'WH_pythia_125', 'ZH_pythia_125', 'ttH_pythia_125','ggH0MToZG_JHUgen_125p6','qq1M_JHUgen_125p6']
        else:
            modelNames = [opt.MODELNAME]
     
        for modelName in modelNames:
            if (runAllSteps or opt.resultsOnly):
                produceDatacards(obsName, observableBins, modelName, physicalModel)
                resultsXS = extractResults(obsName, observableBins, modelName, physicalModel, asimovDataModelName, asimovPhysicalModel, resultsXS)
            print "resultsXS: \n", resultsXS
                


    ## write results
    if (runAllSteps or opt.resultsOnly):
        if (opt.doRatio):
            nameTag = '_Ratio_'+opt.MODELNAME+'_'+obsName
            if ( opt.useAsimov ):
                nameTag += '_Asimov'
            if ( opt.floatPOIs ):
                nameTag += '_floatPOIs'
            if ( opt.fixMH):
                nameTag += '_fixMH'
            if ( opt.fixDeltaMHmZ):
                nameTag += '_fixDeltaMHmZ'
            nameTag += '_all_8TeV_xs_v1_v2'
            output_file = 'resultsXS'+nameTag+'.py'
            with open(output_file, 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
        elif (opt.MODELNAME=="SMZ4l"):
            nameTag = '_Z4l_'+opt.MODELNAME+'_'+obsName
            if ( opt.useAsimov ):
                nameTag += '_Asimov'
            if ( opt.floatPOIs ):
                nameTag += '_floatPOIs'
            if ( opt.fixMZ):
                nameTag += '_fixMZ'
            if (obsName=='mass4l'): nameTag += '_all_8TeV_xs_v3_v2'
            else: nameTag += '_all_8TeV_xs_v3'
            output_file = 'resultsXS'+nameTag+'.py'
            with open(output_file, 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
        else:
            ## Calculate model dependance uncertainties if not Z4l
            modelIndependenceUncert = addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName)
            print "modelIndependenceUncert: \n", modelIndependenceUncert
            with open('resultsXS_'+obsName+'.py', 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('asimovDataModelName = '+json.dumps(asimovDataModelName)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
                f.write('modelIndUncert = '+json.dumps(modelIndependenceUncert))

    ## Make final differential plots
    if (runAllSteps or opt.finalplotsOnly):
        if (opt.doRatio):
            for modelName in modelNames:
                nameTag = '_Ratio_'+opt.MODELNAME+'_'+obsName
                if ( opt.useAsimov ):
                    nameTag = nameTag+'_Asimov'
                if ( opt.floatPOIs ):
                    nameTag = nameTag+'_floatPOIs'
                if ( opt.fixMH):
                    nameTag += '_fixMH'
                if ( opt.fixDeltaMHmZ):
                    nameTag += '_fixDeltaMHmZ'
                nameTag += '_all_8TeV_xs'

                produceDatacardsZ4l(obsName, observableBins, modelName, 'v2')
                resultsXS = extractResultsZ4lInclusive(obsName, modelName, 'v2', resultsXS, False)

                cmd = 'python producePlotsRatio.py -l -q -b --resultTag="'+nameTag+'_v1_v2"'
                output = processCmd(cmd)

                if ( opt.useAsimov ):
                    cmd = 'python plotAsimov_inclusive_ratio.py -l -q -b --resultFile="Combine'+nameTag+'_v2_result_plot.root"'
                else:
                    cmd = 'python plotData_inclusive_ratio.py -l -q -b --resultFile="Combine'+nameTag+'_v2_result_plot.root"'
                print cmd
                output = processCmd(cmd)

        elif (opt.MODELNAME=="SMZ4l"):
            nameTag = '_Z4l_'+opt.MODELNAME+'_'+obsName
            if ( opt.useAsimov ):
                nameTag = nameTag+'_Asimov'
            if ( opt.floatPOIs ):
                nameTag = nameTag+'_floatPOIs'
            if ( opt.fixMZ):
                nameTag += '_fixMZ'
            nameTag += '_all_8TeV_xs'
            if (obsName=='mass4l'):
                cmd = 'python producePlotsZ4lNew.py -l -q -b --resultTag="'+nameTag+'_v3_v2"'
                print cmd
                output = processCmd(cmd)
            else:
                cmd = 'python producePlotsZ4l.py -l -q -b --resultTag="'+nameTag+'_v3" --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+opt.MODELNAME+'"'
                print cmd
                output = processCmd(cmd)
                cmd = 'python producePlotsZ4l.py -l -q -b --resultTag="'+nameTag+'_v3" --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+opt.MODELNAME+'" --setLog '
                print cmd
                output = processCmd(cmd)
        else:
            for modelName in modelNames:
                cmd = 'python producePlots.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'"'
                print cmd
                output = processCmd(cmd)
        
if __name__ == "__main__":
    runFiducialXS()
