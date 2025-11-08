#!/usr/bin/env python

#Standard imports
from operator                   import attrgetter
from math                       import pi, sqrt, cosh, cos, acos, sin
import ROOT, os
import copy
import itertools
import numpy as np

#From RootTools
from RootTools.core.standard     import *

#From Tools
from TT2lUnbinned.Tools.helpers          import deltaPhi, deltaR2, deltaR, getCollection, getObjDict
from TT2lUnbinned.Tools.objectSelection import isBJet, isAnalysisJet

from Analysis.Tools.WeightInfo       import WeightInfo

import logging
logger = logging.getLogger(__name__)

from Analysis.Tools.leptonJetArbitration     import cleanJetsAndLeptons

jetVars          = ['pt/F', 'eta/F', 'phi/F', 'btagDeepFlavB/F', 'btagDeepFlavCvB/F', 'btagDeepFlavQG/F']

jetVarNames      = [x.split('/')[0] for x in jetVars]

#lstm_jets_maxN   = 10
#lstm_jetVars     = ['pt/F', 'eta/F', 'phi/F', 'btagDeepFlavB/F', 'btagDeepFlavCvB/F', 'btagDeepFlavQG/F']#, 'puId/F', 'qgl/F', 'mass/F']
#lstm_jetVarNames = [x.split('/')[0] for x in lstm_jetVars]

lepVars          = ['pt/F','eta/F','phi/F','pdgId/I','cutBased/I','miniPFRelIso_all/F','pfRelIso03_all/F','mvaFall17V2Iso_WP90/O', 'mvaTOP/F', 'sip3d/F','lostHits/I','convVeto/I','dxy/F','dz/F','charge/I','deltaEtaSC/F','mediumId/I','eleIndex/I','muIndex/I']
lepVarNames      = [x.split('/')[0] for x in lepVars]

# Training variables
read_variables = [\
    "weight/F", "nPDF/I", VectorTreeVariable.fromString( "PDF[Weight/F]", nMax=103), 
    "nscale/I", "scale[Weight/F]",
    "nJet/I", "nBTag/I", "nJetGood/I", "nlep/I",

    "JetGood[%s]"%(",".join(jetVars)),
    "Jet[%s]"%(",".join(jetVars)),
    "lep[%s]"%(",".join(lepVars)),

    "met_pt/F", "met_phi/F",
    "l1_pdgId/I", 
    "l1_pt/F",
    "l1_eta/F",
    "l1_phi/F",
    "year/I",
    "ht/F",
    "met_pt/F",

    "top_pt/F",
    "top_eta/F",
    "top_phi/F",
    "top_m/F",
    "top_other_pt/F",
    "top_other_eta/F",
    "top_other_phi/F",
    "top_other_m/F",
    "top_b_index/I",
    "W_pt/F",
    "W_eta/F",
    "W_phi/F",
    "W_m/F",
    "nu_pt/F",
    "nu_eta/F",
    "nu_phi/F",
    "nu_m/F",
    "mT/F",
    "mlb0/F",
    "mlb1/F",
    "pT_bb/F",
    "cosTheta_lb_topRF/F",
    "FW3/F",
    "FW0/F",
    "FW3_R/F",
    "DEta_l_b0/F",
    "DEta_l_b1/F",
    "DEta_top_b0/F",
    "DEta_top_b1/F",
    "Cos_DPhi_top_b0/F",
    "Cos_DPhi_top_b1/F",
    "cos_DPhi_l_met/F",

    "reweightTopPt/F",
    "reweightPU/F",
    "reweightPUUp/F",
    "reweightPUDown/F",
    "reweightL1Prefire/F",
    "reweightL1PrefireUp/F",
    "reweightL1PrefireDown/F",
    "reweightLeptonSF/F",
    "reweightLeptonSFUp/F",
    "reweightLeptonSFDown/F",
#    "reweightTrigger/F",
#    "reweightTriggerUp/F",
#    "reweightTriggerDown/F",
#    "reweightLeptonTrackingSF/F",
    #"reweightBTagSF_down_hf/F",
    #"reweightBTagSF_central/F",
    #"reweightBTagSF_up_cferr1/F",
    #"reweightBTagSF_up_jes/F",
    #"reweightBTagSF_down_cferr2/F",
    #"reweightBTagSF_up_lf/F",
    #"reweightBTagSF_down_lf/F",
    #"reweightBTagSF_down_cferr1/F",
    #"reweightBTagSF_up_lfstats2/F",
    #"reweightBTagSF_up_lfstats1/F",
    #"reweightBTagSF_up_cferr2/F",
    #"reweightBTagSF_up_hfstats1/F",
    #"reweightBTagSF_up_hfstats2/F",
    #"reweightBTagSF_down_lfstats2/F",
    #"reweightBTagSF_up_hf/F",
    #"reweightBTagSF_down_lfstats1/F",
    #"reweightBTagSF_down_hfstats2/F",
    #"reweightBTagSF_down_hfstats1/F",
    #"reweightBTagSF_down_jes/F",
    "reweightBTagSF1a_SF/F",
    "reweightBTagSF1a_SF_b_Down/F",
    "reweightBTagSF1a_SF_b_Up/F",
    "reweightBTagSF1a_SF_l_Down/F",
    "reweightBTagSF1a_SF_l_Up/F",
    ]
