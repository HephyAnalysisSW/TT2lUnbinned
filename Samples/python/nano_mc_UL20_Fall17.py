import copy, os, sys
from RootTools.core.Sample import Sample
import ROOT

def get_parser():
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for samples file")
    argParser.add_argument('--overwrite',   action='store_true',    help="Overwrite current entry in db?")
    argParser.add_argument('--update',      action='store_true',    help="Update current entry in db?")
    argParser.add_argument('--check_completeness', action='store_true',    help="Check competeness?")
    return argParser

# Logging
if __name__=="__main__":
    import Samples.Tools.logger as logger
    logger = logger.get_logger("INFO", logFile = None )
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger("INFO", logFile = None )
    options = get_parser().parse_args()
    ov = options.overwrite
    if options.update:
        ov = 'update'
else:
    import logging
    logger = logging.getLogger(__name__)
    ov = False

from Samples.Tools.config import redirector_global as redirector

# DB
from Samples.Tools.config import dbDir
dbFile = dbDir+'/DB_UL17_nanoAODv9.sql'

logger.info("Using db file: %s", dbFile)


TT01j1lCAv2Ref_HT800 = Sample.fromDirectory( "TT01j1lCAv2Ref_HT800", "/eos/vbc/group/cms/robert.schoefbeck/TT2lUnbinned/nanoAOD/Run2SIM_UL2017/TT01j1lCAv2Ref_HT800", xSection=89.8, redirector = "root://eos.grid.vbc.ac.at/")
TT01j1lCAv2Ref_HT800.reweight_pkl = '/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA/TT01j1lCARef_HT800_reweight_card.pkl'
TT01j1lCAv2Ref_HT800.normalization = 1636910.0

TT01j2lCAv2Ref_HT500 = Sample.fromDirectory( "TT01j2lCAv2Ref_HT500", "/eos/vbc/group/cms/robert.schoefbeck/TT2lUnbinned/nanoAOD/Run2SIM_UL2017/TT01j2lCAv2Ref_HT500", xSection=25.11, redirector = "root://eos.grid.vbc.ac.at/")
TT01j2lCAv2Ref_HT500.reweight_pkl = '/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA/TT01j2lCARef_HT500_reweight_card.pkl'
TT01j2lCAv2Ref_HT500.normalization = 1749046.0

EFT_samples = [TT01j1lCAv2Ref_HT800, TT01j2lCAv2Ref_HT500]

TTLep_pow_CP5_hDown  = Sample.nanoAODfromDAS("TTLep_pow_CP5_hDown","/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", dbFile=dbFile, redirector=redirector, instance="global", overwrite=ov, xSection=88.4)
TTLep_pow_CP5_hUp    = Sample.nanoAODfromDAS("TTLep_pow_CP5_hUp","/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", dbFile=dbFile, redirector=redirector, instance="global", overwrite=ov, xSection=88.4)

syst_samples = [TTLep_pow_CP5_hDown, TTLep_pow_CP5_hUp]

allSamples = EFT_samples + syst_samples

for s in allSamples:
    s.isData = False

from Samples.Tools.AutoClass import AutoClass
samples = AutoClass( allSamples )
if __name__=="__main__":
    if options.check_completeness:
        samples.check_completeness( cores=20 )
