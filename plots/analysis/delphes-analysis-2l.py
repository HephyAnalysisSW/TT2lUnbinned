#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
import itertools
import copy
import array
import operator
from   math                              import sqrt, cos, sin, pi, atan2, cosh

# RootTools
from RootTools.core.standard             import *

# TT2lUnbinned
from TT2lUnbinned.Tools.user                     import plot_directory
from TT2lUnbinned.Tools.delphesCutInterpreter    import cutInterpreter
from TT2lUnbinned.Tools.delphesObjectSelection   import mu_string, ele_string

# Analysis
from Analysis.Tools.helpers                      import deltaPhi, deltaR
from Analysis.Tools.puProfileCache               import *
from Analysis.Tools.puReweighting                import getReweightingFunction
import Analysis.Tools.syncer
from   Analysis.Tools.WeightInfo                 import WeightInfo

import numpy as np

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',          action='store_true', help='Run only on a small subset of the data?')
argParser.add_argument('--no_sorting',     action='store_true', help='Sort histos?', )
argParser.add_argument('--plot_directory', action='store', default='v1')
argParser.add_argument('--selection',      action='store', default='dilep-offZ-njet3p-btag2p-ht500')
args = argParser.parse_args()

# Logger
import TT2lUnbinned.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small: args.plot_directory += "_small"

# Simulated samples
from TT2lUnbinned.Samples.delphes_RunII_postProcessed import *

# group all the simulated backgroundsamples 
mc = [ TTLep ] 
#mc = [ TTLep] 
extra_selection = "1"

preselectionString = cutInterpreter.cutString(args.selection)

# Now we add the data
all_samples = mc 

# Here we compute the scaling of the simulation to the data luminosity (event.weight corresponds to 1/fb for simulation, hence we divide the data lumi in pb^-1 by 1000) 
lumi_scale = 137. 

# We're going to "scale" the simulation if "small" is true. So let's define a "scale" which will correct this
for sample in mc:
    sample.scale  = 1 

# For R&D we just use a fraction of the data
if args.small:
    for sample in mc :
        sample.normalization = 1.
        sample.reduceFiles( to = 5 )
        #sample.reduceFiles( to=1)
        sample.scale /= sample.normalization

# Helpers for putting text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right

def drawObjects( lumi_scale ):
    lines = [
      (0.15, 0.95, 'Delphes Simulation'), 
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale),
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots, mode):
  for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, 'delphes-analysisPlots', args.plot_directory, 'RunII', mode + ("_log" if log else ""), args.selection)
    for plot in plots:
      if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot

      _drawObjects = []

      if isinstance( plot, Plot):
          plotting.draw(plot,
            plot_directory = plot_directory_,
            ratio =   None,
            logX = False, logY = log, sorting = not args.no_sorting,
            yRange = (0.9, "auto") if log else (0.001, "auto"),
            scaling = {},
            legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
            drawObjects = drawObjects( lumi_scale ) + _drawObjects,
            copyIndexPHP = True, extensions = ["png", "pdf", "root"],
          )

read_variables = []

jetVars     = ['pt/F', 'eta/F', 'phi/F', 'bTag/I']#, 'btagDeepB/F', 'btagDeepFlavB/F' ]

jetVarNames     = [x.split('/')[0] for x in jetVars]