# sequence
sequence = []

from TT2lUnbinned.Tools.objectSelection import isBJet
def make_jets( event, sample ):
    event.jets     = [getObjDict(event, 'JetGood_', jetVarNames, i) for i in range(int(event.nJetGood))]
    event.bJets    = filter(lambda j:isBJet(j, year=event.year) and abs(j['eta'])<=2.4    , event.jets)
    event.bJets_medium = filter(lambda j:isBJet(j, WP="medium",year=event.year) and abs(j['eta'])<=2.4    , event.jets)
    event.bJets_loose = filter(lambda j:isBJet(j, WP="loose",year=event.year) and abs(j['eta'])<=2.4    , event.jets)
    event.bJets_tight = filter(lambda j:isBJet(j, WP="tight",year=event.year) and abs(j['eta'])<=2.4    , event.jets)
    
    event.nonbJets = []
    for b in event.jets:
        if b not in event.bJets:
            event.nonbJets.append(b)

    # store all btag flavors in a list
    event.btagDeepFlavB_scores = sorted([jet['btagDeepFlavB'] for jet in event.jets], reverse=True)
    event.sortedBJets = sorted(event.bJets, key=lambda x: x['btagDeepFlavB'], reverse=True)

sequence.append( make_jets )

all_mva_variables = {

     #Global Event Properties
     "jet0_pt"               :(lambda event, sample: event.JetGood_pt[0]          if event.nJetGood >=1 else 0),
     "jet0_eta"              :(lambda event, sample: event.JetGood_eta[0]         if event.nJetGood >=1 else -10),
     "jet0_btagDeepFlavB"    :(lambda event, sample: event.JetGood_btagDeepFlavB[0]   if (event.nJetGood >=1 and event.JetGood_btagDeepFlavB[0]>-10) else -10),
     "jet1_pt"               :(lambda event, sample: event.JetGood_pt[1]          if event.nJetGood >=2 else 0),
     "jet1_eta"              :(lambda event, sample: event.JetGood_eta[1]         if event.nJetGood >=2 else -10),
     "jet1_btagDeepFlavB"    :(lambda event, sample: event.JetGood_btagDeepFlavB[1]   if (event.nJetGood >=2 and event.JetGood_btagDeepFlavB[1]>-10) else -10),
     "jet2_pt"               :(lambda event, sample: event.JetGood_pt[2]          if event.nJetGood >=3 else 0),
     "jet2_eta"              :(lambda event, sample: event.JetGood_eta[2]         if event.nJetGood >=3 else -10),
     "jet2_btagDeepFlavB"    :(lambda event, sample: event.JetGood_btagDeepFlavB[2]   if (event.nJetGood >=3 and event.JetGood_btagDeepFlavB[2]>-10) else -10),

     "jet3_pt"               :(lambda event, sample: event.JetGood_pt[3]          if event.nJetGood >=4 else 0),
     "jet4_pt"               :(lambda event, sample: event.JetGood_pt[4]          if event.nJetGood >=5 else 0),
     "jet5_pt"               :(lambda event, sample: event.JetGood_pt[5]          if event.nJetGood >=6 else 0),
     "jet6_pt"               :(lambda event, sample: event.JetGood_pt[6]          if event.nJetGood >=7 else 0),
     "jet7_pt"               :(lambda event, sample: event.JetGood_pt[7]          if event.nJetGood >=8 else 0),

     "nBTagJetL"             :(lambda event, sample: len(filter( lambda j:isBJet(j, WP="loose"),  event.jets ))),
     "nBTagJetM"             :(lambda event, sample: len(filter( lambda j:isBJet(j, WP="medium"), event.jets ))),
     "nBTagJetT"             :(lambda event, sample: len(filter( lambda j:isBJet(j, WP="tight"),  event.jets ))),

     "bTagScore_max0"        :(lambda event, sample: event.btagDeepFlavB_scores[0] if len(event.btagDeepFlavB_scores)>0 else -1),
     "bTagScore_max1"        :(lambda event, sample: event.btagDeepFlavB_scores[1] if len(event.btagDeepFlavB_scores)>1 else -1),
     "bTagScore_max2"        :(lambda event, sample: event.btagDeepFlavB_scores[2] if len(event.btagDeepFlavB_scores)>2 else -1),
     "bTagScore_max3"        :(lambda event, sample: event.btagDeepFlavB_scores[3] if len(event.btagDeepFlavB_scores)>3 else -1),
     "recoLep0_pt"           :(lambda event, sample: event.l1_pt),
     "nBTag"                 :(lambda event, sample: event.nBTagJetM),
     "nrecoJet"              :(lambda event, sample: event.nJetGood),
}

