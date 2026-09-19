
#include "TauXFastFrame/TauXFastFrame.h"

#include <iostream>

#include "FastFrames/DefineHelpers.h"
#include "FastFrames/UniqueSampleID.h"
#include "TauXFastFrame/Jet.h"
#include "TauXFastFrame/Lepton.h"
#include "TauXFastFrame/Tau.h"
#include "TauXFastFrame/TauXHelpers.h"
#include "TauXFastFrame/WorkingPointMap.h"



ROOT::RDF::RNode TauXFastFrame::defineVariables(ROOT::RDF::RNode mainNode, const std::shared_ptr<Sample>& sample, const UniqueSampleID& id) {



  // Get working point combination
  std::string wpSet = getWP(m_config);


  // print sample info and get simulation type
  std::string simulation_type = "unknown";
  LOG(INFO) << "(Jiaqi) sample name: " << sample->name() << "\n";
  for (const auto& id : sample->uniqueSampleIDs()) {
      LOG(INFO) << "(Jiaqi) sample DSID: " << id.dsid() << "\n";
      LOG(INFO) << "(Jiaqi) sample simulation: " << id.simulation() << "\n";
      if (simulation_type == "unknown") simulation_type = id.simulation();
  }

  
  // Manipulate presel and WP strings
  std::string presel_tau = m_config->customOptions().getOption<std::string>("presel_tau", "");
  std::string presel_el = m_config->customOptions().getOption<std::string>("presel_el", "");
  std::string presel_mu = m_config->customOptions().getOption<std::string>("presel_mu", "");
  std::string presel_jet = m_config->customOptions().getOption<std::string>("presel_jet", ""); 
  if (presel_tau.size() == 0)
    presel_tau = "1";
  if (presel_el.size() == 0)
    presel_el = "1";
  if (presel_mu.size() == 0)
    presel_mu = "1";
  if (presel_jet.size() == 0)
    presel_jet = "1";
  presel_tau = "tau_select_" + wpSet + "_NOSYS" + " && " + presel_tau;
  presel_el = "el_select_" + wpSet + "_NOSYS" + " && " + presel_el;
  presel_mu = "mu_select_" + wpSet + "_NOSYS" + " && " + presel_mu;
  presel_jet = "jet_select_" + wpSet + "_NOSYS" + " && " + presel_jet;

  // Scale factor combinations
  std::string el_sf_def = "el_pt_NOSYS/el_pt_NOSYS";
  std::string mu_sf_def = "mu_pt_NOSYS/mu_pt_NOSYS";
  std::string tau_sf_def = "tau_pt_NOSYS/tau_pt_NOSYS";
  std::string jet_sf_def = "jet_pt_NOSYS/jet_pt_NOSYS";

  LOG(INFO) << "(Jiaqi) presel_tau: " << presel_tau << "\n";
  LOG(INFO) << "(Jiaqi) presel_el: " << presel_el << "\n";
  LOG(INFO) << "(Jiaqi) presel_mu: " << presel_mu << "\n";
  LOG(INFO) << "(Jiaqi) presel_jet: " << presel_jet << "\n";
  
  // std::string wp = presel_tau.substr(presel_tau.find("tau_select_") + 10, presel_tau.find("NOSYS") - presel_tau.find("tau_select_") - 10);

  // if (TauXParticles::TauWP[wpSet]=="LooseRNN"){
  //   tau_sf_def = "tau_ID_effSF_"+TauXParticles::TauWP[wpSet]+"_NOSYS" "*" "tau_Reco_effSF_"+TauXParticles::TauWP[wpSet]+"_NOSYS";
  // }
  // if (TauXParticles::MuonWP[wpSet] == "Loose_Loose_VarRad"){
  //   mu_sf_def = "mu_TTVA_effSF_"+TauXParticles::MuonWP[wpSet]+"_NOSYS" "*" "mu_reco_effSF_"+TauXParticles::MuonWP[wpSet]+"_NOSYS" "*" "mu_isol_effSF_"+TauXParticles::MuonWP[wpSet]+"_NOSYS";
  // }
  // add electron and FTag SFs
  // if (TauXParticles::ElectronWP[wpSet] == "TightLH_Loose_VarRad"){
    // el_sf_def = "el_id_effSF_"+TauXParticles::ElectronWP[wpSet]+"_NOSYS" "*" "el_reco_effSF_"+TauXParticles::ElectronWP[wpSet]+"_NOSYS" "*" "el_isol_effSF_"+TauXParticles::ElectronWP[wpSet]+"_NOSYS";
  // }

  // TODO: (Jiaqi) get the wpSet from the presel object
  


  // customized SFs for taunub analysis (curretnly only fullsim samples avaiable for electron SFs)
  // tau_sf_def = "tau_ID_effSF_TightRNN_noElVeto_NOSYS" "*" "tau_Reco_effSF_TightRNN_noElVeto_NOSYS";
  tau_sf_def = "tau_ID_effSF_MediumRNN_NOSYS" "*" "tau_Reco_effSF_MediumRNN_NOSYS * tau_EvetoTrueTau_effSF_LooseRNN_NOSYS * tau_EvetoFakeTau_effSF_LooseRNN_NOSYS";
  // tau_sf_def = "tau_ID_effSF_LooseRNN_NOSYS" "*" "tau_Reco_effSF_LooseRNN_NOSYS";
  mu_sf_def = "mu_TTVA_effSF_Medium_Tight_VarRad_NOSYS" "*" "mu_reco_effSF_Medium_Tight_VarRad_NOSYS" "*" "mu_isol_effSF_Medium_Tight_VarRad_NOSYS";
  // mu_sf_def = "mu_TTVA_effSF_Loose_Loose_VarRad_NOSYS" "*" "mu_reco_effSF_Loose_Loose_VarRad_NOSYS" "*" "mu_isol_effSF_Loose_Loose_VarRad_NOSYS";
  el_sf_def = "el_id_effSF_TightLH_HighPtCaloOnly_NOSYS" "*" "el_reco_effSF_TightLH_HighPtCaloOnly_NOSYS" "*" "el_isol_effSF_TightLH_HighPtCaloOnly_NOSYS";
  jet_sf_def = "jet_jvtEfficiency_NOSYS";

  
  mainNode = TauXHelpers::add_tau_vector(mainNode, this, presel_tau, tau_sf_def, sample->isData());
  mainNode = TauXHelpers::add_el_vector(mainNode, this, presel_el, el_sf_def, sample->isData());
  mainNode = TauXHelpers::add_mu_vector(mainNode, this, presel_mu, mu_sf_def, sample->isData());
  mainNode = TauXHelpers::add_jet_vector(mainNode, this, presel_jet, jet_sf_def, sample->isData());
  mainNode = TauXHelpers::add_lepton_vector(mainNode, this);
  mainNode = TauXHelpers::add_met(mainNode, wpSet, this);

  if (!sample->isData()) {
    mainNode = MainFrame::systematicRedefine(
        mainNode, "isFakeTau_NOSYS", TauXHelpers::getFakeTauFlag, {"Taus_NOSYS"});
  }

  
  mainNode = MainFrame::systematicStringDefine(mainNode, "pass_zerolep_NOSYS", "Taus_NOSYS.size()>0 && Leptons_NOSYS.size()==0");
  mainNode = MainFrame::systematicStringDefine(mainNode, "pass_onelep_NOSYS", "Taus_NOSYS.size()>0 && Leptons_NOSYS.size()==1");
  mainNode = MainFrame::systematicStringDefine(mainNode, "pass_twolep_NOSYS", "Taus_NOSYS.size()>0 && Leptons_NOSYS.size()==2");

  // nJets vars
  // b-tagging WP: [1,2,3,4,5,6] -> [100%,90%,85%,77%,70%,65%] for GN2v01!
  mainNode = MainFrame::systematicRedefine(mainNode, "nbJets90_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNbjets(jets, 2); }, {"Jets_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "nbJets85_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNbjets(jets, 3); }, {"Jets_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "nbJets77_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNbjets(jets, 4); }, {"Jets_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "nbJets70_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNbjets(jets, 5); }, {"Jets_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "nbJets65_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNbjets(jets, 6); }, {"Jets_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "nJets_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getNjets(jets); }, {"Jets_NOSYS"});

  // add sorted b jets list
  mainNode = MainFrame::systematicRedefine(mainNode, "bJets85_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return TauXHelpers::getbJets(jets, 3); }, {"Jets_NOSYS"});

  // add b jet vars
  mainNode = MainFrame::systematicRedefine(mainNode, "bJets85_pt_0_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return jets.size()>0 ? jets[0].pt() : -999.; }, {"bJets85_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "bJets85_eta_0_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return jets.size()>0 ? jets[0].eta() : -999.; }, {"bJets85_NOSYS"});
  mainNode = MainFrame::systematicRedefine(mainNode, "bJets85_phi_0_NOSYS", [](std::vector<TauXParticles::Jet> jets) { return jets.size()>0 ? jets[0].phi() : -999.; }, {"bJets85_NOSYS"});


  // TODO (Jiaqi) add minDPhi calculation for QCD cleaning
  mainNode = MainFrame::systematicRedefine(mainNode, "flag_minDPhi_NOSYS", [](std::vector<TauXParticles::Jet> jets, std::vector<TauXParticles::Tau  > taus, TauXParticles::MET met) { return TauXHelpers::getMinDPhiFlag(jets, taus, met); }, {"Jets_NOSYS", "Taus_NOSYS", "MET_NOSYS"});


  // TRIGGER (and other) FLAGS
  // TODO: add run 3 triggers and DTT 4J12
  std::string runNumber_str = "randomRunNumber";
  if (sample->isData()) {
    runNumber_str = "runNumber";
  }

  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_SLT_decision_NOSYS",
                                         TauXHelpers::getSLTflag,
                                         {runNumber_str,
                                          "trigPassed_HLT_mu20_iloose_L1MU15",
                                          "trigPassed_HLT_mu26_ivarmedium",
                                          "trigPassed_HLT_mu40",
                                          "trigPassed_HLT_mu50",
                                          "trigPassed_HLT_e24_lhmedium_L1EM20VH",
                                          "trigPassed_HLT_e26_lhtight_nod0_ivarloose",
                                          "trigPassed_HLT_e60_lhmedium",
                                          "trigPassed_HLT_e60_lhmedium_nod0",
                                          "trigPassed_HLT_e120_lhloose",
                                          "trigPassed_HLT_e140_lhloose_nod0",
                                          "trigPassed_HLT_e26_lhtight_ivarloose_L1EM22VHI",
                                          "trigPassed_HLT_e60_lhmedium_L1EM22VHI",
                                          "trigPassed_HLT_e140_lhloose_L1EM22VHI",
                                          "trigPassed_HLT_e26_lhtight_ivarloose_L1eEM26M",
                                          "trigPassed_HLT_e60_lhmedium_L1eEM26M",
                                          "trigPassed_HLT_e140_lhloose_L1eEM26M",
                                          "trigPassed_HLT_mu24_ivarmedium_L1MU14FCH",
                                          "trigPassed_HLT_mu50_L1MU14FCH"});

  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_DLT_decision_NOSYS",
                                         TauXHelpers::getDLTflag,
                                         {runNumber_str,
                                          "trigPassed_HLT_mu18_mu8noL1",
                                          "trigPassed_HLT_mu22_mu8noL1",
                                          "trigPassed_HLT_2e12_lhloose_L12EM10VH",
                                          "trigPassed_HLT_2e17_lhvloose_nod0",
                                          "trigPassed_HLT_2e24_lhvloose_nod0",
                                          "trigPassed_HLT_e17_lhloose_mu14",
                                          "trigPassed_HLT_e17_lhloose_nod0_mu14",
                                          "trigPassed_HLT_mu22_mu8noL1_L1MU14FCH",
                                          "trigPassed_HLT_2e24_lhvloose_L12EM20VH",
                                          "trigPassed_HLT_e17_lhloose_mu14_L1EM15VH_MU8F",
                                          "trigPassed_HLT_2e24_lhvloose_L12eEM24L",
                                          "trigPassed_HLT_e17_lhloose_mu14_L1eEM18L_MU8F"});

  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_MET_decision_NOSYS",
                                         TauXHelpers::getMETflag,
                                         {runNumber_str,
                                          "trigPassed_HLT_xe70_mht",
                                          "trigPassed_HLT_xe90_mht_L1XE50",
                                          "trigPassed_HLT_xe100_mht_L1XE50",
                                          "trigPassed_HLT_xe110_mht_L1XE50",
                                          "trigPassed_HLT_xe110_pufit_L1XE55",
                                          "trigPassed_HLT_xe110_pufit_L1XE50",
                                          "trigPassed_HLT_xe110_pufit_xe70_L1XE50",
                                          "trigPassed_HLT_xe110_pufit_xe65_L1XE50",
                                          "trigPassed_HLT_xe65_cell_xe90_pfopufit_L1XE50",
                                          "trigPassed_HLT_xe65_cell_xe90_pfopufit_L1jXE110"});

  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_STT_decision_NOSYS",
                                         [](std::vector<TauXParticles::Tau> tau,
                                            unsigned int runNumber,
                                            bool HLT_tau80_medium1_tracktwo_L1TAU60,
                                            bool HLT_tau125_medium1_tracktwo,
                                            bool HLT_tau160_medium1_tracktwo,
                                            bool HLT_tau160_medium1_tracktwo_L1TAU100,
                                            bool HLT_tau160_medium1_tracktwoEF_L1TAU100,
                                            bool HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                                            bool HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140) {
                                           return TauXHelpers::getSTTflag(tau,
                                                                          runNumber,
                                                                          HLT_tau80_medium1_tracktwo_L1TAU60,
                                                                          HLT_tau125_medium1_tracktwo,
                                                                          HLT_tau160_medium1_tracktwo,
                                                                          HLT_tau160_medium1_tracktwo_L1TAU100,
                                                                          HLT_tau160_medium1_tracktwoEF_L1TAU100,
                                                                          HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                                                                          HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140,
                                                                          1);
                                         },
                                         {"Taus_NOSYS",
                                          runNumber_str,
                                          "trigPassed_HLT_tau80_medium1_tracktwo_L1TAU60",
                                          "trigPassed_HLT_tau125_medium1_tracktwo",
                                          "trigPassed_HLT_tau160_medium1_tracktwo",
                                          "trigPassed_HLT_tau160_medium1_tracktwo_L1TAU100",
                                          "trigPassed_HLT_tau160_medium1_tracktwoEF_L1TAU100",
                                          "trigPassed_HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100",
                                          "trigPassed_HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140"});

  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_STT_offlineCut_NOSYS",
                                         [](std::vector<TauXParticles::Tau> tau,
                                            unsigned int runNumber,
                                            bool HLT_tau80_medium1_tracktwo_L1TAU60,
                                            bool HLT_tau125_medium1_tracktwo,
                                            bool HLT_tau160_medium1_tracktwo,
                                            bool HLT_tau160_medium1_tracktwo_L1TAU100,
                                            bool HLT_tau160_medium1_tracktwoEF_L1TAU100,
                                            bool HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                                            bool HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140) {
                                           return TauXHelpers::getSTTflag(tau,
                                                                          runNumber,
                                                                          HLT_tau80_medium1_tracktwo_L1TAU60,
                                                                          HLT_tau125_medium1_tracktwo,
                                                                          HLT_tau160_medium1_tracktwo,
                                                                          HLT_tau160_medium1_tracktwo_L1TAU100,
                                                                          HLT_tau160_medium1_tracktwoEF_L1TAU100,
                                                                          HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                                                                          HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140,
                                                                          0);
                                         },
                                         {"Taus_NOSYS",
                                          runNumber_str,
                                          "trigPassed_HLT_tau80_medium1_tracktwo_L1TAU60",
                                          "trigPassed_HLT_tau125_medium1_tracktwo",
                                          "trigPassed_HLT_tau160_medium1_tracktwo",
                                          "trigPassed_HLT_tau160_medium1_tracktwo_L1TAU100",
                                          "trigPassed_HLT_tau160_medium1_tracktwoEF_L1TAU100",
                                          "trigPassed_HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100",
                                          "trigPassed_HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140"});

