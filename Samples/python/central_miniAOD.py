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

from Samples.Tools.config import dbDir, redirector, redirector_global
dbFile = dbDir+"/TT2lUnbinned/central_miniAOD.sql"

logger.info("Using dbFile: %s", dbFile)

TTLep_pow_16        = FWLiteSample.fromDAS("TTLep_pow_16", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_pow_16.normalization = 3146182209.651617 
TTLep_pow_16.xSection = 831.762*((3*0.108)**2)

#[{"file_size":2157501208640,"max_ldate":1624203148,"median_cdate":null,"median_ldate":1623256496,"nblocks":124,"nevents":43630000,"nfiles":1013,"nlumis":43630,"num_block":124,"num_event":43630000,"num_file":1013,"num_lumi":43630}]
TTLep_pow_16preVFP  = FWLiteSample.fromDAS("TTLep_pow_16preVFP", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_pow_16preVFP.normalization = 2704527533.743900 
TTLep_pow_16preVFP.xSection = 831.762*((3*0.108)**2)
#[{"file_size":1824017247219,"max_ldate":1630471569,"median_cdate":null,"median_ldate":1623390632,"nblocks":115,"nevents":37505000,"nfiles":594,"nlumis":37505,"num_block":115,"num_event":37505000,"num_file":594,"num_lumi":37505}]
TTLep_pow_17        = FWLiteSample.fromDAS("TTLep_pow_17", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_pow_17.normalization = 7695841652.17
TTLep_pow_17.xSection = 831.762*((3*0.108)**2)
#[{"file_size":5891474122113,"max_ldate":1615564982,"median_cdate":null,"median_ldate":1615537171,"nblocks":5,"nevents":106724000,"nfiles":1357,"nlumis":106724,"num_block":5,"num_event":106724000,"num_file":1357,"num_lumi":106724}]
TTLep_pow_18        = FWLiteSample.fromDAS("TTLep_pow_18", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_pow_18.normalization = 10528968069.409693 
TTLep_pow_18.xSection = 831.762*((3*0.108)**2)
#[{"file_size":8120016444436,"max_ldate":1619370242,"median_cdate":null,"median_ldate":1617826200,"nblocks":87,"nevents":146010000,"nfiles":3069,"nlumis":146010,"num_block":87,"num_event":146010000,"num_file":3069,"num_lumi":146010}]

# 6033 files
TTLep_pow = FWLiteSample.combine( "TTLep_pow", [TTLep_pow_16, TTLep_pow_16preVFP, TTLep_pow_17, TTLep_pow_18] )
TTLep_pow.xSection = 831.762*((3*0.108)**2)
TTLep_pow.normalization = TTLep_pow_16.normalization + TTLep_pow_16preVFP.normalization + TTLep_pow_17.normalization + TTLep_pow_18.normalization 

TTsemilep_pow_16        = FWLiteSample.fromDAS("TTsemilep_pow_16", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTsemilep_pow_16.normalization = 43548253970.6
TTsemilep_pow_16.xSection = 831.762*(3*0.108)*(1-3*0.108)*2
#[{"file_size":7272568680629,"max_ldate":1624203147,"median_cdate":null,"median_ldate":1623182859,"nblocks":244,"nevents":144974000,"nfiles":3192,"nlumis":144974,"num_block":244,"num_event":144974000,"num_file":3192,"num_lumi":144974}]
TTsemilep_pow_16preVFP  = FWLiteSample.fromDAS("TTsemilep_pow_16preVFP", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTsemilep_pow_16preVFP.normalization = 39772305959.2
TTsemilep_pow_16preVFP.xSection = 831.762*(3*0.108)*(1-3*0.108)*2
#[{"file_size":6511761153190,"max_ldate":1625967751,"median_cdate":null,"median_ldate":1623292759,"nblocks":178,"nevents":132178000,"nfiles":1979,"nlumis":132178,"num_block":178,"num_event":132178000,"num_file":1979,"num_lumi":132178}]
TTsemilep_pow_17        = FWLiteSample.fromDAS("TTsemilep_pow_17", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTsemilep_pow_17.normalization = 1.02781922216e+11
TTsemilep_pow_17.xSection = 831.762*(3*0.108)*(1-3*0.108)*2
#[{"file_size":19785451169163,"max_ldate":1614645509,"median_cdate":null,"median_ldate":1614442402,"nblocks":10,"nevents":355332000,"nfiles":4355,"nlumis":355332,"num_block":10,"num_event":355332000,"num_file":4355,"num_lumi":355332}]
TTsemilep_pow_18        = FWLiteSample.fromDAS("TTsemilep_pow_18", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTsemilep_pow_18.normalization = 1.41808787771e+11
TTsemilep_pow_18.xSection = 831.762*(3*0.108)*(1-3*0.108)*2
#[{"file_size":26841970310765,"max_ldate":1622294617,"median_cdate":null,"median_ldate":1620857283,"nblocks":172,"nevents":478982000,"nfiles":10010,"nlumis":478982,"num_block":172,"num_event":478982000,"num_file":10010,"num_lumi":478982}]

# 19536 files
TTsemilep_pow = FWLiteSample.combine( "TTsemilep_pow", [TTsemilep_pow_16, TTsemilep_pow_16preVFP, TTsemilep_pow_17, TTsemilep_pow_18] )
TTsemilep_pow.xSection = 831.762*(3*0.108)*(1-3*0.108)*2 
TTsemilep_pow.normalization = TTsemilep_pow_16.normalization + TTsemilep_pow_16preVFP.normalization + TTsemilep_pow_17.normalization + TTsemilep_pow_18.normalization 

TTLep_hdampDOWN_16  = FWLiteSample.fromDAS("TTLep_hdampDOWN_16", "/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampDOWN_16.normalization = 1305254547.14
TTLep_hdampDOWN_16.xSection = 831.762*((3*0.108)**2)
#[{"file_size":893452934740,"max_ldate":1626252359,"median_cdate":null,"median_ldate":1623210687,"nblocks":87,"nevents":18100999,"nfiles":426,"nlumis":18101,"num_block":87,"num_event":18100999,"num_file":426,"num_lumi":18101}]
TTLep_hdampDOWN_16preVFP = FWLiteSample.fromDAS("TTLep_hdampDOWN_16preVFP", "/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampDOWN_16preVFP.normalization = 1213354705.720125 
TTLep_hdampDOWN_16preVFP.xSection = 831.762*((3*0.108)**2)
#[{"file_size":822802815332,"max_ldate":1625878829,"median_cdate":null,"median_ldate":1623302918,"nblocks":81,"nevents":16973000,"nfiles":286,"nlumis":16973,"num_block":81,"num_event":16973000,"num_file":286,"num_lumi":16973}]
TTLep_hdampDOWN_17  = FWLiteSample.fromDAS("TTLep_hdampDOWN_17", "/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampDOWN_17.normalization = 4323628205.96
TTLep_hdampDOWN_17.xSection = 831.762*((3*0.108)**2)
#[{"file_size":2235544037076,"max_ldate":1628722923,"median_cdate":null,"median_ldate":1623088415,"nblocks":67,"nevents":40630000,"nfiles":545,"nlumis":40630,"num_block":67,"num_event":40630000,"num_file":545,"num_lumi":40630}]
TTLep_hdampDOWN_18  = FWLiteSample.fromDAS("TTLep_hdampDOWN_18", "/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampDOWN_18.normalization = 4323628201.739369 
TTLep_hdampDOWN_18.xSection = 831.762*((3*0.108)**2)
#[{"file_size":3326306926554,"max_ldate":1630220606,"median_cdate":null,"median_ldate":1628844766,"nblocks":20,"nevents":59958000,"nfiles":1253,"nlumis":59958,"num_block":20,"num_event":59958000,"num_file":1253,"num_lumi":59958}]

#2510 files
TTLep_hdampDOWN = FWLiteSample.combine( "TTLep_hdampDOWN", [TTLep_hdampDOWN_16, TTLep_hdampDOWN_16preVFP, TTLep_hdampDOWN_17, TTLep_hdampDOWN_18] )
TTLep_hdampDOWN.xSection = 831.762*((3*0.108)**2) 
TTLep_hdampDOWN.normalization = TTLep_hdampDOWN_16.normalization + TTLep_hdampDOWN_16preVFP.normalization + TTLep_hdampDOWN_17.normalization + TTLep_hdampDOWN_18.normalization 

TTLep_hdampUP_16    = FWLiteSample.fromDAS("TTLep_hdampUP_16", "/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampUP_16.normalization = 1351609718.337784 
TTLep_hdampUP_16.xSection = 831.762*((3*0.108)**2)
#[{"file_size":936900064852,"max_ldate":1626246092,"median_cdate":null,"median_ldate":1623010375,"nblocks":84,"nevents":18874000,"nfiles":443,"nlumis":18874,"num_block":84,"num_event":18874000,"num_file":443,"num_lumi":18874}]
TTLep_hdampUP_16preVFP = FWLiteSample.fromDAS("TTLep_hdampUP_16preVFP", "/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampUP_16preVFP.normalization = 1066892599.774596 
TTLep_hdampUP_16preVFP.xSection = 831.762*((3*0.108)**2)
#[{"file_size":725952972542,"max_ldate":1639308075,"median_cdate":null,"median_ldate":1638228490,"nblocks":74,"nevents":14865000,"nfiles":249,"nlumis":14865,"num_block":74,"num_event":14865000,"num_file":249,"num_lumi":14865}]
TTLep_hdampUP_17    = FWLiteSample.fromDAS("TTLep_hdampUP_17", "/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampUP_17.normalization = 2899529949.915322 
TTLep_hdampUP_17.xSection = 831.762*((3*0.108)**2)
#[{"file_size":2228954850870,"max_ldate":1628731322,"median_cdate":null,"median_ldate":1623245640,"nblocks":128,"nevents":40292000,"nfiles":574,"nlumis":40292,"num_block":128,"num_event":40292000,"num_file":574,"num_lumi":40292}]
TTLep_hdampUP_18    = FWLiteSample.fromDAS("TTLep_hdampUP_18", "/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
TTLep_hdampUP_18.normalization = 3930877880.471174 
TTLep_hdampUP_18.xSection = 831.762*((3*0.108)**2)
#[{"file_size":3041694284756,"max_ldate":1621499795,"median_cdate":null,"median_ldate":1621454296,"nblocks":5,"nevents":54510000,"nfiles":1134,"nlumis":54510,"num_block":5,"num_event":54510000,"num_file":1134,"num_lumi":54510}]

# 2400 files
TTLep_hdampUP = FWLiteSample.combine( "TTLep_hdampUP", [TTLep_hdampUP_16, TTLep_hdampUP_16preVFP, TTLep_hdampUP_17, TTLep_hdampUP_18] )
TTLep_hdampUP.xSection = 831.762*((3*0.108)**2) 
TTLep_hdampUP.normalization = TTLep_hdampUP_16.normalization + TTLep_hdampUP_16preVFP.normalization + TTLep_hdampUP_17.normalization + TTLep_hdampUP_18.normalization 

ST_tW_top_16            = FWLiteSample.fromDAS("ST_tW_top_16", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_top_16.normalization = 106897143.0
ST_tW_top_16.xSection= 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":157105361838,"max_ldate":1634726954,"median_cdate":null,"median_ldate":1633354383,"nblocks":22,"nevents":3368375,"nfiles":56,"nlumis":3264,"num_block":22,"num_event":3368375,"num_file":56,"num_lumi":3264}]
ST_tW_top_16preVFP     = FWLiteSample.fromDAS("ST_tW_top_16preVFP", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_top_16preVFP.normalization = 105317997.947630 
ST_tW_top_16preVFP.xSection= 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":151265746423,"max_ldate":1637381665,"median_cdate":null,"median_ldate":1633335235,"nblocks":33,"nevents":3294673,"nfiles":66,"nlumis":3192,"num_block":33,"num_event":3294673,"num_file":66,"num_lumi":3192}]
ST_tW_top_17            = FWLiteSample.fromDAS("ST_tW_top_17", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_top_17.normalization = 276021555.940286
ST_tW_top_17.xSection= 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":443383174226,"max_ldate":1622580558,"median_cdate":null,"median_ldate":1620837659,"nblocks":28,"nevents":8507203,"nfiles":122,"nlumis":8242,"num_block":28,"num_event":8507203,"num_file":122,"num_lumi":8242}]
ST_tW_top_18            = FWLiteSample.fromDAS("ST_tW_top_18", "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_top_18.normalization = 365675749.645227
ST_tW_top_18.xSection = 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":591910036528,"max_ldate":1621846445,"median_cdate":null,"median_ldate":1621073235,"nblocks":17,"nevents":11270430,"nfiles":231,"nlumis":109250,"num_block":17,"num_event":11270430,"num_file":231,"num_lumi":109250}]

# 475 files
ST_tW_top = FWLiteSample.combine( "ST_tW_top", [ST_tW_top_16, ST_tW_top_16preVFP, ST_tW_top_17, ST_tW_top_18] )
ST_tW_top.xSection = 35.85*(1.-(1.-0.108*3)*(1.-0.108*3)) 
ST_tW_top.normalization = ST_tW_top_16.normalization + ST_tW_top_16preVFP.normalization + ST_tW_top_17.normalization + ST_tW_top_18.normalization 

ST_tW_antitop_16        = FWLiteSample.fromDAS("ST_tW_antitop_16", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_antitop_16.normalization = 118799348.672
ST_tW_antitop_16.xSection= 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":170598263400,"max_ldate":1627576022,"median_cdate":null,"median_ldate":1623355350.5,"nblocks":66,"nevents":3654510,"nfiles":90,"nlumis":3540,"num_block":66,"num_event":3654510,"num_file":90,"num_lumi":3540}]
ST_tW_antitop_16preVFP  = FWLiteSample.fromDAS("ST_tW_antitop_16preVFP", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_antitop_16preVFP.normalization = 103260113.117
ST_tW_antitop_16preVFP.xSection= 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":145684275759,"max_ldate":1623762433,"median_cdate":null,"median_ldate":1623326587,"nblocks":49,"nevents":3176485,"nfiles":75,"nlumis":3078,"num_block":49,"num_event":3176485,"num_file":75,"num_lumi":3078}]
ST_tW_antitop_17        = FWLiteSample.fromDAS("ST_tW_antitop_17", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_antitop_17.normalization = 274168362.624
ST_tW_antitop_17.xSection = 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":439812589734,"max_ldate":1630113966,"median_cdate":null,"median_ldate":1628830931,"nblocks":20,"nevents":8433998,"nfiles":127,"nlumis":8172,"num_block":20,"num_event":8433998,"num_file":127,"num_lumi":8172}]
ST_tW_antitop_18        = FWLiteSample.fromDAS("ST_tW_antitop_18", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
ST_tW_antitop_18.normalization = 358102361.803906 
ST_tW_antitop_18.xSection = 35.85*(1.-(1.-0.108*3)*(1.-0.108*3))
#[{"file_size":578663258488,"max_ldate":1623128329,"median_cdate":null,"median_ldate":1621171091,"nblocks":30,"nevents":11015956,"nfiles":235,"nlumis":10670,"num_block":30,"num_event":11015956,"num_file":235,"num_lumi":10670}]

#527 files
ST_tW_antitop = FWLiteSample.combine( "ST_tW_antitop", [ST_tW_antitop_16, ST_tW_antitop_16preVFP, ST_tW_antitop_17, ST_tW_antitop_18] )
ST_tW_antitop.xSection = 35.85*(1.-(1.-0.108*3)*(1.-0.108*3)) 
ST_tW_antitop.normalization = ST_tW_antitop_16.normalization + ST_tW_antitop_16preVFP.normalization + ST_tW_antitop_17.normalization + ST_tW_antitop_18.normalization 

DYJetsToLL_M10To50_16   = FWLiteSample.fromDAS("DYJetsToLL_M10To50_16", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M10To50_16.normalization = 23706672
DYJetsToLL_M10To50_16.xSection = 18610
#[{"file_size":736723462782,"max_ldate":1638952828,"median_cdate":null,"median_ldate":1638219984,"nblocks":45,"nevents":23706672,"nfiles":217,"nlumis":23208,"num_block":45,"num_event":23706672,"num_file":217,"num_lumi":23208}]
DYJetsToLL_M10To50_16preVFP   = FWLiteSample.fromDAS("DYJetsToLL_M10To50_16preVFP", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M10To50_16preVFP.normalization = 25799525
DYJetsToLL_M10To50_16preVFP.xSection = 18610
#[{"file_size":824868034549,"max_ldate":1639317730,"median_cdate":null,"median_ldate":1638286658,"nblocks":41,"nevents":25799525,"nfiles":270,"nlumis":25591,"num_block":41,"num_event":25799525,"num_file":270,"num_lumi":25591}]
DYJetsToLL_M10To50_17   = FWLiteSample.fromDAS("DYJetsToLL_M10To50_17", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M10To50_17.normalization = 68480179
DYJetsToLL_M10To50_17.xSection = 18610
#[{"file_size":2623810592673,"max_ldate":1619221193,"median_cdate":null,"median_ldate":1617431684,"nblocks":116,"nevents":68480179,"nfiles":870,"nlumis":68883,"num_block":116,"num_event":68480179,"num_file":870,"num_lumi":68883}]
DYJetsToLL_M10To50_18   = FWLiteSample.fromDAS("DYJetsToLL_M10To50_18", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M10To50_18.normalization = 99288125
DYJetsToLL_M10To50_18.xSection = 18610
#[{"file_size":3830120249546,"max_ldate":1618924421,"median_cdate":null,"median_ldate":1617446432,"nblocks":63,"nevents":99288125,"nfiles":1080,"nlumis":99266,"num_block":63,"num_event":99288125,"num_file":1080,"num_lumi":99266}]

# 2437 files
DYJetsToLL_M10To50 = FWLiteSample.combine( "DYJetsToLL_M10To50", [DYJetsToLL_M10To50_16, DYJetsToLL_M10To50_16preVFP, DYJetsToLL_M10To50_17, DYJetsToLL_M10To50_18] )
DYJetsToLL_M10To50.xSection = 18610
DYJetsToLL_M10To50.normalization = DYJetsToLL_M10To50_16.normalization + DYJetsToLL_M10To50_16preVFP.normalization + DYJetsToLL_M10To50_17.normalization + DYJetsToLL_M10To50_18.normalization 

DYJetsToLL_M50_16 = FWLiteSample.fromDAS( "DYJetsToLL_M50_16", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_16.normalization = 82448537
DYJetsToLL_M50_16.xSection = 2075.14*3
#[{"file_size":3154019094653,"max_ldate":1639080384,"median_cdate":null,"median_ldate":1638259067,"nblocks":56,"nevents":82448537,"nfiles":933,"nlumis":78021,"num_block":56,"num_event":82448537,"num_file":933,"num_lumi":78021}]
DYJetsToLL_M50_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_16preVFP", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_16preVFP.normalization = 95170542
DYJetsToLL_M50_16preVFP.xSection = 2075.14*3
#[{"file_size":3578983108085,"max_ldate":1623764328,"median_cdate":null,"median_ldate":1623201805,"nblocks":57,"nevents":95170542,"nfiles":974,"nlumis":90819,"num_block":57,"num_event":95170542,"num_file":974,"num_lumi":90819}]
DYJetsToLL_M50_17       = FWLiteSample.fromDAS("DYJetsToLL_M50_17", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_17.normalization = 103344974
DYJetsToLL_M50_17.xSection = 2075.14*3
#[{"file_size":4567844856750,"max_ldate":1621271948,"median_cdate":null,"median_ldate":1620408235,"nblocks":19,"nevents":103344974,"nfiles":1230,"nlumis":984980,"num_block":19,"num_event":103344974,"num_file":1230,"num_lumi":984980}]
DYJetsToLL_M50_18       = FWLiteSample.fromDAS("DYJetsToLL_M50_18", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_18.normalization = 96233328
DYJetsToLL_M50_18.xSection = 2075.14*3
#[{"file_size":4282352219566,"max_ldate":1622293460,"median_cdate":null,"median_ldate":1621084269,"nblocks":48,"nevents":96233328,"nfiles":1050,"nlumis":91825,"num_block":48,"num_event":96233328,"num_file":1050,"num_lumi":91825}]

# 4178 files
DYJetsToLL_M50 = FWLiteSample.combine( "DYJetsToLL_M50", [DYJetsToLL_M50_16, DYJetsToLL_M50_16preVFP, DYJetsToLL_M50_17, DYJetsToLL_M50_18] )
DYJetsToLL_M50.xSection = 2075.14*3 
DYJetsToLL_M50.normalization = DYJetsToLL_M50_16.normalization + DYJetsToLL_M50_16preVFP.normalization + DYJetsToLL_M50_17.normalization + DYJetsToLL_M50_18.normalization 

DYJetsToLL_M50_HT100to200_16    = FWLiteSample.fromDAS("DYJetsToLL_M50_HT100to200_16", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT100to200_16.normalization = 8316351
DYJetsToLL_M50_HT100to200_16.xSection=147.4*1.23
#[{"file_size":394033926537,"max_ldate":1634543018,"median_cdate":null,"median_ldate":1630803361,"nblocks":37,"nevents":8316351,"nfiles":129,"nlumis":8300,"num_block":37,"num_event":8316351,"num_file":129,"num_lumi":8300}]
DYJetsToLL_M50_HT200to400_16    = FWLiteSample.fromDAS("DYJetsToLL_M50_HT200to400_16", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT200to400_16.normalization = 5653782
DYJetsToLL_M50_HT200to400_16.xSection=40.99*1.23
#[{"file_size":304095070597,"max_ldate":1634543018,"median_cdate":null,"median_ldate":1631468637,"nblocks":23,"nevents":5653782,"nfiles":108,"nlumis":6247,"num_block":23,"num_event":5653782,"num_file":108,"num_lumi":6247}]
DYJetsToLL_M50_HT400to600_16    =  FWLiteSample.fromDAS("DYJetsToLL_M50_HT400to600_16", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT400to600_16.normalization = 2491416
DYJetsToLL_M50_HT400to600_16.xSection=5.678*1.23
#[{"file_size":151001724692,"max_ldate":1637343185,"median_cdate":null,"median_ldate":1635081680,"nblocks":29,"nevents":2491416,"nfiles":61,"nlumis":3376,"num_block":29,"num_event":2491416,"num_file":61,"num_lumi":3376}]
DYJetsToLL_M50_HT600to800_16    =  FWLiteSample.fromDAS("DYJetsToLL_M50_HT600to800_16", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT600to800_16.normalization = 2299853
DYJetsToLL_M50_HT600to800_16.xSection=1.367*1.23
#[{"file_size":148969766044,"max_ldate":1631390796,"median_cdate":null,"median_ldate":1631336608,"nblocks":4,"nevents":2299853,"nfiles":47,"nlumis":4742,"num_block":4,"num_event":2299853,"num_file":47,"num_lumi":4742}]
DYJetsToLL_M50_HT800to1200_16   = FWLiteSample.fromDAS("DYJetsToLL_M50_HT800to1200_16", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT800to1200_16.normalization = 2393976
DYJetsToLL_M50_HT800to1200_16.xSection=0.6304*1.23
#[{"file_size":162840420985,"max_ldate":1634543019,"median_cdate":null,"median_ldate":1630815653,"nblocks":35,"nevents":2393976,"nfiles":65,"nlumis":3602,"num_block":35,"num_event":2393976,"num_file":65,"num_lumi":3602}]
DYJetsToLL_M50_HT1200to2500_16  = FWLiteSample.fromDAS("DYJetsToLL_M50_HT1200to2500_16", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT1200to2500_16.normalization = 1970857
DYJetsToLL_M50_HT1200to2500_16.xSection=0.1514*1.23
#[{"file_size":142047385635,"max_ldate":1634767522,"median_cdate":null,"median_ldate":1631542616,"nblocks":18,"nevents":1970857,"nfiles":43,"nlumis":4764,"num_block":18,"num_event":1970857,"num_file":43,"num_lumi":4764}]
DYJetsToLL_M50_HT2500toInf_16   = FWLiteSample.fromDAS("DYJetsToLL_M50_HT2500toInf_16", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT2500toInf_16.normalization = 696811
DYJetsToLL_M50_HT2500toInf_16.xSection=0.003565*1.23
#[{"file_size":55594148886,"max_ldate":1634543019,"median_cdate":null,"median_ldate":1631335055.5,"nblocks":22,"nevents":696811,"nfiles":36,"nlumis":1581,"num_block":22,"num_event":696811,"num_file":36,"num_lumi":1581}]

DYJetsToLL_M50_HT100to200_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT100to200_16preVFP", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT100to200_16preVFP.normalization = 9570042
DYJetsToLL_M50_HT100to200_16preVFP.xSection=147.4*1.23
#[{"file_size":447223001358,"max_ldate":1631508787,"median_cdate":null,"median_ldate":1631139214,"nblocks":36,"nevents":9570042,"nfiles":161,"nlumis":9508,"num_block":36,"num_event":9570042,"num_file":161,"num_lumi":9508}]
DYJetsToLL_M50_HT200to400_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT200to400_16preVFP", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT200to400_16preVFP.normalization = 5862631
DYJetsToLL_M50_HT200to400_16preVFP.xSection=40.99*1.23
#[{"file_size":310797336013,"max_ldate":1632697002,"median_cdate":null,"median_ldate":1632676563,"nblocks":11,"nevents":5862631,"nfiles":102,"nlumis":6086,"num_block":11,"num_event":5862631,"num_file":102,"num_lumi":6086}]
DYJetsToLL_M50_HT400to600_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT400to600_16preVFP", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT400to600_16preVFP.normalization = 2716892
DYJetsToLL_M50_HT400to600_16preVFP.xSection=5.678*1.23
#[{"file_size":161785507005,"max_ldate":1637947458,"median_cdate":null,"median_ldate":1635307470,"nblocks":21,"nevents":2716892,"nfiles":57,"nlumis":4241,"num_block":21,"num_event":2716892,"num_file":57,"num_lumi":4241}]
DYJetsToLL_M50_HT600to800_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT600to800_16preVFP", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT600to800_16preVFP.normalization = 2681650
DYJetsToLL_M50_HT600to800_16preVFP.xSection=1.367*1.23
#[{"file_size":170290429758,"max_ldate":1631398446,"median_cdate":null,"median_ldate":1631215274,"nblocks":11,"nevents":2681650,"nfiles":61,"nlumis":3791,"num_block":11,"num_event":2681650,"num_file":61,"num_lumi":3791}]
DYJetsToLL_M50_HT800to1200_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT800to1200_16preVFP", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT800to1200_16preVFP.normalization = 2411091
DYJetsToLL_M50_HT800to1200_16preVFP.xSection=0.6304*1.23
#[{"file_size":161446098876,"max_ldate":1632810976,"median_cdate":null,"median_ldate":1632382402,"nblocks":28,"nevents":2411091,"nfiles":69,"nlumis":6029,"num_block":28,"num_event":2411091,"num_file":69,"num_lumi":6029}]
DYJetsToLL_M50_HT1200to2500_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT1200to2500_16preVFP", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT1200to2500_16preVFP.normalization = 2189664
DYJetsToLL_M50_HT1200to2500_16preVFP.xSection=0.1514*1.23
#[{"file_size":156226314972,"max_ldate":1637677029,"median_cdate":null,"median_ldate":1636415105,"nblocks":38,"nevents":2189664,"nfiles":71,"nlumis":4040,"num_block":38,"num_event":2189664,"num_file":71,"num_lumi":4040}]
DYJetsToLL_M50_HT2500toInf_16preVFP = FWLiteSample.fromDAS("DYJetsToLL_M50_HT2500toInf_16preVFP", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT2500toInf_16preVFP.normalization = 721404
DYJetsToLL_M50_HT2500toInf_16preVFP.xSection=0.003565*1.23
#[{"file_size":57473521471,"max_ldate":1633073364,"median_cdate":null,"median_ldate":1633073361,"nblocks":8,"nevents":721404,"nfiles":23,"nlumis":2134,"num_block":8,"num_event":721404,"num_file":23,"num_lumi":2134}]

DYJetsToLL_M50_HT100to200_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT100to200_17", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT100to200_17.normalization = 18955253
DYJetsToLL_M50_HT100to200_17.xSection=147.4*1.23
#[{"file_size":1002234961081,"max_ldate":1627530372,"median_cdate":null,"median_ldate":1621072520,"nblocks":23,"nevents":18955253,"nfiles":259,"nlumis":18706,"num_block":23,"num_event":18955253,"num_file":259,"num_lumi":18706}]
DYJetsToLL_M50_HT200to400_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT200to400_17", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT200to400_17.normalization = 12513057
DYJetsToLL_M50_HT200to400_17.xSection=40.99*1.23
#[{"file_size":741146719297,"max_ldate":1621879656,"median_cdate":null,"median_ldate":1621085985.5,"nblocks":64,"nevents":12513057,"nfiles":206,"nlumis":12864,"num_block":64,"num_event":12513057,"num_file":206,"num_lumi":12864}]
DYJetsToLL_M50_HT400to600_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT400to600_17", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT400to600_17.normalization = 5543804
DYJetsToLL_M50_HT400to600_17.xSection=5.678*1.23
#[{"file_size":365381658290,"max_ldate":1621742692,"median_cdate":null,"median_ldate":1621085985,"nblocks":19,"nevents":5543804,"nfiles":93,"nlumis":6952,"num_block":19,"num_event":5543804,"num_file":93,"num_lumi":6952}]
DYJetsToLL_M50_HT600to800_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT600to800_17", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT600to800_17.normalization = 5278417
DYJetsToLL_M50_HT600to800_17.xSection=1.367*1.23
#[{"file_size":367168959570,"max_ldate":1621771446,"median_cdate":null,"median_ldate":1621084742,"nblocks":21,"nevents":5278417,"nfiles":94,"nlumis":7850,"num_block":21,"num_event":5278417,"num_file":94,"num_lumi":7850}]
DYJetsToLL_M50_HT800to1200_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT800to1200_17", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT800to1200_17.normalization = 4506887
DYJetsToLL_M50_HT800to1200_17.xSection=0.6304*1.23
#[{"file_size":329290820474,"max_ldate":1621852385,"median_cdate":null,"median_ldate":1621072127,"nblocks":20,"nevents":4506887,"nfiles":89,"nlumis":6677,"num_block":20,"num_event":4506887,"num_file":89,"num_lumi":6677}]
DYJetsToLL_M50_HT1200to2500_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT1200to2500_17", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT1200to2500_17.normalization = 4802716
DYJetsToLL_M50_HT1200to2500_17.xSection=0.1514*1.23
#[{"file_size":369184894810,"max_ldate":1628742923,"median_cdate":null,"median_ldate":1621086822,"nblocks":26,"nevents":4802716,"nfiles":93,"nlumis":8882,"num_block":26,"num_event":4802716,"num_file":93,"num_lumi":8882}]
DYJetsToLL_M50_HT2500toInf_17 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT2500toInf_17", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT2500toInf_17.normalization = 1480047
DYJetsToLL_M50_HT2500toInf_17.xSection=0.003565*1.23
#[{"file_size":125526433662,"max_ldate":1628707908,"median_cdate":null,"median_ldate":1621118891,"nblocks":18,"nevents":1480047,"nfiles":41,"nlumis":3347,"num_block":18,"num_event":1480047,"num_file":41,"num_lumi":3347}]


DYJetsToLL_M50_HT100to200_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT100to200_18", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT100to200_18.normalization = 26202328
DYJetsToLL_M50_HT100to200_18.xSection=147.4*1.23
#[{"file_size":1399854768905,"max_ldate":1627559206,"median_cdate":null,"median_ldate":1621072521,"nblocks":27,"nevents":26202328,"nfiles":549,"nlumis":26430,"num_block":27,"num_event":26202328,"num_file":549,"num_lumi":26430}]
DYJetsToLL_M50_HT200to400_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT200to400_18", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT200to400_18.normalization = 18455718
DYJetsToLL_M50_HT200to400_18.xSection=40.99*1.23
#[{"file_size":1103856147793,"max_ldate":1621943673,"median_cdate":null,"median_ldate":1621085989,"nblocks":27,"nevents":18455718,"nfiles":392,"nlumis":20016,"num_block":27,"num_event":18455718,"num_file":392,"num_lumi":20016}]
DYJetsToLL_M50_HT400to600_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT400to600_18", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT400to600_18.normalization = 8908406
DYJetsToLL_M50_HT400to600_18.xSection=5.678*1.23
#[{"file_size":593847832636,"max_ldate":1622572030,"median_cdate":null,"median_ldate":1621066217,"nblocks":33,"nevents":8908406,"nfiles":195,"nlumis":12724,"num_block":33,"num_event":8908406,"num_file":195,"num_lumi":12724}]
DYJetsToLL_M50_HT600to800_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT600to800_18", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT600to800_18.normalization = 7035971
DYJetsToLL_M50_HT600to800_18.xSection=1.367*1.23
#[{"file_size":493265299999,"max_ldate":1621761877,"median_cdate":null,"median_ldate":1621086402,"nblocks":26,"nevents":7035971,"nfiles":161,"nlumis":11133,"num_block":26,"num_event":7035971,"num_file":161,"num_lumi":11133}]
DYJetsToLL_M50_HT800to1200_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT800to1200_18", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT800to1200_18.normalization = 6678036
DYJetsToLL_M50_HT800to1200_18.xSection=0.6304*1.23
#[{"file_size":489086806085,"max_ldate":1621970421,"median_cdate":null,"median_ldate":1621201871,"nblocks":42,"nevents":6678036,"nfiles":167,"nlumis":16759,"num_block":42,"num_event":6678036,"num_file":167,"num_lumi":16759}]
DYJetsToLL_M50_HT1200to2500_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT1200to2500_18", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT1200to2500_18.normalization = 6166852
DYJetsToLL_M50_HT1200to2500_18.xSection=0.1514*1.23
#[{"file_size":476623598999,"max_ldate":1621974398,"median_cdate":null,"median_ldate":1621072131,"nblocks":20,"nevents":6166852,"nfiles":149,"nlumis":12806,"num_block":20,"num_event":6166852,"num_file":149,"num_lumi":12806}]
DYJetsToLL_M50_HT2500toInf_18 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT2500toInf_18", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DYJetsToLL_M50_HT2500toInf_18.normalization = 1978203
DYJetsToLL_M50_HT2500toInf_18.xSection=0.003565*1.23
#[{"file_size":167368703164,"max_ldate":1629309960,"median_cdate":null,"median_ldate":1621912445,"nblocks":28,"nevents":1978203,"nfiles":67,"nlumis":6067,"num_block":28,"num_event":1978203,"num_file":67,"num_lumi":6067}]

# 1098 files
DYJetsToLL_M50_HT100to200 = FWLiteSample.combine( "DYJetsToLL_M50_HT100to200", [DYJetsToLL_M50_HT100to200_16, DYJetsToLL_M50_HT100to200_16preVFP, DYJetsToLL_M50_HT100to200_17, DYJetsToLL_M50_HT100to200_18] )
DYJetsToLL_M50_HT100to200.xSection = 147.4*1.23 
DYJetsToLL_M50_HT100to200.normalization = DYJetsToLL_M50_HT100to200_16.normalization + DYJetsToLL_M50_HT100to200_16preVFP.normalization + DYJetsToLL_M50_HT100to200_17.normalization + DYJetsToLL_M50_HT100to200_18.normalization 

# 808 files
DYJetsToLL_M50_HT200to400 = FWLiteSample.combine( "DYJetsToLL_M50_HT200to400", [DYJetsToLL_M50_HT200to400_16, DYJetsToLL_M50_HT200to400_16preVFP, DYJetsToLL_M50_HT200to400_17, DYJetsToLL_M50_HT200to400_18] )
DYJetsToLL_M50_HT200to400.xSection = 40.99*1.23 
DYJetsToLL_M50_HT200to400.normalization = DYJetsToLL_M50_HT200to400_16.normalization + DYJetsToLL_M50_HT200to400_16preVFP.normalization + DYJetsToLL_M50_HT200to400_17.normalization + DYJetsToLL_M50_HT200to400_18.normalization 

# 406 files
DYJetsToLL_M50_HT400to600 = FWLiteSample.combine( "DYJetsToLL_M50_HT400to600", [DYJetsToLL_M50_HT400to600_16, DYJetsToLL_M50_HT400to600_16preVFP, DYJetsToLL_M50_HT400to600_17, DYJetsToLL_M50_HT400to600_18] )
DYJetsToLL_M50_HT400to600.xSection = 5.678*1.23 
DYJetsToLL_M50_HT400to600.normalization = DYJetsToLL_M50_HT400to600_16.normalization + DYJetsToLL_M50_HT400to600_16preVFP.normalization + DYJetsToLL_M50_HT400to600_17.normalization + DYJetsToLL_M50_HT400to600_18.normalization 

# 363 files
DYJetsToLL_M50_HT600to800 = FWLiteSample.combine( "DYJetsToLL_M50_HT600to800", [DYJetsToLL_M50_HT600to800_16, DYJetsToLL_M50_HT600to800_16preVFP, DYJetsToLL_M50_HT600to800_17, DYJetsToLL_M50_HT600to800_18] )
DYJetsToLL_M50_HT600to800.xSection = 1.367*1.23 
DYJetsToLL_M50_HT600to800.normalization = DYJetsToLL_M50_HT600to800_16.normalization + DYJetsToLL_M50_HT600to800_16preVFP.normalization + DYJetsToLL_M50_HT600to800_17.normalization + DYJetsToLL_M50_HT600to800_18.normalization 

# 390 fils
DYJetsToLL_M50_HT800to1200 = FWLiteSample.combine( "DYJetsToLL_M50_HT800to1200", [DYJetsToLL_M50_HT800to1200_16, DYJetsToLL_M50_HT800to1200_16preVFP, DYJetsToLL_M50_HT800to1200_17, DYJetsToLL_M50_HT800to1200_18] )
DYJetsToLL_M50_HT800to1200.xSection = 0.6304*1.23 
DYJetsToLL_M50_HT800to1200.normalization = DYJetsToLL_M50_HT800to1200_16.normalization + DYJetsToLL_M50_HT800to1200_16preVFP.normalization + DYJetsToLL_M50_HT800to1200_17.normalization + DYJetsToLL_M50_HT800to1200_18.normalization 

# 356 files
DYJetsToLL_M50_HT1200to2500 = FWLiteSample.combine( "DYJetsToLL_M50_HT1200to2500", [DYJetsToLL_M50_HT1200to2500_16, DYJetsToLL_M50_HT1200to2500_16preVFP, DYJetsToLL_M50_HT1200to2500_17, DYJetsToLL_M50_HT1200to2500_18] )
DYJetsToLL_M50_HT1200to2500.xSection = 0.1514*1.23 
DYJetsToLL_M50_HT1200to2500.normalization = DYJetsToLL_M50_HT1200to2500_16.normalization + DYJetsToLL_M50_HT1200to2500_16preVFP.normalization + DYJetsToLL_M50_HT1200to2500_17.normalization + DYJetsToLL_M50_HT1200to2500_18.normalization 

# 167 files
DYJetsToLL_M50_HT2500toInf = FWLiteSample.combine( "DYJetsToLL_M50_HT2500toInf", [DYJetsToLL_M50_HT2500toInf_16, DYJetsToLL_M50_HT2500toInf_16preVFP, DYJetsToLL_M50_HT2500toInf_17, DYJetsToLL_M50_HT2500toInf_18] )
DYJetsToLL_M50_HT2500toInf.xSection = 0.003565*1.23 
DYJetsToLL_M50_HT2500toInf.normalization = DYJetsToLL_M50_HT2500toInf_16.normalization + DYJetsToLL_M50_HT2500toInf_16preVFP.normalization + DYJetsToLL_M50_HT2500toInf_17.normalization + DYJetsToLL_M50_HT2500toInf_18.normalization 

    
#/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM

#/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTbb_4f_TTTo2L2Nu_TuneCP5-Powheg-Openloops-Pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM
#/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM
#/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_DoubleScattering_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM
#/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/SSWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v4/MINIAODSIM
#/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v4/MINIAODSIM
#/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM
#/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM
#/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTbb_4f_TTTo2L2Nu_TuneCP5-Powheg-Openloops-Pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM
#/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM
#/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_DoubleScattering_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM
#/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/SSWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
#/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM
#/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM
#/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTbb_4f_TTTo2L2Nu_TuneCP5-Powheg-Openloops-Pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_DoubleScattering_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM
#/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/SSWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM
#/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM
#/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM
#/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTbb_4f_TTTo2L2Nu_TuneCP5-Powheg-Openloops-Pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TWZToLL_thad_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TWZToLL_tlept_Whad_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TWZToLL_tlept_Wlept_5f_DS_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM
#/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WWTo2L2Nu_TuneCP5_DoubleScattering_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM
#/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/ZZTo2Q2Nu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM
#/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/SSWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
#/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v3/MINIAODSIM
#/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM
#/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM
#
