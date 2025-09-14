#python nanoPostProcessing.py --forceProxy --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --sample TT01j2lCAv2Ref_HT500  #SPLIT100
#python nanoPostProcessing.py --forceProxy --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --sample TT01j1lCAv2Ref_HT800  #SPLIT100
#

python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --flagTT --sample TTSingleLep_pow_CP5  #SPLIT138
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --flagTT --sample t_sch  #SPLIT19
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --flagTT --sample TTLep_pow_CP5  #SPLIT49
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --sample T_tch_pow   #SPLIT86
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --sample TBar_tch_pow  #SPLIT35
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --sample T_tWch  #SPLIT11
python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim singlelep-njet2p-met30 --era UL2016 --processingEra TT2lUnbinned_v8 --noTriggerSelection --sample TBar_tWch  #SPLIT10

#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --normalizeSys  --sample TTLep_pow_CP5  #SPLIT49
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --normalizeSys  --sigmaJEC 0.5 --sample TTLep_pow_CP5  #SPLIT49
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --normalizeSys  --sigmaJEC 1.5 --sample TTLep_pow_CP5  #SPLIT49
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTT --normalizeSys  --sigmaJEC 2.0 --sample TTLep_pow_CP5  #SPLIT49
#python nanoPostProcessing.py  --forceProxy --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTLep_pow_CP5_hDown #SPLIT18
#python nanoPostProcessing.py  --forceProxy --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTLep_pow_CP5_hUp #SPLIT24
#
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --flagTTbb --normalizeSys --sample TTbb  #SPLIT3
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample T_tch_pow   #SPLIT86
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TBar_tch_pow  #SPLIT35
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample T_tWch  #SPLIT11
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TBar_tWch  #SPLIT10
##python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample TTTT  #SPLIT100
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTWToLNu #SPLIT50
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTWToQQ #SPLIT10
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTZToLLNuNu #SPLIT50
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTZToLLNuNu_m1to10 #SPLIT18
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTZToQQ #SPLIT50
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTHnobb #SPLIT40
#python nanoPostProcessing.py --forceProxy --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample TTHTobb #SPLIT50
#
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT100to200 #SPLIT43
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT200to400 #SPLIT26
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT400to600 #SPLIT32
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT600to800 #SPLIT7
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT800to1200 #SPLIT36
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT1200to2500 #SPLIT19
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50_HT2500toInf #SPLIT22
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M4to50_HT100to200 #SPLIT41
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M4to50_HT200to400 #SPLIT38
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M4to50_HT400to600 #SPLIT45
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M4to50_HT600toInf #SPLIT11
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M10to50_LO #SPLIT34
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --normalizeSys --sample DYJetsToLL_M50 #SPLIT50
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample DYJetsToLL_M50_NLO #SPLIT41
#
#
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WZTo3LNu #SPLIT31
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WWTo2L2Nu #SPLIT7
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WWDoubleTo2L #SPLIT29
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WWTo1L1Nu2Q #SPLIT30
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WWTo4Q #SPLIT40
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample ZZTo2L2Nu #SPLIT15
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample ZZTo2L2Q #SPLIT14
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample ZZTo2Q2Nu #SPLIT23
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample ZZTo4L #SPLIT99
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WZTo1L3Nu #SPLIT21
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WZTo1L1Nu2Q #SPLIT23
#python nanoPostProcessing.py --forceProxy --central --central --btag_WP loose --skim dilep --era UL2016 --processingEra TT2lUnbinned_v7 --sample WZTo2L2Q #SPLIT39
