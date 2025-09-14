#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
import itertools
import copy
import array
import operator
from   math                              import sqrt, cos, sin, pi, atan2, cosh, sinh, acos, log

# RootTools
from RootTools.core.standard             import *

# TT2lUnbinned
from TT2lUnbinned.Tools.user                     import plot_directory
from TT2lUnbinned.Tools.cutInterpreter           import cutInterpreter
from TT2lUnbinned.Tools.objectSelection          import lepString
#from TT2lUnbinned.Analysis.phasespace.v1         import phasespace as phasespace_v1
#from TT2lUnbinned.Analysis.phasespace.v2         import phasespace as phasespace_v2

# Analysis
from Analysis.Tools.helpers                      import deltaPhi, deltaR
from Analysis.Tools.puProfileCache               import *
from Analysis.Tools.puReweighting                import getReweightingFunction
import Analysis.Tools.syncer
from   Analysis.Tools.WeightInfo                 import WeightInfo

import numpy as np

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',          action='store_true', help='Run only on a small subset of the data?')
argParser.add_argument('--ttbarComp',      action='store_true', help='Run only on on TTbar EFT?')
argParser.add_argument('--noData',         action='store_true', default=True, help='Do not plot data.')
argParser.add_argument('--no_sorting',     action='store_true', help='Sort histos?', )
argParser.add_argument('--dataMCScaling',  action='store_true', help='Data MC scaling?')
argParser.add_argument('--plot_directory', action='store', default='v4')
argParser.add_argument('--selection',      action='store', default='njet2-btag2')
argParser.add_argument('--n_cores',        action='store', type=int, default=-1)
args = argParser.parse_args()

# Logger
import TT2lUnbinned.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small: args.plot_directory += "_small"
if args.noData:args.plot_directory += "_noData"
if args.ttbarComp: args.plot_directory += "_ttbarComp"

# Simulated samples
from TT2lUnbinned.Samples.nano_mc_UL20_singlelep_njet2p_met30_postProcessed import *

mc = [ TTSingleLep_pow_CP5_Autumn18, t_sch_Autumn18] 

#preselectionString = cutInterpreter.cutString(args.selection) + "&&" + phasespace_v1.inclusive_selection# + "&&("+phasespace.overflow_counter+"==7)"
preselectionString = cutInterpreter.cutString(args.selection) 

# Now we add the data
if not args.noData:
    #from TT2lUnbinned.samples.nano_private_UL20_RunII_postProcessed_dilep import RunII
    raise NotImplementedError
    data_sample = RunII
    data_sample.name = "data"
    all_samples = mc +  [data_sample]
else:
    all_samples = mc 

# Here we compute the scaling of the simulation to the data luminosity (event.weight corresponds to 1/fb for simulation, hence we divide the data lumi in pb^-1 by 1000) 
lumi_scale = 137. if args.noData else data_sample.lumi/1000.

# We're going to "scale" the simulation if "small" is true. So let's define a "scale" which will correct this
for sample in mc:
    sample.scale  = 1 

# For R&D we just use a fraction of the data
if args.small:
    if not args.noData:
        data_sample.reduceFiles( factor = 100 )
    for sample in mc :
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        #sample.reduceFiles( to=1)
        sample.scale /= sample.normalization

# Helpers for putting text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right

# Helper: build 4-vectors (px, py, pz, E) from (pt, eta, phi, mass)
def p4(pt, eta, phi, mass=0.0):
    px = pt * cos(phi)
    py = pt * sin(phi)
    pz = pt * sinh(eta)
    E  = sqrt(max(0.0, px*px + py*py + pz*pz + mass*mass))
    return (px, py, pz, E)

def add_p4(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2], a[3]+b[3])

def mass_of(p):
    m2 = p[3]*p[3] - (p[0]*p[0] + p[1]*p[1] + p[2]*p[2])
    return sqrt(max(0.0, m2))

def pt_eta_phi_m(p):
    px, py, pz, E = p
    pt  = sqrt(px*px + py*py)
    eta = 0.5*log((E+pz)/(E-pz)) if E > abs(pz) else float('nan')
    phi = atan2(py, px)
    m   = mass_of(p)
    return pt, eta, phi, m

