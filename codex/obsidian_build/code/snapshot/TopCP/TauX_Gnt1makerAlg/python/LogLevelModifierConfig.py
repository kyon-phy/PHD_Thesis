from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock

class LogLevelModifierConfig(ConfigBlock):
    """ConfigBlock to change the outputlevel property of an existing CP::Alg"""
    
    def __init__(self, name=''):
        super(LogLevelModifierConfig, self).__init__()
        self.addOption('algname', None, type=str)
        self.addOption('handle', None, type=str)
        self.addOption('level', None, type=int)
        self.name = name
    
    def makeAlgs(self, config):

        alg=config._algorithms[self.algname]
        getattr(alg,self.handle).OutputLevel = self.level
        #  1=VERBOSE / 2 DEBUG / 3 INFO / 4 WARN / 5 ERR / 6 FATAL

