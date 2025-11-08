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

jes_systematics = [
    #"jesTotal",
    #"jesAbsoluteMPFBias",
    #"jesAbsoluteScale",
    #"jesAbsoluteStat",
    #"jesRelativeBal",
    #"jesRelativeFSR",
    #"jesRelativePtBB",
    #"jesRelativeStatFSR",
    #"jesPileUpDataMC",
    #"jesPileUpPtBB",
    #"jesPileUpPtRef",
    #"jesFlavorQCD",
    #"jesFragmentation",
    #"jesSinglePionECAL",
    #"jesSinglePionHCAL",
    #"jesTimePtEta",
    "jesTotal",
#    "jesTimePtEta",
#    "jesSubTotalPileUp",
#    "jesSubTotalRelative",
#    "jesSubTotalPt",
#    "jesSubTotalScale",
#    "jesSubTotalAbsolute",
#    "jesSubTotalMC",
#    "jesTotalNoFlavor",
#    "jesTotalNoTime",
#    "jesTotalNoFlavorNoTime",
]


#eras = ["UL2016", "UL2016_preVFP", "UL2017", "UL2018"]
eras = [ "UL2018"]

TTLep_0p5    = Sample.fromDirectory( "TTLep_0p5", directory = ['/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v9_JEC0p5/%s/dilep/TTLep_pow_CP5/'%era for era in eras]) 
TTLep_0p5.texName = "t#bar{t} 0.5#sigma"
TTLep_0p5.color   = ROOT.kBlue + 1

TTLep    = Sample.fromDirectory( "TTLep_nominal", directory = ['/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v9/%s/dilep/TTLep_pow_CP5/'%era for era in eras]) 
TTLep.texName = "t#bar{t} nominal"
TTLep.color   = ROOT.kBlue 

TTLep_1p5    = Sample.fromDirectory( "TTLep_1p5", directory = ['/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v9_JEC1p5/%s/dilep/TTLep_pow_CP5/'%era for era in eras])
TTLep_1p5.texName = "t#bar{t} 1.5#sigma"
TTLep_1p5.color   = ROOT.kBlue + 3

TTLep_2p0    = Sample.fromDirectory( "TTLep_1p5", directory = ['/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v9_JEC2p0/%s/dilep/TTLep_pow_CP5/'%era for era in eras]) 
TTLep_2p0.texName = "t#bar{t} 2#sigma"
TTLep_2p0.color   = ROOT.kBlue + 4


# training selection
selection = 'minDLmass20-dilepM-offZ1'
from TT2lUnbinned.Tools.cutInterpreter import cutInterpreter
selectionString = cutInterpreter.cutString( selection )

def getCut( var, upDown, mtt=500, nJetGood=3, nBTag=2):
    if var or upDown:
        return 'tr_ttbar_mass_{var}{upDown}>={mtt}&&nJetGood_{var}{upDown}>={nJetGood}&&nBTag_{var}{upDown}>={nBTag}'.format( var=var, upDown=upDown, mtt=mtt, nJetGood=nJetGood, nBTag=nBTag)
    else:
        return 'tr_ttbar_mass>={mtt}&&nJetGood>={nJetGood}&&nBTag>={nBTag}'.format( mtt=mtt, nJetGood=nJetGood, nBTag=nBTag)

read_variables = [
    "l12_pt/F",
    "l12_mass/F",
    "l1_pdgId/I", "l2_pdgId/I",
    "l1_pt/F",
    "l1_eta/F",
    "l1_phi/F",
    "l2_pt/F",
    "l2_eta/F",
    "l2_phi/F",
]