def boost_to_rest(p, frame):
    # Boost 4-vector p into the rest frame of 'frame'
    px, py, pz, E = p
    fx, fy, fz, FE = frame
    # beta vector of frame
    bx, by, bz = (fx/FE, fy/FE, fz/FE) if FE > 0.0 else (0.0, 0.0, 0.0)
    b2 = bx*bx + by*by + bz*bz
    if b2 >= 1.0 or FE <= 0.0:
        # pathological; return original
        return p
    gamma = 1.0 / sqrt(1.0 - b2)
    bp = bx*px + by*py + bz*pz  # beta dot p
    # p' = p + [ (gamma-1)*(beta dot p)/beta^2 - gamma*E ] * beta
    k = (gamma - 1.0) * (bp / b2) - gamma * E
    pxp = px + k * bx
    pyp = py + k * by
    pzp = pz + k * bz
    Ep  = gamma * (E - bp)
    return (pxp, pyp, pzp, Ep)

def p3_mag(p):
    return sqrt(p[0]*p[0] + p[1]*p[1] + p[2]*p[2])

def p_from_ptetaphi(pt, eta, phi):
    px = pt * cos(phi)
    py = pt * sin(phi)
    pz = pt * sinh(eta)
    return (px, py, pz)

def legendre_P3(x):
    # P3(x) = (5 x^3 - 3 x) / 2
    return 0.5 * (5.0*x*x*x - 3.0*x)


def drawObjects( dataMCScale, lumi_scale ):
    lines = [
      (0.15, 0.95, 'CMS Simulation'), 
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale),
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots, mode, dataMCScale):
  for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, 'RunII', mode + ("_log" if log else ""), args.selection)
    for plot in plots:
      if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot

      _drawObjects = []

      if isinstance( plot, Plot):
          plotting.draw(plot,
            plot_directory = plot_directory_,
            ratio =  {'yRange':(0.1,1.9)} if not args.noData else None,
            logX = False, logY = log, sorting = not args.no_sorting,
            yRange = (0.9, "auto") if log else (0.001, "auto"),
            scaling = {0:1} if (args.dataMCScaling or args.ttbarComp) else {},
            legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
            drawObjects = drawObjects( dataMCScale , lumi_scale ) + _drawObjects,
            copyIndexPHP = True, extensions = ["png", "pdf", "root"],
          )

read_variables = []

jetVars     = ['pt/F', 'eta/F', 'phi/F', 'btagDeepB/F', 'btagDeepFlavB/F' ]

jetVarNames     = [x.split('/')[0] for x in jetVars]

# the following we read for both, data and simulation 
read_variables += [
    "weight/F", "year/I", "met_pt/F", "met_phi/F", "nBTag/I", "nJetGood/I", "PV_npvsGood/I", "LHE_HT/F", "LHE_HTIncoming/F",
    "ht/F",
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPWP/I", "l1_index/I", 
    #"l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPWP/I", "l2_index/I",
    "JetGood[%s]"%(",".join(jetVars)),
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mvaTOP/F]",
    #"Z1_l1_index/I", "Z1_l2_index/I",  
    #"Z1_phi/F", "Z1_pt/F", "Z1_m/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I]",
]

# the following we read only in simulation
read_variables_MC = [
    'reweightBTagSF_central/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightLeptonSF/F', 'reweightLeptonSFDown/F', 'reweightLeptonSFUp/F', 'reweightTopPt/F',
    "GenJet[pt/F,eta/F,phi/F,partonFlavour/I,hadronFlavour/i]"
    ]
            
# Read variables and sequences
sequence       = []

from TT2lUnbinned.Tools.objectSelection import isBJet
from TT2lUnbinned.Tools.helpers import getObjDict