/*
  mainNode = MainFrame::systematicRedefine(mainNode,
                                         "flag_DTT_decision_NOSYS",
                                         TauXHelpers::getDTTflag,
                                         {"Taus_NOSYS",
                                          "Jets_NOSYS",
                                          runNumber_str,
                                          "trigPassed_HLT_tau80_medium1_tracktwo_L1TAU60_tau50_medium1_tracktwo_L1TAU12",
                                          "trigPassed_HLT_tau80_medium1_tracktwo_L1TAU60_tau60_medium1_tracktwo_L1TAU40",
                                          "trigPassed_HLT_tau80_medium1_tracktwoEF_L1TAU60_tau60_medium1_tracktwoEF_L1TAU40",
                                          "trigPassed_HLT_tau80_mediumRNN_tracktwoMVA_L1TAU60_tau60_mediumRNN_tracktwoMVA_L1TAU40",
                                          "trigPassed_HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM",
                                          "trigPassed_HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo",
                                          "trigPassed_HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1DR_TAU20ITAU12I_J25",
                                          "trigPassed_HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1DR_TAU20ITAU12I_J25",
                                          "trigPassed_HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1DR_TAU20ITAU12I_J25",
                                          "trigPassed_HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM_4J12",
                                          "trigPassed_HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1TAU20IM_2TAU12IM_4J12p0ETA23",
                                          "trigPassed_HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1TAU20IM_2TAU12IM_4J12p0ETA23",
                                          "trigPassed_HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1TAU60_2TAU40",
                                          "trigPassed_HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1DR_TAU20ITAU12I_J25",
                                          "trigPassed_HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25"});
*/

  // (Jiaqi) add FTag SFs
  if (!sample->isData()) {
    mainNode = MainFrame::systematicRedefine(mainNode,
                                           "tauSF_NOSYS",
                                           [](std::vector<TauXParticles::Tau> Taus) { return TauXHelpers::getTauSFs(Taus); },
                                           {"Taus_NOSYS"});
    mainNode = MainFrame::systematicRedefine(mainNode,
                                           "muonSF_NOSYS",
                                           [](std::vector<TauXParticles::Muon> Muons) { return TauXHelpers::getMuonSFs(Muons); },
                                           {"Muons_NOSYS"});
    mainNode = MainFrame::systematicRedefine(mainNode,
                                           "elSF_NOSYS",
                                           [](std::vector<TauXParticles::Electron> Electrons) { return TauXHelpers::getElSFs(Electrons); },
                                           {"Electrons_NOSYS"});
    mainNode = MainFrame::systematicRedefine(mainNode,
                                           "jetSF_NOSYS",
                                           [](std::vector<TauXParticles::Jet> Jets) { return TauXHelpers::getJetSFs(Jets); },
                                           {"Jets_NOSYS"});
  }

  std::string NNpath = m_config->customOptions().getOption<std::string>("NNpath", "");
  if (!NNpath.empty()) {
    mainNode = TauXHelpers::addHNLtDNNOutput(mainNode, this);} 
  return mainNode;
}

