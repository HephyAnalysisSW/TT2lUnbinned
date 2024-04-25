selection_central = 'tr-minDLmass20-dilepM-offZ1-njet3p-btagM2p-mtt750'
from TT2lUnbinned.Tools.cutInterpreter import cutInterpreter
selectionString_central = cutInterpreter.cutString( selection_central )

from TT2lUnbinned.Samples.nano_UL20_RunII_postProcessed import TTLep as TTLep_central
#print (TTLep_central.getYieldFromDraw(selectionString=selectionString_central, weightString="weight"))

import TT2lUnbinned.Samples.delphes_RunII_postProcessed as delphes

selection_delphes = 'dilep-offZ-njet3p-btag2p-mtt750'
from TT2lUnbinned.Tools.delphesCutInterpreter import cutInterpreter as cutInterpreter_delphes


#print (delphes.TTLep_delphes.getYieldFromDraw(selectionString=selectionString_delphes, weightString="weight1fb"))

#assert False, ""

for selection in [ 'dilep-offZ-njet3p-btag0p-mtt750', 'dilep-offZ-njet3p-btag1p-mtt750', 'dilep-offZ-njet3p-btag2p-mtt750']:
    selectionString_delphes = cutInterpreter_delphes.cutString( selection )

    for sample in [ 
        delphes.TTLep,
        delphes.TTLep_hdampDOWN,
        delphes.TTLep_hdampUP,
        #delphes.ST_tW_top,
        #delphes.ST_tW_antitop,

        #delphes.DYJetsToLL_M50_HT100to200,
        #delphes.DYJetsToLL_M50_HT200to400,
        #delphes.DYJetsToLL_M50_HT400to600,
        #delphes.DYJetsToLL_M50_HT600to800,
        #delphes.DYJetsToLL_M50_HT800to1200,
        #delphes.DYJetsToLL_M50_HT1200to2500,
        #delphes.DYJetsToLL_M50_HT2500toInf,
        ]:

        print sample.name, selection
        print (sample.getYieldFromDraw(selectionString=selectionString_delphes, weightString="weight1fb"))
        print (sample.getYieldFromDraw(selectionString=selectionString_delphes, weightString="(1)"))
        print
