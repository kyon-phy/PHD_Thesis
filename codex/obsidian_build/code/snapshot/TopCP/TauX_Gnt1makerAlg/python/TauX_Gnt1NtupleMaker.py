from AnalysisAlgorithmsConfig.ConfigSequence import ConfigSequence
from AnalysisAlgorithmsConfig.ConfigAccumulator import ConfigAccumulator
from AsgAnalysisAlgorithms.AsgAnalysisConfig import PerEventSFBlock
from AthenaConfiguration.Enums import LHCPeriod
from TopCPToolkit import metaConfig, commonAlgoConfig
from AnalysisAlgorithmsConfig.ConfigFactory import ConfigFactory
from TauX_Gnt1makerAlg.DSIDList import *
from TauX_Gnt1makerAlg.TriggerList import *
from AsgAnalysisAlgorithms.AsgAnalysisConfig import IFFLeptonDecorationBlock
from TauX_Gnt1makerAlg.WorkingPointHelperTauX import *
from TauX_Gnt1makerAlg.JvtExtraFlagConfig import *
from TauX_Gnt1makerAlg.MetaDataSaverConfig import *
from Campaigns.Utils import Campaign

import os
import itertools
import re
import yaml

# production v4:
# - added mu SF for medium/tight id + tight iso (done)
# - add NNLO ttbar reweighting for ttbar dilep samples (done)
# - add truth electron and muon decorations for fake estimation (done, nomiman-only production?)
# - add FT reduction (done)
# - update b-tagging calibration file (done)
# - update electron SF R22 map file (done)
# - fix the bugged systematics for el isol and loose muon reco efficiency (el done, muon not fixed) 

# TODO production v5:
# - add mu SF for medium id + loose iso (done)
# - fix the eveto tau SF (need new release https://gitlab.cern.ch/atlas-phys/exot/lpx/exot-2022-34/taux_gnt1makeralg/-/commit/35846129f2e65dc78f7e46b026ce7e729376d39a)

