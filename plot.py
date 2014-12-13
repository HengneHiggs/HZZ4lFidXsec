
from ROOT import *

c1 = TCanvas("c1", "c1")
rootfile = TFile("higgsCombine_Scan_Ratio_SM_125_mass4l_floatPOIs_fixMH_fixDeltaMHmZ_all_8TeV_xs_v1_SigmaH.MultiDimFit.mH125.root")
tree = rootfile.Get("limit")
tree.Draw("2*deltaNLL:SigmaH", "deltaNLL<100", "a*")
graph = c1.GetPrimitive("Graph")
#graph.SetName('h_'+poi)
graph.Draw("a*")
c1.Print("c1.pdf")