# the following we read for both, data and simulation 
read_variables += [
    "weight1fb/F", "recoMet_pt/F", "recoMet_phi/F", "nBTag/I", "nrecoJet/I",
    #"ht/F",
    "recoLep0_pt/F", "recoLep0_eta/F" , #"recoLep0_phi/F",  
    "recoLep1_pt/F", "recoLep1_eta/F" , #"recoLep1_phi/F",  
    "recoJet[%s]"%(",".join(jetVars)),
    "recoLep[pt/F,eta/F,phi/F,pdgId/I]",
    #"Z1_l1_index/I", "Z1_l2_index/I",  
    #"Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    #"Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I]",
    #"Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I]",

    "tr_neutrino_pt/F", "tr_neutrino_eta/F", "tr_neutrinoBar_pt/F", "tr_neutrinoBar_eta/F",
    "tr_ttbar_pt/F", "tr_ttbar_eta/F", "tr_ttbar_mass/F",
    "tr_top_pt/F", "tr_top_eta/F", "tr_top_mass/F", "tr_topBar_pt/F", "tr_topBar_eta/F", "tr_topBar_mass/F",
    "tr_Wminus_pt/F", "tr_Wminus_eta/F", "tr_Wminus_mass/F",
    "tr_Wplus_pt/F", "tr_Wplus_eta/F", "tr_Wplus_mass/F",
    "tr_cosThetaPlus_n/F", "tr_cosThetaMinus_n/F", "tr_cosThetaPlus_r/F", "tr_cosThetaMinus_r/F", "tr_cosThetaPlus_k/F", "tr_cosThetaMinus_k/F", "tr_cosThetaPlus_r_star/F", 
    "tr_cosThetaMinus_r_star/F", "tr_cosThetaPlus_k_star/F", "tr_cosThetaMinus_k_star/F",
    "tr_xi_nn/F", "tr_xi_rr/F", "tr_xi_kk/F", "tr_xi_nr_plus/F", "tr_xi_nr_minus/F", "tr_xi_rk_plus/F", "tr_xi_rk_minus/F", "tr_xi_nk_plus/F", "tr_xi_nk_minus/F",
    "tr_cos_phi/F", "tr_cos_phi_lab/F", "tr_abs_delta_phi_ll_lab/F",
    #"tr_top_decayAngle_phi/F", "tr_top_decayAngle_theta/F", 
    #"tr_topBar_decayAngle_phi/F", "tr_topBar_decayAngle_theta/F",
    "recoLep01_pt/F", "recoLep01_mass/F", 
]

# the following we read only in simulation
read_variables_MC = [
    #'reweightBTagSF_central/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightLeptonSF/F', 'reweightLeptonSFDown/F', 'reweightLeptonSFUp/F', 'reweightTrigger/F', 'reweightTopPt/F',
    #"GenJet[pt/F,eta/F,phi/F,partonFlavour/I,hadronFlavour/i]"
    ]
            
# Read variables and sequences
sequence       = []

from TT2lUnbinned.Tools.helpers import getObjDict

def make_jets( event, sample ):
    event.jets  = [getObjDict(event, 'recoJet_', jetVarNames, i) for i in range(int(event.nrecoJet))] 
    event.bJets = filter(lambda j:j['bTag'] and abs(j['eta'])<=2.4    , event.jets)

sequence.append( make_jets )

# Let's make a function that provides string-based lepton selection
def getLeptonSelection( mode ):
    if   mode=="mumu": return "Sum$({mu_string})==2&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mue":  return "Sum$({mu_string})==1&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="ee":   return "Sum$({mu_string})==0&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=='all':    return "Sum$({mu_string})+Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)

def charge(pdgId):
    return -pdgId/abs(pdgId)

# We don't use tree formulas, but I leave them so you understand the syntax. TTreeFormulas are faster than if we compute things in the event loop.
ttreeFormulas = {   
                    #"overflow_counter":phasespace.overflow_counter, 
    }