ROOT::RDF::RNode TauXFastFrame::defineVariablesNtuple(ROOT::RDF::RNode mainNode, const std::shared_ptr<Sample>& sample, const UniqueSampleID& id) {

  mainNode = defineVariables(mainNode, sample, id);

  mainNode = mainNode.Define("tau_0_pt", [](std::vector<TauXParticles::Tau> part) { return part.size()>0 ? part[0].pt()*0.001 : -999.; }, {"Taus_NOSYS"});
  mainNode = mainNode.Define("tau_0_eta", [](std::vector<TauXParticles::Tau> part) { return part.size()>0 ? part[0].eta() : -999.; }, {"Taus_NOSYS"});
  mainNode = mainNode.Define("tau_0_phi", [](std::vector<TauXParticles::Tau> part) { return part.size()>0 ? part[0].phi() : -999.; }, {"Taus_NOSYS"});
  mainNode = mainNode.Define("tau_0_e", [](std::vector<TauXParticles::Tau> part) { return part.size()>0 ? part[0].e()*0.001 : -999.; }, {"Taus_NOSYS"});
  mainNode = mainNode.Define("tau_0_q", [](std::vector<TauXParticles::Tau> part) { return part.size()>0 ? part[0].charge() : -999.; }, {"Taus_NOSYS"});
  mainNode = mainNode.Define("lepton_0_pt", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].pt()*0.001 : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_eta", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].eta() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_phi", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].phi() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_e", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].e()*0.001 : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_q", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].charge() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_isMu", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].is_muon() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_0_isEl", [](std::vector<TauXParticles::Lepton> part) { return part.size()>0 ? part[0].is_electron() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_pt", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].pt()*0.001 : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_eta", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].eta() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_phi", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].phi() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_e", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].e()*0.001 : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_q", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].charge() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_isMu", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].is_muon() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("lepton_1_isEl", [](std::vector<TauXParticles::Lepton> part) { return part.size()>1 ? part[1].is_electron() : -999.; }, {"Leptons_NOSYS"});
  mainNode = mainNode.Define("jet_0_pt", [](std::vector<TauXParticles::Jet> part) { return part.size()>0 ? part[0].pt()*0.001 : -999.; }, {"Jets_NOSYS"});
  mainNode = mainNode.Define("jet_0_eta", [](std::vector<TauXParticles::Jet> part) { return part.size()>0 ? part[0].eta() : -999.; }, {"Jets_NOSYS"});
  mainNode = mainNode.Define("jet_0_phi", [](std::vector<TauXParticles::Jet> part) { return part.size()>0 ? part[0].phi() : -999.; }, {"Jets_NOSYS"});
  mainNode = mainNode.Define("jet_0_e", [](std::vector<TauXParticles::Jet> part) { return part.size()>0 ? part[0].e()*0.001 : -999.; }, {"Jets_NOSYS"});


  return mainNode;
}

