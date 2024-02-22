''' 
Phase space definition 
'''

from collections import OrderedDict
import operator

class PhaseSpace:

    def __init__ (self, variables, counting_variables, overflow_variables): #, sequence=None):

        self.variables          = variables
        self.counting_variables = counting_variables
        self.overflow_variables = overflow_variables

        #self.sequence = sequence

        # make getters
        self.getters = {}
        for var, _ in self.overflow_variables.items():
            if "[" in var:
                varname, index = var.replace(']', '').split('[')
                index = int(index)
                def getter( event, index=index, varname=varname):
                    return operator.itemgetter(index)( getattr( event, varname) )
                self.getters[var] = getter
        
    @property
    def unbinned_selection( self ):
        return "&&".join( ["(%s<%i)"%(var,values[-1]) for var, values in self.overflow_variables.items()] + [self.inclusive_selection] )

    @property
    def inclusive_selection( self ):
        return "&&".join( ["(%s>=0)"%var for var, values in self.overflow_variables.items()] )

    @property 
    def overflow_selections( self ):
        if hasattr( self, "_overflow_selections"):
            return self._overflow_selections
        else:
            selections = [[] for _ in self.overflow_variables.items()]
            for i_var, (var, values) in enumerate(self.overflow_variables.items()):
                for i_sel, sel in enumerate(selections):
                    if i_sel>=i_var:
                        if i_sel==i_var:
                            sel.append("(%s>=%i)"%(var,values[-1]))
                        else:
                            sel.append("(%s<%i)"%(var,values[-1]))
            self._overflow_selections = map( lambda s:"&&".join(s), selections )
            return self._overflow_selections

    def overflow_counter_func( self ):
        if not hasattr( self, "_func"):
            def func( event, sample ):
                for i_var, (var, (_, thrsh)) in enumerate( self.overflow_variables.items() ):
                    val = getattr( event, var) if var not in self.getters else self.getters[var](event) 
                    if val >= thrsh:
                        return i_var+1
                return 0
            self._func = func 
        return self._func       

    @property
    def overflow_counter( self ):
        return "+".join( map( lambda s: str(s[0]+1)+"*("+s[1]+")", list(enumerate(self.overflow_selections)) ))

if __name__=="__main__":

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
    ]

    counting_variables = [ ("nJetGood", [4,5,6,7,8]), ("nBTag", [2,3,4]) ]

    overflow_variables = OrderedDict([   
        ('ht', (0., 1800.)),
        ('tr_ttbar_mass', (0., 4000)),
        ('l1_pt', (0., 400)),
        ('l2_pt', (0., 200)),
        ('JetGood_pt[0]', (0., 900)),
        ('JetGood_pt[1]', (0., 450)),
        ('JetGood_pt[2]', (0., 300)),
        ])

    phaseSpace = PhaseSpace(variables = variables, counting_variables = counting_variables, overflow_variables = overflow_variables)

#Bin 385 cut_value 1915.0
#extra_selection: (1)&&(ht<1915.000000)
#Bin 883 cut_value 4405.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)
#Bin 88 cut_value 430.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)
#Bin 42 cut_value 200.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)&&(l2_pt<200.000000)
#Bin 184 cut_value 910.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)&&(l2_pt<200.000000)&&(JetGood_pt[0]<910.000000)
#Bin 97 cut_value 475.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)&&(l2_pt<200.000000)&&(JetGood_pt[0]<910.000000)&&(JetGood_pt[1]<475.000000)
#Bin 61 cut_value 295.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)&&(l2_pt<200.000000)&&(JetGood_pt[0]<910.000000)&&(JetGood_pt[1]<475.000000)&&(JetGood_pt[2]<295.000000)
#Bin 41 cut_value 195.0
#extra_selection: (1)&&(ht<1915.000000)&&(tr_ttbar_mass<4405.000000)&&(l1_pt<430.000000)&&(l2_pt<200.000000)&&(JetGood_pt[0]<910.000000)&&(JetGood_pt[1]<475.000000)&&(JetGood_pt[2]<295.000000)&&(JetGood_pt[3]<195.000000)
#No files for syncing.
