from ROOT import *
from array import array
import os

RootFiles = {}
SlimRootFiles = {}
TreesPassedEvents = {}
TreesPassedEventsNoHLT = {}
nEvents = {}
TreesPassedEventsSlim = {}

tlist = {}

gROOT.ProcessLine(
    "struct mass4lStruct {\
    Double_t   fmass4l;\
    };" );
gROOT.ProcessLine(
    "struct mass4eStruct {\
    Double_t   fmass4e;\
    };" );
gROOT.ProcessLine(
    "struct mass4muStruct {\
    Double_t   fmass4mu;\
    };" );
gROOT.ProcessLine(
    "struct mass2e2muStruct {\
    Double_t   fmass2e2mu;\
    };" );
gROOT.ProcessLine(
    "struct passedFullSelectionStruct {\
    Bool_t     fpassedFullSelection;\
    };" );
gROOT.ProcessLine(
    "struct eventMCWeightStruct {\
    Double_t   feventMCWeight;\
    };" );
gROOT.ProcessLine(
    "struct totalWeightStruct {\
    Double_t   ftotalWeight;\
    };" );
gROOT.ProcessLine(
    "struct pT4lStruct {\
    Double_t   fpT4l;\
    };" );
gROOT.ProcessLine(
    "struct massZ2Struct {\
    Double_t   fmassZ2;\
    };" );
gROOT.ProcessLine(
    "struct rapidity4lStruct {\
    Double_t   frapidity4l;\
    };" );
gROOT.ProcessLine(
    "struct cosThetaStarStruct {\
    Double_t   fcosThetaStar;\
    };" );
gROOT.ProcessLine(
    "struct njets_reco_pt30_eta4p7Struct {\
    Int_t   fnjets_reco_pt30_eta4p7;\
    };" );



from ROOT import mass4lStruct
from ROOT import mass4eStruct
from ROOT import mass4muStruct
from ROOT import mass2e2muStruct
from ROOT import passedFullSelectionStruct
from ROOT import eventMCWeightStruct
from ROOT import totalWeightStruct
from ROOT import pT4lStruct
from ROOT import massZ2Struct
from ROOT import rapidity4lStruct
from ROOT import cosThetaStarStruct
from ROOT import njets_reco_pt30_eta4p7Struct


global eventfile
global removedfile
global passedeventfile

