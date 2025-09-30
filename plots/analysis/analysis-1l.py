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
from   math                              import sqrt, cos, sin, pi, atan2, cosh, sinh, acos, log

# RootTools
from RootTools.core.standard             import *

# TT2lUnbinned
from TT2lUnbinned.Tools.user                     import plot_directory
from TT2lUnbinned.Tools.cutInterpreter           import cutInterpreter
from TT2lUnbinned.Tools.objectSelection          import lepString
#from TT2lUnbinned.Analysis.phasespace.v1         import phasespace as phasespace_v1
#from TT2lUnbinned.Analysis.phasespace.v2         import phasespace as phasespace_v2

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
argParser.add_argument('--ttbarComp',      action='store_true', help='Run only on on TTbar EFT?')
argParser.add_argument('--noData',         action='store_true', default=True, help='Do not plot data.')
argParser.add_argument('--no_sorting',     action='store_true', help='Sort histos?', )
argParser.add_argument('--dataMCScaling',  action='store_true', help='Data MC scaling?')
argParser.add_argument('--plot_directory', action='store', default='v5')
argParser.add_argument('--selection',      action='store', default='njet2-btag2')
argParser.add_argument('--n_cores',        action='store', type=int, default=-1)
args = argParser.parse_args()

# Logger
import TT2lUnbinned.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small: args.plot_directory += "_small"
if args.noData:args.plot_directory += "_noData"
if args.ttbarComp: args.plot_directory += "_ttbarComp"

# Simulated samples
from TT2lUnbinned.Samples.nano_mc_UL20_singlelep_njet2p_met30_postProcessed import *

#mc = [ TTSingleLep_pow_CP5_Autumn18, t_sch_Autumn18] 
mc = [ TT, ST_tWch, ST_tch_pow, t_sch] 

#preselectionString = cutInterpreter.cutString(args.selection) + "&&" + phasespace_v1.inclusive_selection# + "&&("+phasespace.overflow_counter+"==7)"
preselectionString = cutInterpreter.cutString(args.selection) 

# Now we add the data
if not args.noData:
    #from TT2lUnbinned.samples.nano_private_UL20_RunII_postProcessed_dilep import RunII
    raise NotImplementedError
    data_sample = RunII
    data_sample.name = "data"
    all_samples = mc +  [data_sample]
else:
    all_samples = mc 

# Here we compute the scaling of the simulation to the data luminosity (event.weight corresponds to 1/fb for simulation, hence we divide the data lumi in pb^-1 by 1000) 
lumi_scale = 137. if args.noData else data_sample.lumi/1000.

# We're going to "scale" the simulation if "small" is true. So let's define a "scale" which will correct this
for sample in mc:
    sample.scale  = 1 

# For R&D we just use a fraction of the data
if args.small:
    if not args.noData:
        data_sample.reduceFiles( factor = 100 )
    for sample in mc :
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        #sample.reduceFiles( to=1)
        sample.scale /= sample.normalization

# Helpers for putting text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right


def drawObjects( dataMCScale, lumi_scale ):
    lines = [
      (0.15, 0.95, 'CMS Simulation'), 
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale),
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots, mode, dataMCScale):
  for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, 'RunII', mode + ("_log" if log else ""), args.selection)
    for plot in plots:
      if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot

      _drawObjects = []

      if isinstance( plot, Plot):
          plotting.draw(plot,
            plot_directory = plot_directory_,
            ratio =  {'yRange':(0.1,1.9)} if not args.noData else None,
            logX = False, logY = log, sorting = not args.no_sorting,
            yRange = (0.9, "auto") if log else (0.001, "auto"),
            scaling = {0:1} if (args.dataMCScaling or args.ttbarComp) else {},
            legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
            drawObjects = drawObjects( dataMCScale , lumi_scale ) + _drawObjects,
            copyIndexPHP = True, extensions = ["png", "pdf", "root"],
          )

read_variables = []

jetVars     = ['pt/F', 'eta/F', 'phi/F', 'btagDeepB/F', 'btagDeepFlavB/F' ]

jetVarNames     = [x.split('/')[0] for x in jetVars]

