from collections import OrderedDict
from TT2lUnbinned.Analysis.PhaseSpace       import PhaseSpace
from TT2lUnbinned.Tools.cutInterpreter      import cutInterpreter

#selection       = "dilepL-offZ1-njet3p-btag2p-ht500"
#selectionString = cutInterpreter.cutString(selection)

variables = [
    "tr_cosThetaPlus_n",
    "tr_cosThetaMinus_n",
    "tr_cosThetaPlus_r",
    "tr_cosThetaMinus_r",
    "tr_cosThetaPlus_k",
    "tr_cosThetaMinus_k",
    "tr_cosThetaPlus_r_star",
    "tr_cosThetaMinus_r_star",
    "tr_cosThetaPlus_k_star",
    "tr_cosThetaMinus_k_star",
    "tr_xi_nn",
    "tr_xi_rr",
    "tr_xi_kk",
    "tr_xi_nr_plus",
    "tr_xi_nr_minus",
    "tr_xi_rk_plus",
    "tr_xi_rk_minus",
    "tr_xi_nk_plus",
    "tr_xi_nk_minus",
    "tr_cos_phi",
    "tr_cos_phi_lab",
    "tr_abs_delta_phi_ll_lab",
    "tr_ttbar_dAbsEta",
    "tr_ttbar_eta",
    "tr_top_eta",
    "tr_topBar_eta",
    "jet0_eta",
    "jet1_eta",
    "jet2_eta",
]

counting_variables = [ ("nJetGood", [4,5,6,7,8]), ("nBTag", [2,3,4]) ]

overflow_variables = OrderedDict([   
    ('tr_ttbar_pt', (0., 480)),
    ('tr_ttbar_mass', (0., 2500)),
    ('tr_top_pt', (0., 800)),
    ('tr_topBar_pt', (0., 700)),
    #('ht', (0., 1800.)),
    ('l1_pt', (0., 250)),
    ('l2_pt', (0., 150)),
    #('jet0_pt', (0., 900)),
    #('jet1_pt', (0., 450)),
    #('jet2_pt', (0., 300)),
    ('JetGood_pt[0]', (0., 400)),
    ('JetGood_pt[1]', (0., 250)),
    ('JetGood_pt[2]', (0., 150)),
    ])

#def makeJets( event, sample):
#    event.jet0_pt = JetGood_pt[0]
#    event.jet1_pt = JetGood_pt[1]
#    event.jet2_pt = JetGood_pt[2]
#
#sequence = [makeJets]

phasespace = PhaseSpace( variables = variables, 
                         counting_variables = counting_variables, 
                         overflow_variables = overflow_variables,) 
#                         sequence = sequence)
