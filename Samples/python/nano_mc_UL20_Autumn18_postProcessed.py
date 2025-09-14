import os, sys
from RootTools.core.Sample import Sample
import ROOT

import logging
logger = logging.getLogger(__name__)

from TT2lUnbinned.Samples.color import color

import TT2lUnbinned.Samples.config as config
directory_ = config.location_mc_UL2018

def make_dirs( dirs ):
    return [ os.path.join( directory_, dir_ ) for dir_ in dirs ]

TTLep_Autumn18            = Sample.fromDirectory(name="TTLep_Autumn18", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( ['TTLep_pow_CP5'] ))
#TTLep_pow_hDown  = Sample.fromDirectory(name="TTLep_pow_hDown", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( ['TTLep_pow_CP5_hDown'] ))
#TTLep_pow_hUp    = Sample.fromDirectory(name="TTLep_pow_hUp", treeName="Events", isData=False, color=color.TT, texName="t#bar{t}", directory=make_dirs( ['TTLep_pow_CP5_hUp'] ))
#ST    = Sample.fromDirectory(name="ST",    treeName="Events", isData=False, color=color.T,  texName="t/tW", directory=make_dirs( ['T_tch_pow', 'TBar_tch_pow'] ))
#DY    = Sample.fromDirectory(name="DY",    treeName="Events", isData=False, color=color.DY, texName="DY", directory=make_dirs( ['DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600to800','DYJetsToLL_M50_HT800to1200','DYJetsToLL_M50_HT1200to2500','DYJetsToLL_M50_HT2500toInf','DYJetsToLL_M4to50_HT100to200', 'DYJetsToLL_M-4to50_HT200to400','DYJetsToLL_M-4to50_HT400to600','DYJetsToLL_M4to50_HT600toInf'] ))

#TT01j1lCAv2Ref_HT800 = Sample.fromDirectory(name="TT01j1lCAv2Ref_HT800", treeName="Events", isData=False, color=color.TT_EFT, texName="t#bar{t}", directory=make_dirs( ['TT01j1lCAv2Ref_HT800'] ))
#TT01j2lCAv2Ref_HT500 = Sample.fromDirectory(name="TT01j2lCAv2Ref_HT500", treeName="Events", isData=False, color=color.TT_EFT, texName="t#bar{t}", directory=make_dirs( ['TT01j2lCAv2Ref_HT500'] ))
