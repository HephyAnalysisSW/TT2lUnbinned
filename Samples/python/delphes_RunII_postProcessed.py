from RootTools.core.standard import *
import os
import copy

from TT2lUnbinned.Tools.user import postprocessing_output_directory as directory_
directory = os.path.join( directory_, 'delphes/v1' ) 

directory_fakeB1 = os.path.join( directory_, 'delphes/v1_fakeB1' ) 
directory_fakeB2 = os.path.join( directory_, 'delphes/v1_fakeB2' ) 

TTLep               = Sample.fromDirectory( "TTLep", [os.path.join( directory, "TTLep_pow")], texName = "t#bar{t}")
#
TTLep_hdampDOWN     = Sample.fromDirectory( "TTLep_hdampDOWN", [os.path.join( directory, "TTLep_hdampDOWN")], texName = "t#bar{t} hdamp down")
TTLep_hdampUP       = Sample.fromDirectory( "TTLep_hdampUP", [os.path.join( directory, "TTLep_hdampUP")], texName = "t#bar{t} hdamp up")
ST_tW_top           = Sample.fromDirectory( "ST_tW_top", [os.path.join( directory, "ST_tW_top")], texName = "tW")
ST_tW_antitop       = Sample.fromDirectory( "ST_tW_antitop", [os.path.join( directory, "ST_tW_antitop")], texName = "tBarW")

DYJetsToLL_M50_HT100to200   = Sample.fromDirectory( "DYJetsToLL_M50_HT100to200",    [os.path.join( directory, "DYJetsToLL_M50_HT100to200")], texName = "DY M50 HT100to200") 
DYJetsToLL_M50_HT200to400   = Sample.fromDirectory( "DYJetsToLL_M50_HT200to400",    [os.path.join( directory, "DYJetsToLL_M50_HT200to400")], texName = "DY M50 HT200to400") 
DYJetsToLL_M50_HT400to600   = Sample.fromDirectory( "DYJetsToLL_M50_HT400to600",    [os.path.join( directory, "DYJetsToLL_M50_HT400to600")], texName = "DY M50 HT400to600") 
DYJetsToLL_M50_HT600to800   = Sample.fromDirectory( "DYJetsToLL_M50_HT600to800",    [os.path.join( directory, "DYJetsToLL_M50_HT600to800")], texName = "DY M50 HT600to800") 
DYJetsToLL_M50_HT800to1200  = Sample.fromDirectory( "DYJetsToLL_M50_HT800to1200",   [os.path.join( directory, "DYJetsToLL_M50_HT800to1200")], texName = "DY M50 HT800to1200") 
DYJetsToLL_M50_HT1200to2500 = Sample.fromDirectory( "DYJetsToLL_M50_HT1200to2500",  [os.path.join( directory, "DYJetsToLL_M50_HT1200to2500")], texName = "DY M50 HT1200to2500") 
DYJetsToLL_M50_HT2500toInf  = Sample.fromDirectory( "DYJetsToLL_M50_HT2500toInf",   [os.path.join( directory, "DYJetsToLL_M50_HT2500toInf")], texName = "DY M50 HT2500toInf") 

DYJetsToLL_M50_HT           = Sample.combine( "DYJetsToLL_M50_HT", [DYJetsToLL_M50_HT100to200, DYJetsToLL_M50_HT200to400, DYJetsToLL_M50_HT400to600, DYJetsToLL_M50_HT600to800, DYJetsToLL_M50_HT800to1200, DYJetsToLL_M50_HT1200to2500, DYJetsToLL_M50_HT2500toInf], texName = "DY HT binned")

ST_tW_top_fakeB1           = Sample.fromDirectory( "ST_tW_top_fakeB1", [os.path.join( directory_fakeB1, "ST_tW_top")], texName = "tW (fake B1)")
ST_tW_antitop_fakeB1       = Sample.fromDirectory( "ST_tW_antitop_fakeB1", [os.path.join( directory_fakeB1, "ST_tW_antitop")], texName = "tBarW (fakeB2)")

