from ROOT import *
from tdrStyle import *
setTDRStyle()

from array import array

observables = ['pT4l','rapidity4l','njets_reco_pt30_eta4p7','njets_reco_pt30_eta2p5','massZ1','massZ2','cosThetaStar','cosTheta2','Phi','Phi1','cosTheta1']
#observables = ['cosTheta1']

for obsName in observables:
    for obsbin in ['0','1','2','3']:
    #for obsbin in ['1']:

        if (obsName=="cosTheta1" and obsbin=="0"): continue
        f = TFile("higgsCombine"+obsName+"_SigmaBin"+obsbin+".MultiDimFit.mH125.root","READ")

        if (f==0): continue

        limit = f.Get("limit")
        npoints = limit.GetEntries()
        
        sigma = []
        deltanll = []
        bestfit = 9999.0
        
        for point in range(0,npoints):
            limit.GetEntry(point)
            if (obsbin=="0"):
                if (point==0): bestfit=limit.SigmaBin0
                if (point>0): 
                    if (limit.deltaNLL<2.5):
                        sigma.append(limit.SigmaBin0)
                        deltanll.append(2.0*limit.deltaNLL)
            if (obsbin=="1"):
                if (point==0): bestfit=limit.SigmaBin1
                if (point>0): 
                    if (limit.deltaNLL<2.5):
                        sigma.append(limit.SigmaBin1)
                        deltanll.append(2.0*limit.deltaNLL)
            if (obsbin=="2"):
                if (point==0): bestfit=limit.SigmaBin2
                if (point>0): 
                    if (limit.deltaNLL<2.5):
                        sigma.append(limit.SigmaBin2)
                        deltanll.append(2.0*limit.deltaNLL)
            if (obsbin=="3"):
                if (point==0): bestfit=limit.SigmaBin3
                if (point>0): 
                    if (limit.deltaNLL<2.5):
                        sigma.append(limit.SigmaBin3)
                        deltanll.append(2.0*limit.deltaNLL)

            if point>0 and len(deltanll)>0:
                if deltanll[len(deltanll)-1]>5.0 and sigma[len(sigma)-1]>bestfit: break

        #print sigma
        #print deltanll

        scan = TGraph(len(sigma),array('d',sigma),array('d',deltanll))


        c = TCanvas("c","c",1000,800)

        dummy = TH1D("dummy","dummy",1,sigma[0],sigma[len(sigma)-1])
        dummy.SetMinimum(0.0)
        dummy.SetMaximum(5.0)
        dummy.SetLineColor(0)
        dummy.SetMarkerColor(0)
        dummy.SetLineWidth(0)
        dummy.SetMarkerSize(0)
        dummy.GetYaxis().SetTitle("-2 #Delta lnL")
        dummy.GetXaxis().SetTitle("d#sigma [fb]")
        dummy.Draw()

        scan.SetMarkerStyle(20)
        scan.SetMarkerSize(0.6)
        scan.SetMarkerColor(1)
        scan.Draw("psame")

        gStyle.SetOptFit(0)
        f1 = TF1("f1","pol8",0.0,3.0)
        f1.SetLineColor(2)
        f1.SetLineWidth(2)
        scan.Fit("f1")

        cl68 = TF1("cl68","1.0",0.0,3.0)
        cl68.SetLineStyle(2)
        cl68.SetLineColor(1)
        cl68.Draw("same")

        cl95 = TF1("cl95","3.84",0.0,3.0)
        cl95.SetLineStyle(2)
        cl95.SetLineColor(1)
        cl95.Draw("same")

        cl68up = 0.0
        cl68dn = 0.0
        cl95up = 0.0
        cl95dn = 0.0

        for i in range(0,40000):
            x = 0.+i/20000.
            scanval = f1.Eval(x)
            #if abs(scanval-3.84)<.001: print x,scanval
            if abs(scanval-1.0)<.001 and x<bestfit:
                cl68dn = round((bestfit-x),3)
            if abs(scanval-1.0)<.001 and x>bestfit:
                cl68up = round((x-bestfit),3)
            if abs(scanval-3.84)<.001 and x<bestfit:
                cl95dn = round((bestfit-x),3)
            if abs(scanval-3.84)<.001 and x>bestfit:
                cl95up = round((x-bestfit),3)

        if (cl68dn==0.0): cl68dn=round(bestfit,3)
        if (cl95dn==0.0): cl95dn=round(bestfit,3)
        print obsName,obsbin,round(bestfit,3),"+",cl68up,"-",cl68dn,"(68%)","+",cl95up,"-",cl95dn,"(95%)"

        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right                                                                     
        latex2.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
        latex2.SetTextSize(0.8*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right                                                                     
        latex2.DrawLatex(0.19, 0.95, "CMS")
        latex2.SetTextSize(0.6*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.30, 0.95, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.45*c.GetTopMargin())
        latex2.DrawLatex(0.30,0.85, obsName+" Bin"+obsbin)
        latex2.DrawLatex(0.30,0.78, "d#sigma = "+str(round(bestfit,3))+" ^{+"+str(cl68up)+"}_{-"+str(cl68dn)+"} (68%) ^{+"+str(cl95up)+"}_{-"+str(cl95dn)+"} (95%)")

        c.SaveAs("lhscan_"+obsName+"_SigmaBin"+obsbin+".pdf")
        c.SaveAs("lhscan_"+obsName+"_SigmaBin"+obsbin+".png")

