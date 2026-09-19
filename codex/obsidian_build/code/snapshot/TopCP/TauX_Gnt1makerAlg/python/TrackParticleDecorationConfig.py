from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class TrackParticleDecorationConfig(ConfigBlock):
    """ConfigBlock to add generic particle decorations"""
    
    def __init__(self, name=''):
        super(TrackParticleDecorationConfig, self).__init__()
        self.addOption('electrons', None, type=str)
        self.addOption('muons', None, type=str)
        self.addOption('taus', None, type=str)
        self.name = name
    
    def makeAlgs(self, config):
        # This PrimaryVertexDecorationAlg ensures that the
        # EventInfo container is decorated with the primary vertex position
        # Eventually these decorations can be saved to the tree
        alg = config.createAlgorithm('top::PrimaryVertexDecorationAlg', 'PrimaryVertexDecoration'+self.name)
        alg.EventInfoContainer = 'EventInfo'
        alg.VertexContainer = 'PrimaryVertices'

        # Computes d0, z0, d0sintheta, etc for the leading or primary track of ele/mu/taus
        alg = config.createAlgorithm('top::TrackParticleDecorationAlg', 'TrackParticleDecoration'+self.name)
        alg.EventInfoContainer = 'EventInfo'
        if self.electrons is not None:
            alg.electrons = config.readName(self.electrons)
            config.addOutputVar(self.electrons, 'd0_%SYS%', 'd0', noSys=True)
            config.addOutputVar(self.electrons, 'd0sig_%SYS%', 'd0sig', noSys=True)
            config.addOutputVar(self.electrons, 'z0_%SYS%', 'z0', noSys=True)
            config.addOutputVar(self.electrons, 'deltaz0_%SYS%', 'deltaz0', noSys=True)
            config.addOutputVar(self.electrons, 'deltaz0sinTheta_%SYS%', 'deltaz0sinTheta', noSys=True)
            config.addOutputVar(self.electrons, 'vz_%SYS%', 'vz', noSys=True)
            config.addOutputVar(self.electrons, 'nTrackParticles_%SYS%', 'NtrackParticles', noSys=True)
            config.addOutputVar(self.electrons, 'nInnPixHits_%SYS%', 'NinnPixHits', noSys=True)
            
        if self.muons is not None:
            alg.muons = config.readName(self.muons)
            config.addOutputVar(self.muons, 'd0_%SYS%', 'd0', noSys=True)
            config.addOutputVar(self.muons, 'd0sig_%SYS%', 'd0sig', noSys=True)
            config.addOutputVar(self.muons, 'z0_%SYS%', 'z0', noSys=True)
            config.addOutputVar(self.muons, 'deltaz0_%SYS%', 'deltaz0', noSys=True)
            config.addOutputVar(self.muons, 'deltaz0sinTheta_%SYS%', 'deltaz0sinTheta', noSys=True)
            config.addOutputVar(self.muons, 'vz_%SYS%', 'vz', noSys=True)
            config.addOutputVar(self.muons, 'nInnPixHits_%SYS%', 'NinnPixHits', noSys=True)


        if self.taus is not None:
            alg.taus = config.readName(self.taus)
            config.addOutputVar(self.taus, 'd0_%SYS%', 'd0', noSys=True)
            config.addOutputVar(self.taus, 'd0sig_%SYS%', 'd0sig', noSys=True)
            config.addOutputVar(self.taus, 'z0_%SYS%', 'z0', noSys=True)
            config.addOutputVar(self.taus, 'deltaz0_%SYS%', 'deltaz0', noSys=True)
            config.addOutputVar(self.taus, 'deltaz0sinTheta_%SYS%', 'deltaz0sinTheta', noSys=True)
            config.addOutputVar(self.taus, 'vz_%SYS%', 'vz', noSys=True)
            config.addOutputVar(self.taus, 'trackPt_%SYS%', 'trackPt', noSys=True)

        