# the following we read for both, data and simulation 
read_variables += [
    "weight/F", "year/I", "met_pt/F", "met_phi/F", "nBTag/I", "nJetGood/I", "PV_npvsGood/I", "LHE_HT/F", "LHE_HTIncoming/F",
    "ht/F",
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPWP/I", "l1_index/I", 
    #"l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPWP/I", "l2_index/I",
    "JetGood[%s]"%(",".join(jetVars)),
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mvaTOP/F]",
    #"Z1_l1_index/I", "Z1_l2_index/I",  
    #"Z1_phi/F", "Z1_pt/F", "Z1_m/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I]",
]

read_variables +=  ["top_pt/F", "top_eta/F", "top_phi/F", "top_m/F", "top_other_pt/F", "top_other_eta/F", "top_other_phi/F", "top_other_m/F", "top_b_index/I" ,
        "W_pt/F", "W_eta/F", "W_phi/F", "W_m/F", "nu_pt/F", "nu_eta/F", "nu_phi/F", "nu_m/F",
        "mT/F", "mlb0/F", "mlb1/F", "pT_bb/F", "cosTheta_lb_topRF/F", "FW3/F", "FW0/F", "FW3_R/F",
        "DEta_l_b0/F", "DEta_l_b1/F", "DEta_top_b0/F", "DEta_top_b1/F", "Cos_DPhi_top_b0/F", "Cos_DPhi_top_b1/F", "cos_DPhi_l_met/F",
        ]

# the following we read only in simulation
read_variables_MC = [
    'reweightBTagSF_central/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightLeptonSF/F', 'reweightLeptonSFDown/F', 'reweightLeptonSFUp/F', 'reweightTopPt/F',
    "GenJet[pt/F,eta/F,phi/F,partonFlavour/I,hadronFlavour/i]"
    ]
            
# Read variables and sequences
sequence       = []

from TT2lUnbinned.Tools.objectSelection import isBJet
from TT2lUnbinned.Tools.helpers import getObjDict

def make_reco(event, sample):
    event.jets  = [getObjDict(event, 'JetGood_', jetVarNames, i) for i in range(int(event.nJetGood))]
    event.bJets = list(filter(lambda j: isBJet(j, year=event.year) and abs(j['eta']) <= 2.4, event.jets))

sequence.append( make_reco )

# Let's make a function that provides string-based lepton selection
mu_string  = lepString('mu','VL')
ele_string = lepString('ele','VL')
def getLeptonSelection( mode ):
    if   mode=="mu": return "Sum$({mu_string})==1&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="e":  return "Sum$({mu_string})==0&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=='all':    return "Sum$({mu_string})+Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)

def charge(pdgId):
    return -pdgId/abs(pdgId)

# We don't use tree formulas, but I leave them so you understand the syntax. TTreeFormulas are faster than if we compute things in the event loop.
ttreeFormulas = {   
                    #"overflow_counter":phasespace.overflow_counter, 
    }

yields     = {}
allPlots   = {}
allModes   = ['mu','e', 'all']
for i_mode, mode in enumerate(allModes):
    yields[mode] = {}

    # "event.weight" is 0/1 for data, depending on whether it is from a certified lumi section. For MC, it corresponds to the 1/fb*cross-section/Nsimulated. So we multiply with the lumi in /fb.
    # This weight goes to the plot.
    weight_ = lambda event, sample: event.weight if sample.isData else event.weight

    # coloring
    if args.ttbarComp:
        for sample in mc: sample.style = styles.lineStyle(sample.color)
    else:
        for sample in mc: sample.style = styles.fillStyle(sample.color)

    # read the MC variables only in MC; apply reweighting to simulation for specific detector effects
    for sample in mc:
      sample.read_variables = read_variables_MC 
      sample.weight = lambda event, sample: event.reweightBTagSF_central*event.reweightPU*event.reweightL1Prefire*event.reweightLeptonSF*event.reweightTopPt 

    # Define what we want to see.
    if args.ttbarComp:
        stack = Stack(*[[s] for s in mc])
    elif not args.noData:
        data_sample.style = styles.errorStyle( ROOT.kBlack ) 
        stack = Stack(mc, [data_sample])
    else:
        stack = Stack(mc)

    # Define everything we want to have common to all plots
    Plot.setDefaults(stack = stack, weight = staticmethod(weight_), selectionString = "("+getLeptonSelection(mode)+")&&("+preselectionString+")")

    plots = []

    # A special plot that holds the yields of all modes
    plots.append(Plot(
      name = 'yield', texX = '', texY = 'Number of Events',
      attribute = lambda event, sample: 0.5 + i_mode,
      binning=[2, 0, 2],
    ))

