#!/usr/bin/python
import sys, os, pwd, commands
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *

#obsNames = ['rapidity4l']

obsNames = ['mass4l']
#obsNames = ['pT4l']
#obsNames = ['massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7', 'cosThetaStar']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7', 'cosThetaStar']

tag=""
doRatio=True
finalplotsOnly=True
resultsOnly=False
useAsimov=False
redoEff = False
effOnly = False
redoTemplates = False
templatesOnly = False
floatPOIs = True
fixMH = True
fixDeltaMHmZ = True
inputDir = "/scratch/osghpc/dsperka/Analyzer/SubmitArea_8TeV/Trees_HZZFiducialSamples_Nov22/"
modelName = 'SM_125'
obsBinsDict = {'mass4l' : '"|50|140|"', 'pT4l' : '"|0|15|30|60|200|"', 'massZ2' : '"|12|20|28|35|120|"', 'rapidity4l' : '"|0|0.4|0.8|1.2|2.4|"', 'njets_reco_pt30_eta4p7' : '"|0|1|2|3|10|"', 'cosThetaStar' : '"|0.0|0.25|0.5|0.75|1.0|"'} 


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
    if (not quiet):
        print 'Output:\n   ['+output+'] \n'
    return output

for obsName in obsNames:
    obsBins = obsBinsDict[ obsName ]
    cmd = 'python runHZZFiducialXS.py --dir='+inputDir+' --modelName='+modelName+' --obsName='+obsName+' --obsBins='+obsBins+' '
    if (resultsOnly):
        cmd = cmd + ' --resultsOnly'
    if (finalplotsOnly):
        cmd = cmd + ' --finalplotsOnly'
    if (redoEff):
        cmd = cmd + ' --redoEff '
    if (effOnly):
        cmd = cmd + ' --effOnly '
    if (redoTemplates): 
        cmd = cmd + ' --redoTemplates '
    if (useAsimov):
        cmd = cmd + ' --useAsimov '
    if (doRatio):
        cmd = cmd + ' --doRatio '
    if (templatesOnly): 
        cmd = cmd + ' --templatesOnly '
    if (floatPOIs):
        cmd = cmd + ' --floatPOIs '
    if (fixMH):
        cmd = cmd + ' --fixMH '
    if (fixDeltaMHmZ):
        cmd = cmd + ' --fixDeltaMHmZ '

    cmd = cmd + ' &> testratio_'+modelName+'_'+obsName
    if (resultsOnly):
        cmd = cmd + '_resultsOnly'
    if (finalplotsOnly):
        cmd = cmd + '_finalplotsOnly'
    if (useAsimov):
        cmd = cmd + '_Asimov'
    if (doRatio):
        cmd = cmd + '_doRatio'
    if (redoEff):
        cmd = cmd + '_redoEff'
    if (effOnly):
        cmd = cmd + '_effOnly'
    if (redoTemplates):
        cmd = cmd + '_redoTemplates'
    if (templatesOnly):
        cmd = cmd + '_templatesOnly'
    if (floatPOIs):
        cmd = cmd + '_floatPOIs'
    if (fixMH):
        cmd = cmd + '_fixMH'
    if (fixDeltaMHmZ):
        cmd = cmd + '_fixDeltaMHmZ'
    cmd = cmd + tag + '.log &'

    print cmd
    output=processCmd(cmd)
    print output