for var in [
    "weight",   
    "met_pt", "nJetGood", "nBTag", 
    "l1_pt", "l1_eta", "l1_phi", 
    "year",  
    "ht", "met_pt", 

    "top_pt",
    "top_eta",
    "top_phi",
    "top_m",
    "top_other_pt",
    "top_other_eta",
    "top_other_phi",
    "top_other_m",
    "W_pt",
    "W_eta",
    "W_phi",
    "W_m",
    "nu_pt",
    "nu_eta",
    "nu_phi",
    "nu_m",
    "mT",
    "mlb0",
    "mlb1",
    "pT_bb",
    "cosTheta_lb_topRF",
    "FW3",
    "FW0",
    "FW3_R",
    "DEta_l_b0",
    "DEta_l_b1",
    "DEta_top_b0",
    "DEta_top_b1",
    "Cos_DPhi_top_b0",
    "Cos_DPhi_top_b1",
    "cos_DPhi_l_met",

    "reweightTopPt",
    "reweightPU",
    "reweightPUUp",
    "reweightPUDown",
    "reweightL1Prefire",
    "reweightL1PrefireUp",
    "reweightL1PrefireDown",
    "reweightLeptonSF",
    "reweightLeptonSFUp",
    "reweightLeptonSFDown",
    #"reweightTrigger",
    #"reweightTriggerUp",
    #"reweightTriggerDown",
    #"reweightLeptonTrackingSF",
    #"reweightBTagSF_down_hf",
    #"reweightBTagSF_central",
    #"reweightBTagSF_up_cferr1",
    #"reweightBTagSF_up_jes",
    #"reweightBTagSF_down_cferr2",
    #"reweightBTagSF_up_lf",
    #"reweightBTagSF_down_lf",
    #"reweightBTagSF_down_cferr1",
    #"reweightBTagSF_up_lfstats2",
    #"reweightBTagSF_up_lfstats1",
    #"reweightBTagSF_up_cferr2",
    #"reweightBTagSF_up_hfstats1",
    #"reweightBTagSF_up_hfstats2",
    #"reweightBTagSF_down_lfstats2",
    #"reweightBTagSF_up_hf",
    #"reweightBTagSF_down_lfstats1",
    #"reweightBTagSF_down_hfstats2",
    #"reweightBTagSF_down_hfstats1",
    #"reweightBTagSF_down_jes",
    "reweightBTagSF1a_SF",
    "reweightBTagSF1a_SF_b_Down",
    "reweightBTagSF1a_SF_b_Up",
    "reweightBTagSF1a_SF_l_Down",
    "reweightBTagSF1a_SF_l_Up",

]:
    all_mva_variables[var] = (lambda event, sample, var=var: getattr( event, var ))

#def lstm_jets(event, sample):
#    jets = [ getObjDict( event, 'Jet_', lstm_jetVarNames, event.JetGood_index[i] ) for i in range(int(event.nJetGood)) ]
#    #jets = filter( jet_vector_var['selector'], jets )
#    return jets

def PDF_Weight(event, sample):
    return  [ getObjDict( event, 'PDF_', ["Weight"], i ) for i in range(int(event.nPDF)) ]
def scale_Weight(event, sample):
    #print  [ getObjDict( event, 'scale_', ["Weight"], i ) for i in range(int(event.nscale)) ]
    return  [ getObjDict( event, 'scale_', ["Weight"], i ) for i in range(int(event.nscale)) ]