def make_reco(event, sample):
    event.jets  = [getObjDict(event, 'JetGood_', jetVarNames, i) for i in range(int(event.nJetGood))]
    event.bJets = list(filter(lambda j: isBJet(j, year=event.year) and abs(j['eta']) <= 2.4, event.jets))

    if len( event.bJets )>=1:
        event.mlb0 = sqrt(2*event.bJets[0]['pt']*event.l1_pt*(cosh(event.bJets[0]['eta']-event.l1_eta)-cos(event.bJets[0]['phi']-event.l1_phi)))
    else:
        event.mlb0 = float('nan')
    # pT_bb (px, py add in quadrature)
    if len(event.bJets) >= 2:
        px_sum = event.bJets[0]['pt']*cos(event.bJets[0]['phi']) + event.bJets[1]['pt']*cos(event.bJets[1]['phi'])
        py_sum = event.bJets[0]['pt']*sin(event.bJets[0]['phi']) + event.bJets[1]['pt']*sin(event.bJets[1]['phi'])
        event.pT_bb = sqrt(px_sum**2 + py_sum**2)
        event.mlb1 = sqrt(2*event.bJets[1]['pt']*event.l1_pt*(cosh(event.bJets[1]['eta']-event.l1_eta)-cos(event.bJets[1]['phi']-event.l1_phi)))
    else:
        event.pT_bb = float('nan')
        event.mlb1  = float('nan')

    # Angles & transverse mass
    dphi = event.l1_phi - event.met_phi
    event.cos_dPhi = cos(dphi)
    sin2_phi = max(0.0, 1.0 - event.cos_dPhi**2)  # = sin^2(phi), robust to tiny negatives
    event.mT = sqrt(2.0 * event.l1_pt * event.met_pt * (1.0 - event.cos_dPhi))

    # Constants & shorthands
    mW = 80.4
    mW2 = mW*mW
    pTl = event.l1_pt
    met = event.met_pt
    eta = event.l1_eta

    # Massless lepton: pz_l = pTl*sinh(eta), E_l = pTl*cosh(eta)
    pzl = pTl * sinh(eta)
    El  = pTl * cosh(eta)

    # Lambda with measured MET direction & magnitude
    # (this is the "original" setup where pT,nu = MET when the discriminant is >= 0)
    Lambda = 0.5*mW2 + pTl*met*event.cos_dPhi

    # Quadratic in pz_nu:  pz_nu = (Lambda*pzl +/- El * sqrt(Lambda^2 - pTl^2 * met^2)) / pTl^2
    # -> Discriminant:
    disc = Lambda*Lambda - (pTl*pTl) * (met*met)

    if disc >= 0.0:
        # Two real solutions: pick the one with the smaller |pz|
        A    = (Lambda * pzl) / (pTl*pTl)
        root = (El / (pTl*pTl)) * sqrt(disc)
        pz_nu_1 = A + root
        pz_nu_2 = A - root

        event.pT_nu = met          # keep measured MET when solutions are real
        event.pz_nu = pz_nu_1 if abs(pz_nu_1) < abs(pz_nu_2) else pz_nu_2

    else:
        # Complex: enforce reality by Delta=0 and choose the neutrino pT on the boundary
        # If we keep the nu direction fixed to the MET direction, the boundary gives a scalar quadratic in rho = |pT,nu|:
        # Handle small sin phi separately to avoid division by ~0.
        eps = 1e-6  # threshold on sin^2 phi

        if sin2_phi < eps:
            # Collinear / anti-collinear limit: linear solution
            # rho = - mW^2 / (4 pTl cos phi)
            # Only meaningful when cos phi approx +/-1; here we are already in the Delta<0 branch so phi ~ pi is the typical case.
            if abs(event.cos_dPhi) < 1e-12:
                # extremely degenerate: fall back to using MET magnitude as a harmless default
                rho = met
            else:
                rho = - mW2 / (4.0 * pTl * event.cos_dPhi)

            # If numerical noise produces negative rho, clamp to zero (non-physical otherwise)
            if rho < 0.0:
                rho = 0.0

            event.pT_nu = rho
            Lambda_star = 0.5*mW2 + pTl * rho * event.cos_dPhi
            event.pz_nu = (Lambda_star * pzl) / (pTl*pTl)

        else:
            # Generic quadratic: two roots for rho
            # rho +/-  = [ (mW^2/2) (cos phi +/- 1) ] / [ pTl sin^2 phi ]
            denom = pTl * sin2_phi
            rho1 = (0.5*mW2 * (event.cos_dPhi + 1.0)) / denom
            rho2 = (0.5*mW2 * (event.cos_dPhi - 1.0)) / denom

            # Choose rho closest to measured MET magnitude
            rho = rho1 if abs(met - rho1) < abs(met - rho2) else rho2
            if rho < 0.0:  # guard against tiny negative due to rounding
                rho = 0.0

            event.pT_nu = rho
            Lambda_star = 0.5*mW2 + pTl * rho * event.cos_dPhi
            event.pz_nu = (Lambda_star * pzl) / (pTl*pTl)

    # Lepton 4-vector
    p4_l = p4(event.l1_pt, event.l1_eta, event.l1_phi, 0.0)

    # Neutrino 4-vector
    px_nu = event.pT_nu * cos(event.met_phi)
    py_nu = event.pT_nu * sin(event.met_phi)
    pz_nu = event.pz_nu
    E_nu  = sqrt(max(0.0, event.pT_nu*event.pT_nu + pz_nu*pz_nu))
    p4_nu = (px_nu, py_nu, pz_nu, E_nu)

    # W boson
    p4_W = add_p4(p4_l, p4_nu)

    # Store neutrino kinematics
    nu_pt, nu_eta, nu_phi, nu_m = pt_eta_phi_m(p4_nu)
    event.nu_pt  = nu_pt
    event.nu_eta = nu_eta
    event.nu_phi = nu_phi
    # massless
    event.nu_m   = 0.0

    # Store W kinematics
    W_pt, W_eta, W_phi, W_m = pt_eta_phi_m(p4_W)
    event.W_pt  = W_pt
    event.W_eta = W_eta
    event.W_phi = W_phi
    event.W_m   = W_m

    # --- Top reconstruction with two b-tagged jets (2j2t or 3j2t) ---
    # Use the SAME b-jet counting as for pT_bb: event.bJets already filtered with |eta|<=2.4

    if len(event.bJets) >= 1:

        # b-jet 4-vector
        b0 = event.bJets[0]
        m_b0 = b0.get('mass', 0.0)
        p4_b0 = p4(b0['pt'], b0['eta'], b0['phi'], m_b0)

        # Top candidate
        p4_t0 = add_p4(p4_W, p4_b0)
        m_t0 = mass_of(p4_t0)

        event.top_b_index = 0
        event.mtop        = m_t0
        event.mtop_other  = float('nan')
        event.mtop_diff   = abs(m_t0 - 172.5)

        # Store chosen top candidate
        top_pt, top_eta, top_phi, top_m = pt_eta_phi_m(p4_t0)
        event.top_pt  = top_pt
        event.top_eta = top_eta
        event.top_phi = top_phi
        event.top_m   = top_m

        # No "other" top
        event.top_other_pt  = float('nan')
        event.top_other_eta = float('nan')
        event.top_other_phi = float('nan')
        event.top_other_m   = float('nan')

    if len(event.bJets) >= 2:

        # Build top candidates with each of the two b jets
        # (In 2j2t / 3j2t categories there should be exactly two b-tagged jets.)
        b0 = event.bJets[0]
        b1 = event.bJets[1]

        # If your jets include a 'mass' field, use it; otherwise treat as massless
        m_b0 = b0.get('mass', 0.0)
        m_b1 = b1.get('mass', 0.0)

        p4_b0 = p4(b0['pt'], b0['eta'], b0['phi'], m_b0)
        p4_b1 = p4(b1['pt'], b1['eta'], b1['phi'], m_b1)

        p4_t0 = add_p4(p4_W, p4_b0)
        p4_t1 = add_p4(p4_W, p4_b1)

        m_t0 = mass_of(p4_t0)
        m_t1 = mass_of(p4_t1)

        # Choose the b jet whose top mass is closer to the nominal 172.5 GeV
        mtop_nominal = 172.5
        if abs(m_t0 - mtop_nominal) <= abs(m_t1 - mtop_nominal):
            event.top_b_index = 0
            event.mtop        = m_t0
            event.mtop_other  = m_t1
        else:
            event.top_b_index = 1
            event.mtop        = m_t1
            event.mtop_other  = m_t0

        event.mtop_diff = abs(event.mtop - mtop_nominal)

        # Top candidate with chosen b
        if event.top_b_index == 0:
            p4_top      = p4_t0
            p4_top_other= p4_t1
        else:
            p4_top      = p4_t1
            p4_top_other= p4_t0

        # Store chosen top
        top_pt, top_eta, top_phi, top_m = pt_eta_phi_m(p4_top)
        event.top_pt  = top_pt
        event.top_eta = top_eta
        event.top_phi = top_phi
        event.top_m   = top_m

        # Store "other" top
        o_pt, o_eta, o_phi, o_m = pt_eta_phi_m(p4_top_other)
        event.top_other_pt  = o_pt
        event.top_other_eta = o_eta
        event.top_other_phi = o_phi
        event.top_other_m   = o_m

    if len(event.bJets) == 0:
        # Not enough b-tagged jets to do this selection
        event.top_b_index = -1
        event.mtop        = float('nan')
        event.mtop_other  = float('nan')
        event.mtop_diff   = float('nan')
        event.top_pt        = float('nan')
        event.top_eta       = float('nan')
        event.top_phi       = float('nan')
        event.top_m         = float('nan')
        event.top_other_pt  = float('nan')
        event.top_other_eta = float('nan')
        event.top_other_phi = float('nan')
        event.top_other_m   = float('nan')

    # -------------------------------------------------
    # a) cos(theta) between lepton and spectator b jet
    #     in the top-quark rest frame
    # -------------------------------------------------
    # Identify spectator b: the other b-jet than the one used for top
    if len(event.bJets) >= 2 and event.top_b_index in (0, 1):
        b_spec = event.bJets[1 - event.top_b_index]
        m_bspec = b_spec.get('mass', 0.0)
        p4_bspec = p4(b_spec['pt'], b_spec['eta'], b_spec['phi'], m_bspec)

        # Boost lepton and spectator b into top rest frame
        p4_l_topRF     = boost_to_rest(p4_l, p4_top)
        p4_bspec_topRF = boost_to_rest(p4_bspec, p4_top)

        pl = (p4_l_topRF[0], p4_l_topRF[1], p4_l_topRF[2])
        pb = (p4_bspec_topRF[0], p4_bspec_topRF[1], p4_bspec_topRF[2])
        ml = p3_mag(p4_l_topRF)
        mb = p3_mag(p4_bspec_topRF)

        if ml > 0.0 and mb > 0.0:
            cos_theta = (pl[0]*pb[0] + pl[1]*pb[1] + pl[2]*pb[2]) / (ml * mb)
            # Numerical safety
            if cos_theta > 1.0:  cos_theta = 1.0
            if cos_theta < -1.0: cos_theta = -1.0
            event.cosTheta_lb_topRF = cos_theta
        else:
            event.cosTheta_lb_topRF = float('nan')
    else:
        # Not enough b-jets or no chosen index
        event.cosTheta_lb_topRF = float('nan')

    # -------------------------------------------------
    # b) Fox-Wolfram third moment (and normalized)
    #     Build from all selected jets + lepton + neutrino
    # -------------------------------------------------
    # Collect 3-momenta (px,py,pz) and magnitudes
    p_list = []

    # jets
    for j in event.jets:
        px = j['pt'] * cos(j['phi'])
        py = j['pt'] * sin(j['phi'])
        pz = j['pt'] * sinh(j['eta'])
        p_list.append((px, py, pz))

    # lepton (massless)
    p_list.append(p_from_ptetaphi(event.l1_pt, event.l1_eta, event.l1_phi))

    # neutrino (use reconstructed pT and pz, phi from MET; eta is not needed)
    px_nu = event.pT_nu * cos(event.met_phi)
    py_nu = event.pT_nu * sin(event.met_phi)
    pz_nu = event.pz_nu
    p_list.append((px_nu, py_nu, pz_nu))

    # Compute H0 and H3
    H0 = 0.0
    H3 = 0.0
    # Precompute magnitudes
    mags = [sqrt(px*px + py*py + pz*pz) for (px,py,pz) in p_list]

    n = len(p_list)
    for i in range(n):
        pi = p_list[i]
        mi = mags[i]
        if mi == 0.0:
            continue
        for j in range(n):
            pj = p_list[j]
            mj = mags[j]
            if mj == 0.0:
                continue
            # cos(theta_ij)
            cij = (pi[0]*pj[0] + pi[1]*pj[1] + pi[2]*pj[2]) / (mi * mj)
            # numerical clamp
            if cij > 1.0:  cij = 1.0
            if cij < -1.0: cij = -1.0
            H0 += mi * mj
            H3 += mi * mj * legendre_P3(cij)

    event.FW3   = H3
    event.FW0   = H0
    event.FW3_R = (H3 / H0) if H0 > 0.0 else float('nan')