sys_scalar_variables = [#"MET_T1_pt{var}/F", 
     "ht{var}/F", "nJetGood{var}/I", "nBTag{var}/I",
    "tr_neutrino_pt{var}/F", "tr_neutrino_eta{var}/F", "tr_neutrinoBar_pt{var}/F", "tr_neutrinoBar_eta{var}/F",
    "tr_ttbar_pt{var}/F", "tr_ttbar_eta{var}/F", "tr_ttbar_mass{var}/F",
    "tr_top_pt{var}/F", "tr_top_eta{var}/F", "tr_top_mass{var}/F",
    "tr_topBar_pt{var}/F", "tr_topBar_eta{var}/F", "tr_topBar_mass{var}/F",
    "tr_Wminus_pt{var}/F", "tr_Wminus_eta{var}/F", "tr_Wminus_mass{var}/F",
    "tr_Wplus_pt{var}/F", "tr_Wplus_eta{var}/F", "tr_Wplus_mass{var}/F",
    "tr_ttbar_dAbsEta{var}/F", "tr_ttbar_dEta{var}/F",
    "tr_cosThetaPlus_n{var}/F", "tr_cosThetaMinus_n{var}/F", "tr_cosThetaPlus_r{var}/F", "tr_cosThetaMinus_r{var}/F", "tr_cosThetaPlus_k{var}/F", "tr_cosThetaMinus_k{var}/F",
    "tr_cosThetaPlus_r_star{var}/F", "tr_cosThetaMinus_r_star{var}/F", "tr_cosThetaPlus_k_star{var}/F", "tr_cosThetaMinus_k_star{var}/F",
    "tr_xi_nn{var}/F", "tr_xi_rr{var}/F", "tr_xi_kk{var}/F",
    "tr_xi_nr_plus{var}/F", "tr_xi_nr_minus{var}/F", "tr_xi_rk_plus{var}/F", "tr_xi_rk_minus{var}/F", "tr_xi_nk_plus{var}/F", "tr_xi_nk_minus{var}/F",
    "tr_cos_phi{var}/F", "tr_cos_phi_lab{var}/F", "tr_abs_delta_phi_ll_lab{var}/F",
    "tr_xi_r_star_k{var}/F", "tr_xi_k_r_star{var}/F", "tr_xi_kk_star{var}/F",
] 
sys_vector_variables = ["JetGood[pt{var}/F,eta/F,btagDeepFlavB/F]"]

replacements         = [(variable.format(var='').split('/')[0], variable.split('/')[0]) for variable in sys_scalar_variables]
replacements        += [("JetGood_pt", "JetGood_pt{var}")]

training_samples = [TTLep]
training_samples[-1].postfix=None
training_samples[-1].read_variables = [variable.format(var='') for variable in sys_scalar_variables+sys_vector_variables] 
training_samples[-1].replacements = []
training_samples[-1].setSelectionString( getCut(None, None) )
for sigma, sample in [(0.5, TTLep_0p5), (1.0, TTLep), (1.5, TTLep_1p5), (2.0, TTLep_2p0)]:
    for upDown in ['Up', 'Down']:
        for var in jes_systematics:
            training_sample = copy.deepcopy(sample)
            training_sample.name = ("TTLep_%2.1f_%s%s"%( sigma, var, upDown)).replace('.', 'p')
            training_sample.setSelectionString( getCut(var, upDown) )

            training_sample.read_variables = [variable.format(var='_'+var+upDown) for variable in sys_scalar_variables+sys_vector_variables]
            training_sample.replacements   = [(r[0], r[1].format(var='_'+var+upDown)) for r in replacements]
            training_samples.append( training_sample )

def copy( event, sample):
    for rep in sample.replacements:
            setattr( event, rep[0], getattr( event, rep[1]) ) 

