import itertools
from pprint import pprint
from EventSelectionAlgorithms.EventSelectionConfig import makeEventSelectionConfig, EventSelectionMergerConfig

def CombineWorkingPoints(TauX_OR,prefix='wpSet',silent=False):
    objNames = list(TauX_OR.keys())
    objNames.sort()

    
    ## Get combinations of WPs to use for OverlapRemoval
    WPcomb = list(itertools.product( *[ TauX_OR[x] for x in objNames ] ))

    WPset = {}

    for iComb, comb in enumerate(WPcomb):
        WPset[prefix+str(iComb)]={}
        for iObj, obj in enumerate(objNames):
            WPset['wpSet'+str(iComb)][obj]=comb[iObj]

    if not silent:
        print('\n')
        print(80*'=')
        print(" Tau+X Working Point Selections for OverlapRemoval / MET ")
        print(80*'=')
        pprint(WPset)
        print(80*'=')
        print('\n')

    return(WPset)
                
            

def makeMultipleWPEventSelectionConfigs(seq,
                                        WPs=None,
                                        electrons=None, muons=None, jets=None,
                                        largeRjets=None,
                                        photons=None, taus=None, met=None, metTerm='Final',
                                        btagDecoration=None, preselection=None,
                                        selectionCutsDict=None, noFilter=None,
                                        debugMode=None, cutFlowHistograms=None):
    """
       Modified version of  makeMultipleEventSelectionConfigs
       from PhysicsAnalysis/Algorithms/EventSelectionAlgorithms/python/EventSelectionConfig.py
       to accommodate multiple WPs, running the selections separately for all of them and creating
       separate flags, then saving the logical OR of all of them

       Keyword arguments:
        WPs               -- labels to use for working points choices
        electrons         -- the electron container and selection
        muons             -- the muon container and selection
        jets              -- the jet container and selection
        largeRjets        -- the large-R jet container and selection
        photons           -- the photon container and selection
        taus              -- the tau-jet container and selection
        met               -- the MET container
        metTerm           -- the MET term to use (e.g. 'Final', 'NonInt')
        btagDecoration    -- the b-tagging decoration to use when defining b-jets
        preselection      -- optional event-wise selection flag to start from
        selectionCutsDict -- a dictionary with key the name of the selection and value a string listing one selection cut per line
        noFilter          -- whether to disable the event filter
        debugMode         -- enables saving all intermediate decorations
        cutFlowHistograms -- whether to toggle event cutflow histograms per region and per systematic
    """

    if (btagDecoration):
        raise NotImplementedError()
    if len(WPs)==0:
        raise ValueError('TauX_Gnt1makerAlg.WorkingPointHelperTauX.makeMultipleWPEventSelectionConfigs() called without passing WPs')
    else:
        for wp in WPs:
            # first, we generate all the individual event selections
            # !!! it's important to pass noFilter=True, to avoid applying the individual filters in series
            for name, selectionCuts in selectionCutsDict.items():
                makeEventSelectionConfig(seq,
                                         name+"_"+wp,
                                         electrons=(electrons+'.'+wp if electrons else None),
                                         muons=(muons+'.'+wp if muons else None),
                                         jets=(jets+'.'+wp if jets else None),
                                         largeRjets=(largeRjets+'.'+wp if largeRjets else None),
                                         photons=(photons+'.'+wp if photons else None),
                                         taus=(taus+'.'+wp if taus else None),
                                         met=(met+"_"+wp if met else None),
                                         metTerm=metTerm,
                                         btagDecoration=btagDecoration,
                                         preselection=preselection,
                                         selectionCuts=selectionCuts,
                                         noFilter=True,
                                         debugMode=debugMode,
                                         cutFlowHistograms=cutFlowHistograms)
            
        # now we are ready to collect all the filters and apply their logical OR
        # !!! subregions (name starts with "SUB") are not used in the final filtering
        config = EventSelectionMergerConfig()
        selToMerge = []
        for name in selectionCutsDict.keys():
            for wp in WPs:
                if not name.startswith("SUB"):
                    selToMerge.append(f'pass_{name}_{wp}_%SYS%')
        config.setOptionValue ('selections', selToMerge)
        config.setOptionValue ('noFilter', noFilter)
        seq.append(config)