sequence.append( make_reco )

# Let's make a function that provides string-based lepton selection
mu_string  = lepString('mu','VL')
ele_string = lepString('ele','VL')
def getLeptonSelection( mode ):
    if   mode=="mu": return "Sum$({mu_string})==1&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="e":  return "Sum$({mu_string})==0&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=='all':    return "Sum$({mu_string})+Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)

def charge(pdgId):
    return -pdgId/abs(pdgId)

# We don't use tree formulas, but I leave them so you understand the syntax. TTreeFormulas are faster than if we compute things in the event loop.
ttreeFormulas = {   
                    #"overflow_counter":phasespace.overflow_counter, 
    }

yields     = {}
allPlots   = {}
allModes   = ['mu','e', 'all']
for i_mode, mode in enumerate(allModes):
    yields[mode] = {}

    # "event.weight" is 0/1 for data, depending on whether it is from a certified lumi section. For MC, it corresponds to the 1/fb*cross-section/Nsimulated. So we multiply with the lumi in /fb.
    # This weight goes to the plot.
    weight_ = lambda event, sample: event.weight if sample.isData else event.weight

    # coloring
    if args.ttbarComp:
        for sample in mc: sample.style = styles.lineStyle(sample.color)
    else:
        for sample in mc: sample.style = styles.fillStyle(sample.color)

    # read the MC variables only in MC; apply reweighting to simulation for specific detector effects
    for sample in mc:
      sample.read_variables = read_variables_MC 
      sample.weight = lambda event, sample: event.reweightBTagSF_central*event.reweightPU*event.reweightL1Prefire*event.reweightLeptonSF*event.reweightTopPt 

    # Define what we want to see.
    if args.ttbarComp:
        stack = Stack(*[[s] for s in mc])
    elif not args.noData:
        data_sample.style = styles.errorStyle( ROOT.kBlack ) 
        stack = Stack(mc, [data_sample])
    else:
        stack = Stack(mc)

    # Define everything we want to have common to all plots
    Plot.setDefaults(stack = stack, weight = staticmethod(weight_), selectionString = "("+getLeptonSelection(mode)+")&&("+preselectionString+")")

    plots = []

    # A special plot that holds the yields of all modes
    plots.append(Plot(
      name = 'yield', texX = '', texY = 'Number of Events',
      attribute = lambda event, sample: 0.5 + i_mode,
      binning=[2, 0, 2],
    ))

