from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock
from AnalysisAlgorithmsConfig.ConfigAccumulator import DataType
from AthenaConfiguration.Enums import LHCPeriod
from AthenaCommon.SystemOfUnits	import GeV

class JvtExtraFlagConfig (ConfigBlock) :
    """Block that only computes JVT score for jets adding a new decoration"""

    def __init__ (self, containerName='') :
        super (JvtExtraFlagConfig, self).__init__ ()
        self.setBlockName('JVTExtra')
        self.addOption ('containerName', containerName, type=str,
            noneAction='error',
            info="the name of the input container.")
        self.addOption ('selectionName', '', type=str, info="")
        self.addOption ('runJvtSelection', False, type=bool,
            info="whether to run JVT selection. The default is False.")
        self.addOption ('runFJvtSelection', False, type=bool,
            info="whether to run forward JVT selection. The default is False.")
        self.addOption ('jvtWP', "FixedEffPt", type=str,
            info="which Jvt WP to apply. The default is FixedEffPt.")
        self.addOption ('fJvtWP', "Loose", type=str,
            info="which fJvt WP to apply. The default is Loose.")
        self.addOption ('runJvtEfficiency', True, type=bool,
            info="whether to calculate the JVT efficiency. The default is False.")
        self.addOption ('runFJvtEfficiency', True, type=bool,
            info="whether to calculate the forward JVT efficiency. The default is False.")


    def makeAlgs (self, config) :


        jetCollectionName="AntiKt4EMPFlowJets"


        if self.jvtWP not in ["FixedEffPt"]:
            raise ValueError(
                "Unsupported NNJvt WP '{0}'".format(self.jvtWP) )

        if self.fJvtWP not in ["Loose", "Tight", "Tighter"]:
            raise ValueError(
                "Unsupported fJvt WP '{0}'".format(self.fJvtWP) )

        # Set up the jet efficiency scale factor calculation algorithm
        # Change the truthJetCollection property to AntiKt4TruthWZJets if preferred
        if self.runJvtSelection :
            alg = config.createAlgorithm('CP::AsgSelectionAlg', f'JvtSelectionAlg{self.containerName+self.selectionName}')
            config.addPrivateTool('selectionTool', 'CP::NNJvtSelectionTool')
            alg.selectionTool.JetContainer = config.readName(self.containerName)
            alg.selectionTool.WorkingPoint = self.jvtWP
            alg.selectionTool.MaxPtForJvt = 60*GeV
            alg.selectionDecoration = f"jvt_{self.selectionName},as_char"
            alg.particles = config.readName(self.containerName)

            if self.runJvtEfficiency and config.dataType() is not DataType.Data:
                alg = config.createAlgorithm( 'CP::JvtEfficiencyAlg', 'JvtEfficiencyAlg'+self.containerName+self.selectionName )
                config.addPrivateTool( 'efficiencyTool', 'CP::NNJvtEfficiencyTool' )
                alg.efficiencyTool.JetContainer = config.readName(self.containerName)
                alg.efficiencyTool.MaxPtForJvt = 60*GeV
                alg.efficiencyTool.WorkingPoint = self.jvtWP
                if config.geometry() is LHCPeriod.Run2:
                    alg.efficiencyTool.SFFile = "JetJvtEfficiency/May2024/NNJvtSFFile_Run2_EMPFlow.root"
                else:
                    alg.efficiencyTool.SFFile = "JetJvtEfficiency/May2024/NNJvtSFFile_Run3_EMPFlow.root"
                alg.selection = f"jvt_{self.selectionName},as_char"
                alg.scaleFactorDecoration = f'jvt_{self.selectionName}_effSF_%SYS%'
                alg.outOfValidity = 2
                alg.outOfValidityDeco = 'no_jvt'
                alg.skipBadEfficiency = False
                alg.jets = config.readName (self.containerName)
                alg.preselection = config.getPreselection (self.containerName, '')
                config.addOutputVar (self.containerName, alg.scaleFactorDecoration, 'jvtEfficiency'+self.selectionName)
            config.addSelection (self.containerName, self.selectionName+'Jvt', f"jvt_{self.selectionName},as_char", preselection=False)

        if self.runFJvtSelection :
            alg = config.createAlgorithm('CP::AsgSelectionAlg', f'FJvtSelectionAlg{self.containerName+self.selectionName}')
            config.addPrivateTool('selectionTool', 'CP::FJvtSelectionTool')
            alg.selectionTool.JetContainer = config.readName(self.containerName)
            alg.selectionTool.WorkingPoint = self.fJvtWP
            alg.selectionDecoration = f"fjvt_{self.selectionName},as_char"
            alg.particles = config.readName(self.containerName)

            if self.runFJvtEfficiency and config.dataType() is not DataType.Data:
                alg = config.createAlgorithm( 'CP::JvtEfficiencyAlg', 'FJvtEfficiencyAlg'+self.containerName+self.selectionName )
                config.addPrivateTool( 'efficiencyTool', 'CP::FJvtEfficiencyTool' )
                alg.efficiencyTool.JetContainer = config.readName(self.containerName)
                alg.efficiencyTool.WorkingPoint = self.fJvtWP
                if config.geometry() is LHCPeriod.Run2:
                    alg.efficiencyTool.SFFile = "JetJvtEfficiency/May2024/fJvtSFFile_Run2_EMPFlow.root"
                else:
                    alg.efficiencyTool.SFFile = "JetJvtEfficiency/May2024/fJvtSFFile_Run3_EMPFlow.root"
                alg.selection = f"fjvt_{self.selectionName},as_char"
                alg.scaleFactorDecoration = f'fjvt_{self.selectionName}_effSF_%SYS%'
                alg.outOfValidity = 2
                alg.outOfValidityDeco = 'no_fjvt'
                alg.skipBadEfficiency = False
                alg.jets = config.readName (self.containerName)
                alg.preselection = config.getPreselection (self.containerName, '')
                config.addOutputVar (self.containerName, alg.scaleFactorDecoration, 'fjvtEfficiency'+self.selectionName)
            config.addSelection (self.containerName, self.selectionName+'FJvt', f"fjvt_{self.selectionName},as_char", preselection=False)