#    # A special plot that shows the overflow bins 
#    plots.append(Plot(
#      name = 'overflow_counter_v1', texX = '', texY = 'Number of Events',
#      attribute = phasespace_v1.overflow_counter_func(), #lambda event, sample: event.overflow_counter,
#      binning=[len(phasespace_v1.overflow_selections), 1, 1+len(phasespace_v1.overflow_selections)],
#    ))

#    plots.append(Plot(
#      name = 'overflow_counter_v2', texX = '', texY = 'Number of Events',
#      attribute = phasespace_v2.overflow_counter_func(), #lambda event, sample: event.overflow_counter,
#      binning=[len(phasespace_v2.overflow_selections), 1, 1+len(phasespace_v2.overflow_selections)],
#    ))

    plots.append(Plot(
      name = 'nVtxs', texX = 'vertex multiplicity', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "PV_npvsGood/I" ),
      binning=[50,0,50],
      addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'l1_pt',
        texX = 'p_{T}(l_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample:event.l1_pt,
        binning=[15,0,300],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'l1_eta',
        texX = '#eta(l_{1})', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_eta,
        binning=[20,-3,3],
    ))

    plots.append(Plot(
        name = 'l1_mvaTOP',
        texX = 'MVA_{TOP}(l_{1})', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOP,
        binning=[20,-1,1],
    ))

    plots.append(Plot(
        name = 'l1_mvaTOPWP',
        texX = 'MVA_{TOP}(l_{1}) WP', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOPWP,
        binning=[5,0,5],
    ))

    plots.append(Plot(
        texX = 'H_{T} (GeV)', texY = 'Number of Events / 100 GeV',
        attribute = TreeVariable.fromString( "ht/F" ),
        binning=[20,0,2000],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_pt/F" ),
        binning=[400/20,0,400],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = 'm_{T} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample: event.mT,
        name = "mT",
        binning=[400/40,0,400],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = '#phi(E_{T}^{miss})', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_phi/F" ),
        binning=[10,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'N_{jets}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nJetGood/I" ), #nJetSelected
      binning=[8,1.5,9.5],
    ))

    plots.append(Plot(
      texX = 'N_{b-tag}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nBTag/I" ), #nJetSelected
      binning=[5, 0.5,5.5],
    ))

    plots.append(Plot(
      texX = 'LHE_HT (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'LHE_HT', attribute = lambda event, sample: event.LHE_HT,
      binning=[1500/50,0,1500],
    ))

    plots.append(Plot(
      texX = 'LHE_HTIncoming (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'LHE_HTIncoming', attribute = lambda event, sample: event.LHE_HTIncoming,
      binning=[1500/50,0,1500],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet0_pt', attribute = lambda event, sample: event.JetGood_pt[0],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(subleading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet1_pt', attribute = lambda event, sample: event.JetGood_pt[1],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading b jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'bjet0_pt', attribute = lambda event, sample: event.bJets[0]['pt'] if len(event.bJets)>=1 else float('nan'),
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(subleading b jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'bjet1_pt', attribute = lambda event, sample: event.bJets[1]['pt'] if len(event.bJets)>=2 else float('nan'),
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(leading b jet) (GeV)', texY = 'Number of Events',
      name = 'bjet0_eta', attribute = lambda event, sample: event.bJets[0]['eta'] if len(event.bJets)>=1 else float('nan'),
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = '#eta(sub leading b jet) (GeV)', texY = 'Number of Events',
      name = 'bjet1_eta', attribute = lambda event, sample: event.bJets[1]['eta'] if len(event.bJets)>=2 else float('nan'),
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'p_{T}(bb) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'pT_bb', attribute = lambda event, sample: event.pT_bb,
      binning=[600/30,0,600],
    ))


    plots.append(Plot(
      texX = '#Delta#eta(l,b_0)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_lb0', attribute = lambda event, sample: event.DEta_l_b0,
      binning=[30,0,6],
    ))
    plots.append(Plot(
      texX = '#Delta#eta(l,b_1)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_lb1', attribute = lambda event, sample: event.DEta_l_b1,
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = '#Delta#eta(top,b_0)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_top_b0', attribute = lambda event, sample: event.DEta_top_b0,
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = '#Delta#eta(top,b_1)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_top_b1', attribute = lambda event, sample: event.DEta_top_b1,
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = 'Cos(#Delta#phi(top,b_0))', texY = 'Number of Events / 30 GeV',
      name = 'Cos_DPhi_top_b0', attribute = lambda event, sample: event.Cos_DPhi_top_b0,
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'Cos(#Delta#phi(l,MET))', texY = 'Number of Events / 30 GeV',
      name = 'cos_DPhi_l_met', attribute = lambda event, sample: event.cos_DPhi_l_met,
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'Cos(#Delta#phi(top,b_1))', texY = 'Number of Events / 30 GeV',
      name = 'Cos_DPhi_top_b1', attribute = lambda event, sample: event.Cos_DPhi_top_b1,
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'p_{T}(W) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'W_pt', attribute = lambda event, sample: event.W_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(W)', texY = 'Number of Events / 30 GeV',
      name = 'W_eta', attribute = lambda event, sample: event.W_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(W)', texY = 'Number of Events / 20 GeV',
        name = "W_phi", attribute =  lambda event, sample: event.W_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'p_{T}(nu) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'nu_pt', attribute = lambda event, sample: event.nu_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(nu)', texY = 'Number of Events / 30 GeV',
      name = 'nu_eta', attribute = lambda event, sample: event.nu_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(nu)', texY = 'Number of Events / 20 GeV',
        name = "nu_phi", attribute =  lambda event, sample: event.nu_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'p_{T}(t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_pt', attribute = lambda event, sample: event.top_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(t)', texY = 'Number of Events / 30 GeV',
      name = 'top_eta', attribute = lambda event, sample: event.top_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(t)', texY = 'Number of Events / 20 GeV',
        name = "top_phi", attribute =  lambda event, sample: event.top_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'M(t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_m', attribute = lambda event, sample: event.top_m,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(other t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_pt', attribute = lambda event, sample: event.top_other_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(other t)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_eta', attribute = lambda event, sample: event.top_other_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(other t)', texY = 'Number of Events / 20 GeV',
        name = "top_other_phi", attribute =  lambda event, sample: event.top_other_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'M(other t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_m', attribute = lambda event, sample: event.top_other_m,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'cos(#theta^#ast)', texY = 'Number of Events',
      name = 'cosTheta_lb_topRF', attribute = lambda event, sample: event.cosTheta_lb_topRF,
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'FW3/FW0', texY = 'Number of Events',
      name = 'FW3_R', attribute = lambda event, sample: event.FW3_R,
      binning=[30,0,1],
    ))

    plots.append(Plot(
      texX = 'M(l, b_0) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'mlb0', attribute = lambda event, sample: event.mlb0,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'M(l, b_1) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'mlb1', attribute = lambda event, sample: event.mlb1,
      binning=[600/30,0,600],
    ))


    plotting.fill(plots, read_variables = read_variables, sequence = sequence, ttreeFormulas = ttreeFormulas)

    # Get normalization yields from yield histogram
    for plot in plots:
      if plot.name == "yield":
        for i, l in enumerate(plot.histos):
          for j, h in enumerate(l):
            yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+i_mode))
            h.GetXaxis().SetBinLabel(1, "#mu")
            h.GetXaxis().SetBinLabel(2, "e")

    yields[mode]["MC"] = sum(yields[mode][s.name] for s in mc)
    if args.noData:
        dataMCScale = 1.
    else:
        dataMCScale        = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')

    drawPlots(plots, mode, dataMCScale)
    allPlots[mode] = plots

# Add the different channels into SF and all
for mode in ["all"]:
    yields[mode] = {}
    for y in yields[allModes[0]]:
        try:    yields[mode][y] = sum(yields[c][y] for c in (['e','mu'] ))
        except: yields[mode][y] = 0
    if args.noData:
        dataMCScale = 1.
    else:
        dataMCScale = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')
    for plot in allPlots['mu']:
        for plot2 in (p for p in (allPlots['e']) if p.name == plot.name):  #For SF add EE, second round add EMu for all
            for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
                for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
                    if i==k: j.Add(l)

    drawPlots(allPlots['mu'], mode, dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