#    # A special plot that shows the overflow bins 
#    plots.append(Plot(
#      name = 'overflow_counter_v1', texX = '', texY = 'Number of Events',
#      attribute = phasespace_v1.overflow_counter_func(), #lambda event, sample: event.overflow_counter,
#      binning=[len(phasespace_v1.overflow_selections), 1, 1+len(phasespace_v1.overflow_selections)],
#    ))

#    plots.append(Plot(
#      name = 'overflow_counter_v2', texX = '', texY = 'Number of Events',
#      attribute = phasespace_v2.overflow_counter_func(), #lambda event, sample: event.overflow_counter,
#      binning=[len(phasespace_v2.overflow_selections), 1, 1+len(phasespace_v2.overflow_selections)],
#    ))

    plots.append(Plot(
      name = 'nVtxs', texX = 'vertex multiplicity', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "PV_npvsGood/I" ),
      binning=[50,0,50],
      addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'l1_pt',
        texX = 'p_{T}(l_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample:event.l1_pt,
        binning=[15,0,300],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        name = 'l1_eta',
        texX = '#eta(l_{1})', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_eta,
        binning=[20,-3,3],
    ))

    plots.append(Plot(
        name = 'l1_mvaTOP',
        texX = 'MVA_{TOP}(l_{1})', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOP,
        binning=[20,-1,1],
    ))

    plots.append(Plot(
        name = 'l1_mvaTOPWP',
        texX = 'MVA_{TOP}(l_{1}) WP', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOPWP,
        binning=[5,0,5],
    ))

    plots.append(Plot(
        texX = 'H_{T} (GeV)', texY = 'Number of Events / 100 GeV',
        attribute = TreeVariable.fromString( "ht/F" ),
        binning=[20,0,2000],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = 'E_{T}^{miss} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_pt/F" ),
        binning=[400/20,0,400],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = 'm_{T} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample: event.mT,
        name = "mT",
        binning=[400/40,0,400],
        addOverFlowBin='upper',
    ))

    plots.append(Plot(
        texX = '#phi(E_{T}^{miss})', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "met_phi/F" ),
        binning=[10,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'N_{jets}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nJetGood/I" ), #nJetSelected
      binning=[8,1.5,9.5],
    ))

    plots.append(Plot(
      texX = 'N_{b-tag}', texY = 'Number of Events',
      attribute = TreeVariable.fromString( "nBTag/I" ), #nJetSelected
      binning=[5, 0.5,5.5],
    ))

    plots.append(Plot(
      texX = 'LHE_HT (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'LHE_HT', attribute = lambda event, sample: event.LHE_HT,
      binning=[1500/50,0,1500],
    ))

    plots.append(Plot(
      texX = 'LHE_HTIncoming (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'LHE_HTIncoming', attribute = lambda event, sample: event.LHE_HTIncoming,
      binning=[1500/50,0,1500],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet0_pt', attribute = lambda event, sample: event.JetGood_pt[0],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(subleading jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'jet1_pt', attribute = lambda event, sample: event.JetGood_pt[1],
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(leading b jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'bjet0_pt', attribute = lambda event, sample: event.bJets[0]['pt'] if len(event.bJets)>=1 else float('nan'),
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(subleading b jet) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'bjet1_pt', attribute = lambda event, sample: event.bJets[1]['pt'] if len(event.bJets)>=2 else float('nan'),
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(leading b jet) (GeV)', texY = 'Number of Events',
      name = 'bjet0_eta', attribute = lambda event, sample: event.bJets[0]['eta'] if len(event.bJets)>=1 else float('nan'),
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = '#eta(sub leading b jet) (GeV)', texY = 'Number of Events',
      name = 'bjet1_eta', attribute = lambda event, sample: event.bJets[1]['eta'] if len(event.bJets)>=2 else float('nan'),
      binning=[30,-3,3],
    ))

    plots.append(Plot(
      texX = 'p_{T}(bb) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'pT_bb', attribute = lambda event, sample: event.pT_bb,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#Delta#eta(l,b_0)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_lb0', attribute = lambda event, sample: abs(event.bJets[0]['eta']-event.l1_eta) if len(event.bJets)>=1 else float('nan'),
      binning=[30,0,6],
    ))
    plots.append(Plot(
      texX = '#Delta#eta(l,b_1)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_lb1', attribute = lambda event, sample: abs(event.bJets[1]['eta']-event.l1_eta) if len(event.bJets)>=2 else float('nan'),
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = '#Delta#eta(top,b_0)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_top_b0', attribute = lambda event, sample: abs(event.bJets[0]['eta']-event.top_eta) if len(event.bJets)>=1 else float('nan'),
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = '#Delta#eta(top,b_1)', texY = 'Number of Events / 30 GeV',
      name = 'DEta_top_b1', attribute = lambda event, sample: abs(event.bJets[1]['eta']-event.top_eta) if len(event.bJets)>=2 else float('nan'),
      binning=[30,0,6],
    ))

    plots.append(Plot(
      texX = 'Cos(#Delta#phi(top,b_0))', texY = 'Number of Events / 30 GeV',
      name = 'Cos_DPhi_top_b0', attribute = lambda event, sample: cos(event.bJets[0]['phi']-event.top_phi) if len(event.bJets)>=1 else float('nan'),
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'Cos(#Delta#phi(top,b_1))', texY = 'Number of Events / 30 GeV',
      name = 'Cos_DPhi_top_b1', attribute = lambda event, sample: cos(event.bJets[1]['phi']-event.top_phi) if len(event.bJets)>=2 else float('nan'),
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'p_{T}(W) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'W_pt', attribute = lambda event, sample: event.W_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(W)', texY = 'Number of Events / 30 GeV',
      name = 'W_eta', attribute = lambda event, sample: event.W_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(W)', texY = 'Number of Events / 20 GeV',
        name = "W_phi", attribute =  lambda event, sample: event.W_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'p_{T}(nu) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'nu_pt', attribute = lambda event, sample: event.nu_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(nu)', texY = 'Number of Events / 30 GeV',
      name = 'nu_eta', attribute = lambda event, sample: event.nu_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(nu)', texY = 'Number of Events / 20 GeV',
        name = "nu_phi", attribute =  lambda event, sample: event.nu_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'p_{T}(t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_pt', attribute = lambda event, sample: event.top_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(t)', texY = 'Number of Events / 30 GeV',
      name = 'top_eta', attribute = lambda event, sample: event.top_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(t)', texY = 'Number of Events / 20 GeV',
        name = "top_phi", attribute =  lambda event, sample: event.top_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'M(t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_m', attribute = lambda event, sample: event.top_m,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'p_{T}(other t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_pt', attribute = lambda event, sample: event.top_other_pt,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = '#eta(other t)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_eta', attribute = lambda event, sample: event.top_other_eta,
      binning=[30,-3,3],
    ))

    plots.append(Plot(
        texX = '#phi(other t)', texY = 'Number of Events / 20 GeV',
        name = "top_other_phi", attribute =  lambda event, sample: event.top_other_phi,
        binning=[30,-pi,pi],
    ))

    plots.append(Plot(
      texX = 'M(other t) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'top_other_m', attribute = lambda event, sample: event.top_other_m,
      binning=[600/30,0,600],
    ))


    plots.append(Plot(
      texX = 'cos(#theta^#ast)', texY = 'Number of Events',
      name = 'cosTheta_lb_topRF', attribute = lambda event, sample: event.cosTheta_lb_topRF,
      binning=[30,-1,1],
    ))

    plots.append(Plot(
      texX = 'FW3/FW0', texY = 'Number of Events',
      name = 'FW3_R', attribute = lambda event, sample: event.FW3_R,
      binning=[30,0,1],
    ))

    plots.append(Plot(
      texX = 'M(l, b_0) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'mlb0', attribute = lambda event, sample: event.mlb0,
      binning=[600/30,0,600],
    ))

    plots.append(Plot(
      texX = 'M(l, b_1) (GeV)', texY = 'Number of Events / 30 GeV',
      name = 'mlb1', attribute = lambda event, sample: event.mlb1,
      binning=[600/30,0,600],
    ))

    plotting.fill(plots, read_variables = read_variables, sequence = sequence, ttreeFormulas = ttreeFormulas)

    # Get normalization yields from yield histogram
    for plot in plots:
      if plot.name == "yield":
        for i, l in enumerate(plot.histos):
          for j, h in enumerate(l):
            yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+i_mode))
            h.GetXaxis().SetBinLabel(1, "#mu")
            h.GetXaxis().SetBinLabel(2, "e")

    yields[mode]["MC"] = sum(yields[mode][s.name] for s in mc)
    if args.noData:
        dataMCScale = 1.
    else:
        dataMCScale        = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')

    drawPlots(plots, mode, dataMCScale)
    allPlots[mode] = plots

# Add the different channels into SF and all
for mode in ["all"]:
    yields[mode] = {}
    for y in yields[allModes[0]]:
        try:    yields[mode][y] = sum(yields[c][y] for c in (['e','mu'] ))
        except: yields[mode][y] = 0
    if args.noData:
        dataMCScale = 1.
    else:
        dataMCScale = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')
    for plot in allPlots['mu']:
        for plot2 in (p for p in (allPlots['e']) if p.name == plot.name):  #For SF add EE, second round add EMu for all
            for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
                for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
                    if i==k: j.Add(l)

    drawPlots(allPlots['mu'], mode, dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
