# How to find out the definition of ME weights:
# untar the gridpack and run runcmsgrid.sh 100 1
# Look at the .lhe file; look up the pdf set here: https://lhapdf.hepforge.org/pdfsets


from RootTools.core.standard import *
from Analysis.Tools.WeightInfo import WeightInfo
from Analysis.Tools.HyperPoly2  import HyperPoly
import ROOT

import Analysis.Tools.logger as _logger
import RootTools.core.logger as _logger_rt
logger    = _logger.get_logger(   'DEBUG', logFile = None)
logger_rt = _logger_rt.get_logger('INFO', logFile = None)

#weightInfo = WeightInfo("/eos/vbc/user/robert.schoefbeck/test_reweighting/reweight_card.pkl")
weightInfo = WeightInfo("/eos/vbc/group/cms/robert.schoefbeck/gridpacks/CA_v3/TT01j2lCAMyRef_reweight_card.pkl")
weightInfo.set_order(2)

# get list of values of ref point in correct order
hyperPoly  = HyperPoly( weightInfo.order )

logger.info( "Coefficients: %i (%s), order: %i number of weights: %i", len(weightInfo.variables), ",".join(weightInfo.variables), weightInfo.order,  weightInfo.nid)

max_n = 20

def interpret_weight(weight_id):
    str_s = weight_id.split('_')
    res={}
    for i in range(len(str_s)/2):
        res[str_s[2*i]] = float(str_s[2*i+1].replace('m','-').replace('p','.'))
    return res

# from here on miniAOD specific:
#miniAOD = FWLiteSample.fromFiles("miniAOD", ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18MiniAODv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/30000/A2EFBE59-538E-EC43-B4FB-381853992495.root"])
miniAOD = FWLiteSample.fromFiles("miniAOD", ["/users/robert.schoefbeck/CMS/CMSSW_10_6_27/src/Samples/crab/gen/GEN_LO_0j_102X.root"])
logger.info("Compute parametrisation from miniAOD relying on the same sequence of weights as in the card file.")

fwliteReader = miniAOD.fwliteReader( products = { 
    'lhe':{'type':'LHEEventProduct', 'label':("externalLHEProducer")}, 
    'genInfo':{'type':'GenEventInfoProduct', 'label':("generator")}} 
    )
fwliteReader.start()
counter=0

p_C_miniAOD = []
rw_miniAOD_debug  = [] # not needed to store base point weights

while fwliteReader.run( ):
    gen_weights = fwliteReader.products['genInfo'].weights()
    for w in range(16):
        print w, gen_weights[w]
    print

    #lhe_weights = fwliteReader.products['lhe'].weights()
    #weights      = []
    #param_points = []
    #for weight in lhe_weights:

    #    print weight.id, weight.wgt
    #    # Store nominal weight (First position!) 
    #    if weight.id in ['rwgt_1','dummy']: rw_nominal = weight.wgt
    #    if not weight.id in weightInfo.id: continue
    #    pos = weightInfo.data[weight.id]
    #    weights.append( weight.wgt/rw_nominal )
    #    interpreted_weight = interpret_weight(weight.id) 
    #    # weight data for interpolation
    #    if not hyperPoly.initialized:
    #        param_points.append( tuple(interpreted_weight[var] for var in weightInfo.variables) )
    #        logger.debug( "Weight %s -> base point %r. val: %f", weight.id, param_points[-1], weight.wgt ) 

    #rw_miniAOD_debug.append( weights ) 
    ## Initialize with Reference Point

    #if not hyperPoly.initialized: 
    #    #print "ref point", ref_point_coordinates
    #    #for i_p, p in enumerate(param_points):
    #    #    print "weight", i_p, weights[i_p]/rw_nominal, p
    #    hyperPoly.initialize( param_points )
    #coeff = hyperPoly.get_parametrization( weights )
    #np = hyperPoly.ndof
    #
    #p_C_miniAOD.append( [ coeff[n] for n in xrange(hyperPoly.ndof) ] )

    counter+=1
    if counter>=max_n:
        break

assert False, ""

