import os, sys
from RootTools.core.Sample import Sample
import ROOT

import logging
logger = logging.getLogger(__name__)

from TT2lUnbinned.Samples.color import color

directory_ = "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v8/"
subdir_    = "singlelep-njet2p-met30"

def make_dirs( dirs ):
    return os.path.join( directory_, *dirs )


#UL2016/singlelep-njet2p-met30/TBar_tWch
#UL2016/singlelep-njet2p-met30/TBar_tch_pow
#UL2016/singlelep-njet2p-met30/TTLep_pow_CP5
#UL2016/singlelep-njet2p-met30/TTSingleLep_pow_CP5
#UL2016/singlelep-njet2p-met30/T_tWch
#UL2016/singlelep-njet2p-met30/T_tch_pow
#UL2016/singlelep-njet2p-met30/t_sch
#UL2016_preVFP/singlelep-njet2p-met30/TBar_tWch
#UL2016_preVFP/singlelep-njet2p-met30/TBar_tch_pow
#UL2016_preVFP/singlelep-njet2p-met30/TTLep_pow_CP5
#UL2016_preVFP/singlelep-njet2p-met30/TTSingleLep_pow_CP5
#UL2016_preVFP/singlelep-njet2p-met30/T_tWch
#UL2016_preVFP/singlelep-njet2p-met30/T_tch_pow
#UL2016_preVFP/singlelep-njet2p-met30/t_sch
#UL2017/singlelep-njet2p-met30/TBar_tWch
#UL2017/singlelep-njet2p-met30/TBar_tch_pow
#UL2017/singlelep-njet2p-met30/TTLep_pow_CP5
#UL2017/singlelep-njet2p-met30/TTSingleLep_pow_CP5
#UL2017/singlelep-njet2p-met30/T_tWch
#UL2017/singlelep-njet2p-met30/T_tch_pow
#UL2017/singlelep-njet2p-met30/t_sch
#UL2018/singlelep-njet2p-met30/TBar_tWch
#UL2018/singlelep-njet2p-met30/TBar_tch_pow
#UL2018/singlelep-njet2p-met30/TTLep_pow_CP5
#UL2018/singlelep-njet2p-met30/TTSingleLep_pow_CP5
#UL2018/singlelep-njet2p-met30/T_tWch
#UL2018/singlelep-njet2p-met30/T_tch_pow
#UL2018/singlelep-njet2p-met30/t_sch