sequence = [copy]

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

     "recoLep0_pt"           :(lambda event, sample: event.l1_pt),
     "recoLep1_pt"           :(lambda event, sample: event.l2_pt),
     "recoLepPos_pt"         :(lambda event, sample: event.l1_pt if event.l1_pdgId<0 else event.l2_pt),
     "recoLepNeg_pt"         :(lambda event, sample: event.l1_pt if event.l1_pdgId>0 else event.l2_pt),
     "recoLep01_pt"          :(lambda event, sample: event.l12_pt),
     "recoLep01_mass"        :(lambda event, sample: event.l12_mass),
     "recoLep_dEta"          :(lambda event, sample: (event.l1_eta if event.l1_pdgId<0 else event.l2_eta) - (event.l1_eta if event.l1_pdgId>0 else event.l2_eta)),
     "recoLep_dAbsEta"       :(lambda event, sample: (abs(event.l1_eta) if event.l1_pdgId<0 else abs(event.l2_eta)) - (abs(event.l1_eta) if event.l1_pdgId>0 else abs(event.l2_eta))),
     "nBTag"                 :(lambda event, sample: event.nBTag),
     "nrecoJet"              :(lambda event, sample: event.nJetGood),
     "tr_neutrino_pt"        : (lambda event, sample : event.tr_neutrino_pt),
     "tr_neutrino_eta"      : (lambda event, sample : event.tr_neutrino_eta),
     "tr_neutrinoBar_pt"    : (lambda event, sample : event.tr_neutrinoBar_pt),
     "tr_neutrinoBar_eta"   : (lambda event, sample : event.tr_neutrinoBar_eta),
     "tr_ttbar_pt"          : (lambda event, sample : event.tr_ttbar_pt),
     "tr_ttbar_eta"         : (lambda event, sample : event.tr_ttbar_eta),
     "tr_ttbar_mass"        : (lambda event, sample : event.tr_ttbar_mass),
     "tr_top_pt"            : (lambda event, sample : event.tr_top_pt),
     "tr_top_eta"           : (lambda event, sample : event.tr_top_eta),
     "tr_top_mass"          : (lambda event, sample : event.tr_top_mass),
     "tr_topBar_pt"         : (lambda event, sample : event.tr_topBar_pt),
     "tr_topBar_eta"        : (lambda event, sample : event.tr_topBar_eta),
     "tr_topBar_mass"       : (lambda event, sample : event.tr_topBar_mass),
     "tr_Wminus_pt"         : (lambda event, sample : event.tr_Wminus_pt),
     "tr_Wminus_eta"        : (lambda event, sample : event.tr_Wminus_eta),
     "tr_Wminus_mass"       : (lambda event, sample : event.tr_Wminus_mass),
     "tr_Wplus_pt"          : (lambda event, sample : event.tr_Wplus_pt),
     "tr_Wplus_eta"         : (lambda event, sample : event.tr_Wplus_eta),
     "tr_Wplus_mass"        : (lambda event, sample : event.tr_Wplus_mass),
     "tr_ttbar_dAbsEta"     : (lambda event, sample : event.tr_ttbar_dAbsEta),
     "tr_ttbar_dEta"        : (lambda event, sample : event.tr_ttbar_dEta),
     "tr_cosThetaPlus_n"    : (lambda event, sample : event.tr_cosThetaPlus_n),
     "tr_cosThetaMinus_n"   : (lambda event, sample : event.tr_cosThetaMinus_n),
     "tr_cosThetaPlus_r"    : (lambda event, sample : event.tr_cosThetaPlus_r),
     "tr_cosThetaMinus_r"   : (lambda event, sample : event.tr_cosThetaMinus_r),
     "tr_cosThetaPlus_k"    : (lambda event, sample : event.tr_cosThetaPlus_k),
     "tr_cosThetaMinus_k"   : (lambda event, sample : event.tr_cosThetaMinus_k),
     "tr_cosThetaPlus_r_star": (lambda event, sample : event.tr_cosThetaPlus_r_star),
     "tr_cosThetaMinus_r_star": (lambda event, sample : event.tr_cosThetaMinus_r_star),
     "tr_cosThetaPlus_k_star": (lambda event, sample : event.tr_cosThetaPlus_k_star),
     "tr_cosThetaMinus_k_star": (lambda event, sample : event.tr_cosThetaMinus_k_star),
     "tr_xi_nn"             : (lambda event, sample : event.tr_xi_nn),
     "tr_xi_rr"             : (lambda event, sample : event.tr_xi_rr),
     "tr_xi_kk"             : (lambda event, sample : event.tr_xi_kk),
     "tr_xi_nr_plus"        : (lambda event, sample : event.tr_xi_nr_plus),
     "tr_xi_nr_minus"       : (lambda event, sample : event.tr_xi_nr_minus),
     "tr_xi_rk_plus"        : (lambda event, sample : event.tr_xi_rk_plus),
     "tr_xi_rk_minus"       : (lambda event, sample : event.tr_xi_rk_minus),
     "tr_xi_nk_plus"        : (lambda event, sample : event.tr_xi_nk_plus),
     "tr_xi_nk_minus"       : (lambda event, sample : event.tr_xi_nk_minus),
     "tr_cos_phi"           : (lambda event, sample : event.tr_cos_phi),
     "tr_cos_phi_lab"       : (lambda event, sample : event.tr_cos_phi_lab),
     "tr_abs_delta_phi_ll_lab": (lambda event, sample : event.tr_abs_delta_phi_ll_lab),
     "tr_xi_r_star_k"       : (lambda event, sample : event.tr_xi_r_star_k),
     "tr_xi_k_r_star"       : (lambda event, sample : event.tr_xi_k_r_star),
     "tr_xi_kk_star"        : (lambda event, sample : event.tr_xi_kk_star),
}

# for the filler
mva_vector_variables    =   {
}

## Using all variables
mva_variables_ = all_mva_variables.keys()
mva_variables_.sort()
mva_variables  = [ (key, value) for key, value in all_mva_variables.iteritems() if key in mva_variables_ and not "reweightBTagSF" in key ]

import numpy as np
import operator

#def predict_inputs( event, sample):
#    return np.array([[getattr( event, mva_variable) for mva_variable, _ in mva_variables]])

classes          = [ ]

assert len(training_samples)==len(set([s.name for s in training_samples])), "training_samples names are not unique!"
