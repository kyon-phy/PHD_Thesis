from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class MetaDataSaverConfig(ConfigBlock):
    
    def __init__(self, name=''):
        super(MetaDataSaverConfig, self).__init__()
        self.addOption('treeName', "metadata", type=str)
        self.addOption('metadata', "", type=str)
        self.name = name
    
    def makeAlgs(self, config):
        alg = config.createAlgorithm('top::MetaDataSaverAlg', 'MetaDataSaver'+self.name)
        alg.TreeName = self.treeName
        alg.metadata = self.metadata

        

        
        
