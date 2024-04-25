import copy, os, sys
from RootTools.fwlite.FWLiteSample import FWLiteSample
import ROOT

def get_parser():
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for samples file")
    argParser.add_argument('--overwrite',   action='store_true',    help="Overwrite current entry in db?")
    return argParser

# Logging
if __name__=="__main__":
    import Samples.Tools.logger as logger
    logger = logger.get_logger("INFO", logFile = None )
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger("INFO", logFile = None )
    options = get_parser().parse_args()
    ov = options.overwrite

else:
    import logging
    logger = logging.getLogger(__name__)
    ov = False


from Samples.Tools.config import dbDir, redirector, redirector_global, redirector_clip
dbFile = dbDir+"/TT2lUnbinned_private_GEN.sql"

# Hannah's ref point
TT01j2lCAMyRef = FWLiteSample.fromDAS("TT01j2lCAMyRef", "/TT01j2lCAMyRef/schoef-TT01j2lCAMyRef-fc6320e66404feda4775676c476a065d/USER", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True, instance="phys03")
TT01j2lCAMyRef.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v3/TT01j2lCAMyRef_reweight_card.pkl"
TT01j2lCAMyRef.normalization = 9403401
TT01j2lCAMyRef.xSection = 183.4050759

# My ref point
TT01j2lCAOldRef_HT300 = FWLiteSample.fromDAS("TT01j2lCAOldRef_HT300", "/TT01j2lCAOldRef_HT300/schoef-TT01j2lCAOldRef_HT300-d498dc23f6596e551a0afa6318e35840/USER", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True, instance="phys03")
TT01j2lCAOldRef_HT300.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v4/TT01j2lCAOldRef_HT300_reweight_card.pkl"
TT01j2lCAOldRef_HT300.normalization = 9466119
TT01j2lCAOldRef_HT300.xSection = 81.42615636

# Hannah's ref point
ST_tW01j2lCAMyRef = FWLiteSample.fromDAS("ST_tW01j2lCAMyRef", "/ST_tW01j2lCAMyRef/schoef-ST_tW01j2lCAMyRef-73cc3f0b7e7ec35b300554e420d538e3/USER", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True, instance="phys03")
ST_tW01j2lCAMyRef.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v3/ST_tW01j2lCAMyRef_reweight_card.pkl"
ST_tW01j2lCAMyRef.normalization = 4433678
ST_tW01j2lCAMyRef.xSection = 10.6338271257

# my ref point, Mtt500
TT01j2lCAOldRef_Mtt500_ext = FWLiteSample.fromDirectory( "TT01j2lCAOldRef_Mtt500_ext", 
    [
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500/TT01j2lCAOldRef_Mtt500/240408_093551/0000",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500/TT01j2lCAOldRef_Mtt500/240408_093551/0001",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500/TT01j2lCAOldRef_Mtt500/240408_093551/0002",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500/TT01j2lCAOldRef_Mtt500/240408_093551/0003",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500_ext/TT01j2lCAOldRef_Mtt500_ext/240411_181040/0000",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500_ext/TT01j2lCAOldRef_Mtt500_ext/240411_181040/0001",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500_ext/TT01j2lCAOldRef_Mtt500_ext/240411_181040/0002",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500_ext/TT01j2lCAOldRef_Mtt500_ext/240411_181040/0003",
    "/eos/vbc/experiments/cms/store/user/schoef/TT01j2lCAOldRef_Mtt500_ext/TT01j2lCAOldRef_Mtt500_ext/240411_181040/0004",
],
    prefix = redirector_clip, )
TT01j2lCAOldRef_Mtt500_ext.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v4/TT01j2lCAOldRef_reweight_card.pkl"
#TT01j2lCAOldRef_Mtt500.normalization = 31379921
TT01j2lCAOldRef_Mtt500_ext.normalization = 91182394
TT01j2lCAOldRef_Mtt500_ext.xSection = 244.922426846 #MISSES the filter efficiecny

# this sample WAS obtained with the Mtt500 filter. I forgot to put it in the DAS name.
ST_tW01j2lCAOldRef = FWLiteSample.fromDAS("ST_tW01j2lCAOldRef_Mtt500", "/ST_tW01j2lCAOldRef/schoef-ST_tW01j2lCAOldRef-c827b858693a75adc13493b6de93d3d7/USER", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True, instance="phys03")
ST_tW01j2lCAOldRef.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v4/ST_tW01j2lCAOldRef_reweight_card.pkl"
ST_tW01j2lCAOldRef.normalization = 31379921
ST_tW01j2lCAOldRef.xSection = float('nan')
