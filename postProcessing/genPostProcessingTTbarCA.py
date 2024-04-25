#!/usr/bin/env python
'''  produce fat jet ntuple 
'''
#
# Standard imports and batch mode
#
import os, sys, imp, uuid
import copy, shutil
import random
import ROOT
ROOT.gROOT.SetBatch(True)
from math                             import sqrt, cos, sin, pi, acos, cosh, sinh
import numpy as np
#RootTools
from RootTools.core.standard          import *

#Analysis
from Analysis.Tools.WeightInfo        import WeightInfo
from Analysis.Tools.HyperPoly2        import HyperPoly
from Analysis.Tools.GenSearch         import GenSearch
from Analysis.Tools.helpers           import deltaPhi, deltaR, deltaR2, checkRootFile
from Analysis.Tools.DelphesProducer   import DelphesProducer

# HadronicSMEFT
import TT2lUnbinned.Tools.user                 as user
from TT2lUnbinned.Tools.genObjectSelection     import genJetId
from TT2lUnbinned.Tools.DelphesObjectSelection import isGoodRecoLepton, isGoodRecoJet, isGoodRecoPhoton
import TT2lUnbinned.Tools.fixTVecMul

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--genTTbar',           action='store_true', help='Store parton-level truth for ttbar?')#, default = True)
#argParser.add_argument('--central',            action='store_true', help='A central sample?')#, default = True)
argParser.add_argument('--miniAOD',            action='store_true', help='miniAOD sample?')#, default = True)
argParser.add_argument('--overwrite',          action='store',      nargs='?', choices = ['none', 'all', 'target'], default = 'none', help='Overwrite?')#, default = True)
argParser.add_argument('--targetDir',          action='store',      default='v1')
#argParser.add_argument('--sample',             action='store',      default='tt1LepHad', help="Name of the sample loaded from fwlite_benchmarks. Only if no inputFiles are specified")
argParser.add_argument('--sample',             action='store',      nargs='?',  type=str, default='TTlep_pow_16', help="Sample to be post-processed" )
argParser.add_argument('--inputFiles',         action='store',      nargs = '*', default=[])
argParser.add_argument('--targetSampleName',   action='store',      help="Name of the sample if files are used.")
argParser.add_argument('--targetFileName',     action='store',      default=None, type=str, help="targetFileName? If not specified, sample name is used")
argParser.add_argument('--delphesEra',         action='store',      default = "RunII", choices = ["RunII", "ATLAS", "RunIICentral", "RunIInoDelphesIso", "RunIIPileUp", "PhaseII", "None"], help="specify delphes era")
argParser.add_argument('--addEFTWeights',       action='store_true', help="Add reweights?")
argParser.add_argument('--addGenWeights',       action='store_true', help="Add all the PDF/ME/PS weights?")
argParser.add_argument('--nJobs',              action='store',      nargs='?', type=int, default=1,  help="Maximum number of simultaneous jobs.")
argParser.add_argument('--job',                action='store',      nargs='?', type=int, default=0,  help="Run only job i")
argParser.add_argument('--removeDelphesFiles', action='store_true', help="remove Delphes file after postprocessing?")
argParser.add_argument('--fakeB',              action='store',  type=int, default=0, help="Randomly fake b")
argParser.add_argument('--interpolationOrder', action='store',      nargs='?', type=int, default=2,  help="Interpolation order for EFT weights.")
argParser.add_argument('--trainingCoefficients', action='store',    nargs='*', default=[],  help="Training vectors for particle net")
args = argParser.parse_args()

# Logger
import TT2lUnbinned.Tools.logger as _logger
import RootTools.core.logger as _logger_rt
logger    = _logger.get_logger(   args.logLevel, logFile = None)
logger_rt = _logger_rt.get_logger(args.logLevel, logFile = None)

# Load sample either from 
if len(args.inputFiles)>0:
    logger.info( "Input files found. Ignoring 'sample' argument. Files: %r", args.inputFiles)
    sample = FWLiteSample( args.targetSampleName, args.inputFiles)
else:
    if args.miniAOD:
        sample_file = "$CMSSW_BASE/python/TT2lUnbinned/Samples/central_miniAOD.py"
    else:
        sample_file = "$CMSSW_BASE/python/TT2lUnbinned/Samples/private_GEN.py"
    all_samples = imp.load_source( "samples", os.path.expandvars( sample_file ) )
    sample = getattr( all_samples, args.sample )
    logger.debug( 'Loaded sample %s with %i files.', sample.name, len(sample.files) )

maxEvents = -1
if args.small: 
    args.targetDir += "_small"
    maxEvents       = 100 
    sample.files=sample.files[:1]

if args.fakeB>0:
    args.targetDir += ("_fakeB%i"%args.fakeB)

# variables (to be stored)
variables = []

# Load reweight pickle file if supposed to keep weights. 
if args.addEFTWeights:
    weightInfo = WeightInfo( sample.reweight_pkl )
    weightInfo.set_order( args.interpolationOrder ) 
    # Determine coefficients for storing in vector
    # Sort Ids wrt to their position in the card file

    # weights from base base points 
    weight_base      = TreeVariable.fromString( "weight[base/F]")
    weight_base.nMax = weightInfo.nid
    variables.append(weight_base)

    # coefficients for the weight parametrization
    param_vector      = TreeVariable.fromString( "p[C/F]" )
    param_vector.nMax = HyperPoly.get_ndof(weightInfo.nvar, args.interpolationOrder)
    hyperPoly         = HyperPoly( args.interpolationOrder )
    variables.append(param_vector)
    #variables.append(TreeVariable.fromString( "chi2_ndof/F"))
    def interpret_weight(weight_id):
        str_s = weight_id.rstrip('_nlo').split('_')
        res={}
        for i in range(len(str_s)/2):
            res[str_s[2*i]] = float(str_s[2*i+1].replace('m','-').replace('p','.'))
        return res

    # Suddenly only lower case weight.id ... who on earth does such things?
    weightInfo_data_lower = {k.lower():val for k, val in weightInfo.data.iteritems()}
    weightInfo_data_lower.update(weightInfo.data)

# output directory
output_directory = os.path.join(user.postprocessing_output_directory, 'delphes', args.targetDir, sample.name) 

if not os.path.exists( output_directory ): 
    try:
        os.makedirs( output_directory )
    except OSError:
        pass
    logger.info( "Created output directory %s", output_directory )

# Run only job number "args.job" from total of "args.nJobs"
xSection      = sample.xSection
normalization = sample.normalization 
if args.nJobs>1:
    n_files_before = len(sample.files)
    sample = sample.split(args.nJobs)[args.job]
    n_files_after  = len(sample.files)
    logger.info( "Running job %i/%i over %i files from a total of %i.", args.job, args.nJobs, n_files_after, n_files_before)

# tmp_output_directory
tmp_output_directory  = os.path.join( user.postprocessing_tmp_directory, str(uuid.uuid3(uuid.NAMESPACE_OID, sample.name)) )
try:    #Avoid trouble with race conditions in multithreading
    os.makedirs(tmp_output_directory)
    logger.info( "Created output directory %s.", tmp_output_directory )
except:
    pass

# output file & log files
output_filename =  os.path.join(output_directory, (args.targetFileName if args.targetFileName is not None else sample.name)+ '.root')
_logger.   add_fileHandler( output_filename.replace('.root', '.log'), args.logLevel )
_logger_rt.add_fileHandler( output_filename.replace('.root', '_rt.log'), args.logLevel )

# Check whether we have to do anything
if os.path.exists( output_filename ) and checkRootFile( output_filename, checkForObjects=["Events"]) and args.overwrite =='none' :
    logger.info( "File %s found. Quit.", output_filename )
    sys.exit(0)

# small helpers
def makeP4(cand):
     v = ROOT.TLorentzVector()
     v.SetPtEtaPhiM(cand.pt(),cand.eta(),cand.phi(),cand.mass())
     return v
def makeP4FromComp(pt, eta, phi, mass):
     v = ROOT.TLorentzVector()
     v.SetPtEtaPhiM(pt, eta, phi, mass)
     return v

def varnames( vec_vars ):
    return [v.split('/')[0] for v in vec_vars.split(',')]

def addIndex( collection ):
    for i  in range(len(collection)):
        collection[i]['index'] = i

def vecSumPt(*args):
    return sqrt( sum([o['pt']*cos(o['phi']) for o in args],0.)**2 + sum([o['pt']*sin(o['phi']) for o in args],0.)**2 )

def fill_vector_collection( event, collection_name, collection_varnames, objects):
    setattr( event, "n"+collection_name, len(objects) )
    for i_obj, obj in enumerate(objects):
        for var in collection_varnames:
            getattr(event, collection_name+"_"+var)[i_obj] = obj[var]

