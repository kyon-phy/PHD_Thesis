from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class TauInspectionConfig(ConfigBlock):
    """ConfigBlock to add generic particle decorations"""
    
    def __init__(self, name=''):
        super(TauInspectionConfig, self).__init__()
        self.addOption('taus', None, type=str)
        self.name = name
    
    def makeAlgs(self, config):
        # Computes d0, z0, d0sintheta, etc for the leading or primary track of ele/mu/taus
        alg = config.createAlgorithm('top::TauXTauInspectorAlg', 'TauInspection'+self.name)
        alg.EventInfoContainer = 'EventInfo'
        if self.taus is not None:
            alg.taus = config.readName(self.taus)

        