def LoadData(dirMC):

    dirData = '/scratch/osghpc/dsperka/Analyzer/SubmitArea_8TeV/'
    SamplesData = ['Data_2012.root']

    # 125 GeV
    SamplesMC = ['SMHiggsToZZTo4L_M-125_8TeV-powheg15-JHUgenV3-pythia6.root','GluGluToHToZZTo4L_M-125_8TeV-powheg15-pythia6.root','GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6.root','GluGluToHToZZTo4L_M-125_8TeV-minloHJJ-pythia6-tauola.root','VBF_HToZZTo4L_M-125_8TeV-powheg-pythia6.root','WH_HToZZTo4L_M-125_8TeV-pythia6.root','ZH_HToZZTo4L_M-125_8TeV-pythia6.root','TTbarH_HToZZTo4L_M-125_8TeV-pythia6.root']

    # 126 GeV
    SamplesMC.extend(['SMHiggsToZZTo4L_M-126_8TeV-powheg15-JHUgenV3-pythia6.root','GluGluToHToZZTo4L_M-126_8TeV-powheg15-pythia6.root','GluGluToHToZZTo4L_M-126_8TeV-powheg-pythia6.root','GluGluToHToZZTo4L_M-126_8TeV-minloHJJ-pythia6-tauola.root','VBF_HToZZTo4L_M-126_8TeV-powheg-pythia6.root','WH_HToZZTo4L_M-126_8TeV-pythia6.root','ZH_HToZZTo4L_M-126_8TeV-pythia6.root','TTbarH_HToZZTo4L_M-126_8TeV-pythia6.root','Vector1MToZZTo4L_M-126_8TeV-JHUgenV3-pythia6-tauola.root','Vector1PToZZTo4L_M-126_8TeV-JHUgenV3-pythia6-tauola.root'])

    # 125.6 JHUGen Spin 0
    SamplesMC.extend(['Higgs0PMToZZTo4L_M-125p6_8TeV-powheg15-JHUgenV3.root','JJHiggs0PToZZTo4L_M-125p6_8TeV-JHUGenV4.root','VBFHiggs0PToZZTo4L_M-125p6_8TeV-JHUGenV4.root','WHiggs0PToZZTo4L_M-125p6_8TeV-JHUGenV4.root','ZHiggs0PToZZTo4L_M-125p6_8TeV-JHUGenV4.root'])

    # 125.6 Spin 2
    SamplesMC.extend(['Graviton2HMqqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2HPqqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH2ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH2qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH3ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH3qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH6ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH6qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH7ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2PH7qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2MH9ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2MH9qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2MH10ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Graviton2MH10qqbarToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root'])

    # 125.6 Spin 1
    SamplesMC.extend(['Vector1MToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Vector1Mf05ph01Pf05ph0ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Vector1Mf05ph01Pf05ph90ToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root','Vector1PToZZTo4L_M-125p6_8TeV-JHUGenV3-pythia6.root'])

    # 125.6 GG/ZG 
    SamplesMC.extend(['Higgs0MToGGTo4L_M-125p6_8TeV-powheg15-JHUgenV4.root','Higgs0MToZGTo4L_M-125p6_8TeV-powheg15-JHUgenV4.root','Higgs0PMToZGTo4L_M-125p6_8TeV-powheg15-JHUgenV4.root','Higgs0PMToGGTo4L_M-125p6_8TeV-powheg15-JHUgenV4.root'])


    # Tprime (120 GeV)
    #SamplesMC.extend(['TprimeTprimeToTHBW_HToZZTo4L_M-500_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHBW_HToZZTo4L_M-600_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHBW_HToZZTo4L_M-700_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHBW_HToZZTo4L_M-800_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHBW_HToZZTo4L_M-900_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTH_HToZZTo4L_M-500_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTH_HToZZTo4L_M-600_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTH_HToZZTo4L_M-700_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTH_HToZZTo4L_M-800_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTH_HToZZTo4L_M-900_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTZ_HToZZ_M-500_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTZ_HToZZ_M-600_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTZ_HToZZ_M-700_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTZ_HToZZ_M-800_TuneZ2star_8TeV-madgraph.root','TprimeTprimeToTHTZ_HToZZ_M-900_TuneZ2star_8TeV-madgraph.root'])

    # Backgrounds 8 TeV
    SamplesMC.extend(['GluGluToZZTo2L2L_TuneZ2star_8TeV-gg2zz-pythia6.root','GluGluToZZTo4L_8TeV-gg2zz-pythia6.root','ZZTo2e2mu_8TeV-powheg-pythia6.root','ZZTo2e2tau_8TeV-powheg-pythia6.root','ZZTo2mu2tau_8TeV-powheg-pythia6.root','ZZTo4e_8TeV-powheg-pythia6.root','ZZTo4mu_8TeV-powheg-pythia6.root','ZZTo4tau_8TeV-powheg-pythia6.root'])

    # Signals 7 TeV
    #SamplesMC.extend(['GluGluToHToZZTo4L_M-125_mll1_7TeV-powheg-pythia6.root','GluGluToHToZZTo4L_M-126_mll1_7TeV-powheg-pythia6.root','SMHiggsToZZTo4L_M-126_7TeV_ext-JHUgenV2-PYTHIA6_Tauola.root','TTbarH_HToZZTo4L_M-126_7TeV-pythia6.root','VBF_ToHToZZTo4L_M-120_7TeV-powheg-pythia6.root','WH_HToZZTo4L_M-125_7TeV-pythia6.root','WH_HToZZTo4L_M-126_7TeV-pythia6.root','ZH_HToZZTo4L_M-125_7TeV-pythia6.root','ZH_HToZZTo4L_M-126_7TeV-pythia6.root','TTbarH_HToZZTo4L_M-125_7TeV-pythia6.root'])
  
    # Backgrounds 7 TeV
    #SamplesMC.extend(['GluGluToZZTo2L2L_7TeV-gg2zz-pythia6.root','GluGluToZZTo4L_7TeV-gg2zz-pythia6.root','ZZTo2e2mu_mll4_7TeV-powheg-pythia6.root','ZZTo2e2tau_mll4_7TeV-powheg-pythia6.root','ZZTo2mu2tau_mll4_7TeV-powheg-pythia6.root','ZZTo4e_mll4_7TeV-powheg-pythia6.root','ZZTo4mu_mll4_7TeV-powheg-pythia6.root','ZZTo4tau_mll4_7TeV-powheg-pythia6.root'])

    for i in range(0,len(SamplesMC)):
        
        sample = SamplesMC[i].rstrip('.root') 
        
        RootFiles[sample] = TFile(dirMC+'/'+sample+'.root',"READ")        
        TreesPassedEvents[sample]  = RootFiles[sample].Get("passedEvents_dataMC") 
        TreesPassedEventsNoHLT[sample]  = RootFiles[sample].Get("Ana/passedEvents") 
        
        h_nevents = RootFiles[sample].Get("Ana/nEvents")

        if (h_nevents):
            nEvents[sample] = h_nevents.Integral()
        else:
            nEvents[sample] = 0.
            
        nremoved = 0

        # make a slimmed down tree saving only stuff you want for events you want
        mass4lstruct = mass4lStruct()
        mass4estruct = mass4eStruct()
        mass4mustruct = mass4muStruct()
        mass2e2mustruct = mass2e2muStruct()
        passedFullSelectionstruct = passedFullSelectionStruct()
        eventMCWeightstruct = eventMCWeightStruct()
        totalWeightstruct = totalWeightStruct()
        pT4lstruct = pT4lStruct()
        massZ2struct = massZ2Struct()
        rapidity4lstruct = rapidity4lStruct()
        cosThetaStarstruct = cosThetaStarStruct()
        njets_reco_pt30_eta4p7struct = njets_reco_pt30_eta4p7Struct()
        
        slimfileexists = False

        if (os.path.isfile(dirMC+'/'+sample+'_slim.root')):
            slimfileexists = True            
            SlimRootFiles[sample] = TFile(dirMC+'/'+sample+'_slim.root',"READ")
            TreesPassedEventsSlim[sample] = SlimRootFiles[sample].Get("treeslim"+sample);    
        else:
            SlimRootFiles[sample] = TFile(dirMC+'/'+sample+'_slim.root',"RECREATE") 
            TreesPassedEventsSlim[sample] = TTree("treeslim"+sample,"treeslim"+sample);    
        
            TreesPassedEventsSlim[sample].Branch( 'mass4l', mass4lstruct, 'mass4l/D' )
            TreesPassedEventsSlim[sample].Branch( 'mass4e', mass4estruct, 'mass4e/D' )
            TreesPassedEventsSlim[sample].Branch( 'mass4mu', mass4mustruct, 'mass4mu/D' )
            TreesPassedEventsSlim[sample].Branch( 'mass2e2mu', mass2e2mustruct, 'mass2e2mu/D' )
            TreesPassedEventsSlim[sample].Branch( 'passedFullSelection', passedFullSelectionstruct, 'passedFullSelection/O' )
            TreesPassedEventsSlim[sample].Branch( 'eventMCWeight', eventMCWeightstruct, 'eventMCWeight/D' )
            TreesPassedEventsSlim[sample].Branch( 'totalWeight', totalWeightstruct, 'totalWeight/D' )
            TreesPassedEventsSlim[sample].Branch( 'pT4l', pT4lstruct, 'pT4l/D' )
            TreesPassedEventsSlim[sample].Branch( 'massZ2', massZ2struct, 'massZ2/D' )
            TreesPassedEventsSlim[sample].Branch( 'rapidity4l', rapidity4lstruct, 'rapidity4l/D' )
            TreesPassedEventsSlim[sample].Branch( 'cosThetaStar', cosThetaStarstruct, 'cosThetaStar/D' )
            TreesPassedEventsSlim[sample].Branch( 'njets_reco_pt30_eta4p7', njets_reco_pt30_eta4p7struct, 'njets_reco_pt30_eta4p7/I' )
                                
            
        if (not TreesPassedEvents[sample]): print sample+' has no passedEvents_dataMC tree'
        
        checkDuplicates = False 
        
        if (TreesPassedEvents[sample] and (checkDuplicates or (not slimfileexists)) ):

            ### Here we remove duplicate events or Create a slimmed ntuple file

            # keep track of seen events
            run_lumi_events = set()
            tlist[sample] = TEntryList(TreesPassedEvents[sample]); 
            
            Nevents = TreesPassedEvents[sample].GetEntriesFast()
            
            for entry in xrange(Nevents):
            
                TreesPassedEvents[sample].GetEntry(entry)

                event = TreesPassedEvents[sample].Event
                run   = TreesPassedEvents[sample].Run
                lumi  = TreesPassedEvents[sample].LumiSect
                run_lumi_event = int(str(run)+str(lumi)+str(event))

                mass4lstruct.fmass4l = TreesPassedEvents[sample].mass4l
                mass4estruct.fmass4e = TreesPassedEvents[sample].mass4e
                mass4mustruct.fmass4mu = TreesPassedEvents[sample].mass4mu
                mass2e2mustruct.fmass2e2mu = TreesPassedEvents[sample].mass2e2mu
                eventMCWeightstruct.feventMCWeight = TreesPassedEvents[sample].eventMCWeight
                totalWeightstruct.ftotalWeight = TreesPassedEvents[sample].totalWeight
                passedFullSelectionstruct.fpassedFullSelection = TreesPassedEvents[sample].passedFullSelection
                pT4lstruct.fpT4l = TreesPassedEvents[sample].pT4l
                massZ2struct.fmassZ2 = TreesPassedEvents[sample].massZ2
                rapidity4lstruct.frapidity4l = TreesPassedEvents[sample].rapidity4l
                cosThetaStarstruct.fcosThetaStar = TreesPassedEvents[sample].cosThetaStar
                njets_reco_pt30_eta4p7struct.fnjets_reco_pt30_eta4p7 = TreesPassedEvents[sample].njets_reco_pt30_eta4p7
                
                # Reduce size of tree
                if (passedFullSelectionstruct.fpassedFullSelection>0.5 and mass4lstruct.fmass4l>100 and mass4lstruct.fmass4l<200): 
                    if (not slimfileexists): TreesPassedEventsSlim[sample].Fill()

                # if we have not seen this event yet, add it to the set
                if ( (run_lumi_event not in run_lumi_events) and checkDuplicates):
                    run_lumi_events.add(run_lumi_event)
                    tlist[sample].Enter(entry,TreesPassedEvents[sample])
                else:
                    nremoved +=1
                
            if (not slimfileexists): SlimRootFiles[sample].Write()        
            if (checkDuplicates): TreesPassedEvents[sample].SetEntryList(tlist[sample]);        
            #print sample+' nEvents: '+str(nEvents[sample]),' nremoved: ',nremoved,' nslimmed: ',TreesPassedEventsSlim[sample].GetEntriesFast()
        
        
    for i in range(0,len(SamplesData)):
        sample = SamplesData[i].replace('.root','')
        #print sample
        RootFiles[sample] = TFile(dirData+'/'+sample+'.root')
        TreesPassedEvents[sample] = RootFiles[sample].Get("AnaAfterHlt/passedEvents")
    
        ### Here we remove duplicate events
        run_lumi_events = set() # keep track of seen events, format is runlumievent, i.e. 201718625438970290 if run=201718 ls=62 event=5438970290
        tlist[sample] = TEntryList(TreesPassedEvents[sample]); 
        
        # loop over the entries in 'tree'
        Nevents = TreesPassedEvents[sample].GetEntriesFast()
        for entry in xrange(Nevents):
            TreesPassedEvents[sample].GetEntry(entry)

            event = TreesPassedEvents[sample].Event
            run   = TreesPassedEvents[sample].Run
            lumi  = TreesPassedEvents[sample].LumiSect
            run_lumi_event = int(str(run)+str(lumi)+str(event))
            
            passedFullSelection = TreesPassedEvents[sample].passedFullSelection
            mass4l = TreesPassedEvents[sample].mass4l
            mass4e = TreesPassedEvents[sample].mass4e
            mass4mu = TreesPassedEvents[sample].mass4mu
            mass2e2mu = TreesPassedEvents[sample].mass2e2mu
            massErrUFCorr = TreesPassedEvents[sample].massErrorUFCorr

            # if we have not seen this event yet, add it to the set
            if ( run_lumi_event not in run_lumi_events):
                run_lumi_events.add(run_lumi_event)
                tlist[sample].Enter(entry,TreesPassedEvents[sample])
                
    # apply the entry list to the tree
    TreesPassedEvents[sample].SetEntryList(tlist[sample])
    

#LoadData('/scratch/osghpc/dsperka/Analyzer/SubmitArea_8TeV/Trees_HZZFiducialSamples_Oct14/')
        