def fill_vector( event, collection_name, collection_varnames, obj):
    for var in collection_varnames:
        try:
            setattr(event, collection_name+"_"+var, obj[var] )
        except TypeError as e:
            logger.error( "collection_name %s var %s obj[var] %r", collection_name, var,  obj[var] )
            raise e
        except KeyError as e:
            logger.error( "collection_name %s var %s obj[var] %r", collection_name, var,  obj[var] )
            raise e

# Delphes reader if we run Delphes
from TT2lUnbinned.Tools.DelphesReaderEFlow     import DelphesReader
if args.delphesEra == 'RunII':
    delphesCard = 'delphes_card_CMS'
elif args.delphesEra == 'ATLAS':
    delphesCard = 'delphes_card_ATLAS'
elif args.delphesEra == 'RunIICentral':
    delphesCard = 'delphes_card_CMS_Central'
elif args.delphesEra == 'RunIInoDelphesIso':
    delphesCard = 'delphes_card_CMS_noLepIso'
elif args.delphesEra == 'RunIIPileUp':
    delphesCard = 'delphes_card_CMS_PileUp'
elif args.delphesEra == 'PhaseII':
    delphesCard = 'CMS_PhaseII/CMS_PhaseII_200PU_v03'
elif args.delphesEra == "None":
    delphesCard     = None
    args.delphesEra = None

if args.addEFTWeights:
    # for each Wilson coefficient listed in args.trainingCoefficients, store a separate length-3 ntuple of ('w0'*10**6, 'w1', 'w2') to facilitate particle-net training 
    for coefficient in args.trainingCoefficients:    
        variables += [VectorTreeVariable.fromString("%s[coeff/F]"%coefficient, nMax=3 )]

# EDM standard variables
variables  += ["run/I", "lumi/I", "evt/l", "weight1fb/F", "ht/F"]


if args.addGenWeights:
    # PDF weights (run runcmsgrid.sh 100 1 from gridpack and look up the pdf sets)
    PDF_index = {}
    for i in range(100):
        variables.append( "PDF_%03i/F"%i ) 
        PDF_index[str(2001+i+1)] = "PDF_%03i"%i
    # ME scale weights
    ME_scales_index = {'1001':'muR1p0_muF1p0', '1002':'muR1p0_muF2p0',  '1003':'muR1p0_muF0p5', '1004': 'muR2p0_muF1p0',  '1005':'muR2p0_muF2p0', '1006': 'muR2p0_muF0p5',  '1007':'muR0p5_muF1p0',  '1008':'muR0p5_muF2p0', '1009':'muR0p5_muF0p5'}
    for w in ME_scales_index.values():
        variables.append( w+"/F" )

    # PS ISR/FSR weights https://twiki.cern.ch/twiki/bin/view/CMS/TopModGen#Event_Generation
    variables += ["isrRedHi/F", "fsrRedHi/F", "isrRedLo/F", "fsrRedLo/F", "isrDefHi/F", "fsrDefHi/F", "fsrDefLo/F", "isrConHi/F", "isrConLo/F", "fsrConLo/F"]
    PS_weight_index = { 2:'isrRedHi', 3:'fsrRedHi', 4:'isrRedLo', 5:'fsrRedLo', 6:'isrDefHi', 7:'fsrDefHi', 8:'isrDefLo', 9:'fsrDefLo', 10:'isrConHi', 11:'fsrConHi', 12:'isrConLo', 13:'fsrConLo' }
    for w in PS_weight_index.values():
        variables.append( w+"/F" )

# lepton vector 
lep_vars       =  "pt/F,eta/F,phi/F,pdgId/I,status/I"
lep_extra_vars =  "mother_pdgId/I,grandmother_pdgId/I"
lep_varnames   =  varnames( lep_vars )
lep_all_varnames = lep_varnames + varnames(lep_extra_vars)
variables     += ["genLep[%s]"%(','.join([lep_vars, lep_extra_vars]))]

if args.genTTbar:
    variables += ["parton_top1_pt/F", "parton_top1_eta/F", "parton_top1_phi/F", "parton_top1_mass/F", "parton_top1_pdgId/I", 
                  #"parton_top1_decayAngle_theta/F", "parton_top1_decayAngle_phi/F", 
                  "parton_top1_isHad/I", "parton_top1_isLep/I"]
    variables += ["parton_top1_f1_pt/F",  "parton_top1_f1_eta/F",  "parton_top1_f1_phi/F",  "parton_top1_f1_mass/F",  "parton_top1_f1_pdgId/I"]
    variables += ["parton_top1_f2_pt/F",  "parton_top1_f2_eta/F",  "parton_top1_f2_phi/F",  "parton_top1_f2_mass/F",  "parton_top1_f2_pdgId/I"]
    variables += ["parton_top1_b_pt/F",   "parton_top1_b_eta/F",   "parton_top1_b_phi/F",   "parton_top1_b_mass/F",   "parton_top1_b_pdgId/I"]
    variables += ["parton_top1_W_pt/F",   "parton_top1_W_eta/F",   "parton_top1_W_phi/F",   "parton_top1_W_mass/F", "parton_top1_W_pdgId/I"]

    variables += ["parton_top2_pt/F",   "parton_top2_eta/F",   "parton_top2_phi/F",   "parton_top2_mass/F",  "parton_top2_pdgId/I", 
                  #"parton_top2_decayAngle_theta/F", "parton_top2_decayAngle_phi/F", 
                  "parton_top2_isHad/I", "parton_top2_isLep/I"]
    variables += ["parton_top2_f1_pt/F", "parton_top2_f1_eta/F", "parton_top2_f1_phi/F", "parton_top2_f1_mass/F", "parton_top2_f1_pdgId/I"]
    variables += ["parton_top2_f2_pt/F", "parton_top2_f2_eta/F", "parton_top2_f2_phi/F", "parton_top2_f2_mass/F", "parton_top2_f2_pdgId/I"]
    variables += ["parton_top2_b_pt/F", "parton_top2_b_eta/F", "parton_top2_b_phi/F", "parton_top2_b_mass/F", "parton_top2_b_pdgId/I"]
    variables += ["parton_top2_W_pt/F", "parton_top2_W_eta/F", "parton_top2_W_phi/F", "parton_top2_W_mass/F", "parton_top2_W_pdgId/I"]

    variables += ["parton_top12_pt/F", "parton_top12_mass/F", "parton_top12_eta/F", "parton_top12_dEta/F", "parton_top12_dAbsEta/F"]

    variables += ["parton_cosThetaPlus_n/F", "parton_cosThetaMinus_n/F", "parton_cosThetaPlus_r/F", "parton_cosThetaMinus_r/F", "parton_cosThetaPlus_k/F", "parton_cosThetaMinus_k/F", 
                  "parton_cosThetaPlus_r_star/F", "parton_cosThetaMinus_r_star/F", "parton_cosThetaPlus_k_star/F", "parton_cosThetaMinus_k_star/F",
                  "parton_xi_nn/F", "parton_xi_rr/F", "parton_xi_kk/F", 
                  "parton_xi_nr_plus/F", "parton_xi_nr_minus/F", "parton_xi_rk_plus/F", "parton_xi_rk_minus/F", "parton_xi_nk_plus/F", "parton_xi_nk_minus/F", 
                  "parton_xi_r_star_k/F", "parton_xi_k_r_star/F", "parton_xi_kk_star/F",
                  "parton_cos_phi/F", "parton_cos_phi_lab/F", "parton_abs_delta_phi_ll_lab/F",
                 ] 
 
