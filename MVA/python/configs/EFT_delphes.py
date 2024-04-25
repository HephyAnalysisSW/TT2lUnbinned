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

jetVars          = ['pt/F', 'eta/F', 'phi/F', 'bTag/I']

jetVarNames      = [x.split('/')[0] for x in jetVars]

lepVars          = ['pt/F','eta/F','phi/F','pdgId/I',]
lepVarNames      = [x.split('/')[0] for x in lepVars]

# Training variables
read_variables = [\
    "weight1fb/F", 
    "nrecoJet/I", "nBTag/I", "nrecoLep/I",

    "recoJet[%s]"%(",".join(jetVars)),
    "recoLep[%s]"%(",".join(lepVars)),

    "recoLepPos_pt/F", "recoLepNeg_pt/F",
    "recoLep_dEta/F", "recoLep_dAbsEta/F",

    "recoMet_pt/F", "recoMet_phi/F",
    "recoLep0_pt/F",
    "recoLep0_eta/F",
    "recoLep1_pt/F",
    "recoLep1_eta/F",

    "recoLep01_pt/F",
    "recoLep01_mass/F",
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

    ]
# sequence
sequence = []

from TT2lUnbinned.Tools.objectSelection import isBJet
def make_jets( event, sample ):
    event.jets     = [getObjDict(event, 'nrecoJet_', jetVarNames, i) for i in range(int(event.nrecoJet))]
    event.bJets    = filter(lambda j:j['bTag'] and abs(j['eta'])<=2.4    , event.jets)
    
    event.nonbJets = []
    for b in event.jets:
        if b not in event.bJets:
            event.nonbJets.append(b)

sequence.append( make_jets )

all_mva_variables = {

     #Global Event Properties
     "jet0_pt"               :(lambda event, sample: event.recoJet_pt[0]          if event.nrecoJet >=1 else 0),
     "jet0_eta"              :(lambda event, sample: event.recoJet_eta[0]         if event.nrecoJet >=1 else -10),
     "jet0_bTag"             :(lambda event, sample: event.recoJet_bTag[0]   if (event.nrecoJet >=1 and event.recoJet_bTag[0]>-10) else -10),
     "jet1_pt"               :(lambda event, sample: event.recoJet_pt[1]          if event.nrecoJet >=2 else 0),
     "jet1_eta"              :(lambda event, sample: event.recoJet_eta[1]         if event.nrecoJet >=2 else -10),
     "jet1_bTag"             :(lambda event, sample: event.recoJet_bTag[1]   if (event.nrecoJet >=2 and event.recoJet_bTag[1]>-10) else -10),
     "jet2_pt"               :(lambda event, sample: event.recoJet_pt[2]          if event.nrecoJet >=3 else 0),
     "jet2_eta"              :(lambda event, sample: event.recoJet_eta[2]         if event.nrecoJet >=3 else -10),
     "jet2_bTag"             :(lambda event, sample: event.recoJet_bTag[2]   if (event.nrecoJet >=3 and event.recoJet_bTag[2]>-10) else -10),

     "jet3_pt"               :(lambda event, sample: event.recoJet_pt[3]          if event.nrecoJet >=4 else 0),
     "jet4_pt"               :(lambda event, sample: event.recoJet_pt[4]          if event.nrecoJet >=5 else 0),
     "jet5_pt"               :(lambda event, sample: event.recoJet_pt[5]          if event.nrecoJet >=6 else 0),
     "jet6_pt"               :(lambda event, sample: event.recoJet_pt[6]          if event.nrecoJet >=7 else 0),
     "jet7_pt"               :(lambda event, sample: event.recoJet_pt[7]          if event.nrecoJet >=8 else 0),

}

for var in [
    "weight1fb",   
    "recoMet_pt", "nrecoJet", "nBTag", 
    "recoLep0_pt", "recoLep0_eta", "recoLep1_pt", "recoLep1_eta",
    "recoLep01_pt", "recoLep01_mass",
    "recoLepPos_pt", "recoLepNeg_pt",
    "recoLep_dEta", "recoLep_dAbsEta",
    "nrecoLep",
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

]:
    all_mva_variables[var] = (lambda event, sample, var=var: getattr( event, var ))

# for the filler
mva_vector_variables    =   {
}


## Using all variables
mva_variables_ = all_mva_variables.keys()
mva_variables_.sort()
mva_variables  = [ (key, value) for key, value in all_mva_variables.iteritems() if key in mva_variables_ ]

import numpy as np
import operator

#define training samples for multiclassification
import TT2lUnbinned.Samples.delphes_RunII_postProcessed as samples

training_samples = [ 
    samples.TT01j2lCAOldRef_Mtt500_ext,
    samples.TTLep,
    #samples.TTLep_hdampDOWN,
    #samples.TTLep_hdampUP,
    samples.ST_tW_antitop_fakeB1,
    samples.ST_tW_top_fakeB1,
    samples.DYJetsToLL_M50_HT_fakeB2,
    ]

# Add weight infos
for sample in training_samples:
    sample.read_variables = []
    if hasattr( sample, "reweight_pkl" ):
        sample.weightInfo = WeightInfo( sample.reweight_pkl )
        sample.weightInfo.set_order(2)
        sample.read_variables += [
                VectorTreeVariable.fromString( "p[C/F]", nMax=len(sample.weightInfo.combinations) ),
            ]

powheg_read_variables = [
    "muR0p5_muF0p5/F", "muR0p5_muF2p0/F", "muR0p5_muF1p0/F", "muR2p0_muF0p5/F", "muR2p0_muF2p0/F", "muR2p0_muF1p0/F", "muR1p0_muF0p5/F", "muR1p0_muF2p0/F", "muR1p0_muF1p0/F", 
    "isrRedHi/F", "fsrRedHi/F", "isrRedLo/F", "fsrRedLo/F", "isrDefHi/F", "fsrDefHi/F", "fsrDefLo/F", 
    "isrConHi/F", "isrConLo/F", "fsrConLo/F", "isrRedHi/F", "fsrRedHi/F", "isrRedLo/F", "fsrRedLo/F", 
    "isrDefHi/F", "fsrDefHi/F", "isrDefLo/F", "fsrDefLo/F", "isrConHi/F", "fsrConHi/F", "isrConLo/F", "fsrConLo/F",
] 
samples.TTLep.read_variables  += powheg_read_variables
samples.TTLep.extra_variables = powheg_read_variables
#def extra_sequence( event, sample):
#    for var in powheg_read_variables:
#        getattr( event, var )

assert len(training_samples)==len(set([s.name for s in training_samples])), "training_samples names are not unique!"

# training selection
#selection = 'dilep-offZ-njet3p-btag2p'
selection = 'dilep-offZ-njet3p-btag2p-mtt750'
from TT2lUnbinned.Tools.delphesCutInterpreter import cutInterpreter
selectionString = cutInterpreter.cutString( selection )
