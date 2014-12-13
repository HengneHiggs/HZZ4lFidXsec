
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *

Procs = {}
Tags = {}

# Z4l only
_temp = __import__('inputs_sig_z4l_mass4l', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio'], -1)
acc = _temp.acc
dacc = _temp.dacc
eff = _temp.eff
deff = _temp.deff
outinratio = _temp.outinratio
doutinratio = _temp.doutinratio


Procs[0]='SMZ4l_'

Tags[0]='Z$\\to$4l ({\sc powheg}) '


print 'Acceptance'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(acc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(dacc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Efficiency'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(eff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(deff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Out-in-ratio'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(outinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(doutinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'





# Z4l in ratio
_temp = __import__('inputs_sig_ratio_z4l_mass4l', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio'], -1)
acc = _temp.acc
dacc = _temp.dacc
eff = _temp.eff
deff = _temp.deff
outinratio = _temp.outinratio
doutinratio = _temp.doutinratio

Procs[0]='SMZ4l_'

Tags[0]='Z$\\to$4l ({\sc powheg}) '


print 'Acceptance'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(acc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(dacc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Efficiency'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(eff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(deff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Out-in-ratio'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(1):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(outinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(doutinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


# Higgs

_temp = __import__('inputs_sig_ratio_h4l_mass4l', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio','inc_wrongfrac'], -1)
acc = _temp.acc
dacc = _temp.dacc
eff = _temp.eff
deff = _temp.deff
outinratio = _temp.outinratio
doutinratio = _temp.doutinratio
inc_wrongfrac = _temp.inc_wrongfrac




Procs[0]='ggH_powheg15_JHUgen_125_'
Procs[1]='ggH_powheg15_JHUgen_126_'
Procs[2]='ggH_powheg15_125_'
Procs[3]='ggH_powheg15_126_'
Procs[4]='ggH_powheg_125_'
Procs[5]='ggH_powheg_126_'
Procs[6]='ggH_minloHJJ_125_'
Procs[7]='ggH_minloHJJ_126_'
Procs[8]='VBF_powheg_125_'
Procs[9]='VBF_powheg_126_'
Procs[10]='WH_pythia_125_'
Procs[11]='WH_pythia_126_'
Procs[12]='ZH_pythia_125_'
Procs[13]='ZH_pythia_126_'
Procs[14]='ttH_pythia_125_'
Procs[15]='ttH_pythia_126_'

Tags[0]='gg$\\rightarrow$H ({\sc powheg+JHUgen}) 125 $\GeV$'
Tags[1]='gg$\\rightarrow$H ({\sc powheg+JHUgen}) 126 $\GeV$'
Tags[2]='gg$\\rightarrow$H ({\sc powheg}) 125 $\GeV$'
Tags[3]='gg$\\rightarrow$H ({\sc powheg}) 126 $\GeV$'
Tags[4]='gg$\\rightarrow$H ({\sc powheg1.0}) 125 $\GeV$'
Tags[5]='gg$\\rightarrow$H ({\sc powheg1.0}) 126 $\GeV$'
Tags[6]='gg$\\rightarrow$H ({\sc minloHJJ}) 125 $\GeV$'
Tags[7]='gg$\\rightarrow$H ({\sc minloHJJ}) 126 $\GeV$'
Tags[8]='VBF ({\sc powheg}) 125 $\GeV$'
Tags[9]='VBF ({\sc powheg}) 126 $\GeV$'
Tags[10]='WH ({\sc pythia}) 125 $\GeV$'
Tags[11]='WH ({\sc pythia}) 126 $\GeV$'
Tags[12]='ZH ({\sc pythia}) 125 $\GeV$'
Tags[13]='ZH ({\sc pythia}) 126 $\GeV$'
Tags[14]='ttH ({\sc pythia}) 125 $\GeV$'
Tags[15]='ttH ({\sc pythia}) 126 $\GeV$'


print 'Acceptance'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(16):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(acc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(dacc[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Efficiency'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(16):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(eff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(deff[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'


print 'Out-in-ratio'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(16):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(outinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' $\pm$ ',
        print str(round(doutinratio[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),
    print ' \\\\'

 
print 'fake rate'
print '\\begin{tabular}{|l|c|c|c|c|} \hline'
print 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline'
for id in range(16):
    print Tags[id],
    for fstate in ['4e','4mu','2e2mu','4l']:
        print ' & '+str(round(inc_wrongfrac[Procs[id]+fstate+'_mass4l_genbin0_recobin0'],3)),' ',
    print ' \\\\'