def makeRecoConfiguration(flags, algSeq, configSeq, factory, noSystematics=False, noFilter=False):
    makeConfig = factory.makeConfig

    use_electrons   = True
    use_muons       = True
    use_jets        = True
    use_taus        = True
    use_MET         = True

    outputContainers = {'': 'EventInfo'}  # for output NTuple config block
    reco_branches = []
    met_branches = []
    TauX_Wp={}
    TauX_OR={"electrons":[], 'muons':[], 'taus':[]}

    # UsefulFlags
    isRun3 = flags.Input.LHCPeriod == LHCPeriod.Run3
    isMC   = flags.Input.DataType != flags.Input.DataType.Data
    isSignal = int(flags.Input.MCChannelNumber) in SignalDSIDList
    isWtaunu = int(flags.Input.MCChannelNumber) in WtaunuDSID
    isFullSim = flags.Input.DataType == flags.Input.DataType.FullSim
    isPHYSLITE = flags.Input.isPHYSLITE
    ptag = -1
    if isMC and flags.Input.AMITag.startswith("e"):
        ptag=flags.Input.AMITag.split("_")[-1][1:]
        ptag=int(ptag)

    ### Forcing nofilter to be true when running on signal events
    forceNoFilter=False
    if isSignal:
        forceNoFilter=True


    #----------------------------------------
    #   Event Info
    #----------------------------------------
    # primary vertex ,event cleaning (jet clean loosebad)
    configSeq += makeConfig ('EventCleaning')
    configSeq.setOptionValue ('.runEventCleaning', True)

    # GoodRunsList selection
    # https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/GoodRunListsForAnalysisRun3
    # Run-3 GRLs have specific use cases, need explicit choice
    # Assuming "not relying on BS", "relying on jet triggers at L1 or HLT", "relying on jet, met or b-jet triggers"
    if isRun3:
        configSeq.setOptionValue ('.userGRLFiles', ["GoodRunsLists/data22_13p6TeV/20230207/data22_13p6TeV.periodAllYear_DetStatus-v109-pro28-04_MERGED_PHYS_StandardGRL_All_Good_25ns.xml",
                                                    "GoodRunsLists/data23_13p6TeV/20230828/data23_13p6TeV.periodAllYear_DetStatus-v110-pro31-06_MERGED_PHYS_StandardGRL_All_Good_25ns.xml",
                                                    "GoodRunsLists/data24_13p6TeV/20241118/physics_25ns_data24_IgnoreBSPOT_INVALID.xml"]
                                  )

    # run PMG TruthWeightTool on MC only
    configSeq += makeConfig ('GeneratorLevelAnalysis')
    configSeq.setOptionValue('.saveCutBookkeepers',True)
    configSeq.setOptionValue('.cutBookkeepersSystematics',(not noSystematics))


    # PRW
    if not isPHYSLITE:
        configSeq += makeConfig ('PileupReweighting')
        configSeq.setOptionValue('.campaign',flags.Input.MCCampaign)
    else:
        ### The following branches are added by the PRW config, but not for PHYSLITE
        reco_branches+=['EventInfo.runNumber -> runNumber',
                        'EventInfo.eventNumber -> eventNumber']
        if isMC:
            reco_branches += ['EventInfo.mcChannelNumber -> mcChannelNumber',
                              'EventInfo.PileupWeight_NOSYS -> weight_pileup',
                              'EventInfo.beamSpotWeight -> weight_beamspot']

    if isMC and int(flags.Input.MCChannelNumber) in HFDSIDList:
        reco_branches += ['EventInfo.HF_Classification -> HF_Classification']


    ### Information on mu
    ### Currently saving only the Mu info without PRW, as the decoration is not
    ### saved by the algo... To be fixed
    reco_branches+=['EventInfo.averageInteractionsPerCrossing -> mu_avg',
                    'EventInfo.actualInteractionsPerCrossing -> mu_act']

    ### RandomRunNumber
    if isMC:
        reco_branches+=["EventInfo.RandomRunNumber -> randomRunNumber"]

    ### Saving MC weight variations for LQ_tanujet
    if isMC and int(flags.Input.MCChannelNumber) in SignalDSID['LQ_tanujet_hadtau']:
        reco_branches+=["EventInfo.mcEventWeights -> mc_EventWeights"]
    if isMC and int(flags.Input.MCChannelNumber) in SignalDSID['LQ_tanujet_lephadtau']:
        reco_branches+=["EventInfo.mcEventWeights -> mc_EventWeights"]
        ## MC weight correction for LQ taunubjets
        from TauX_Gnt1makerAlg.LQWeightCorrectionConfig import LQWeightCorrectionConfig
        cfg = LQWeightCorrectionConfig('LQWeightCorrectionDec')
        configSeq.append(cfg)



    #----------------------------------------
    #   Electrons
    #----------------------------------------

    if use_electrons:

        ## Electron Calibration
        #configSeq += makeConfig('Electrons', containerName='AnaElectrons')
        from TauX_Gnt1makerAlg.TauX_ElectronAnalysisConfig import ElectronCalibrationConfig, ElectronWorkingPointConfig
        cfg = ElectronCalibrationConfig(containerName="AnaElectrons")
        cfg.setOptionValue('crackVeto',True)
        cfg.setOptionValue('recalibratePhyslite', False)
        cfg.setOptionValue('minPt',5e3)
        configSeq.append(cfg)

        # Electrons:
        TauX_Wp['Electrons']=[{'quality' : 'TightLH',       'iso' : 'Loose_VarRad',            'noSF' : False,          'doOR' : True },
                              {'quality' : 'TightLH',       'iso' : 'Tight_VarRad',            'noSF' : False,          'doOR' : False },
                              {'quality' : 'TightLH',       'iso' : 'HighPtCaloOnly',          'noSF' : False,          'doOR' : False },
                              {'quality' : 'TightLH',       'iso' : 'TightTrackOnly_VarRad',   'noSF' : False,          'doOR' : False },
                              {'quality' : 'TightLH',       'iso' : 'TightTrackOnly_FixedRad', 'noSF' : False,          'doOR' : False },
                              {'quality' : 'LooseBLayerLH', 'iso' : 'NonIso',                  'noSF' : False,          'doOR' : False },
                              {'quality' : 'LooseDNN',      'iso' : 'NonIso',                  'noSF' : True,           'doOR' : False },
                              {'quality' : 'MediumDNN',     'iso' : 'NonIso',                  'noSF' : True,           'doOR' : False },
                              {'quality' : 'TightDNN',      'iso' : 'NonIso',                  'noSF' : True,           'doOR' : False },
                              ]

        for WP in TauX_Wp['Electrons']:
            flagName = WP['quality']+"_"+WP['iso']
            if WP['doOR']:
                TauX_OR['electrons'].append(flagName)

            cfg = ElectronWorkingPointConfig(containerName='AnaElectrons', selectionName=flagName)
            cfg.setOptionValue('containerName','AnaElectrons')
            cfg.setOptionValue('identificationWP',WP['quality'])
            cfg.setOptionValue('isolationWP',WP['iso'])
            cfg.setOptionValue('maxD0Significance',5)
            cfg.setOptionValue('noEffSF', WP['noSF'])
            cfg.setOptionValue('correlationModelReco','TOTAL')
            cfg.setOptionValue('correlationModelIso','TOTAL')
            cfg.setOptionValue('correlationModelId','TOTAL')
            configSeq.append(cfg)
        outputContainers['el_'] = 'OutElectrons'
        if isMC:
            reco_branches+=["OutElectrons_NOSYS.firstEgMotherPdgId -> el_FirstEgMotherPdgId",
                            "OutElectrons_NOSYS.firstEgMotherTruthOrigin -> el_FirstEgMotherTruthOrigin",
                            "OutElectrons_NOSYS.firstEgMotherTruthType -> el_FirstEgMotherTruthType"
                            ]
        # Electron ambiguity flags
        if not isPHYSLITE:
            reco_branches+=["OutElectrons_NOSYS.DFCommonAddAmbiguity -> el_DFCommonAddAmbiguity",
                            "OutElectrons_NOSYS.ambiguityType -> el_AmbiguityType"]
        else:
            reco_branches+=["OutElectrons_NOSYS.ambiguityType -> el_AmbiguityType"]

        # IFF electron classification
        cfg = IFFLeptonDecorationBlock('AnaElectrons')
        cfg.setOptionValue('decoration','IFFtype_%SYS%')
        configSeq.append(cfg)


    #----------------------------------------
    #   Muons
    #----------------------------------------

    if use_muons:
        # Muon Calibration
        configSeq += makeConfig('Muons', containerName='AnaMuons')
        configSeq.setOptionValue('.minPt',5e3)
        configSeq.setOptionValue('.maxEta',2.5)
        configSeq.setOptionValue ('.recalibratePhyslite', False)

        # Muons:
        TauX_Wp[ 'Muons'] =[{ 'quality' : 'Loose',           'iso' : 'Loose_VarRad',      'noSF' : False , 'doOR' : True },
                            { 'quality' : 'Loose',           'iso' : 'Tight_VarRad',      'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Loose',           'iso' : 'PflowLoose_VarRad', 'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Loose',           'iso' : 'PflowTight_VarRad', 'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Medium',          'iso' : 'NonIso',            'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Medium',          'iso' : 'Loose_VarRad',      'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Medium',          'iso' : 'Tight_VarRad',      'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Tight',           'iso' : 'NonIso',            'noSF' : False , 'doOR' : False },
                            { 'quality' : 'Tight',           'iso' : 'Tight_VarRad',      'noSF' : False , 'doOR' : False },
                            { 'quality' : 'HighPt',          'iso' : 'NonIso',            'noSF' : False , 'doOR' : False },
                            { 'quality' : 'LowPtEfficiency', 'iso' : 'NonIso',            'noSF' : True ,  'doOR' : False },
                            { 'quality' : 'Loose',           'iso' : 'NonIso',            'noSF' : False , 'doOR' : False  },
                            { 'quality' : 'VeryLoose',       'iso' : 'NonIso',            'noSF' : True , 'doOR' : False  },
                            { 'quality' : 'VeryLoose',       'iso' : 'Loose_VarRad',      'noSF' : True , 'doOR' : False  },
                            { 'quality' : 'VeryLoose',       'iso' : 'PflowLoose_VarRad',      'noSF' : True , 'doOR' : False  },
                            # { 'quality' : 'HighPt',       'iso' : 'NonIso',      'noSF' : True , 'doOR' : False  },
                           ]
        for WP in TauX_Wp['Muons']:
            flagName = WP['quality']+"_"+WP['iso']
            if WP['doOR']:
                TauX_OR['muons'].append(flagName)

            configSeq += makeConfig ('Muons.WorkingPoint',containerName='AnaMuons', selectionName=flagName)
            configSeq.setOptionValue('.quality',WP['quality'])
            configSeq.setOptionValue('.isolation',WP['iso'])
            configSeq.setOptionValue('.maxD0Significance',3)
            configSeq.setOptionValue('.noEffSF', WP['noSF'])


        outputContainers['mu_'] = 'OutMuons'

        cfg = IFFLeptonDecorationBlock('AnaMuons')
        cfg.setOptionValue('decoration','IFFtype_%SYS%')
        configSeq.append(cfg)

        if isMC:
            ### Iacopo: Following up with IFF people to fix it
            ### In many MC background and signal samples I am getting
            ### Warnings from the IFF tool
            from TauX_Gnt1makerAlg.LogLevelModifierConfig import LogLevelModifierConfig
            print("WARNING - IFFClassifierAlg silenced for muons!!!")
            cfg = LogLevelModifierConfig('')
            cfg.setOptionValue('algname','IFFClassifierAlgAnaMuons')
            cfg.setOptionValue('handle','tool')
            cfg.setOptionValue('level',5)
            configSeq.append(cfg)

    #----------------------------------------
    #   Jets
    #----------------------------------------

    if use_jets:
        configSeq += makeConfig ('Jets', containerName='AnaJets', jetCollection='AntiKt4EMPFlowJets')
        configSeq.setOptionValue ('.recalibratePhyslite', False)
        configSeq.setOptionValue ('.runGhostMuonAssociation', True)
        configSeq.setOptionValue ('.runFJvtSelection', True)  # keep True to compute FJvt flag
        configSeq.setOptionValue ('.runFJvtEfficiency', True)
        configSeq.setOptionValue ('.runNNJvtUpdate', True)
        configSeq.setOptionValue ('.runFJvtUpdate', False)

        ## Private alg to run save additional JVT WPs
        cfg = JvtExtraFlagConfig(containerName='AnaJets')
        cfg.setOptionValue('selectionName','Tight')
        cfg.setOptionValue('runFJvtSelection',True)
        cfg.setOptionValue('fJvtWP','Tight')
        configSeq.append(cfg)
        cfg = JvtExtraFlagConfig(containerName='AnaJets')
        cfg.setOptionValue('selectionName','Tighter')
        cfg.setOptionValue('runFJvtSelection',True)
        cfg.setOptionValue('fJvtWP','Tighter')
        configSeq.append(cfg)

        configSeq += makeConfig ('Jets.PtEtaSelection', containerName='AnaJets')
        configSeq.setOptionValue ('.selectionDecoration', 'selectPtEta')
        configSeq.setOptionValue ('.minPt', 15e3)
        configSeq.setOptionValue ('.maxEta', 2.5)

        #configSeq += makeConfig ('Jets.JVT', containerName='AnaJets')


        # b-tagging
        bTaggers = ['GN2v01']
        WPs = ['FixedCutBEff_85','FixedCutBEff_77','FixedCutBEff_70','FixedCutBEff_65','Continuous'] #
        for btagger in bTaggers:
            for WP in WPs:
                configSeq += makeConfig ('Jets.FlavourTagging', containerName='AnaJets')
                configSeq.setOptionValue ('.btagger', btagger)
                configSeq.setOptionValue ('.btagWP', WP)
                configSeq.setOptionValue ('.bTagCalibFile',"xAODBTaggingEfficiency/13TeV/MC20_2025-06-17_GN2v01_v4.root")
                if isRun3:
                    configSeq.setOptionValue ('.bTagCalibFile',"xAODBTaggingEfficiency/13p6TeV/MC23_2025-06-17_GN2v01_v4.root")
                if WP=='Continuous':
                    configSeq += makeConfig ('Jets.FlavourTaggingEventSF', containerName='AnaJets')
                    configSeq.setOptionValue ('.btagger', btagger)
                    configSeq.setOptionValue ('.btagWP', WP)
                    configSeq.setOptionValue ('.eigenvectorReductionB', 'Medium')
                    configSeq.setOptionValue ('.eigenvectorReductionC', 'Medium')
                    configSeq.setOptionValue ('.eigenvectorReductionLight', 'Medium')
                    if isWtaunu: # need to manually set generator for the MET Filetered Wtaunu samples
                        configSeq.setOptionValue ('.generator', 'Sherpa2211')
                    else:
                        configSeq.setOptionValue ('.generator', 'autoconfig')
    
                #generator='default'
                #configSeq.setOptionValue ('.generator', generator)

        ### Extra variables for jets
        # Disabling them to keep jet branches at a  reasonable size
        # reco_branches+=["OutJets_NOSYS.DFCommonJets_QGTagger_NTracks -> jet_DFCommonJets_QGTagger_NTracks",
        #                 "OutJets_NOSYS.DFCommonJets_QGTagger_TracksWidth -> jet_DFCommonJets_QGTagger_TracksWidth",
        #                 "OutJets_NOSYS.DFCommonJets_QGTagger_TracksC1 -> jet_DFCommonJets_QGTagger_TracksC1"]
        if isMC:
            reco_branches+=[
                "OutJets_NOSYS.PartonTruthLabelID -> jet_PartonTruthLabelID",
                "OutJets_NOSYS.HadronConeExclExtendedTruthLabelID -> jet_HadronConeExclExtendedTruthLabelID",
                "OutJets_NOSYS.HadronConeExclTruthLabelID   -> jet_HadronConeExclTruthLabelID"]
        outputContainers['jet_'] = 'OutJets'

    #----------------------------------------
    #   Taus
    #----------------------------------------
    if use_taus:
        configSeq += makeConfig ('TauJets', containerName='AnaTaus')
        configSeq.setOptionValue ('.decorateTruth', True)


        ## The "baseline" are not including any cut on the RNN / GNTau
        ## Then the other based on RNN / GNN, with and without EVeto are w. increasing cuts
        TauX_Wp['Taus'] = [{'wp': 'BaselineForFakes', 'GNTau': False, 'eVeto': True,  'doOR' : False },
                           {'wp': 'Loose',            'GNTau': False, 'eVeto': True,  'doOR' : True },
                           {'wp': 'Medium',           'GNTau': False, 'eVeto': True,  'doOR' : False },
                           {'wp': 'Tight',            'GNTau': False, 'eVeto': True,  'doOR' : False },
                           {'wp': 'BaselineForFakes', 'GNTau': True,  'eVeto': True,  'doOR' : False },
                           {'wp': 'Loose',            'GNTau': True,  'eVeto': True,  'doOR' : False  },
                           {'wp': 'Medium',           'GNTau': True,  'eVeto': True,  'doOR' : False },
                           {'wp': 'Tight',            'GNTau': True,  'eVeto': True,  'doOR' : False },
                           {'wp': 'BaselineForFakes', 'GNTau': False, 'eVeto': False, 'doOR' : False },
                           {'wp': 'Loose',            'GNTau': False, 'eVeto': False, 'doOR' : False },
                           {'wp': 'Medium',           'GNTau': False, 'eVeto': False, 'doOR' : False },
                           {'wp': 'Tight',            'GNTau': False, 'eVeto': False, 'doOR' : False },
                           {'wp': 'BaselineForFakes', 'GNTau': True,  'eVeto': False, 'doOR' : False },
                           {'wp': 'Loose',            'GNTau': True,  'eVeto': False, 'doOR' : False },
                           {'wp': 'Medium',           'GNTau': True,  'eVeto': False, 'doOR' : False },
                           {'wp': 'Tight',            'GNTau': True,  'eVeto': False, 'doOR' : False }
                           ]

        for WP in TauX_Wp['Taus']:
            # Skip GNTau for PHYSLITE / PHYS w old derivation
            if ( WP['GNTau'] and
                 ( isPHYSLITE or
                   (not isPHYSLITE and ((isMC and ptag < 6400))))):
                print(f"Skipping GNTau: isPHYSLITE={isPHYSLITE}; isMC={isMC}; ptag={ptag}")
                continue
            flagName = WP['wp']
            flagName += ("GNTau" if WP['GNTau'] else 'RNN')
            if not WP['eVeto']:
                flagName += "_noElVeto"

            if WP['doOR']:
                TauX_OR['taus'].append(flagName)

            configSeq += makeConfig ('TauJets.WorkingPoint', containerName='AnaTaus', selectionName=flagName)
            configSeq.setOptionValue('.quality',WP['wp'])
            configSeq.setOptionValue('.useGNTau',WP['GNTau'])
            configSeq.setOptionValue('.use_eVeto',WP['eVeto'])
            configSeq.setOptionValue('.noEffSF',True)
            if (WP['wp'] in ["Loose","Medium"]) or (WP['wp']=="Tight" and not WP['eVeto']):
                configSeq.setOptionValue('.noEffSF',False)

        configSeq += makeConfig ('TauJets.PtEtaSelection', containerName='AnaTaus')
        configSeq.setOptionValue ('.selectionDecoration', 'selectPtEta')
        configSeq.setOptionValue ('.minPt', 15e3)
        configSeq.setOptionValue ('.maxEta', 2.5)

        if not isRun3:
            configSeq += makeConfig ('TauJets.TriggerSF')
            configSeq.setOptionValue ('.triggerChainsPerYear', tauTriggerChainsPerYear)
            configSeq.setOptionValue ('.tauID', 'Loose')
            configSeq.setOptionValue ('.containerName', 'AnaTaus')



        outputContainers['tau_'] = 'OutTaus'

        reco_branches+=["OutTaus_NOSYS.RNNJetScoreSigTrans -> tau_RNNJetScoreSigTrans",
                        "OutTaus_NOSYS.PanTau_DecayMode -> tau_PanTauDecayMode"]
        if not isPHYSLITE:
            reco_branches+=["OutTaus_NOSYS.trackWidth -> tau_trackWidth",
                            "OutTaus_NOSYS.RNNJetScore -> tau_RNNJetScore"]
            if ((isMC and ptag > 6400)):
                reco_branches+=["OutTaus_NOSYS.GNTauScoreSigTrans_v0prune -> tau_GNTauScoreSigTrans_v0prune",
                                "OutTaus_NOSYS.GNTauScoreSigTrans_v1trunc -> tau_GNTauScoreSigTrans_v1trunc",
                                ]


    WPset=CombineWorkingPoints(TauX_OR)

    # #Used for debugging: prints Tau Variables
    # from TauX_Gnt1makerAlg.TauInspectorConfig import TauInspectionConfig
    # cfg=TauInspectionConfig('TauInspector')
    # cfg.setOptionValue('taus','AnaTaus')
    # configSeq.append(cfg)


    #----------------------------------------
    #   MET
    #----------------------------------------
    if use_MET:
        for setName, wp_set in WPset.items():
            configSeq+=makeConfig("MissingET")
            configSeq.setOptionValue('.containerName', 'OutMet'+"_"+setName)
            configSeq.setOptionValue('.electrons', (f'AnaElectrons.{wp_set["electrons"]}' if use_electrons else ''))
            configSeq.setOptionValue('.muons', (f'AnaMuons.{wp_set["muons"]}' if use_muons else ''))
            configSeq.setOptionValue('.taus', (f'AnaTaus.{wp_set["taus"]}' if use_taus else ''))
            configSeq.setOptionValue('.jets', ('AnaJets' if use_jets else ''))  # use all jets for MET it does it's own selections!!!
            outputContainers['MET_'+setName+"_"] = 'OutMet'+"_"+setName


    #--------------------------------------------------------
    # Track particle decorations for electrons/muons/taus
    #--------------------------------------------------------
    if use_electrons or use_muons or use_taus:
        from TauX_Gnt1makerAlg.TrackParticleDecorationConfig import TrackParticleDecorationConfig
        cfg=TrackParticleDecorationConfig('LeptonTrackDecor')
        if use_electrons:
            cfg.setOptionValue('electrons','AnaElectrons')
        if use_muons:
            cfg.setOptionValue('muons','AnaMuons')
        if use_taus:
            cfg.setOptionValue('taus','AnaTaus')
        configSeq.append(cfg)



    #--------------------------------------------------------
    #  Overlap Removal
    #--------------------------------------------------------
    for setName, wp_set in WPset.items():
        configSeq += makeConfig ('OverlapRemoval')
        configSeq.setOptionValue('.inputLabel'             ,'pre'+setName)
        configSeq.setOptionValue('.addPreselection'        ,True)
        configSeq.setOptionValue('.electrons'              ,(f'AnaElectrons.{wp_set["electrons"]}' if use_electrons else ''))
        configSeq.setOptionValue('.muons'                  ,(f'AnaMuons.{wp_set["muons"]}' if use_muons else ''))
        configSeq.setOptionValue('.taus'                   ,(f'AnaTaus.{wp_set["taus"]}' if use_taus else ''))
        configSeq.setOptionValue('.electronsSelectionName' ,setName)
        configSeq.setOptionValue('.muonsSelectionName'     ,setName)
        configSeq.setOptionValue('.tausSelectionName'      ,setName)
        configSeq.setOptionValue('.jets'                   ,('AnaJets.baselineJvt' if use_jets else ''))
        configSeq.setOptionValue('.jetsSelectionName'      ,setName)
        configSeq.setOptionValue('.outputLabel','passOR_'+setName)


    #--------------------------------------------------------
    #  Triggers
    #--------------------------------------------------------
    # Setting up trigger config selecting only on the flag   
    configSeq += makeConfig ('Trigger')
    configSeq.setOptionValue('.triggerChainsForSelection', allTriggers)
    configSeq.setOptionValue('.noFilter', noFilter or forceNoFilter )
    configSeq.setOptionValue('.triggerMatchingChainsPerYear',triggerMatchChainsPerYear)    
    configSeq.setOptionValue('.noGlobalTriggerEff',True)
    configSeq.setOptionValue('.muons','AnaMuons')
    configSeq.setOptionValue('.electrons','AnaElectrons')
    configSeq.setOptionValue('.taus','AnaTaus')

    # Setting Trigger SF
    if (( not isMC and flags.Input.DataYear < 2024) or (isMC and flags.Input.MCCampaign != Campaign.MC23e)):
        for setName, wp_set in WPset.items():
            configSeq += makeConfig ('Trigger')
            configSeq.setOptionValue('.noFilter', True)
            configSeq.setOptionValue('.multiTriggerChainsPerYear', triggerChainsSF)
            configSeq.setOptionValue('.muons',f'AnaMuons.{wp_set["muons"]}' )
            configSeq.setOptionValue('.muonID','Loose')
            configSeq.setOptionValue('.electrons',f'AnaElectrons.{wp_set["electrons"]}')
            configSeq.setOptionValue('.electronID','Tight')
            configSeq.setOptionValue('.electronIsol','Tight_VarRad')
            configSeq.setOptionValue('.taus',f'AnaTaus.{wp_set["taus"]}')
            configSeq.setOptionValue('.postfix',"_"+setName)

    # #--------------------------------------------------------
    # # ObjectCutFlow blocks
    # #--------------------------------------------------------
    for setName in WPset.keys():
        configSeq += makeConfig ('ObjectCutFlow',
                                 containerName='AnaJets',
                                 selectionName=setName)
        configSeq += makeConfig ('ObjectCutFlow',
                                 containerName='AnaElectrons',
                                 selectionName=setName)
        configSeq += makeConfig ('ObjectCutFlow',
                                 containerName='AnaMuons',
                                 selectionName=setName)
        configSeq += makeConfig ('ObjectCutFlow',
                                 containerName='AnaTaus',
                                 selectionName=setName)


    #--------------------------------------------------------
    #  Object branchs thinning (slimming)
    #--------------------------------------------------------
    if use_electrons:
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', 'AnaElectrons')
        configSeq.setOptionValue('.selectionName', "||".join(WPset.keys()))
        configSeq.setOptionValue('.outputName', 'OutElectrons')
    if use_muons:
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', 'AnaMuons')
        configSeq.setOptionValue('.selectionName', "||".join(WPset.keys()))
        configSeq.setOptionValue('.outputName', 'OutMuons')
    if use_jets:
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', 'AnaJets')
        configSeq.setOptionValue('.selectionName', "||".join(WPset.keys()))
        configSeq.setOptionValue('.outputName', 'OutJets')
    if use_taus:
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', 'AnaTaus')
        configSeq.setOptionValue('.selectionName', "||".join(WPset.keys()))
        configSeq.setOptionValue('.outputName', 'OutTaus')


    #--------------------------------------------------------
    #  Event selection
    #--------------------------------------------------------
    mycuts = {
        'zerolep': """
TAU_N 50000 == 1
SUM_EL_N_MU_N 5000 == 0
MET >= 150000
SAVE
""",
        'onelep': """
TAU_N 50000 == 1
SUM_EL_N_MU_N 20000 == 1
MET >= 50000
SAVE
""",
        'zerotau': """
TAU_N 1000 == 0
SUM_EL_N_MU_N 150000 == 1
MET >= 150000
SAVE
"""
      }

    makeMultipleWPEventSelectionConfigs(configSeq,
                                        WPs=list(WPset.keys()),
                                        electrons=f"AnaElectrons",
                                        muons = f"AnaMuons",
                                        taus = f"AnaTaus",
                                        met= "OutMet",
                                        metTerm = None,
                                        jets = f"AnaJets",
                                        btagDecoration=None,
                                        preselection=None,
                                        selectionCutsDict = mycuts,
                                        noFilter=forceNoFilter, # keep this filter always on for background/data
                                        cutFlowHistograms=True)



    #--------------------------------------------------------
    #  Truth info
    #--------------------------------------------------------
    from TopCPToolkit.truthConfig import truthConfig
    cfg = truthConfig()
    cfg.setOptionValue ('histories', 'Ttbar')
    configSeq.append(cfg)

    # Vjets/VGamma Truth-level Overlap Removal
    configSeq += makeConfig("VGammaOR")
    configSeq.setOptionValue('.keepInOverlap', VGammaDSID) #list of DSIDs of Vgamma
    configSeq.setOptionValue('.removeInOverlap', VJetsDSID) #list of DSIDs of Vgamma
    configSeq.setOptionValue('.noFilter', True)


    # NNLO reweighting
    from TopCPToolkit.TtbarNNLORecursiveRewConfig import TtbarNNLORecursiveRewConfig
    cfg = TtbarNNLORecursiveRewConfig()
    configSeq.append(cfg)

    cfg = TtbarNNLORecursiveRewConfig()
    cfg.setOptionValue('reweightType','3D')
    configSeq.append(cfg)


    ## Save particle level objects
    if isMC:
        configSeq += makeConfig("PL_Electrons")
        # configSeq += makeConfig ('PL_Electrons.PtEtaSelection')
        # configSeq.setOptionValue ('.selectionDecoration', 'selectPtEta')
        # configSeq.setOptionValue ('.maxEta', 2.5)
        configSeq += makeConfig("PL_Muons")
        configSeq += makeConfig("PL_Taus")
        # configSeq += makeConfig ('PL_Electrons.PtEtaSelection')
        # configSeq.setOptionValue ('.selectionDecoration', 'selectPtEta')
        # configSeq.setOptionValue ('.maxEta', 2.5)
        configSeq += makeConfig("PL_Jets")
        configSeq += makeConfig("PL_Neutrinos")
        configSeq += makeConfig("PL_MissingET")

        configSeq += makeConfig("PL_OverlapRemoval")
        configSeq.setOptionValue("electrons","TruthElectrons")
        configSeq.setOptionValue("muons","TruthMuons")
        configSeq.setOptionValue("jets","AntiKt4TruthDressedWZJets")

        ## PL Thinning
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', "TruthElectrons")
        configSeq.setOptionValue('.outputName', 'OutPLElectrons')
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', "TruthMuons")
        configSeq.setOptionValue('.outputName', 'OutPLMuons')
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', "TruthTaus")
        configSeq.setOptionValue('.outputName', 'OutPLTaus')
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', "AntiKt4TruthDressedWZJets")
        configSeq.setOptionValue('.outputName', 'OutPLJets')
        configSeq+=makeConfig("Thinning")
        configSeq.setOptionValue('.containerName', "TruthNeutrinos")
        configSeq.setOptionValue('.outputName', 'OutPLNeutrinos')


        outputContainers['PL_tau_']='OutPLTaus'
        outputContainers['PL_MET_']='TruthMET'
        outputContainers['PL_el_']='OutPLElectrons'
        outputContainers['PL_mu_']='OutPLMuons'
        outputContainers['PL_jet_']='OutPLJets'
        outputContainers['PL_nu_']='OutPLNeutrinos'

        # if isSignal:
        #     outputContainers['PL_el_']='OutPLElectrons'
        #     outputContainers['PL_mu_']='OutPLMuons'
        #     outputContainers['PL_jet_']='OutPLJets'
        #     outputContainers['PL_nu_']='OutPLNeutrinos'


    #--------------------------------------------------------
    #  Metadata saving
    #--------------------------------------------------------
    cfg = MetaDataSaverConfig('metadata')
    cfg.setOptionValue("treeName","metadataTauX")
    cfg.setOptionValue("metadata",yaml.dump({"wp" : TauX_Wp, "WPSet_OR": WPset}))
    configSeq.append(cfg)

    #--------------------------------------------------------
    #  Output AsgNtuple
    #--------------------------------------------------------
    configSeq += makeConfig ('Output')
    configSeq.setOptionValue ('.treeName', 'reco')
    configSeq.setOptionValue ('.vars', reco_branches)
    configSeq.setOptionValue ('.containers', outputContainers)
    configSeq.setOptionValue ('.storeSelectionFlags', True)
    configSeq.setOptionValue ('.commands', ['disable .*_select_outputSelect.*'])

    #This will print how many times decorations are accessed
    #keep it for debug
    # configSeq += makeConfig ('IOStats')
    # configSeq.setOptionValue('.printOption','ByEntries')



    configAccumulator = ConfigAccumulator(algSeq, flags.Input.DataType,
                                          isPhyslite=isPHYSLITE,
                                          geometry=flags.Input.LHCPeriod,
                                          autoconfigFromFlags=flags,
                                          noSystematics=noSystematics)
    configSeq.fullConfigure(configAccumulator)


