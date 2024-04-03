from Samples.nanoAOD.UL16_nanoAODv9 import allSamples as mcSamples_16
from Samples.nanoAOD.UL16_nanoAODAPVv9 import allSamples as mcSamples_16preVFP
from Samples.nanoAOD.UL17_nanoAODv9 import allSamples as mcSamples_17
from Samples.nanoAOD.UL18_nanoAODv9 import allSamples as mcSamples_18

for s in mcSamples_16+mcSamples_16preVFP+mcSamples_17+mcSamples_18:
    try:
        print s.get_parent()
    except:
        pass
