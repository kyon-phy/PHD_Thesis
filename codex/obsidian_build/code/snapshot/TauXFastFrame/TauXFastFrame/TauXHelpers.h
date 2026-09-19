#include "FastFrames/DefineHelpers.h"
#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TauXFastFrame/Electron.h"
#include "TauXFastFrame/Jet.h"
#include "TauXFastFrame/Lepton.h"
#include "TauXFastFrame/Muon.h"
#include "TauXFastFrame/Tau.h"
#include "TauXFastFrame/Met.h"
#include "TauXFastFrame/TauXFastFrame.h"
#include "FastFrames/ONNXWrapper.h" 

using RNode = ROOT::RDF::RNode;

namespace TauXHelpers {

unsigned int getNbjets(std::vector<TauXParticles::Jet> jets, int WP);
unsigned int getNjets(std::vector<TauXParticles::Jet> jets);
std::vector<TauXParticles::Jet> getbJets(const std::vector<TauXParticles::Jet>& jets, int WP);
bool getFakeTauFlag(std::vector<TauXParticles::Tau> Taus);
float getTauSFs(std::vector<TauXParticles::Tau> Taus);
float getMuonSFs(std::vector<TauXParticles::Muon> Muons);
float getElSFs(std::vector<TauXParticles::Electron> Electrons);
float getJetSFs(std::vector<TauXParticles::Jet> Jets);
bool getMinDPhiFlag(std::vector<TauXParticles::Jet> jets, std::vector<TauXParticles::Tau> taus, TauXParticles::MET met);

bool getSLTflag(unsigned int runNumber,
                bool HLT_mu20_iloose_L1MU15,
                bool HLT_mu26_ivarmedium,
                bool HLT_mu40,
                bool HLT_mu50,
                bool HLT_e24_lhmedium_L1EM20VH,
                bool HLT_e26_lhtight_nod0_ivarloose,
                bool HLT_e60_lhmedium,
                bool HLT_e60_lhmedium_nod0,
                bool HLT_e120_lhloose,
                bool HLT_e140_lhloose_nod0,
                bool HLT_e26_lhtight_ivarloose_L1EM22VHI,
                bool HLT_e60_lhmedium_L1EM22VHI,
                bool HLT_e140_lhloose_L1EM22VHI,
                bool HLT_e26_lhtight_ivarloose_L1eEM26M,
                bool HLT_e60_lhmedium_L1eEM26M,
                bool HLT_e140_lhloose_L1eEM26M,
                bool HLT_mu24_ivarmedium_L1MU14FCH,
                bool HLT_mu50_L1MU14FCH);

bool getDLTflag(unsigned int runNumber,
                bool HLT_mu18_mu8noL1,
                bool HLT_mu22_mu8noL1,
                bool HLT_2e12_lhloose_L12EM10VH,
                bool HLT_2e17_lhvloose_nod0,
                bool HLT_2e24_lhvloose_nod0,
                bool HLT_e17_lhloose_mu14,
                bool HLT_e17_lhloose_nod0_mu14,
                bool HLT_mu22_mu8noL1_L1MU14FCH,
                bool HLT_2e24_lhvloose_L12EM20VH,
                bool HLT_e17_lhloose_mu14_L1EM15VH_MU8F,
                bool HLT_2e24_lhvloose_L12eEM24L,
                bool HLT_e17_lhloose_mu14_L1eEM18L_MU8F);

bool getMETflag(unsigned int runNumber,
                bool HLT_xe70_mht,
                bool HLT_xe90_mht_L1XE50,
                bool HLT_xe100_mht_L1XE50,
                bool HLT_xe110_mht_L1XE50,
                bool HLT_xe110_pufit_L1XE55,
                bool HLT_xe110_pufit_L1XE50,
                bool HLT_xe110_pufit_xe70_L1XE50,
                bool HLT_xe110_pufit_xe65_L1XE50,
                bool HLT_xe65_cell_xe90_pfopufit_L1XE50,
                bool HLT_xe65_cell_xe90_pfopufit_L1jXE110);

bool getSTTflag(std::vector<TauXParticles::Tau> tau,
                unsigned int runNumber,
                bool HLT_tau80_medium1_tracktwo_L1TAU60,
                bool HLT_tau125_medium1_tracktwo,
                bool HLT_tau160_medium1_tracktwo,
                bool HLT_tau160_medium1_tracktwo_L1TAU100,
                bool HLT_tau160_medium1_tracktwoEF_L1TAU100,
                bool HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                bool HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140,
                bool isTriggerDecision);

bool getDTTflag(std::vector<TauXParticles::Tau> tau,
                std::vector<TauXParticles::Jet> jet,
                unsigned int runNumber,
                bool HLT_tau80_medium1_tracktwo_L1TAU60_tau50_medium1_tracktwo_L1TAU12,
                bool HLT_tau80_medium1_tracktwo_L1TAU60_tau60_medium1_tracktwo_L1TAU40,
                bool HLT_tau80_medium1_tracktwoEF_L1TAU60_tau60_medium1_tracktwoEF_L1TAU40,
                bool HLT_tau80_mediumRNN_tracktwoMVA_L1TAU60_tau60_mediumRNN_tracktwoMVA_L1TAU40,
                bool HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM,
                bool HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo,
                bool HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1DR_TAU20ITAU12I_J25,
                bool HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1DR_TAU20ITAU12I_J25,
                bool HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1DR_TAU20ITAU12I_J25,
                bool HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM_4J12,
                bool HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1TAU20IM_2TAU12IM_4J12p0ETA23,
                bool HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1TAU20IM_2TAU12IM_4J12p0ETA23,
                bool HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1TAU60_2TAU40,
                bool HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1DR_TAU20ITAU12I_J25,
                bool HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25);

RNode add_lepton_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame);
RNode add_met(ROOT::RDF::RNode mainNode, std::string wpSet, TauXFastFrame* frame);

RNode add_tau_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData);
RNode add_el_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData);
RNode add_mu_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData);
RNode add_jet_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData);

//trial function to add DNN score
RNode addHNLtDNNOutput(ROOT::RDF::RNode mainNode, TauXFastFrame* frame);
  
}  // namespace TauXHelpers