yields     = {}
allPlots   = {}
allModes   = ['mumu','mue', 'ee']
for i_mode, mode in enumerate(allModes):
    yields[mode] = {}

    # "event.weight" is 0/1 for data, depending on whether it is from a certified lumi section. For MC, it corresponds to the 1/fb*cross-section/Nsimulated. So we multiply with the lumi in /fb.
    # This weight goes to the plot.
    weight_ = lambda event, sample: event.weight1fb*lumi_scale 

    # read the MC variables only in MC; apply reweighting to simulation for specific detector effects
    for sample in mc:
      sample.read_variables = read_variables_MC + ([VectorTreeVariable.fromString( "p[C/F]", nMax=200 )] if hasattr(sample, "isEFT") and sample.isEFT  else [] ) 
      sample.weight = lambda event, sample: (event.p_C[0] if hasattr(sample, "isEFT") and sample.isEFT  else 1. )

    # Define what we want to see.
    stack = Stack(mc)

    # Define everything we want to have common to all plots
    Plot.setDefaults(stack = stack, weight = staticmethod(weight_), selectionString = "("+getLeptonSelection(mode)+")&&("+preselectionString+")&&("+extra_selection+")")

    plots = []

    # A special plot that holds the yields of all modes
    plots.append(Plot(
      name = 'yield', texX = '', texY = 'Number of Events',
      attribute = lambda event, sample: 0.5 + i_mode,
      binning=[3, 0, 3],
    ))

    plots.append(Plot(
        name = 'recoLep0_pt',
        texX = 'p_{T}(l_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample:event.recoLep0_pt,
        binning=[15,0,300],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'recoLep0_eta',
        texX = '#eta(l_{1})', texY = 'Number of Events',
        attribute = lambda event, sample: event.recoLep0_eta,
        binning=[20,-3,3],
    ))

    plots.append(Plot(
        name = 'recoLep1_pt',
        texX = 'p_{T}(l_{2}) (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample:event.recoLep1_pt,
        binning=[15,0,300],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'recoLep1_eta',
        texX = '#eta(l_{2})', texY = 'Number of Events',
        attribute = lambda event, sample: event.recoLep1_eta,
        binning=[20,-3,3],
    ))

    #plots.append(Plot(
    #    texX = 'H_{T} (GeV)', texY = 'Number of Events / 100 GeV',
    #    attribute = TreeVariable.fromString( "ht/F" ),
    #    binning=[20,0,2000],
    #    addOverFlowBin='upper',
    #))

    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "recoMet_pt/F" ),
        binning=[400/20,0,400],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = '#phi(E_{T}^{miss})', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "recoMet_phi/F" ),
        binning=[10,-pi,pi],
    ))

    #plots.append(Plot(
    #    name = "Z1_pt",
    #    texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
    #    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    #    binning=[20,0,400],
    #    addOverFlowBin='upper',
    #))

    #plots.append(Plot(
    #    name = 'Z1_pt_coarse', texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 50 GeV',
    #    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    #    binning=[16,0,800],
    #    addOverFlowBin='upper',
    #))

    #plots.append(Plot(
    #    name = 'Z1_pt_superCoarse', texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events',
    #    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    #    binning=[3,0,600],
    #    addOverFlowBin='upper',
    #))

    #plots.append(Plot(
    #    name = 'Z1_pt_coarse', texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 50 GeV',
    #    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    #    binning=[16,0,800],
    #))

    #plots.append(Plot(
    #    name = 'Z1_pt_superCoarse', texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events',
    #    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    #    binning=[3,0,600],
    #))

    #plots.append(Plot(
    #    texX = 'M(ll) (GeV)', texY = 'Number of Events / 20 GeV',
    #    attribute = TreeVariable.fromString( "Z1_mass/F" ),
    #    binning=[10,81,101],
    #    addOverFlowBin='upper',
    #))

    #plots.append(Plot(
    #    name = "Z1_mass_wide",
    #    texX = 'M(ll) (GeV)', texY = 'Number of Events / 2 GeV',
    #    attribute = TreeVariable.fromString( "Z1_mass/F" ),
    #    binning=[25,20,120],
    #    addOverFlowBin='upper',
    #)) 

    #plots.append(Plot(
    #    name = "Z1_cosThetaStar", texX = 'cos#theta(l-)', texY = 'Number of Events / 0.2',
    #    attribute = lambda event, sample:event.Z1_cosThetaStar,
    #    binning=[10,-1,1],
    #))

    #plots.append(Plot(
    #    name = "Z2_mass_wide",
    #    texX = 'M(ll) of 2nd OSDL pair', texY = 'Number of Events / 2 GeV',
    #    attribute = TreeVariable.fromString( "Z2_mass/F" ),
    #    binning=[60,0,120],
    #    addOverFlowBin='upper',
    #)) 

    #plots.append(Plot(
    #    name = "minDLmass",
    #    texX = 'min mass of all DL pairs', texY = 'Number of Events / 2 GeV',
    #    attribute = TreeVariable.fromString( "minDLmass/F" ),
    #    binning=[60,0,120],
    #    addOverFlowBin='upper',
    #)) 

    #plots.append(Plot(
    #    texX = '#Delta#phi(Z_{1}(ll))', texY = 'Number of Events',
    #    attribute = TreeVariable.fromString( "Z1_lldPhi/F" ),
    #    binning=[30,0,pi],
    #))

    #plots.append(Plot(
    #    texX = '#Delta R(Z_{1}(ll))', texY = 'Number of Events',
    #    attribute = TreeVariable.fromString( "Z1_lldR/F" ),
    #    binning=[30,0,6],
    #))

    plots.append(Plot(
      texX = 'N_{jets}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nrecoJet/I" ), #nJetSelected
      binning=[8,3.5,11.5],
    ))

    plots.append(Plot(
      texX = 'N_{b-tag}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nBTag/I" ), #nJetSelected
      binning=[5, 1.5,6.5],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet0_pt', attribute = lambda event, sample: event.recoJet_pt[0],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(subleading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet1_pt', attribute = lambda event, sample: event.recoJet_pt[1],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(l_{1+2}) (GeV)', texY = 'Number of Events',
      name = 'recoLep01_pt', attribute = lambda event, sample: event.recoLep01_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = 'M(l_{1},l_{2}) (GeV)', texY = 'Number of Events',
      name = 'recoLep01_mass', attribute = lambda event, sample: event.recoLep01_mass,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = 'p_{T}(#nu) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'tr_neutrino_pt', attribute = lambda event, sample: event.tr_neutrino_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(#nu)', texY = 'Number of Events',
      name = 'tr_neutrino_eta', attribute = lambda event, sample: event.tr_neutrino_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'p_{T}(#bar{#nu}) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'tr_neutrinoBar_pt', attribute = lambda event, sample: event.tr_neutrinoBar_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(#bar{#nu})', texY = 'Number of Events',
      name = 'tr_neutrinoBar_eta', attribute = lambda event, sample: event.tr_neutrinoBar_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'p_{T}(t#bar{t}) (GeV)', texY = 'Number of Events',
      name = 'tr_ttbar_pt', attribute = lambda event, sample: event.tr_ttbar_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = '#eta(t#bar{t})', texY = 'Number of Events',
      name = 'tr_ttbar_eta', attribute = lambda event, sample: event.tr_ttbar_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'M(t#bar{t}) (GeV)', texY = 'Number of Events',
      name = 'tr_ttbar_mass', attribute = lambda event, sample: event.tr_ttbar_mass,
      binning=[30,0,2400],
    ))

    plots.append(Plot(
      texX = 'p_{T}(t) (GeV)', texY = 'Number of Events',
      name = 'tr_top_pt', attribute = lambda event, sample: event.tr_top_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = '#eta(t)', texY = 'Number of Events',
      name = 'tr_top_eta', attribute = lambda event, sample: event.tr_top_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'M(t) (GeV)', texY = 'Number of Events',
      name = 'tr_top_mass', attribute = lambda event, sample: event.tr_top_mass,
      binning=[30,130,210],
    ))

    plots.append(Plot(
      texX = 'p_{T}(#bar{t}) (GeV)', texY = 'Number of Events',
      name = 'tr_topBar_pt', attribute = lambda event, sample: event.tr_topBar_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = '#eta(#bar{t})', texY = 'Number of Events',
      name = 'tr_topBar_eta', attribute = lambda event, sample: event.tr_topBar_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'M(#bar{t}) (GeV)', texY = 'Number of Events',
      name = 'tr_topBar_mass', attribute = lambda event, sample: event.tr_topBar_mass,
      binning=[30,130,210],
    ))

    plots.append(Plot(
      texX = 'p_{T}(W^{-}) (GeV)', texY = 'Number of Events',
      name = 'tr_Wminus_pt', attribute = lambda event, sample: event.tr_Wminus_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = '#eta(W^{-})', texY = 'Number of Events',
      name = 'tr_Wminus_eta', attribute = lambda event, sample: event.tr_Wminus_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'M(W^{-}) (GeV)', texY = 'Number of Events',
      name = 'tr_Wminus_mass', attribute = lambda event, sample: event.tr_Wminus_mass,
      binning=[30,130,210],
    ))

    plots.append(Plot(
      texX = 'p_{T}(W^{+}) (GeV)', texY = 'Number of Events',
      name = 'tr_Wplus_pt', attribute = lambda event, sample: event.tr_Wplus_pt,
      binning=[30,0,1200],
    ))

    plots.append(Plot(
      texX = '#eta(W^{+})', texY = 'Number of Events',
      name = 'tr_Wplus_eta', attribute = lambda event, sample: event.tr_Wplus_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'M(W^{+}) (GeV)', texY = 'Number of Events',
      name = 'tr_Wplus_mass', attribute = lambda event, sample: event.tr_Wplus_mass,
      binning=[30,130,210],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{+}_{n})', texY = 'Number of Events',
      name = 'cosThetaPlus_n', attribute = lambda event, sample: event.tr_cosThetaPlus_n,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{-}_{n})', texY = 'Number of Events',
      name = 'cosThetaMinus_n', attribute = lambda event, sample: event.tr_cosThetaMinus_n,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{+}_{r})', texY = 'Number of Events',
      name = 'cosThetaPlus_r', attribute = lambda event, sample: event.tr_cosThetaPlus_r,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{-}_{r})', texY = 'Number of Events',
      name = 'cosThetaMinus_r', attribute = lambda event, sample: event.tr_cosThetaMinus_r,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{+}_{k})', texY = 'Number of Events',
      name = 'cosThetaPlus_k', attribute = lambda event, sample: event.tr_cosThetaPlus_k,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{-}_{k})', texY = 'Number of Events',
      name = 'cosThetaMinus_k', attribute = lambda event, sample: event.tr_cosThetaMinus_k,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{+*}_{r})', texY = 'Number of Events',
      name = 'cosThetaPlus_r_star', attribute = lambda event, sample: event.tr_cosThetaPlus_r_star,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{-*}_{r})', texY = 'Number of Events',
      name = 'cosThetaMinus_r_star', attribute = lambda event, sample: event.tr_cosThetaMinus_r_star,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{+*}_{k})', texY = 'Number of Events',
      name = 'cosThetaPlus_k_star', attribute = lambda event, sample: event.tr_cosThetaPlus_k_star,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^{-*}_{k})', texY = 'Number of Events',
      name = 'cosThetaMinus_k_star', attribute = lambda event, sample: event.tr_cosThetaMinus_k_star,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{nn}', texY = 'Number of Events',
      name = 'xi_nn', attribute = lambda event, sample: event.tr_xi_nn,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{rr}', texY = 'Number of Events',
      name = 'xi_rr', attribute = lambda event, sample: event.tr_xi_rr,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{kk}', texY = 'Number of Events',
      name = 'xi_kk', attribute = lambda event, sample: event.tr_xi_kk,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{nr}^{+}', texY = 'Number of Events',
      name = 'xi_nr_plus', attribute = lambda event, sample: event.tr_xi_nr_plus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{nr}^{-}', texY = 'Number of Events',
      name = 'xi_nr_minus', attribute = lambda event, sample: event.tr_xi_nr_minus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{rk}^{+}', texY = 'Number of Events',
      name = 'xi_rk_plus', attribute = lambda event, sample: event.tr_xi_rk_plus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{rk}^{-}', texY = 'Number of Events',
      name = 'xi_rk_minus', attribute = lambda event, sample: event.tr_xi_rk_minus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{nk}^{+}', texY = 'Number of Events',
      name = 'xi_nk_plus', attribute = lambda event, sample: event.tr_xi_nk_plus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '#xi_{nk}^{-}', texY = 'Number of Events',
      name = 'xi_nk_minus', attribute = lambda event, sample: event.tr_xi_nk_minus,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#phi)', texY = 'Number of Events',
      name = 'cos_phi', attribute = lambda event, sample: event.tr_cos_phi,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = 'cos(#phi_{lab})', texY = 'Number of Events',
      name = 'cos_phi_lab', attribute = lambda event, sample: event.tr_cos_phi_lab,
      binning=[20,-1,1],
    ))

    plots.append(Plot(
      texX = '|#Delta#phi(ll)| lab', texY = 'Number of Events',
      name = 'tr_abs_delta_phi_ll_lab', attribute = lambda event, sample: event.tr_abs_delta_phi_ll_lab,
      binning=[20,0,2],
    ))

    plotting.fill(plots, read_variables = read_variables, sequence = sequence, ttreeFormulas = ttreeFormulas)

    # Get normalization yields from yield histogram
    for plot in plots:
      if plot.name == "yield":
        for i, l in enumerate(plot.histos):
          for j, h in enumerate(l):
            yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+i_mode))
            h.GetXaxis().SetBinLabel(1, "#mu#mu")
            h.GetXaxis().SetBinLabel(2, "#mue")
            h.GetXaxis().SetBinLabel(3, "ee")
      if plot.name.endswith("_Flag"):
        for i, l in enumerate(plot.histos):
          for j, h in enumerate(l):
            h.GetXaxis().SetBinLabel(1, "fail")
            h.GetXaxis().SetBinLabel(2, "veto")
            h.GetXaxis().SetBinLabel(3, "loose")
            h.GetXaxis().SetBinLabel(4, "medium")
            h.GetXaxis().SetBinLabel(5, "tight")
        
    #yields[mode]["data"] = 0

    drawPlots(plots, mode)
    allPlots[mode] = plots

# Add the different channels into SF and all
for mode in ["SF","all"]:
    yields[mode] = {}
    for y in yields[allModes[0]]:
        try:    yields[mode][y] = sum(yields[c][y] for c in (['ee','mumu'] if mode=="SF" else ['ee','mumu','mue']))
        except: yields[mode][y] = 0
    for plot in allPlots['mumu']:
        for plot2 in (p for p in (allPlots['ee'] if mode=="SF" else allPlots["mue"]) if p.name == plot.name):  #For SF add EE, second round add EMu for all
            for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
                for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
                    if i==k: j.Add(l)

    drawPlots(allPlots['mumu'], mode)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
