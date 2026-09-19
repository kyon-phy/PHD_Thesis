from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class LQWeightCorrectionConfig(ConfigBlock):
    """ConfigBlock to add LQ weight correction"""
    
    def __init__(self, name=''):
        super(LQWeightCorrectionConfig, self).__init__()
        self.addOption('truthTaus', None, type=str)
        self.addOption('truthBottoms', None, type=str)
        self.addOption('truthBSM', None, type=str)
        self.addOption('truthElectrons', None, type=str)
        self.addOption('truthJets', None, type=str)
        self.name = name
    
    def makeAlgs(self, config):

        # only run on specific samples (TODO: to be implemented)

        # Create algorithm
        alg = config.createAlgorithm('top::LQWeightCorrectionAlg', 'LQWeightCorrectionAlgorithm'+self.name)
        
        # pass configurations to the algorithm
        alg.EventInfoContainer = 'EventInfo'
        if self.truthTaus is not None:
            alg.truthTaus = config.readName(self.truthTaus)
        if self.truthBottoms is not None:
            alg.truthBottoms = config.readName(self.truthBottoms)
        if self.truthBSM is not None:
            alg.truthBSM = config.readName(self.truthBSM)
        if self.truthElectrons is not None:
            alg.truthElectrons = config.readName(self.truthElectrons)
        if self.truthJets is not None:
            alg.truthJets = config.readName(self.truthJets)
        config.addPrivateTool('truthWeightTool', 'PMGTools::PMGTruthWeightTool')            
        
        # add the output variables
        config.addOutputVar('EventInfo', 'corr_weight_mc_%SYS%', 'weight_mc_corrected')
        config.addOutputVar('EventInfo', 'truth_jet_pt_0_%SYS%', 'truth_jet_pt_0')
        config.addOutputVar('EventInfo', 'truth_jet_pt_1_%SYS%', 'truth_jet_pt_1')
        config.addOutputVar('EventInfo', 'truth_tauB_bestMass_%SYS%', 'truth_tauB_bestMass')
        config.addOutputVar('EventInfo', 'truth_tauB_Mass_%SYS%', 'truth_tauB_Mass')
        config.addOutputVar('EventInfo', 'truth_BSM_LQMass_%SYS%', 'truth_BSM_LQMass')