# for the filler
mva_vector_variables    =   {
    #"PDF":  {"name":"PDF", "vars":["Weight/F"], "varnames":["Weight"], "func": (lambda event, sample: [{'Weight':event.PDF_Weight[i]} for i in range(int(event.nPDF))]), 'maxN':103}
    "PDF":  {"name":"PDF", "vars":["Weight/F"], "varnames":["Weight"], "func": PDF_Weight, 'maxN':103},
    "scale": {"name":"scale", "vars":["Weight/F"], "varnames":["Weight"], "func": scale_Weight, 'maxN':9}
}


## Using all variables
mva_variables_ = all_mva_variables.keys()
mva_variables_.sort()
mva_variables  = [ (key, value) for key, value in all_mva_variables.iteritems() if key in mva_variables_ ]

import numpy as np
import operator

#directory_ = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/"
#def make_dirs( name, selection='dilep', eras = ["UL2016_preVFP", "UL2016", "UL2017", "UL2018"]):
#    return [ os.path.join( directory_, dir_ , selection, name) for dir_ in eras ]
#
#from TT2lUnbinned.Samples.color import color
#
#TTLep_RunII = Sample.fromDirectory(name="TTLep_RunII", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( 'TTLep_pow_CP5'))
#TTLep_UL2016_preVFP = Sample.fromDirectory(name="TTLep_UL2016_preVFP", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( 'TTLep_pow_CP5', eras=['UL2016_preVFP']))
#TTLep_UL2016= Sample.fromDirectory(name="TTLep_UL2016", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( 'TTLep_pow_CP5', eras=['UL2016']))
#TTLep_UL2017= Sample.fromDirectory(name="TTLep_UL2017", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( 'TTLep_pow_CP5', eras=['UL2017']))
#TTLep_UL2018= Sample.fromDirectory(name="TTLep_UL2018", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( 'TTLep_pow_CP5', eras=['UL2018']))

#define training samples for multiclassification
import TT2lUnbinned.Samples.nano_mc_UL20_singlelep_njet2p_met30_postProcessed as samples

training_samples = [
    samples.TBar_tWch_Summer16_preVFP,
    samples.TBar_tch_pow_Summer16_preVFP,
    samples.TTLep_pow_CP5_Summer16_preVFP,
    samples.TTSingleLep_pow_CP5_Summer16_preVFP,
    samples.T_tWch_Summer16_preVFP,
    samples.T_tch_pow_Summer16_preVFP,
    samples.t_sch_Summer16_preVFP,
    samples.ST_tWch_Summer16_preVFP,
    samples.ST_tch_pow_Summer16_preVFP,
    samples.TT_Summer16_preVFP,
    
    samples.TBar_tWch_Summer16,
    samples.TBar_tch_pow_Summer16,
    samples.TTLep_pow_CP5_Summer16,
    samples.TTSingleLep_pow_CP5_Summer16,
    samples.T_tWch_Summer16,
    samples.T_tch_pow_Summer16,
    samples.t_sch_Summer16,
    samples.ST_tWch_Summer16,
    samples.ST_tch_pow_Summer16,
    samples.TT_Summer16,

    samples.TBar_tWch_Fall17,
    samples.TBar_tch_pow_Fall17,
    samples.TTLep_pow_CP5_Fall17,
    samples.TTSingleLep_pow_CP5_Fall17,
    samples.T_tWch_Fall17,
    samples.T_tch_pow_Fall17,
    samples.t_sch_Fall17,
    samples.ST_tWch_Fall17,
    samples.ST_tch_pow_Fall17,
    samples.TT_Fall17,

    samples.TBar_tWch_Autumn18,
    samples.TBar_tch_pow_Autumn18,
    samples.TTLep_pow_CP5_Autumn18,
    samples.TTSingleLep_pow_CP5_Autumn18,
    samples.T_tWch_Autumn18,
    samples.T_tch_pow_Autumn18,
    samples.t_sch_Autumn18,
    samples.ST_tWch_Autumn18,
    samples.ST_tch_pow_Autumn18,
    samples.TT_Autumn18,

    samples.TBar_tWch,
    samples.TBar_tch_pow,
    samples.TTLep_pow_CP5,
    samples.TTSingleLep_pow_CP5,
    samples.T_tWch,
    samples.T_tch_pow,
    samples.t_sch,
    samples.ST_tWch,
    samples.ST_tch_pow,
    samples.TT,
    
    ]

assert len(training_samples)==len(set([s.name for s in training_samples])), "training_samples names are not unique!"

# training selection

#selection = 'tr-minDLmass20-dilepM-offZ1-njet2p-mtt750'
selection = 'singlelep-njet2p-met30'
from TT2lUnbinned.Tools.cutInterpreter import cutInterpreter
selectionString = cutInterpreter.cutString( selection )
