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
from TT2lUnbinned.Tools.cutInterpreter           import cutInterpreter
from TT2lUnbinned.Tools.objectSelection          import lepString

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
argParser.add_argument('--selection',      action='store', default='tr-dilepM-offZ1-njet3p-btagM2p-ht500')
args = argParser.parse_args()

# Logger
import TT2lUnbinned.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# Simulated samples
from TT2lUnbinned.Samples.nano_mc_UL20_Summer16_preVFP_postProcessed import *

sample = TTLep

# For R&D we just use a fraction of the data
if args.small:
    sample.normalization = 1.
    sample.reduceFiles( to = 5 )

from TT2lUnbinned.Tools.objectSelection import isBJet
from TT2lUnbinned.Tools.helpers import getObjDict

def make_jets( event, sample ):
    event.jets  = [getObjDict(event, 'JetGood_', jetVarNames, i) for i in range(int(event.nJetGood))] 
    event.bJets = filter(lambda j:isBJet(j, year=event.year) and abs(j['eta'])<=2.4    , event.jets)

# Let's make a function that provides string-based lepton selection
mu_string  = lepString('mu','VL')
ele_string = lepString('ele','VL')
def getLeptonSelection( mode ):
    if   mode=="mumu": return "Sum$({mu_string})==2&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mue":  return "Sum$({mu_string})==1&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="ee":   return "Sum$({mu_string})==0&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=='all':    return "Sum$({mu_string})+Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)

#from TT2lUnbinned.Analysis.phasespace.v1    import phasespace
from TT2lUnbinned.Analysis.phasespace.v2    import phasespace

pre_selection  = "("+getLeptonSelection("all")+")&&("+cutInterpreter.cutString(args.selection)+")&&("+phasespace.inclusive_selection+")" 
this_selection = pre_selection 
extra_selection="1"
# 5 GeV steps, cumulative distribution

minEvents = 3000
for variable, _ in phasespace.overflow_variables.iteritems():

    this_selection+="&&("+extra_selection+")"
    
    #print "variable", variable, "selection", this_selection
    h_c = sample.get1DHistoFromDraw(variable, [1000,0,5000], selectionString = this_selection).GetCumulative(False)

    found=False
    for i_b in range(1,1+h_c.GetNbinsX()):
        #print variable, h_c.GetBinContent(i_b), h_c.GetBinLowEdge(i_b-1)
        if h_c.GetBinContent(i_b)<minEvents:
            cut_value = h_c.GetBinLowEdge(i_b-1)
            found = True
            break
    if found:
        print "Bin", i_b, variable, "cut_value", cut_value
        extra_selection+="&&(%s<%f)"%( variable, cut_value )

for selection in phasespace.overflow_selections:
    print selection, sample.chain.GetEntries( pre_selection+"&&"+selection )
for i_selection, _ in enumerate(phasespace.overflow_selections):
    print i_selection, sample.chain.GetEntries( pre_selection+"&&("+phasespace.overflow_counter+"=="+str(i_selection+1)+")" )