DYJetsToLL_M50_HT100to200_fakeB2   = Sample.fromDirectory( "DYJetsToLL_M50_HT100to200_fakeB2",    [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT100to200")], texName = "DY M50 HT100to200") 
DYJetsToLL_M50_HT200to400_fakeB2   = Sample.fromDirectory( "DYJetsToLL_M50_HT200to400_fakeB2",    [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT200to400")], texName = "DY M50 HT200to400") 
DYJetsToLL_M50_HT400to600_fakeB2   = Sample.fromDirectory( "DYJetsToLL_M50_HT400to600_fakeB2",    [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT400to600")], texName = "DY M50 HT400to600") 
DYJetsToLL_M50_HT600to800_fakeB2   = Sample.fromDirectory( "DYJetsToLL_M50_HT600to800_fakeB2",    [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT600to800")], texName = "DY M50 HT600to800") 
DYJetsToLL_M50_HT800to1200_fakeB2  = Sample.fromDirectory( "DYJetsToLL_M50_HT800to1200_fakeB2",   [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT800to1200")], texName = "DY M50 HT800to1200") 
DYJetsToLL_M50_HT1200to2500_fakeB2 = Sample.fromDirectory( "DYJetsToLL_M50_HT1200to2500_fakeB2",  [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT1200to2500")], texName = "DY M50 HT1200to2500") 
DYJetsToLL_M50_HT2500toInf_fakeB2  = Sample.fromDirectory( "DYJetsToLL_M50_HT2500toInf_fakeB2",   [os.path.join( directory_fakeB2, "DYJetsToLL_M50_HT2500toInf")], texName = "DY M50 HT2500toInf") 

DYJetsToLL_M50_HT_fakeB2           = Sample.combine( "DYJetsToLL_M50_HT_fakeB2", [DYJetsToLL_M50_HT100to200_fakeB2, DYJetsToLL_M50_HT200to400_fakeB2, DYJetsToLL_M50_HT400to600_fakeB2, DYJetsToLL_M50_HT600to800_fakeB2, DYJetsToLL_M50_HT800to1200_fakeB2, DYJetsToLL_M50_HT1200to2500_fakeB2, DYJetsToLL_M50_HT2500toInf_fakeB2], texName = "DY HT binned (fake B2)")


#TT01j2lCAMyRef      = Sample.fromDirectory( "TT01j2lCAMyRef", [os.path.join( directory, "TT01j2lCAMyRef")], texName = "t#bar{t}")
#TT01j2lCAMyRef.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v3/TT01j2lCAMyRef_reweight_card.pkl"
TT01j2lCAOldRef_Mtt500_ext      = Sample.fromDirectory( "TT01j2lCAOldRef_Mtt500_ext", [os.path.join( directory, "TT01j2lCAOldRef_Mtt500_ext")], texName = "t#bar{t}")
TT01j2lCAOldRef_Mtt500_ext.reweight_pkl = "/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v4/TT01j2lCAOldRef_reweight_card.pkl"

TT01j2lCAOldRef_Mtt500_small      = copy.deepcopy( TT01j2lCAOldRef_Mtt500_ext )
TT01j2lCAOldRef_Mtt500_small.name = "TT01j2lCAOldRef_Mtt500_small"
TT01j2lCAOldRef_Mtt500_small.files = TT01j2lCAOldRef_Mtt500_ext.files[:50] 

TT01j2lCAOldRef_Mtt500_20percent      = copy.deepcopy( TT01j2lCAOldRef_Mtt500_ext )
TT01j2lCAOldRef_Mtt500_20percent.name = "TT01j2lCAOldRef_Mtt500_20percent"
TT01j2lCAOldRef_Mtt500_20percent.reduceFiles( factor=5 ) 

TT01j2lCAOldRef_Mtt500_50percent      = copy.deepcopy( TT01j2lCAOldRef_Mtt500_ext )
TT01j2lCAOldRef_Mtt500_50percent.name = "TT01j2lCAOldRef_Mtt500_50percent"
TT01j2lCAOldRef_Mtt500_50percent.reduceFiles( factor=2 ) 
