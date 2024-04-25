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
    "l1_pt/F",
    "l1_eta/F",
    "l1_phi/F",
    "l2_pt/F",
    "l2_eta/F",
    "l2_phi/F",
    "year/I",
    "overflow_counter_v1/I",
    "overflow_counter_v2/I",
    "ht/F",
    "met_pt/F",
    "Z1_pt/F",
    "Z1_mass/F",
    "minDLmass/F",
    "l12_pt/F",
    "l12_mass/F",
    "tr_neutrino_pt/F", "tr_neutrino_eta/F", "tr_neutrinoBar_pt/F", "tr_neutrinoBar_eta/F",
    "tr_ttbar_pt/F", "tr_ttbar_eta/F", "tr_ttbar_mass/F", 
    "tr_top_pt/F", "tr_top_eta/F", "tr_top_mass/F", 
    "tr_topBar_pt/F", "tr_topBar_eta/F", "tr_topBar_mass/F", 
    "tr_Wminus_pt/F", "tr_Wminus_eta/F", "tr_Wminus_mass/F", 
    "tr_Wplus_pt/F", "tr_Wplus_eta/F", "tr_Wplus_mass/F",
    "tr_ttbar_dAbsEta/F", "tr_ttbar_dEta/F",
    "tr_cosThetaPlus_n/F", "tr_cosThetaMinus_n/F", "tr_cosThetaPlus_r/F", "tr_cosThetaMinus_r/F", "tr_cosThetaPlus_k/F", "tr_cosThetaMinus_k/F",
    "tr_cosThetaPlus_r_star/F", "tr_cosThetaMinus_r_star/F", "tr_cosThetaPlus_k_star/F", "tr_cosThetaMinus_k_star/F",
    "tr_xi_nn/F", "tr_xi_rr/F", "tr_xi_kk/F",
    "tr_xi_nr_plus/F", "tr_xi_nr_minus/F", "tr_xi_rk_plus/F", "tr_xi_rk_minus/F", "tr_xi_nk_plus/F", "tr_xi_nk_minus/F",
    "tr_xi_r_star_k/F", "tr_xi_k_r_star/F", "tr_xi_kk_star/F",
    "tr_cos_phi/F", "tr_cos_phi_lab/F", "tr_abs_delta_phi_ll_lab/F",

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
    "reweightTrigger/F",
    "reweightTriggerUp/F",
    "reweightTriggerDown/F",
    "reweightLeptonTrackingSF/F",
    "reweightBTagSF_down_hf/F",
    "reweightBTagSF_central/F",
    "reweightBTagSF_up_cferr1/F",
    "reweightBTagSF_up_jes/F",
    "reweightBTagSF_down_cferr2/F",
    "reweightBTagSF_up_lf/F",
    "reweightBTagSF_down_lf/F",
    "reweightBTagSF_down_cferr1/F",
    "reweightBTagSF_up_lfstats2/F",
    "reweightBTagSF_up_lfstats1/F",
    "reweightBTagSF_up_cferr2/F",
    "reweightBTagSF_up_hfstats1/F",
    "reweightBTagSF_up_hfstats2/F",
    "reweightBTagSF_down_lfstats2/F",
    "reweightBTagSF_up_hf/F",
    "reweightBTagSF_down_lfstats1/F",
    "reweightBTagSF_down_hfstats2/F",
    "reweightBTagSF_down_hfstats1/F",
    "reweightBTagSF_down_jes/F",

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

#def make_leptons(event, sample):
#    event.leptons   = [getObjDict(event, 'lep_', lepVarNames, i) for i in range(int(event.nlep))]
#
#    #(Second) smallest dR between any lepton and medium b-tagged jet
#    dR_vals = sorted([deltaR(event.bJets[i], event.leptons[j]) for i in range(len(event.bJets)) for j in range(len(event.leptons))])
#    if len(dR_vals)>=2:
#        event.dR_min0 = dR_vals[0]
#        event.dR_min1 = dR_vals[1]
#    else:
#        event.dR_min0 = -1
#        event.dR_min1 = -1
#
#sequence.append(make_leptons)

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
}