if args.delphesEra is not None:

    from Analysis.TopReco.TopReco import TopReco
    topReco = TopReco( ROOT.Era.run2_13tev_2016, 2, 1, 0, tagger='bTag')

    # reconstructed leptons
    recoLep_vars       = "pt/F,eta/F,phi/F,pdgId/I,isolationVar/F,isolationVarRhoCorr/F,sumPtCharged/F,sumPtNeutral/F,sumPtChargedPU/F,sumPt/F,ehadOverEem/F,genMatched/I,MT/F"
    variables         += ["recoLep[%s]"%recoLep_vars]
    recoLep_varnames   = varnames( recoLep_vars )

    # reconstructed jets
    #btagWPs = ["loose"]#, "medium", "tight"] #, "looswMTD", "mediumMTD", "tightMTD"]
    #default_btagWP = "loose"
    variables.append( "nBTag/I" )
    recoJet_vars    = 'pt/F,eta/F,phi/F,bTag/I,nCharged/I,nNeutrals/I,trueB/I,trueC/I'#,matchGenBJet/I'#,pt_JEC_up/F,pt_JEC_up/F'

    variables += ["recoJet[%s]"%recoJet_vars]
    recoJet_varnames = varnames( recoJet_vars )
    variables += ["recoBj0_%s"%var for var in recoJet_vars.split(',')]
    variables += ["recoBj1_%s"%var for var in recoJet_vars.split(',')]

    variables += ["recoMet_pt/F", "recoMet_phi/F"]
    variables += ["delphesGenMet_pt/F", "delphesGenMet_phi/F"]

    variables += ["recoBj01_pt/F", "recoBj01_mass/F"]
    variables += ["recoLep0_pt/F", "recoLep0_eta/F", "recoLep1_pt/F", "recoLep1_eta/F", "recoLepPos_pt/F", "recoLepPos_eta/F", "recoLepPos_phi/F", "recoLepNeg_pt/F", "recoLepNeg_eta/F", "recoLepNeg_phi/F", "recoLep01_pt/F", "recoLep01_mass/F", "recoLep_dPhi/F", "recoLep_dEta/F", "recoLep_dAbsEta/F"]

    variables.extend( [
        "tr_jetB_index/I", "tr_jetBbar_index/I", "tr_ntags/I",
        "tr_neutrino_pt/F", "tr_neutrino_eta/F", "tr_neutrino_phi/F", "tr_neutrino_mass/F",
        "tr_neutrinoBar_pt/F", "tr_neutrinoBar_eta/F", "tr_neutrinoBar_phi/F", "tr_neutrinoBar_mass/F",
        "tr_ttbar_pt/F", "tr_ttbar_eta/F", "tr_ttbar_phi/F", "tr_ttbar_mass/F", "tr_ttbar_dAbsEta/F", "tr_ttbar_dEta/F",
        "tr_top_pt/F", "tr_top_eta/F", "tr_top_phi/F", "tr_top_mass/F", "tr_topBar_pt/F", "tr_topBar_eta/F", "tr_topBar_phi/F", "tr_topBar_mass/F",
        "tr_Wminus_pt/F", "tr_Wminus_eta/F", "tr_Wminus_phi/F", "tr_Wminus_mass/F", "tr_Wplus_pt/F", "tr_Wplus_eta/F", "tr_Wplus_phi/F", "tr_Wplus_mass/F",
        "tr_cosThetaPlus_n/F", "tr_cosThetaMinus_n/F", "tr_cosThetaPlus_r/F", "tr_cosThetaMinus_r/F", "tr_cosThetaPlus_k/F", "tr_cosThetaMinus_k/F",
        "tr_cosThetaPlus_r_star/F", "tr_cosThetaMinus_r_star/F", "tr_cosThetaPlus_k_star/F", "tr_cosThetaMinus_k_star/F",
        "tr_xi_nn/F", "tr_xi_rr/F", "tr_xi_kk/F",
        "tr_xi_nr_plus/F", "tr_xi_nr_minus/F", "tr_xi_rk_plus/F", "tr_xi_rk_minus/F", "tr_xi_nk_plus/F", "tr_xi_nk_minus/F",
        "tr_xi_r_star_k/F", "tr_xi_k_r_star/F", "tr_xi_kk_star/F",
        "tr_cos_phi/F", "tr_cos_phi_lab/F", "tr_abs_delta_phi_ll_lab/F",
        #"tr_top_decayAngle_phi/F", "tr_top_decayAngle_theta/F", "tr_topBar_decayAngle_phi/F", "tr_topBar_decayAngle_theta/F"
     ]) 

readers = []

# FWLite reader 
products = {
    'lhe':{'type':'LHEEventProduct', 'label':("externalLHEProducer")},
    'gen':{'type':'GenEventInfoProduct', 'label':'generator'},
}
if args.miniAOD:
    products['genJets'] = {'type':'vector<reco::GenJet>', 'label':("slimmedGenJets")}
    products['gp']      = {'type':'vector<reco::GenParticle>', 'label':("prunedGenParticles")}
else:
    products['genJets'] = {'type':'vector<reco::GenJet>', 'label':("ak4GenJetsNoNu")}
    products['gp']      = {'type':'vector<reco::GenParticle>', 'label':("genParticles")}

# relocate original
sample.copy_files( os.path.join(tmp_output_directory, "input") )

fwliteReader = sample.fwliteReader( products = products )
readers.append( fwliteReader )

# some ad-hoc DELPHES jet selection
if args.delphesEra is not None and "ATLAS" in args.delphesEra:
    _isGoodRecoJet    = lambda j:isGoodRecoJet(j, minNCharged=0, minNNeutrals=5)
    _isGoodRecoLepton = lambda l:isGoodRecoLepton(l, maxIso = 0.4)
elif args.delphesEra is not None:
    _isGoodRecoJet    = isGoodRecoJet 
    _isGoodRecoLepton = isGoodRecoLepton

logger.info( "Running over files: %s", ", ".join(sample.files ) )

# run Delphes
if args.delphesEra is not None:
    delphes_file = os.path.join( output_directory, 'delphes', os.path.basename(output_filename) )
    if      ( not os.path.exists( delphes_file )) or \
            ( os.path.exists( delphes_file ) and not checkRootFile( delphes_file, checkForObjects=["Delphes"])) or \
            args.overwrite in ['all']:
        logger.debug( "Reproducing delphes file %s", delphes_file)
        delphesProducer = DelphesProducer( card = delphesCard )
        delphesProducer.produce( sample.files, delphes_file)
    delphesReader = DelphesReader( Sample.fromFiles( delphes_file, delphes_file, treeName = "Delphes" ) ) # RootTools version
    readers.append( delphesReader )

# TreeMaker initialisation
tmp_dir     = ROOT.gDirectory
output_file = ROOT.TFile( output_filename, 'recreate')
output_file.cd()
maker = TreeMaker(
    #sequence  = [ filler ],
    variables = [ (TreeVariable.fromString(x) if type(x)==str else x) for x in variables ],
    treeName = "Events"
    )
tmp_dir.cd()

