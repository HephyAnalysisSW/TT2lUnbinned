jesUncertainties = [
    "Total",
    "AbsoluteMPFBias",
    "AbsoluteScale",
    "AbsoluteStat",
    "RelativeBal",
    "RelativeFSR",
    "RelativeJEREC1",
    "RelativeJEREC2",
    "RelativeJERHF",
    "RelativePtBB",
    "RelativePtEC1",
    "RelativePtEC2",
    "RelativePtHF",
    "RelativeStatEC",
    "RelativeStatFSR",
    "RelativeStatHF",
    "PileUpDataMC",
    "PileUpPtBB",
    "PileUpPtEC1",
    "PileUpPtEC2",
    "PileUpPtHF",
    "PileUpPtRef",
    "FlavorQCD",
    "Fragmentation",
    "SinglePionECAL",
    "SinglePionHCAL",
    "TimePtEta",
]
from TT2lUnbinned.Samples.nano_UL20_RunII_postProcessed import *

TTLep.reduceFiles(to=1)
from RootTools.core.standard import *
from TT2lUnbinned.Tools.user import plot_directory
import os
import ROOT
import Analysis.Tools.syncer
for sys in jesUncertainties:
    upMnom  = TTLep.get1DHistoFromDraw("JetGood_pt_jes{sys}Up-JetGood_pt".format(sys=sys), [200,-1,1])
    numMdown=TTLep.get1DHistoFromDraw("JetGood_pt-JetGood_pt_jes{sys}Down".format(sys=sys), [200,-1,1])
    upMdown = TTLep.get1DHistoFromDraw("JetGood_pt_jes{sys}Up-JetGood_pt_jes{sys}Down".format(sys=sys), [200,-1,1])

    upMnom.style = styles.lineStyle(ROOT.kRed)
    numMdown.style = styles.lineStyle(ROOT.kBlue)
    upMdown.style = styles.lineStyle(ROOT.kBlack)

    upMnom.legendText = "Up - Nom"
    numMdown.legendText = "Nom - Down"
    upMdown.legendText = "Up - Down"

    plot = Plot.fromHisto(sys, [ [upMnom], [numMdown], [upMdown]], texX="Difference" )
    
    plotting.draw( plot, plot_directory = os.path.join( plot_directory, "JECCheck_JetGood" ), logY=True, logX=False, copyIndexPHP=True)