for var in [
    "weight",   
    "met_pt", "nJetGood", "nBTag", 
    "l1_pt", "l1_eta", "l1_phi", "l2_pt", "l2_eta", "l2_phi",
    "year", "overflow_counter_v1", "overflow_counter_v2", 
    "ht", "met_pt", "Z1_pt", "Z1_mass", "minDLmass", "l12_pt", "l12_mass",
    "tr_neutrino_pt", "tr_neutrino_eta", "tr_neutrinoBar_pt", "tr_neutrinoBar_eta",
    "tr_ttbar_pt", "tr_ttbar_eta", "tr_ttbar_mass",
    "tr_top_pt", "tr_top_eta", "tr_top_mass",
    "tr_topBar_pt", "tr_topBar_eta", "tr_topBar_mass",
    "tr_Wminus_pt", "tr_Wminus_eta", "tr_Wminus_mass",
    "tr_Wplus_pt", "tr_Wplus_eta", "tr_Wplus_mass",
    "tr_ttbar_dAbsEta", "tr_ttbar_dEta",
    "tr_cosThetaPlus_n", "tr_cosThetaMinus_n", "tr_cosThetaPlus_r", "tr_cosThetaMinus_r", "tr_cosThetaPlus_k", "tr_cosThetaMinus_k",
    "tr_cosThetaPlus_r_star", "tr_cosThetaMinus_r_star", "tr_cosThetaPlus_k_star", "tr_cosThetaMinus_k_star",
    "tr_xi_nn", "tr_xi_rr", "tr_xi_kk",
    "tr_xi_nr_plus", "tr_xi_nr_minus", "tr_xi_rk_plus", "tr_xi_rk_minus", "tr_xi_nk_plus", "tr_xi_nk_minus",
    "tr_cos_phi", "tr_cos_phi_lab", "tr_abs_delta_phi_ll_lab",
    "tr_xi_r_star_k", "tr_xi_k_r_star", "tr_xi_kk_star",

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
    "reweightTrigger",
    "reweightTriggerUp",
    "reweightTriggerDown",
    "reweightLeptonTrackingSF",
    "reweightBTagSF_down_hf",
    "reweightBTagSF_central",
    "reweightBTagSF_up_cferr1",
    "reweightBTagSF_up_jes",
    "reweightBTagSF_down_cferr2",
    "reweightBTagSF_up_lf",
    "reweightBTagSF_down_lf",
    "reweightBTagSF_down_cferr1",
    "reweightBTagSF_up_lfstats2",
    "reweightBTagSF_up_lfstats1",
    "reweightBTagSF_up_cferr2",
    "reweightBTagSF_up_hfstats1",
    "reweightBTagSF_up_hfstats2",
    "reweightBTagSF_down_lfstats2",
    "reweightBTagSF_up_hf",
    "reweightBTagSF_down_lfstats1",
    "reweightBTagSF_down_hfstats2",
    "reweightBTagSF_down_hfstats1",
    "reweightBTagSF_down_jes",

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

#define training samples for multiclassification
import TT2lUnbinned.Samples.nano_UL20_RunII_postProcessed as samples

training_samples = [ 
#    samples.TT01j2lCAv2Ref_HT500,
#    samples.TTLep,
#    samples.TTLep_pow_CP5_hUp,
#    samples.TTLep_pow_CP5_hDown,
#
#    samples.ST,
#    samples.TTW,
#    samples.TTZ,
#    samples.TTH,
#    samples.DY,
#    samples.DiBoson,

    ]

# Add weight infos
for sample in training_samples:
    if hasattr( sample, "reweight_pkl" ):
        sample.weightInfo = WeightInfo( sample.reweight_pkl )
        sample.weightInfo.set_order(2)
        sample.read_variables = [
                VectorTreeVariable.fromString( "p[C/F]", nMax=len(sample.weightInfo.combinations) ),
            ]

assert len(training_samples)==len(set([s.name for s in training_samples])), "training_samples names are not unique!"

# training selection

#selection = 'tr-minDLmass20-dilepL-offZ1-njet3p-btag2p-ht500'
selection = 'tr-minDLmass20-dilepM-offZ1-njet3p-btagM2p-mtt750'
from TT2lUnbinned.Tools.cutInterpreter import cutInterpreter
selectionString = cutInterpreter.cutString( selection )