# from here on nanoAOD specific:
#nanoAOD = Sample.fromFiles("nanoAOD", ["/eos/vbc/user/robert.schoefbeck/test_reweighting/nanoAOD.root"])
nanoAOD = Sample.fromFiles("nanoAOD", ["/eos/vbc/user/robert.schoefbeck/topNanoAODSim_fast_private/v6/WGToLNu/NANOAODSIMoutput_115.root"])
logger.info("Compute parametrisation from nanoAOD, relying on the sequence of weights as in weightInfo.data")

# Hack for broken naming convention for the LHEReweightingWeight vector:
#nanoAOD.chain.SetAlias("nLHEReweighting",       "nLHEReweightingWeight")
#nanoAOD.chain.SetAlias("LHEReweighting_Weight", "LHEReweightingWeight")

# construct the sorted list of basepoints 
weightInfo_data = list(weightInfo.data.iteritems())
weightInfo_data.sort( key = lambda w: w[1] )

basepoint_coordinates = map( lambda d: [d[v] for v in weightInfo.variables] , map( lambda w: interpret_weight(w[0]), weightInfo_data) )

hyperPoly  = HyperPoly( weightInfo.order ) # make a new HyperPoly
hyperPoly.initialize( basepoint_coordinates)


reader = nanoAOD.treeReader( variables=["nLHEReweightingWeight/I","LHEWeight_originalXWGTUP/F"] )
#for hack: 
#reader = nanoAOD.treeReader( variables=["LHEWeight_originalXWGTUP/F", "nLHEReweightingWeight/I", "nLHEReweighting/I", VectorTreeVariable.fromString("LHEReweighting[Weight/F]", nMax=1000) ] )
reader.start()
reader.activateAllBranches()

p_C_nanoAOD = []
rw_nanoAOD_debug  = [] # not needed to store base point weights
counter=0

## modify loop for hack:
#while True:
#
#    # 
#    reader.sample.chain.SetBranchStatus("*",1)
#    reader.sample.chain.SetBranchAddress("LHEReweightingWeight",  ROOT.AddressOf(reader.event, "LHEReweighting_Weight" ))
#    reader.activateAllBranches()
#
#    run = reader.run()
#    if not run: break 

while reader.run():

    r = reader.event

    include_missing_refpoint = False
    if weightInfo.nid == r.nLHEReweightingWeight + 1:
        logger.warning( "addReweights: pkl file has %i base-points but nLHEReweightWeight=%i, hence it is likely that the ref-point is among the base points and is missing. Fingers crossed.", weightInfo.nid, r.nLHEReweightingWeight )
        if ref_point_index is None:
            raise RuntimeError( "weightInfo.nid == r.nLHEReweightingWeight + 1 but ref_point_index = None -> something is wrong." )
        include_missing_refpoint = True
    elif weightInfo.nid == r.nLHEReweightingWeight:
        pass
    else:
        raise RuntimeError("reweight_pkl and nLHEReweightWeight are inconsistent.")
   
    # here we check the consistency with miniAOD, hence multiply with LHEWeight_originalXWGTUP 
    weights = [reader.sample.chain.GetLeaf("LHEReweightingWeight").GetValue(i_weight) for i_weight in range(r.nLHEReweightingWeight)] 
         
    if include_missing_refpoint:
        weights = weights[:ref_point_index] + [1] + weights[ref_point_index:]

    coeff           = hyperPoly.get_parametrization( weights )
    #print weights, coeff
    np        = hyperPoly.ndof
    chi2_ndof = hyperPoly.chi2_ndof( coeff, weights )

    if chi2_ndof > 10**-6:
        logger.warning( "chi2_ndof is large: %f", chi2_ndof )

#    for n in xrange( hyperPoly.ndof ):
#        p_C[n] = coeff[n]
    p_C_nanoAOD.append( [ coeff[n] for n in xrange(hyperPoly.ndof) ] )

    counter+=1
    if counter>=max_n:
        break

chop = lambda v: v if abs(v)>10**-8 else 0

for i in range(max_n):
    print "Event", i
    for j, (mini, nano) in enumerate(zip(map(chop,p_C_miniAOD[i]), map(chop,p_C_nanoAOD[i]))):
        print "p_C[%i]"%j, "mini",mini,"nano",nano

    print 
