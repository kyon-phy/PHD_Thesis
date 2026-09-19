from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class PrimaryVertexDecorationConfig(ConfigBlock):
    """ConfigBlock to add generic particle decorations"""
    
    def __init__(self, name=''):
        super(PrimaryVertexDecorationConfig, self).__init__('PrimaryVertexDecoration')
        self.addOption('electrons', None, type=str)
        self.addOption('muons', None, type=str)
        self.name = name
    
    def makeAlgs(self, config):
        alg = config.createAlgorithm('top::PrimaryVertexDecorationAlg', 'PrimaryVertexDecoration'+self.name)
        alg.EventInfoContainer = 'EventInfo'
        alg.VertexContainer = 'PrimaryVertices'

        # config.addOutputVar('EventInfo', 'priVtx_x', 'priVtx_x', noSys=True)
        # config.addOutputVar('EventInfo', 'priVtx_y', 'priVtx_y', noSys=True)
        # config.addOutputVar('EventInfo', 'priVtx_z', 'priVtx_z', noSys=True)

        
        