ROOT::RDF::RNode TauXFastFrame::defineVariablesTruth(ROOT::RDF::RNode node,
                                                     const std::string& /*sample*/,
                                                     const std::shared_ptr<Sample>& /*sample*/,
                                                     const UniqueSampleID& /*sampleID*/) {
  return node;
}

ROOT::RDF::RNode TauXFastFrame::defineVariablesNtupleTruth(ROOT::RDF::RNode node,
                                                           const std::string& /*treeName*/,
                                                           const std::shared_ptr<Sample>& /*sample*/,
                                                           const UniqueSampleID& /*sampleID*/) {
  return node;
}

std::string TauXFastFrame::getWP(const std::shared_ptr<ConfigSetting>& m_config){
  std::string wpSet = m_config->customOptions().getOption<std::string>("wpSet", "");
  std::string wpElectron = m_config->customOptions().getOption<std::string>("wpElectron", "");
  std::string wpMuon = m_config->customOptions().getOption<std::string>("wpMuon", "");
  std::string wpTau = m_config->customOptions().getOption<std::string>("wpTau", "");

  // Check if the provided WP Set is not invalid or find it based on the specified Wps for Ele/Mu/Tau
  if ( wpSet.size() >0 && (wpElectron.size() + wpMuon.size() + wpTau.size())==0 ) {
    if (TauXParticles::ElectronWP.find(wpSet) == TauXParticles::ElectronWP.end()){
      LOG(ERROR) << "The specified WP set is not valid, available WPs are:\n";
      for (const auto& [key, value] : TauXParticles::ElectronWP) {
 	LOG(ERROR) << "WP set \"" << key << ":\n";
	LOG(ERROR)   << " Electron " << TauXParticles::ElectronWP[key] << "\n";
	LOG(ERROR)   << " Muon     " << TauXParticles::MuonWP[key] << "\n";
	LOG(ERROR)  << " Tau      " << TauXParticles::TauWP[key] << "\n";
      }
      throw std::invalid_argument("");
    }    
  }else if ( wpSet.size()==0 && wpElectron.size()>0 && wpMuon.size()>0 && wpTau.size()>0 ){
    // Resolve WPset
    for (const auto& [key, value] : TauXParticles::ElectronWP) {
      if (TauXParticles::ElectronWP.at(key) == wpElectron &&
	  TauXParticles::MuonWP.at(key) == wpMuon &&
	  TauXParticles::TauWP.at(key) == wpTau)
	{
	  wpSet = key;
	}
    }
    if (wpSet.size()==0) {
      LOG(ERROR) << "Could not guess a WP set from the provided options, available WPs are:\n";
      for (const auto& [key, value] : TauXParticles::ElectronWP) {
 	LOG(ERROR) << "WP set \"" << key << ":\n";
	LOG(ERROR)   << " Electron " << TauXParticles::ElectronWP[key] << "\n";
	LOG(ERROR)   << " Muon     " << TauXParticles::MuonWP[key] << "\n";
	LOG(ERROR)  << " Tau      " << TauXParticles::TauWP[key] << "\n";
      }
      throw std::invalid_argument("");      
    }   
  }
  else{
    LOG(ERROR) << "Error when processing working points, either wpSet is missing or swpSet and wpElectron/wpMuon/wpTau are set at the same time\n";
    throw std::invalid_argument("");
  }
  LOG(INFO) << "------------------------------------------------------------\n";
  LOG(INFO) << "Using working point set " << wpSet << "\n";
  LOG(INFO) << " Electrons: " << TauXParticles::ElectronWP[wpSet] << "\n";
  LOG(INFO) << " Muons:     " << TauXParticles::MuonWP[wpSet] << "\n";
  LOG(INFO) << " Taus:      " << TauXParticles::TauWP[wpSet] << "\n";
  LOG(INFO) << "------------------------------------------------------------\n";
return wpSet;  
}
