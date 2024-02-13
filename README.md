# Recipe for <= CMSSW_12 (python 2) 
```
cmsrel CMSSW_10_6_28
cd CMSSW_10_6_28/src
cmsenv
git cms-init
curl -sLO https://gist.githubusercontent.com/dietrichliko/8aaeec87556d6dd2f60d8d1ad91b4762/raw/a34563dfa03e4db62bb9d7bf8e5bf0c1729595e3/install_correctionlib.sh
. ./install_correctionlib.sh
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone git@github.com:HephyAnalysisSW/TT2lUnbinned.git
git clone git@github.com:HephyAnalysisSW/TMB
git clone git@github.com:HephyAnalysisSW/Analysis
git clone git@github.com:HephyAnalysisSW/Samples
git clone git@github.com:HephyAnalysisSW/RootTools
cd $CMSSW_BASE
scram b -j40

```

## Delphes

```
cd $CMSSW_BASE/..
git clone https://github.com/TTXPheno/delphes.git
#patch $CMSSW_BASE/../delphes/cards/delphes_card_CMS.tcl < $CMSSW_BASE/src/TTXPheno/patches/slim_delphes.diff # Reduce Delphes output
cd delphes
./configure
sed -i -e 's/c++0x/c++17/g' Makefile
make -j 4 
```
