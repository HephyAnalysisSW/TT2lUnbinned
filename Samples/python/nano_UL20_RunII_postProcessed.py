from RootTools.core.standard import *

#from TT2lUnbinned.Samples.nano_data_private_UL20_Run2016_postProcessed import Run2016
#from TT2lUnbinned.Samples.nano_data_private_UL20_Run2016_preVFP_postProcessed import Run2016_preVFP
#from TT2lUnbinned.Samples.nano_data_private_UL20_Run2017_postProcessed import Run2017
#from TT2lUnbinned.Samples.nano_data_private_UL20_Run2018_postProcessed import Run2018
#
#RunII      = Sample.combine( "RunII", [Run2016, Run2016_preVFP, Run2017, Run2018], texName = "Data (Run II)")
#RunII.lumi = Run2016.lumi + Run2016_preVFP.lumi + Run2017.lumi + Run2018.lumi
#
#lumi_era  = {'Run2016':Run2016.lumi, 'Run2016_preVFP':Run2016_preVFP.lumi, 'Run2017':Run2017.lumi, 'Run2018':Run2018.lumi}

import TT2lUnbinned.Samples.nano_mc_UL20_Summer16_preVFP_postProcessed as Summer16_preVFP
import TT2lUnbinned.Samples.nano_mc_UL20_Summer16_postProcessed as Summer16
import TT2lUnbinned.Samples.nano_mc_UL20_Fall17_postProcessed as Fall17
import TT2lUnbinned.Samples.nano_mc_UL20_Autumn18_postProcessed as Autumn18

TTLep           = Sample.combine( "TTLep", [Summer16_preVFP.TTLep_Summer16_preVFP, Summer16.TTLep_Summer16, Fall17.TTLep_Fall17, Autumn18.TTLep_Autumn18], texName = "t#bar{t}")
#TTLep_pow_hDown = Sample.combine( "TTLep_pow_hDown", [Summer16_preVFP.TTLep_pow_hDown, Summer16.TTLep_pow_hDown, Fall17.TTLep_pow_hDown, Autumn18.TTLep_pow_hDown], texName = "t#bar{t}")
#TTLep_pow_hUp   = Sample.combine( "TTLep_pow_hUp", [Summer16_preVFP.TTLep_pow_hUp, Summer16.TTLep_pow_hUp, Fall17.TTLep_pow_hUp, Autumn18.TTLep_pow_hUp], texName = "t#bar{t}")
#ST          = Sample.combine( "ST",    [Summer16_preVFP.ST, Summer16.ST, Fall17.ST, Autumn18.ST],             texName = "t/tW")
#DY          = Sample.combine( "DY",    [Summer16_preVFP.DY, Summer16.DY, Fall17.DY, Autumn18.DY],             texName = "DY")

#TT01j1lCAv2Ref_HT800 =  Sample.combine( "TT01j1lCAv2Ref_HT800", [Summer16_preVFP.TT01j1lCAv2Ref_HT800, Summer16.TT01j1lCAv2Ref_HT800, Fall17.TT01j1lCAv2Ref_HT800, Autumn18.TT01j1lCAv2Ref_HT800], texName = "TT01j1lCAv2Ref_HT800") 
#TT01j1lCAv2Ref_HT800.reweight_pkl = '/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA/TT01j1lCARef_HT800_reweight_card.pkl'

#TT01j2lCAv2Ref_HT500 =  Sample.combine( "TT01j2lCAv2Ref_HT500", [Summer16_preVFP.TT01j2lCAv2Ref_HT500, Summer16.TT01j2lCAv2Ref_HT500, Fall17.TT01j2lCAv2Ref_HT500, Autumn18.TT01j2lCAv2Ref_HT500], texName = "TT01j2lCAv2Ref_HT500") 
#TT01j2lCAv2Ref_HT500.reweight_pkl = '/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA/TT01j2lCARef_HT500_reweight_card.pkl'
