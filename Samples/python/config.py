import os

# Default "latest & greatest"

location_data_UL2016             = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2016/dilep-ht500/"
location_data_UL2016_preVFP      = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2016_preVFP/dilep-ht500/"
location_data_UL2017             = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2017/dilep-ht500/"
location_data_UL2018             = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2018/dilep-ht500/"

location_mc_UL2016               = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2016/dilep-ht500/"
location_mc_UL2016_preVFP        = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2016_preVFP/dilep-ht500/"
location_mc_UL2017               = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2017/dilep-ht500/"
location_mc_UL2018               = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v4/UL2018/dilep-ht500/"

#elif os.environ["USER"] in ["robert.schoefbeck"]:
#    pass

lumi_era = {"Run2016" : (16.5)*1000, "Run2016_preVFP" : (19.5)*1000, "Run2017" : (41.5)*1000, "Run2018" : (59.97)*1000}