def filler( event ):

    event.run, event.lumi, event.evt = fwliteReader.evt
    if fwliteReader.position % 100==0: logger.info("At event %i/%i", fwliteReader.position, fwliteReader.nEvents)

    # retrieve weights
    gen_weights = fwliteReader.products['gen'].weights()
    if args.addEFTWeights or args.addGenWeights:
        lhe_weights = fwliteReader.products['lhe'].weights()

    # GEN weights
    nominal = None if args.miniAOD else 1.
    for weight in lhe_weights:
        # PDF weights (run runcmsgrid.sh 100 1 from gridpack and look up the pdf sets)
        if weight.id == '1001' and args.miniAOD:
            nominal = weight.wgt
        if args.addGenWeights:
            if weight.id in PDF_index.keys():
                setattr( event, PDF_index[weight.id], weight.wgt/nominal )
            # ME scale weights
            if weight.id in ME_scales_index.keys():
                setattr( event, ME_scales_index[weight.id], weight.wgt/nominal )

    if args.addGenWeights:
        # PS ISR/FSR weights https://twiki.cern.ch/twiki/bin/view/CMS/TopModGen#Event_Generation
        for i_val in range( gen_weights.size() ):
            if i_val in PS_weight_index.keys():
                setattr( event, PS_weight_index[i_val], gen_weights[i_val]/nominal )
    event.weight1fb = xSection*1000*nominal/normalization

    # EFT weights 
    if args.addEFTWeights:
        event.nweight = weightInfo.nid
        weights      = []
        param_points = []
        for weight in lhe_weights:
            # Store nominal weight (First position!)
            weight_id = weight.id.rstrip('_nlo')
            if weight_id in ['rwgt_1','dummy']: 
                event.rw_nominal = weight.wgt
            #print "Hello weight", weight_id, ( weight_id.lower() in weightInfo_data_lower.keys()) 
            if not weight_id.lower() in weightInfo_data_lower.keys(): 
                continue
            pos = weightInfo_data_lower[weight_id]
            #print "pos", weight.wgt, event.weight_base[pos]
            event.weight_base[pos] = weight.wgt
            weights.append( weight.wgt )
            interpreted_weight = interpret_weight(weight_id.lower()) 
            #for var in weightInfo.variables:
            #    getattr( event, "rw_"+var )[pos] = interpreted_weight[var]
            # weight data for interpolation
            if not hyperPoly.initialized: param_points.append( tuple(interpreted_weight[var.lower()] for var in weightInfo.variables) )

        # get list of values of ref point in specific order
        ref_point_coordinates = [weightInfo.ref_point_coordinates[var] for var in weightInfo.variables]

        # Initialize with Reference Point
        if not hyperPoly.initialized: 
            #print "evt,run,lumi", event.run, event.lumi, event.evt
            #print "ref point", ref_point_coordinates, "param_points", param_points
            #for i_p, p in enumerate(param_points):
                #print "weight", i_p, weights[i_p], " ".join([ "%s=%3.2f"%( weightInfo.variables[i], p[i]) for i in range(len(p)) if p[i]!=0])
            hyperPoly.initialize( param_points, ref_point_coordinates )

        coeff = hyperPoly.get_parametrization( weights )
        event.np = hyperPoly.ndof

        #if fwliteReader.position==3: raise RuntimeError

        #event.chi2_ndof = hyperPoly.chi2_ndof(coeff, weights)
        #logger.debug( "chi2_ndof %f coeff %r", event.chi2_ndof, coeff )
        #if event.chi2_ndof>10**-6: logger.warning( "chi2_ndof is large: %f", event.chi2_ndof )
        for n in xrange(hyperPoly.ndof):
            event.p_C[n] = coeff[n]

        # convinience coefficient vectors for particlenet training
        truth_weight_dict = {}
        for coefficient in args.trainingCoefficients:
            setattr(event, "n"+coefficient, 3)
            getattr(event, coefficient+"_coeff")[0] = event.p_C[0]*10**6
            index_lin  = weightInfo.combinations.index((coefficient,))
            index_quad = weightInfo.combinations.index((coefficient, coefficient))
            getattr(event, coefficient+"_coeff")[1] = event.p_C[index_lin]/event.p_C[0] 
            getattr(event, coefficient+"_coeff")[2] = event.p_C[index_quad]/event.p_C[0]
            truth_weight_dict["truth_"+coefficient+"_lin"] = event.p_C[index_lin]/event.p_C[0]
            truth_weight_dict["truth_"+coefficient+"_quad"] = event.p_C[index_quad]/event.p_C[0]

    # genJets
    genJets   = filter( lambda j: genJetId(j, args.miniAOD),  fwliteReader.products['genJets'] )

    # All gen particles
    gp        = fwliteReader.products['gp']

    # for searching
    search  = GenSearch( gp )

    # generated leptons from SM bosons
    genLeps    = [ (search.ascend(l), l) for l in filter( lambda p:abs(p.pdgId()) in [11, 12, 13, 14, 15, 16]  and abs(p.mother(0).pdgId()) in [22, 23, 24, 25], gp)]
    genLeps.sort( key = lambda p: -p[1].pt() )
    genLeps_from_bosons =  [first for first, last in genLeps]
    genLeps_dict = [ {var: getattr(last, var)() for var in lep_varnames} for first, last in genLeps ]
    addIndex( genLeps_dict )
    for i_genLep, (first, last) in enumerate(genLeps):
        mother = first.mother(0) if first.numberOfMothers()>0 else None
        if mother is not None:
            mother_pdgId      = mother.pdgId()
            mother_ascend     = search.ascend(mother)
            grandmother       = mother_ascend.mother(0) if mother_ascend.numberOfMothers()>0 else None
            grandmother_pdgId = grandmother.pdgId() if grandmother is not None else 0
        else:
            mother_pdgId = 0
            grandmother_pdgId = 0
        genLeps_dict[i_genLep]['mother_pdgId']      = mother_pdgId
        genLeps_dict[i_genLep]['grandmother_pdgId'] = grandmother_pdgId
    fill_vector_collection( event, "genLep", lep_all_varnames, genLeps_dict )

    # all gen-tops
    W_partons = filter( lambda p:abs(p.pdgId())==24 and search.isFirst(p), gp)
    Z_partons = filter( lambda p:abs(p.pdgId())==23 and search.isFirst(p), gp)
    b_partons = filter( lambda p:abs(p.pdgId())==5 and search.isFirst(p) and abs(p.mother(0).pdgId())==6, gp)

    all_b_partons = filter( lambda p:abs(p.pdgId())==5 and search.isFirst(p), gp)
    all_c_partons = filter( lambda p:abs(p.pdgId())==4 and search.isFirst(p), gp)

    # require at least two W close to the resonance

    # sanity
    isGenTTbar = True
    if len(W_partons)<2: 
        isGenTTbar = False 
    elif not len(W_partons)==len(b_partons)==2:
        logger.warning("Not a ttbar candidate event! nW %i nb %i", len(W_partons), len(b_partons) )
        isGenTTbar = False
    elif  W_partons[0].pdgId()+W_partons[1].pdgId()!=0:
        logger.warning( "W bosons not OS!" )
        isGenTTbar = False
    elif  b_partons[0].pdgId()+b_partons[1].pdgId()!=0: 
        logger.warning( "b quarks bosons not OS!" )
        isGenTTbar = False

    if isGenTTbar and args.genTTbar:
        # two lists of Ws and bs -> resolve sorting ambiguity
        # flip sequence of b in case W[0] and b[0] can not come from the same top/anti-top
        if not ( (W_partons[0].pdgId() == 24 and b_partons[0].pdgId() == 5) or (W_partons[0].pdgId() == -24 and b_partons[0].pdgId() == -5) ):
            b_partons.reverse()
            print "Reversed" # never happens because of how MG fills LHE

        # make top quark partons from the two lists of W_partons = [W1, W2] and b_partons = [b1, b2] -> t1=W1+b1, t2=W2+b2. The ambiguity is already resolved.
        top_partons = []
        for i_W, W in enumerate(W_partons):
            
            W_p4 = makeP4(W)
            b_p4 = makeP4(b_partons[i_W])
     
            top_partons.append( {'p4': W_p4+b_p4, 'pdgId':6 if W.pdgId()==24 else -6, 
                'W_p4':W_p4, 'b_p4':b_p4, 'W':W, 'b':b_partons[i_W], 
                'W_pt':W_p4.Pt(), 'b_pt':b_p4.Pt(),
            } )

        partons = [] 
        for t in top_partons:
            t['pt']   = t['p4'].Pt()
            t['eta']  = t['p4'].Eta()
            t['phi']  = t['p4'].Phi()
            t['mass'] = t['p4'].M()
            W_last = search.descend(t['W'])
            t['isHad'] = ( not (abs(W_last.daughter(0).pdgId()) in [11,12,13,14,15,16] ))
            t['isLep'] = not t['isHad'] 
            if t['isHad']:
                if W_last.daughter(0).pdgId()%2==1: # down-type quarks have odd pdgId 
                    t['f1'], t['f2'] = W_last.daughter(0), W_last.daughter(1)
                else:
                    t['f1'], t['f2'] = W_last.daughter(1), W_last.daughter(0)
                t['f1_p4'] = makeP4(t['f1'].p4())
                t['f2_p4'] = makeP4(t['f2'].p4())
                partons.append(t)
            else:
                if abs(W_last.daughter(0).pdgId()) in [12,14,16]:
                    t['f2'], t['f1'] = W_last.daughter(0), W_last.daughter(1) 
                else: 
                    t['f1'], t['f2'] = W_last.daughter(0), W_last.daughter(1) 
                t['f1_p4'] = makeP4(t['f1'].p4())
                t['f2_p4'] = makeP4(t['f2'].p4())
                partons.append(t)

        partons.sort( key=lambda t:-t['pt'] )
        if len(partons)>=2:
            top1_parton, top2_parton = (partons+[None,None])[:2]
        
        if top1_parton is not None:        

            event.parton_top1_pt      = top1_parton['pt']
            event.parton_top1_eta     = top1_parton['eta']
            event.parton_top1_phi     = top1_parton['phi']
            event.parton_top1_mass    = top1_parton['mass']
            event.parton_top1_pdgId   = top1_parton['pdgId']
            event.parton_top1_isHad   = top1_parton['isHad']
            event.parton_top1_isLep   = top1_parton['isLep']

            event.parton_top1_f1_pt   = top1_parton['f1'].pt()
            event.parton_top1_f1_eta  = top1_parton['f1'].eta()
            event.parton_top1_f1_phi  = top1_parton['f1'].phi()
            event.parton_top1_f1_mass = top1_parton['f1'].mass()
            event.parton_top1_f1_pdgId= top1_parton['f1'].pdgId()

            event.parton_top1_f2_pt   = top1_parton['f2'].pt()
            event.parton_top1_f2_eta  = top1_parton['f2'].eta()
            event.parton_top1_f2_phi  = top1_parton['f2'].phi()
            event.parton_top1_f2_mass = top1_parton['f2'].mass()
            event.parton_top1_f2_pdgId= top1_parton['f2'].pdgId()

            event.parton_top1_b_pt    = top1_parton['b'].pt()
            event.parton_top1_b_eta   = top1_parton['b'].eta()
            event.parton_top1_b_phi   = top1_parton['b'].phi()
            event.parton_top1_b_mass  = top1_parton['b'].mass()
            event.parton_top1_b_pdgId = top1_parton['b'].pdgId()

            event.parton_top1_W_pt    = top1_parton['W'].pt()
            event.parton_top1_W_eta   = top1_parton['W'].eta()
            event.parton_top1_W_phi   = top1_parton['W'].phi()
            event.parton_top1_W_mass  = top1_parton['W'].mass()
            event.parton_top1_W_pdgId = top1_parton['W'].pdgId()
            
            ## compute theta and phi (Suman approved)
            #beam = ROOT.TLorentzVector()
            #beam.SetPxPyPzE(0,0,6500,6500)

            #boost_t = top1_parton['p4'].BoostVector()

            ## copy the vectors, originals will still be needed
            #W_p4  = copy.deepcopy(top1_parton['W_p4'])
            #f1_p4 = copy.deepcopy(top1_parton['f1_p4'])
            #f2_p4 = copy.deepcopy(top1_parton['f2_p4'])
            #W_p4  .Boost(-boost_t)
            #f1_p4 .Boost(-boost_t)
            #f2_p4 .Boost(-boost_t)

            #n_scatter = ((beam.Vect().Unit()).Cross(W_p4.Vect())).Unit()
            #n_decay   = (f1_p4.Vect().Cross(f2_p4.Vect())).Unit()
            #sign_flip =  1 if ( ((n_scatter.Cross(n_decay))*(W_p4.Vect())) > 0 ) else -1

            #try:
            #    event.parton_top1_decayAngle_phi = sign_flip*acos(n_scatter.Dot(n_decay))
            #except ValueError:
            #    event.parton_top1_decayAngle_phi = -100

            #boost_W = W_p4.BoostVector()
            #f1_p4.Boost(-boost_W)

            #try:
            #    event.parton_top1_decayAngle_theta = (W_p4).Angle(f1_p4.Vect())
            #except ValueError:
            #    event.parton_top1_decayAngle_theta = -100

            ## let's not confuse ourselves later on
            #del W_p4, f1_p4, f2_p4

        # Leptonic top quark parton, for basic ttbar parton-level kinematics 
        if top2_parton is not None:        

            event.parton_top2_pt      = top2_parton['pt']
            event.parton_top2_eta     = top2_parton['eta']
            event.parton_top2_phi     = top2_parton['phi']
            event.parton_top2_mass    = top2_parton['mass']
            event.parton_top2_pdgId   = top2_parton['pdgId']
            event.parton_top2_isHad   = top2_parton['isHad']
            event.parton_top2_isLep   = top2_parton['isLep']

            event.parton_top2_f1_pt         = top2_parton['f1'].pt()
            event.parton_top2_f1_eta        = top2_parton['f1'].eta()
            event.parton_top2_f1_phi        = top2_parton['f1'].phi()
            event.parton_top2_f1_mass       = top2_parton['f1'].mass()
            event.parton_top2_f1_pdgId      = top2_parton['f1'].pdgId()
            event.parton_top2_f2_pt         = top2_parton['f2'].pt()
            event.parton_top2_f2_eta        = top2_parton['f2'].eta()
            event.parton_top2_f2_phi        = top2_parton['f2'].phi()
            event.parton_top2_f2_mass       = top2_parton['f2'].mass()
            event.parton_top2_f2_pdgId      = top2_parton['f2'].pdgId()

            event.parton_top2_b_pt    = top2_parton['b'].pt()
            event.parton_top2_b_eta   = top2_parton['b'].eta()
            event.parton_top2_b_phi   = top2_parton['b'].phi()
            event.parton_top2_b_mass  = top2_parton['b'].mass()
            event.parton_top2_b_pdgId = top2_parton['b'].pdgId()

            event.parton_top2_W_pt    = top2_parton['W'].pt()
            event.parton_top2_W_eta   = top2_parton['W'].eta()
            event.parton_top2_W_phi   = top2_parton['W'].phi()
            event.parton_top2_W_mass  = top2_parton['W'].mass()
            event.parton_top2_W_pdgId = top2_parton['W'].pdgId()

            event.parton_top12_pt     = (top1_parton['p4'] + top2_parton['p4']).Pt()
            event.parton_top12_mass   = (top1_parton['p4'] + top2_parton['p4']).M()
            event.parton_top12_eta    = (top1_parton['p4'] + top2_parton['p4']).Eta()
            if top1_parton['pdgId']>top2_parton['pdgId']: # 'neg' - 'pos' by convention
                event.parton_top12_dEta   = (top2_parton['p4'].Eta() - top1_parton['p4'].Eta())
                event.parton_top12_dAbsEta= (abs(top2_parton['p4'].Eta()) - abs(top1_parton['p4'].Eta()))
            else:
                event.parton_top12_dEta   = (top1_parton['p4'].Eta() - top2_parton['p4'].Eta())
                event.parton_top12_dAbsEta= (abs(top1_parton['p4'].Eta()) - abs(top2_parton['p4'].Eta()))

            ## compute theta and phi (Suman approved)
            #beam = ROOT.TLorentzVector()
            #beam.SetPxPyPzE(0,0,6500,6500)

            #boost_t = top2_parton['p4'].BoostVector()

            ## copy the vectors, originals will still be needed
            #W_p4  = copy.deepcopy(top2_parton['W_p4'])
            #f1_p4 = copy.deepcopy(top2_parton['f1_p4'])
            #f2_p4 = copy.deepcopy(top2_parton['f2_p4'])
            #W_p4  .Boost(-boost_t)
            #f1_p4 .Boost(-boost_t)
            #f2_p4 .Boost(-boost_t)

            #n_scatter = ((beam.Vect().Unit()).Cross(W_p4.Vect())).Unit()
            #n_decay   = (f1_p4.Vect().Cross(f2_p4.Vect())).Unit()
            #sign_flip =  1 if ( ((n_scatter.Cross(n_decay))*(W_p4.Vect())) > 0 ) else -1

            #try:
            #    event.parton_top2_decayAngle_phi = sign_flip*acos(n_scatter.Dot(n_decay))
            #except ValueError:
            #    event.parton_top2_decayAngle_phi = -100

            #boost_W = W_p4.BoostVector()
            #f1_p4.Boost(-boost_W)

            #try:
            #    event.parton_top2_decayAngle_theta = (W_p4).Angle(f1_p4.Vect())
            #except ValueError:
            #    event.parton_top2_decayAngle_theta = -100

            ## let's not confuse ourselves later on
            #del W_p4, f1_p4, f2_p4

        # full ttbar gen-information available
        if top2_parton and top1_parton:
            boost_tt =  (top2_parton['p4'] + top1_parton['p4']).BoostVector()

            assert top1_parton['pdgId']+top2_parton['pdgId']==0, "Tops not OS!"
            top, antitop = (top1_parton, top2_parton) if top1_parton['pdgId']==6 else (top2_parton, top1_parton)

            p4_top      = copy.deepcopy(top['p4'])
            p4_antitop  = copy.deepcopy(antitop['p4'])

            # Eq 4.21 Bernreuther (k* and r*) #Lab frame!!
            sign_star = float(np.sign(abs(p4_top.Rapidity()) - abs(p4_antitop.Rapidity())))

            p4_top1_f1 = makeP4(top1_parton['f1'].p4()) #down-type quark is f1, defined above
            p4_top2_f1 = makeP4(top2_parton['f1'].p4()) 

            # define momenta equivalent to 2l bernreuther 2l definition
            p4_l_plus, p4_l_minus = (p4_top2_f1, p4_top1_f1) if top2_parton['f1'].pdgId()<0 else (p4_top1_f1, p4_top2_f1)
            #sign_charge = -1 if  top2_parton['pdgId']==-6 else +1 # the l- in Bernreuther has a - for each axis. So we add a - to the axis if our lepton is negatively charged (coming from anti-top)
            #print
            #print "p4_l_plus"
            #p4_l_plus.Print()
            #print "p4_l_minus"
            #p4_l_minus.Print()

            # lab frame cosine of lepton unit vectors (TOP-18-006 Table 1 http://cds.cern.ch/record/2649926/files/TOP-18-006-pas.pdf)
            cos_phi_lab      = p4_l_minus.Vect().Unit().Dot(p4_l_plus.Vect().Unit())
            abs_delta_phi_ll_lab = abs( deltaPhi( p4_l_minus.Phi(), p4_l_plus.Phi() ) )
            #print ("cos_phi_lab", cos_phi_lab, "abs_delta_phi_ll_lab", abs_delta_phi_ll_lab)

            #print "top"
            #print p4_top.Print()
            #print "anti-top"
            #print p4_antitop.Print()

            #print "Boost vector"
            #ost_tt.Print()

            p4_top.Boost(-boost_tt)
            p4_antitop.Boost(-boost_tt)
            #print "top after boost"
            #print p4_top.Print()
            #print "anti-top after boost"
            #print p4_antitop.Print()

            p4_l_plus.Boost(-boost_tt)
            p4_l_minus.Boost(-boost_tt)
            #print "After boost p4_l_plus"
            #p4_l_plus.Print()
            #print "After boost p4_l_minus"
            #p4_l_minus.Print()

            # lepton momenta definitions below Eq. 4.6 in Bernreuther -> from the ZMF boost into t (or tbar) system and take unit vectors 
            p4_l_plus.Boost(-p4_top.BoostVector())
            p4_l_minus.Boost(-p4_antitop.BoostVector())
            l_plus = p4_l_plus.Vect().Unit() 
            l_minus = p4_l_minus.Vect().Unit()

            # Eq. 4.13 basis of the ttbar system
            k_hat = p4_top.Vect().Unit()
            p_hat = ROOT.TVector3(0,0,1) # Eq. 4.13 Bernreuther! 
            y = k_hat.Dot(p_hat)
            r = sqrt( 1-y**2 )  
            r_hat = 1./r*(p_hat - (k_hat*y) ) #This needs the import of fixTVecMul. 
            n_hat = 1./r*(p_hat.Cross(k_hat))

            sign_ =  float(np.sign(y)) # Bernreuther Table 5
            n_a =  sign_*n_hat
            r_a =  sign_*r_hat
            k_a =  k_hat

            # Eq 4.21 Bernreuther (k* and r*)
            k_a_star  = sign_star*k_hat
            r_a_star  = sign_star*sign_*r_hat
        
            # Bernreuther Eq. 4.7
            event.parton_cosThetaPlus_n  = n_a.Dot(l_plus)
            event.parton_cosThetaMinus_n =-n_a.Dot(l_minus)
            event.parton_cosThetaPlus_r  = r_a.Dot(l_plus)
            event.parton_cosThetaMinus_r =-r_a.Dot(l_minus)
            event.parton_cosThetaPlus_k  = k_a.Dot(l_plus)
            event.parton_cosThetaMinus_k =-k_a.Dot(l_minus)

            event.parton_cosThetaPlus_r_star  = r_a_star.Dot(l_plus)
            event.parton_cosThetaMinus_r_star =-r_a_star.Dot(l_minus)
            event.parton_cosThetaPlus_k_star  = k_a_star.Dot(l_plus)
            event.parton_cosThetaMinus_k_star =-k_a_star.Dot(l_minus)

            # TOP-18-006 table 1 http://cds.cern.ch/record/2649926/files/TOP-18-006-pas.pdf
            event.parton_xi_nn = event.parton_cosThetaPlus_n*event.parton_cosThetaMinus_n 
            event.parton_xi_rr = event.parton_cosThetaPlus_r*event.parton_cosThetaMinus_r 
            event.parton_xi_kk = event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_k

            event.parton_xi_nr_plus = event.parton_cosThetaPlus_n*event.parton_cosThetaMinus_r + event.parton_cosThetaPlus_r*event.parton_cosThetaMinus_n
            event.parton_xi_nr_minus= event.parton_cosThetaPlus_n*event.parton_cosThetaMinus_r - event.parton_cosThetaPlus_r*event.parton_cosThetaMinus_n
            event.parton_xi_rk_plus = event.parton_cosThetaPlus_r*event.parton_cosThetaMinus_k + event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_r
            event.parton_xi_rk_minus= event.parton_cosThetaPlus_r*event.parton_cosThetaMinus_k - event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_r
            event.parton_xi_nk_plus = event.parton_cosThetaPlus_n*event.parton_cosThetaMinus_k + event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_n
            event.parton_xi_nk_minus= event.parton_cosThetaPlus_n*event.parton_cosThetaMinus_k - event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_n

            event.parton_xi_r_star_k = event.parton_cosThetaPlus_r_star*event.parton_cosThetaMinus_k 
            event.parton_xi_k_r_star = event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_r_star
            event.parton_xi_kk_star  = event.parton_cosThetaPlus_k*event.parton_cosThetaMinus_k_star

            event.parton_cos_phi     = l_plus.Dot(l_minus)
            event.parton_cos_phi_lab = cos_phi_lab 
            event.parton_abs_delta_phi_ll_lab = abs_delta_phi_ll_lab

            #print "cos", event.parton_cosThetaPlus_n, event.parton_cosThetaMinus_n ,event.parton_cosThetaPlus_r, event.parton_cosThetaMinus_r, event.parton_cosThetaPlus_k ,event.parton_cosThetaMinus_k
            #print "xi", event.parton_xi_nn, event.parton_xi_rr ,event.parton_xi_kk ,event.parton_xi_nr_plus ,event.parton_xi_nr_minus ,event.parton_xi_rk_plus ,event.parton_xi_rk_minus ,event.parton_xi_nk_plus ,event.parton_xi_nk_minus
            #print "parton_cos_phi", event.parton_cos_phi, "parton_cos_phi_lab", event.parton_cos_phi_lab, "parton_abs_delta_phi_ll_lab", event.parton_abs_delta_phi_ll_lab

    if args.delphesEra is not None:

        # Delphes AK4 jets 
        allRecoJets = delphesReader.jets()

        # read jets
        recoJets =  filter( lambda j: _isGoodRecoJet(j), allRecoJets)
        recoJets.sort( key = lambda p:-p['pt'] )
        addIndex( recoJets )

        #print len(allRecoJets), len(recoJets)

        ## upgrade JEC are flavor dependent
        for jet in recoJets:
            jet['trueB'] = False 
            jet['trueC'] = False 
            if   min( [999]+[deltaR2( jet, {'eta':b.eta(), 'phi':b.phi()}) for b in all_b_partons] )<0.4**2 :
                jet['trueB'] = True
            elif min( [999]+[deltaR2( jet, {'eta':c.eta(), 'phi':c.phi()}) for c in all_c_partons] )<0.4**2 :
                jet['trueC'] = True
            
        #    #btag_ = jet ["bTag_"+default_btagWP]
        #    jet["matchGenBJet"] = min( [999]+[ deltaR( jet, trueBJet ) for trueBJet in trueBjets ] )<0.4

        # fake B for higher bkg stats
        for i in range(args.fakeB):
            if len(recoJets)>0:
                recoJets[random.randrange(len(recoJets))]['bTag'] = 1

        # make reco b jets
        recoBJets    = filter( lambda j:     j['bTag'] and abs(j['eta'])<2.4 , recoJets )
        recoNonBJets = filter( lambda j:not (j['bTag'] and abs(j['eta'])<2.4), recoJets )

        event.nBTag = len( recoBJets )

        # select AK4 bjets
        recoBj0, recoBj1 = ( recoBJets + recoNonBJets + [None, None] )[:2]

        if recoBj0: fill_vector( event, "recoBj0", recoJet_varnames, recoBj0)
        if recoBj1: fill_vector( event, "recoBj1", recoJet_varnames, recoBj1)

        if recoBj1:
            recoBj01_px = cos(recoBj0['phi'])*recoBj0['pt'] + cos(recoBj1['phi'])*recoBj1['pt']
            recoBj01_py = sin(recoBj0['phi'])*recoBj0['pt'] + sin(recoBj1['phi'])*recoBj1['pt']
            event.recoBj01_pt   = sqrt(recoBj01_px**2 + recoBj01_py**2)
            event.recoBj01_mass = sqrt(2*recoBj0['pt']*recoBj1['pt']*(cosh(recoBj0['eta']-recoBj1['eta'])-cos(recoBj0['phi']-recoBj1['phi'])))

        # read leptons
        allRecoLeps = delphesReader.muons() + delphesReader.electrons()
        allRecoLeps.sort( key = lambda p:-p['pt'] )
        recoLeps =  filter( _isGoodRecoLepton, allRecoLeps )

        #delphesGenLeptons = filter( lambda p: abs(p['pdgId']) in [11,13] and p['status']==1, delphesReader.genParticles() )
        # gen-match leptons with delphes particles
        for recoLep in allRecoLeps:
            #recoLep['genMatched'] = any( deltaR( recoLep, genLep )<0.1 for genLep in delphesGenLeptons )
            recoLep['genMatched'] = any( deltaR( recoLep, genLep )<0.1 for genLep in genLeps_dict )
            #print recoLep, recoLep['genMatched'], recoLep['genMatched2']

            #print recoLep['genMatched'], [deltaR( recoLep, genLep ) for genLep in delphesGenLeptons], recoLep

        # cross-cleaning of reco-objects
        nrecoLeps_uncleaned = len( recoLeps )
        recoLeps = filter( lambda l: (min([999]+[deltaR2(l, j) for j in recoJets if j['pt']>30]) > 0.4**2 ), recoLeps )
        #logger.info( "Before photon cleaning: %i after: %i allRecoLeps: %i, recoLeps %i", nrecoLeps_uncleaned, len(recoLeps), len( allRecoLeps ), len( recoLeps ) )

        # give index to leptons
        addIndex( recoLeps )

        # MET
        recoMet = delphesReader.met()[0]
        event.recoMet_pt  = recoMet['pt']
        event.recoMet_phi = recoMet['phi']

        delphesGenMet = delphesReader.genMet()[0]
        event.delphesGenMet_pt  = delphesGenMet['pt']
        event.delphesGenMet_phi = delphesGenMet['phi']

        # transverse mass for each lepton
        for recoLep in allRecoLeps:
            recoLep['MT'] = sqrt(2*event.recoMet_pt*recoLep['pt']*(1-cos(deltaPhi(recoLep['phi'],event.recoMet_phi))))

        # Store leptons and jets
        fill_vector_collection( event, "recoLep",    recoLep_varnames, recoLeps )
        fill_vector_collection( event, "recoJet",    recoJet_varnames, recoJets )
        recoLep0, recoLep1 = ( recoLeps + [None, None] )[:2]

        event.ht = sum([j['pt'] for j in recoJets]+[0.])

        if recoLep0 is not None:
            event.recoLep0_pt = recoLep0['pt']
            event.recoLep0_eta = recoLep0['eta']
            if recoLep0==recoLep1:
                pass
            elif recoLep0['pdgId']<0:
                event.recoLepPos_pt = recoLep0['pt']
                event.recoLepPos_eta = recoLep0['eta']
                event.recoLepPos_phi = recoLep0['phi']
            else:
                event.recoLepNeg_pt = recoLep0['pt']
                event.recoLepNeg_eta = recoLep0['eta']
                event.recoLepNeg_phi = recoLep0['phi']
        if recoLep1 is not None:
            event.recoLep1_pt = recoLep1['pt']
            event.recoLep1_eta = recoLep1['eta']
            if recoLep0==recoLep1:
                pass
            elif recoLep1['pdgId']<0:
                event.recoLepPos_pt = recoLep1['pt']
                event.recoLepPos_eta = recoLep1['eta']
                event.recoLepPos_phi = recoLep1['phi']
            else:
                event.recoLepNeg_pt = recoLep1['pt']
                event.recoLepNeg_eta = recoLep1['eta']
                event.recoLepNeg_phi = recoLep1['phi']

        if recoLep1 is not None and recoLep0['pdgId']*recoLep1['pdgId']<0:
            recoLep01_px = cos(recoLep0['phi'])*recoLep0['pt'] + cos(recoLep1['phi'])*recoLep1['pt']
            recoLep01_py = sin(recoLep0['phi'])*recoLep0['pt'] + sin(recoLep1['phi'])*recoLep1['pt']
            event.recoLep01_pt   = sqrt(recoLep01_px**2 + recoLep01_py**2)
            event.recoLep01_mass = sqrt(2*recoLep0['pt']*recoLep1['pt']*(cosh(recoLep0['eta']-recoLep1['eta'])-cos(recoLep0['phi']-recoLep1['phi'])))
            event.recoLep_dPhi = event.recoLepNeg_phi -  event.recoLepPos_phi
            event.recoLep_dEta = event.recoLepNeg_eta -  event.recoLepPos_eta
            event.recoLep_dAbsEta = abs(event.recoLepNeg_eta) -  abs(event.recoLepPos_eta)

            sol = topReco.evaluate( leptons = [{'pt':recoLep0['pt'], 'eta':recoLep0['eta'], 'phi':recoLep0['phi'], 'pdgId':recoLep0['pdgId']},
                                               {'pt':recoLep1['pt'], 'eta':recoLep1['eta'], 'phi':recoLep1['phi'], 'pdgId':recoLep1['pdgId']},],
                                    jets    = recoJets,
                                    met     = {'pt':event.recoMet_pt, 'phi':event.recoMet_phi} )
            if sol:
                event.tr_jetB_index    = sol.jetB_index
                event.tr_jetBbar_index = sol.jetBbar_index
                event.tr_ntags         = sol.ntags

                event.tr_neutrino_pt   = sol.neutrino.Pt()
                event.tr_neutrino_eta  = sol.neutrino.Eta()
                event.tr_neutrino_phi  = sol.neutrino.Phi()
                event.tr_neutrino_mass = sol.neutrino.M()

                event.tr_neutrinoBar_pt   = sol.neutrinoBar.Pt()
                event.tr_neutrinoBar_eta  = sol.neutrinoBar.Eta()
                event.tr_neutrinoBar_phi  = sol.neutrinoBar.Phi()
                event.tr_neutrinoBar_mass = sol.neutrinoBar.M()

                event.tr_ttbar_pt   = sol.ttbar.Pt()
                event.tr_ttbar_eta  = sol.ttbar.Eta()
                event.tr_ttbar_phi  = sol.ttbar.Phi()
                event.tr_ttbar_mass = sol.ttbar.M()

                event.tr_top_pt   = sol.top.Pt()
                event.tr_top_eta  = sol.top.Eta()
                event.tr_top_phi  = sol.top.Phi()
                event.tr_top_mass = sol.top.M()

                event.tr_topBar_pt   = sol.topBar.Pt()
                event.tr_topBar_eta  = sol.topBar.Eta()
                event.tr_topBar_phi  = sol.topBar.Phi()
                event.tr_topBar_mass = sol.topBar.M()

                event.tr_ttbar_dEta    = event.tr_top_eta - event.tr_topBar_eta
                event.tr_ttbar_dAbsEta = abs(event.tr_top_eta) - abs(event.tr_topBar_eta)

                event.tr_Wminus_pt   = sol.Wminus.Pt()
                event.tr_Wminus_eta  = sol.Wminus.Eta()
                event.tr_Wminus_phi  = sol.Wminus.Phi()
                event.tr_Wminus_mass = sol.Wminus.M()

                event.tr_Wplus_pt   = sol.Wplus.Pt()
                event.tr_Wplus_eta  = sol.Wplus.Eta()
                event.tr_Wplus_phi  = sol.Wplus.Phi()
                event.tr_Wplus_mass = sol.Wplus.M()

                ## compute theta and phi (Suman approved)
                #beam = ROOT.TLorentzVector()
                #beam.SetPxPyPzE(0,0,6500,6500)

                #boost_t    = sol.top.BoostVector() 
                #boost_tBar = sol.topBar.BoostVector() 

                ## copy the vectors, originals will still be needed
                #Wplus_p4  = copy.deepcopy(sol.Wplus)
                #lplus_p4  = makeP4(sol.leptonPlus.Pt(), sol.leptonPlus.Eta(),sol.leptonPlus.Phi(), 0.)
                #lnu_p4    = copy.deepcopy(sol.neutrino)

                #print "sol.top"
                #sol.top.Print()
                #print "sol.topBar"
                #sol.topBar.Print()

                #print "boost_t"
                #boost_t.Print()
                #print "boost_tBar"
                #boost_tBar.Print()

                #print "Wplus_p4 before"
                #Wplus_p4.Print()
                #
                #Wplus_p4 .Boost(-boost_t)
                #lplus_p4 .Boost(-boost_t)
                #lnu_p4   .Boost(-boost_t)

                #print "Wplus_p4 after"
                #Wplus_p4.Print()

                #Wminus_p4  = copy.deepcopy(sol.Wminus)
                #lminus_p4  = makeP4(sol.leptonMinus.Pt(), sol.leptonMinus.Eta(),sol.leptonMinus.Phi(), 0.)
                #lnuBar_p4  = copy.deepcopy(sol.neutrinoBar)

                #Wminus_p4 .Boost(-boost_tBar)
                #lminus_p4 .Boost(-boost_tBar)
                #lnuBar_p4 .Boost(-boost_tBar)

                #nplus_scatter  = ((beam.Vect().Unit()).Cross(Wplus_p4.Vect())).Unit()
                #nplus_decay    = (lplus_p4.Vect().Cross(lnu_p4.Vect())).Unit()
                #sign_flip_plus =  1 if ( ((nplus_scatter.Cross(nplus_decay))*(Wplus_p4.Vect())) > 0 ) else -1

                #try:
                #    event.tr_top_decayAngle_phi = sign_flip_plus*acos(nplus_scatter.Dot(nplus_decay))
                #except ValueError:
                #    event.tr_top_decayAngle_phi = -100

                #boost_Wplus = Wplus_p4.BoostVector()
                #print "boost_Wplus"
                #boost_Wplus.Print()

                #print "lplus_p4 before boost_Wplus"
                #lplus_p4.Print()
                #boost_Wplus.Print()
                #lplus_p4.Boost(-boost_Wplus)

                #print "lplus_p4 after boost_Wplus"
                #lplus_p4.Print()

                #try:
                #    event.tr_top_decayAngle_theta = (Wplus_p4).Angle(lplus_p4.Vect())
                #except ValueError:
                #    event.tr_top_decayAngle_theta = -100
        
                #print "4-vec (3)"
                #print "lplus_p4"
                #lplus_p4.Print()
                #print

                ## let's not confuse ourselves later on
                #del Wplus_p4, lplus_p4, lnu_p4 

                #nminus_scatter  = ((beam.Vect().Unit()).Cross(Wminus_p4.Vect())).Unit()
                #nminus_decay    = (lminus_p4.Vect().Cross(lnuBar_p4.Vect())).Unit()
                #sign_flip_minus =  1 if ( ((nminus_scatter.Cross(nminus_decay))*(Wminus_p4.Vect())) > 0 ) else -1

                #try:
                #    event.tr_topBar_decayAngle_phi = sign_flip_minus*acos(nminus_scatter.Dot(nminus_decay))
                #except ValueError:
                #    event.tr_topBar_decayAngle_phi = -100

                #boost_Wminus = Wminus_p4.BoostVector()
                #lminus_p4.Boost(-boost_Wminus)

                #try:
                #    event.tr_topBar_decayAngle_theta = (Wminus_p4).Angle(lminus_p4.Vect())
                #except ValueError:
                #    event.tr_topBar_decayAngle_theta = -100

                ## let's not confuse ourselves later on
                #del Wminus_p4, lminus_p4, lnuBar_p4 

                # Eq 4.21 Bernreuther for (k* and r*); absolute rapidity difference in the lab frame!
                sign_star = float(np.sign(abs(sol.top.Rapidity()) - abs(sol.topBar.Rapidity())))

                boost_tt =  sol.ttbar.BoostVector()

                #print "sol.top.Rapidity()", sol.top.Rapidity(),"sol.topBar.Rapidity()",sol.topBar.Rapidity()

                p4_top      = copy.deepcopy(sol.top)
                p4_antitop  = copy.deepcopy(sol.topBar)
            
                p4_l1 = makeP4FromComp( recoLep0['pt'], recoLep0['eta'], recoLep0['phi'], 0.)
                p4_l2 = makeP4FromComp( recoLep1['pt'], recoLep1['eta'], recoLep1['phi'], 0.)
                # define momenta equivalent to 2l bernreuther 2l definition
                p4_l_plus, p4_l_minus = (p4_l1, p4_l2) if recoLep0['pdgId']<0 else (p4_l2, p4_l1) 
                #sign_charge = -1 if  lepTop_parton['pdgId']==-6 else +1 # the l- in Bernreuther has a - for each axis. So we add a - to the axis if our lepton is negatively charged (coming from anti-top)

                # lab frame cosine of lepton unit vectors (TOP-18-006 Table 1 http://cds.cern.ch/record/2649926/files/TOP-18-006-pas.pdf)
                event.tr_cos_phi_lab          = p4_l_minus.Vect().Unit().Dot(p4_l_plus.Vect().Unit())
                event.tr_abs_delta_phi_ll_lab = abs( deltaPhi( p4_l_minus.Phi(), p4_l_plus.Phi() ) )
                #print ("cos_phi_lab", cos_phi_lab, "abs_delta_phi_ll_lab", abs_delta_phi_ll_lab)
                #print "Before Boost into ttbar system"
                #print "top"
                #print p4_top.Print()
                #print "anti-top"
                #print p4_antitop.Print()

                #print "Boost vector"
                #boost_tt.Print()

                p4_top.Boost(-boost_tt)
                p4_antitop.Boost(-boost_tt)
                #print "top after boost"
                #print p4_top.Print()
                #print "anti-top after boost"
                #print p4_antitop.Print()

                p4_l_plus.Boost(-boost_tt)
                p4_l_minus.Boost(-boost_tt)
                #print "After boost p4_l_plus"
                #p4_l_plus.Print()
                #print "After boost p4_l_minus"
                #p4_l_minus.Print()

                # lepton momenta definitions below Eq. 4.6 in Bernreuther -> from the ZMF boost into t (or tbar) system and take unit vectors 
                p4_l_plus.Boost(-p4_top.BoostVector())
                p4_l_minus.Boost(-p4_antitop.BoostVector())
                l_plus = p4_l_plus.Vect().Unit() 
                l_minus = p4_l_minus.Vect().Unit()

                # Eq. 4.13 basis of the ttbar system
                k_hat = p4_top.Vect().Unit()
                p_hat = ROOT.TVector3(0,0,1) # Eq. 4.13 Bernreuther! 
                y = k_hat.Dot(p_hat)
                r = sqrt( 1-y**2 )  
                r_hat = 1./r*(p_hat - (k_hat*y) ) #This needs the import of fixTVecMul. 
                n_hat = 1./r*(p_hat.Cross(k_hat))

                sign_ =  float(np.sign(y)) # Bernreuther Table 5
                n_a =  sign_*n_hat
                r_a =  sign_*r_hat
                k_a =  k_hat

                #print "n_a"
                #n_a.Print()
                #print "r_a"
                #r_a.Print()
                #print "k_a"
                #k_a.Print()
                #print "r_hat"
                #r_hat.Print()
                #print "n_hat"
                #n_hat.Print()

                # Eq 4.21 Bernreuther (k* and r*)
                #sign_star = float(np.sign(abs(p4_top.Rapidity()) - abs(p4_antitop.Rapidity()))) #WRONG it must be in the lab frame!!
                k_a_star  = sign_star*k_hat
                r_a_star  = sign_star*sign_*r_hat


                #print "p4_top.Rapidity()",p4_top.Rapidity(),"p4_antitop.Rapidity()",p4_antitop.Rapidity(),"np.sign(abs(p4_top.Rapidity()) - abs(p4_antitop.Rapidity()))",np.sign(abs(p4_top.Rapidity()) - abs(p4_antitop.Rapidity()))
                #print "r",r,"y",y,"k_hat*y",k_hat*y
                #print "sign_star",sign_star,"sign_",sign_,"r_hat",r_hat
           
                #if sign_star==0: raise RuntimeError
 
                # Bernreuther Eq. 4.7
                event.tr_cosThetaPlus_n  = n_a.Dot(l_plus)
                event.tr_cosThetaMinus_n =-n_a.Dot(l_minus)
                event.tr_cosThetaPlus_r  = r_a.Dot(l_plus)
                event.tr_cosThetaMinus_r =-r_a.Dot(l_minus)
                event.tr_cosThetaPlus_k  = k_a.Dot(l_plus)
                event.tr_cosThetaMinus_k =-k_a.Dot(l_minus)

                event.tr_cosThetaPlus_r_star  = r_a_star.Dot(l_plus)
                event.tr_cosThetaMinus_r_star =-r_a_star.Dot(l_minus)
                event.tr_cosThetaPlus_k_star  = k_a_star.Dot(l_plus)
                event.tr_cosThetaMinus_k_star =-k_a_star.Dot(l_minus)

                #print "r_a_star"
                #r_a_star.Print()
                #print "k_a_star"
                #k_a_star.Print()
                #print "l_plus"
                #l_plus.Print()
                #print "l_minus"
                #l_minus.Print()

                #print "tr_cosThetaPlus_r_star", event.tr_cosThetaPlus_r_star
                #print "tr_cosThetaMinus_r_star", event.tr_cosThetaMinus_r_star
                #print "tr_cosThetaPlus_k_star", event.tr_cosThetaPlus_k_star
                #print "tr_cosThetaMinus_k_star", event.tr_cosThetaMinus_k_star

                # TOP-18-006 table 1 http://cds.cern.ch/record/2649926/files/TOP-18-006-pas.pdf
                event.tr_xi_nn = event.tr_cosThetaPlus_n*event.tr_cosThetaMinus_n 
                event.tr_xi_rr = event.tr_cosThetaPlus_r*event.tr_cosThetaMinus_r 
                event.tr_xi_kk = event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_k

                event.tr_xi_nr_plus = event.tr_cosThetaPlus_n*event.tr_cosThetaMinus_r + event.tr_cosThetaPlus_r*event.tr_cosThetaMinus_n
                event.tr_xi_nr_minus= event.tr_cosThetaPlus_n*event.tr_cosThetaMinus_r - event.tr_cosThetaPlus_r*event.tr_cosThetaMinus_n
                event.tr_xi_rk_plus = event.tr_cosThetaPlus_r*event.tr_cosThetaMinus_k + event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_r
                event.tr_xi_rk_minus= event.tr_cosThetaPlus_r*event.tr_cosThetaMinus_k - event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_r
                event.tr_xi_nk_plus = event.tr_cosThetaPlus_n*event.tr_cosThetaMinus_k + event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_n
                event.tr_xi_nk_minus= event.tr_cosThetaPlus_n*event.tr_cosThetaMinus_k - event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_n

                event.tr_xi_r_star_k = event.tr_cosThetaPlus_r_star*event.tr_cosThetaMinus_k
                event.tr_xi_k_r_star = event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_r_star
                event.tr_xi_kk_star  = event.tr_cosThetaPlus_k*event.tr_cosThetaMinus_k_star
                #print "l_plus unit"
                #l_plus.Print()
                #print "l_minus unit"
                #l_minus.Print()

                event.tr_cos_phi     = l_plus.Dot(l_minus)



    maker.fill()
    maker.event.init()

counter = 0
for reader in readers:
    reader.start()
maker.start()

while readers[0].run( ):
    for reader in readers[1:]:
        reader.run()

    filler( maker.event )
         
    counter += 1
    if counter == maxEvents:  break

logger.info( "Done with running over %i events.", readers[0].nEvents )

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written output file %s", output_filename )

##cleanup delphes file:
if os.path.exists( output_filename ) and args.removeDelphesFiles:
    os.remove( delphes_file )
    logger.info( "Removing Delphes file %s", delphes_file )

if os.path.exists(tmp_output_directory):
    shutil.rmtree(tmp_output_directory)
    logger.info( "Cleaned tmp directory %s", tmp_output_directory )