TBar_tWch_Summer16_preVFP          = Sample.fromDirectory(name="TBar_tWch_Summer16_preVFP",           color=color.tW , texName="#bar{t}W (16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"TBar_tWch"] ))
TBar_tch_pow_Summer16_preVFP       = Sample.fromDirectory(name="TBar_tch_pow_Summer16_preVFP",        color=color.tCh, texName="#bar{t} t-chan. (16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"TBar_tch_pow"] ))
TTLep_pow_CP5_Summer16_preVFP      = Sample.fromDirectory(name="TTLep_pow_CP5_Summer16_preVFP",       color=color.TT , texName="t#bar{t} (2l, 16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"TTLep_pow_CP5"] ))
TTSingleLep_pow_CP5_Summer16_preVFP= Sample.fromDirectory(name="TTSingleLep_pow_CP5_Summer16_preVFP", color=color.TT , texName="t#bar{t} (1l, 16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"TTSingleLep_pow_CP5"] ))
T_tWch_Summer16_preVFP             = Sample.fromDirectory(name="T_tWch_Summer16_preVFP",              color=color.tW , texName="tW (16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"T_tWch"] ))
T_tch_pow_Summer16_preVFP          = Sample.fromDirectory(name="T_tch_pow_Summer16_preVFP",           color=color.tCh, texName="t t-chan. (16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"T_tch_pow"] ))
t_sch_Summer16_preVFP              = Sample.fromDirectory(name="t_sch_Summer16_preVFP",               color=color.sCh , texName="t s-chan. (16, pre)", directory=make_dirs( ['UL2016_preVFP', subdir_,"t_sch"] ))

TBar_tWch_Summer16           = Sample.fromDirectory(name="TBar_tWch_Summer16",          color=color.tW , texName="#bar{t}W (16)"       , directory=make_dirs( ['UL2016', subdir_,"TBar_tWch"] ))
TBar_tch_pow_Summer16        = Sample.fromDirectory(name="TBar_tch_pow_Summer16",       color=color.tCh, texName="#bar{t} t-chan (16)" , directory=make_dirs( ['UL2016', subdir_,"TBar_tch_pow"] ))
TTLep_pow_CP5_Summer16       = Sample.fromDirectory(name="TTLep_pow_CP5_Summer16",      color=color.TT , texName="t#bar{t} (2l, 16)"   , directory=make_dirs( ['UL2016', subdir_,"TTLep_pow_CP5"] ))
TTSingleLep_pow_CP5_Summer16 = Sample.fromDirectory(name="TTSingleLep_pow_CP5_Summer16",color=color.TT , texName="t#bar{t} (1l, 16)"   , directory=make_dirs( ['UL2016', subdir_,"TTSingleLep_pow_CP5"] ))
T_tWch_Summer16              = Sample.fromDirectory(name="T_tWch_Summer16",             color=color.tW , texName="tW (16)"             , directory=make_dirs( ['UL2016', subdir_,"T_tWch"] ))
T_tch_pow_Summer16           = Sample.fromDirectory(name="T_tch_pow_Summer16",          color=color.tCh, texName="t t-chan. (16)"      , directory=make_dirs( ['UL2016', subdir_,"T_tch_pow"] ))
t_sch_Summer16               = Sample.fromDirectory(name="t_sch_Summer16",              color=color.sCh , texName="t s-chan. (16)"      , directory=make_dirs( ['UL2016', subdir_,"t_sch"] ))


TBar_tWch_Fall17             = Sample.fromDirectory(name="TBar_tWch_Fall17",            color=color.tW , texName="#bar{t}W (17)"       , directory=make_dirs( ['UL2017', subdir_,"TBar_tWch"] ))
TBar_tch_pow_Fall17          = Sample.fromDirectory(name="TBar_tch_pow_Fall17",         color=color.tCh, texName="#bar{t} t-chan (17)" , directory=make_dirs( ['UL2017', subdir_,"TBar_tch_pow"] ))
TTLep_pow_CP5_Fall17         = Sample.fromDirectory(name="TTLep_pow_CP5_Fall17",        color=color.TT , texName="t#bar{t} (2l, 17)"   , directory=make_dirs( ['UL2017', subdir_,"TTLep_pow_CP5"] ))
TTSingleLep_pow_CP5_Fall17   = Sample.fromDirectory(name="TTSingleLep_pow_CP5_Fall17",  color=color.TT , texName="t#bar{t} (1l, 17)"   , directory=make_dirs( ['UL2017', subdir_,"TTSingleLep_pow_CP5"] ))
T_tWch_Fall17                = Sample.fromDirectory(name="T_tWch_Fall17",               color=color.tW , texName="tW (17)"             , directory=make_dirs( ['UL2017', subdir_,"T_tWch"] ))
T_tch_pow_Fall17             = Sample.fromDirectory(name="T_tch_pow_Fall17",            color=color.tCh, texName="t t-chan. (17)"      , directory=make_dirs( ['UL2017', subdir_,"T_tch_pow"] ))
t_sch_Fall17                 = Sample.fromDirectory(name="t_sch_Fall17",                color=color.sCh , texName="t s-chan. (17)"      , directory=make_dirs( ['UL2017', subdir_,"t_sch"] ))

TBar_tWch_Autumn18           = Sample.fromDirectory(name="TBar_tWch_Autumn18",          color=color.tW , texName="#bar{t}W (18)"      , directory=make_dirs( ['UL2018', subdir_,"TBar_tWch"] ))
TBar_tch_pow_Autumn18        = Sample.fromDirectory(name="TBar_tch_pow_Autumn18",       color=color.tCh, texName="#bar{t} t-chan (18)", directory=make_dirs( ['UL2018', subdir_,"TBar_tch_pow"] ))
TTLep_pow_CP5_Autumn18       = Sample.fromDirectory(name="TTLep_pow_CP5_Autumn18",      color=color.TT , texName="t#bar{t} (2l, 18)"  , directory=make_dirs( ['UL2018', subdir_,"TTLep_pow_CP5"] ))
TTSingleLep_pow_CP5_Autumn18 = Sample.fromDirectory(name="TTSingleLep_pow_CP5_Autumn18",color=color.TT , texName="t#bar{t} (1l, 18)"  , directory=make_dirs( ['UL2018', subdir_,"TTSingleLep_pow_CP5"] ))
T_tWch_Autumn18              = Sample.fromDirectory(name="T_tWch_Autumn18",             color=color.tW , texName="tW (18)"            , directory=make_dirs( ['UL2018', subdir_,"T_tWch"] ))
T_tch_pow_Autumn18           = Sample.fromDirectory(name="T_tch_pow_Autumn18",          color=color.tCh, texName="t t-chan. (18)"     , directory=make_dirs( ['UL2018', subdir_,"T_tch_pow"] ))
t_sch_Autumn18               = Sample.fromDirectory(name="t_sch_Autumn18",              color=color.sCh , texName="t s-chan. (18)"     , directory=make_dirs( ['UL2018', subdir_,"t_sch"] ))
