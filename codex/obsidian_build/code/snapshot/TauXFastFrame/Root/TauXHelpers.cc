#include "TauXFastFrame/TauXHelpers.h"

#include <vector>

bool TauXHelpers::getFakeTauFlag(std::vector<TauXParticles::Tau> Taus) {
  for (auto & tau : Taus){
    if (!(tau.truth_IsHadronicTau())) return true;
  }
  return false;
}


unsigned int getRunYear(unsigned int runNumber) {
  // Numbers taken from https://aiatlas029.cern.ch/tagservices/RunBrowser/index.html
  unsigned int runYear = 0;
  if (runNumber >= 266904 && runNumber <= 284484)
    runYear = 2015;
  else if (runNumber >= 296939 && runNumber <= 311481)
    runYear = 2016;
  else if (runNumber >= 324320 && runNumber <= 341649)
    runYear = 2017;
  else if (runNumber >= 348197 && runNumber <= 364485)
    runYear = 2018;
  else if (runNumber >= 427394 && runNumber <= 440613)
    runYear = 2022;
  else if (runNumber >= 450360 && runNumber <= 456749)
    runYear = 2023;
  return runYear;
}

unsigned int TauXHelpers::getNbjets(std::vector<TauXParticles::Jet> jets, int WP) {
  unsigned int nBJets = 0;
  for (TauXParticles::Jet& iJet : jets) {
    if (iJet.GN2v01_Continuous_quantile() >= WP)
      nBJets++;
  }
  return nBJets;
}

unsigned int TauXHelpers::getNjets(std::vector<TauXParticles::Jet> jets) {
  unsigned int nJets = 0;
  for (TauXParticles::Jet& iJet : jets) {
    nJets++;
  }
  return nJets;
}

// (Jiaqi) get b jets
std::vector<TauXParticles::Jet> TauXHelpers::getbJets(const std::vector<TauXParticles::Jet>& jets, int WP) {
  std::vector<TauXParticles::Jet> bJets;
  for (std::size_t i = 0; i < jets.size(); ++i) {
    if (jets.at(i).GN2v01_Continuous_quantile() < WP) continue;
    bJets.emplace_back(jets.at(i));
  }
  return bJets;
}

// (Jiaqi) add get function for SFs
float TauXHelpers::getTauSFs(std::vector<TauXParticles::Tau> Taus) {
  float tauSF = 1;
  for (TauXParticles::Tau& tau : Taus) {
    tauSF *= abs(tau.sf());
  }
  return tauSF;
}

float TauXHelpers::getMuonSFs(std::vector<TauXParticles::Muon> Muons) {
  float muonSF = 1;
  for (TauXParticles::Muon& muon : Muons) {
    muonSF *= abs(muon.sf());
  }
  return muonSF;
}

float TauXHelpers::getElSFs(std::vector<TauXParticles::Electron> Electrons) {
  float elSF = 1;
  for (TauXParticles::Electron& el : Electrons) {
    elSF *= abs(el.sf());
  }
  return elSF;
}

float TauXHelpers::getJetSFs(std::vector<TauXParticles::Jet> Jets) {
  float jetSF = 1;
  for (TauXParticles::Jet& jet : Jets) {
    jetSF *= abs(jet.sf()); // jvt effSF could be -1 if the jet is not applied jvt
  }
  return jetSF;
}

// (Jiaqi) get minDPhi and energy ratio flag for QCD cleanning
bool TauXHelpers::getMinDPhiFlag(std::vector<TauXParticles::Jet> jets, std::vector<TauXParticles::Tau> taus, TauXParticles::MET met) {
  float minDPhi = 1000;
  float energyRatio = 0;
  for (TauXParticles::Jet& jet : jets) {
    float dPhi = abs(jet.DeltaPhi(met));
    if (dPhi < minDPhi) {
      minDPhi = dPhi;
      energyRatio = met.pt() / jet.pt();
    }
  }
  for (TauXParticles::Tau& tau : taus) {
    float dPhi = abs(tau.DeltaPhi(met));
    if (dPhi < minDPhi) {
      minDPhi = dPhi;
      energyRatio = met.pt() / tau.pt();
    }
  }
  if (minDPhi >= 0.4 || energyRatio >= 6) {
    return true;
  } else {
    return false;
  }
}

bool TauXHelpers::getMETflag(unsigned int runNumber,
                             bool HLT_xe70_mht,
                             bool HLT_xe90_mht_L1XE50,
                             bool HLT_xe100_mht_L1XE50,
                             bool HLT_xe110_mht_L1XE50,
                             bool HLT_xe110_pufit_L1XE55,
                             bool HLT_xe110_pufit_L1XE50,
                             bool HLT_xe110_pufit_xe70_L1XE50,
                             bool HLT_xe110_pufit_xe65_L1XE50,
                             bool HLT_xe65_cell_xe90_pfopufit_L1XE50,
                             bool HLT_xe65_cell_xe90_pfopufit_L1jXE110) {
  unsigned int year = getRunYear(runNumber);
  if (year == 2015 && HLT_xe70_mht)
    return true;  // 2015
  else if (year == 2016 && runNumber >= 296939 && runNumber <= 302872 && HLT_xe90_mht_L1XE50)
    return true;  // 2016 A-D3
  else if (year == 2016 && runNumber >= 302919 && runNumber <= 303892 && HLT_xe100_mht_L1XE50)
    return true;  // 2016 D4-F1
  else if (year == 2016 && runNumber >= 303943 && HLT_xe110_mht_L1XE50)
    return true;  // 2016 F2-(open)
  else if (year == 2017 && runNumber >= 325713 && runNumber <= 331975 && HLT_xe110_pufit_L1XE55)
    return true;  // 2017 B1-D5
  else if (year == 2017 && runNumber >= 332303 && HLT_xe110_pufit_L1XE50)
    return true;  // 2017 D6-(open)
  else if (year == 2018 && runNumber >= 348885 && runNumber <= 350013 && HLT_xe110_pufit_xe70_L1XE50)
    return true;  // 2018 B-C5
  else if (year == 2018 && runNumber >= 350067 && HLT_xe110_pufit_xe65_L1XE50)
    return true;  // 2018 C5-(open)
  else if ((year == 2022 || year == 2023) && HLT_xe65_cell_xe90_pfopufit_L1XE50)
    return true;  // 2022 and 2023
  else if (year == 2024 && HLT_xe65_cell_xe90_pfopufit_L1jXE110)
    return true;  // 2024
  return false;
}

bool TauXHelpers::getSLTflag(unsigned int runNumber,
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
                             bool HLT_mu50_L1MU14FCH) {
  unsigned int year = getRunYear(runNumber);
  bool SLT_2015 = HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose || HLT_mu20_iloose_L1MU15 || HLT_mu40;
  bool SLT_20161718 = HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0 || HLT_mu26_ivarmedium || HLT_mu50;
  bool SLT_2022 = HLT_e26_lhtight_ivarloose_L1EM22VHI || HLT_e60_lhmedium_L1EM22VHI || HLT_e140_lhloose_L1EM22VHI || HLT_mu24_ivarmedium_L1MU14FCH || HLT_mu50_L1MU14FCH;
  bool SLT_202324 = HLT_e26_lhtight_ivarloose_L1eEM26M || HLT_e60_lhmedium_L1eEM26M || HLT_e140_lhloose_L1eEM26M || HLT_mu24_ivarmedium_L1MU14FCH || HLT_mu50_L1MU14FCH;
  if (year == 2015) {
    return SLT_2015;
  } else if (year == 2016 || year == 2017 || year == 2018) {
    return SLT_20161718;
  } else if (year == 2022) {
    return SLT_2022;
  } else if (year == 2023 || year == 2024) {
    return SLT_202324;
  }
  return false;
}

bool TauXHelpers::getDLTflag(unsigned int runNumber,
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
                             bool HLT_e17_lhloose_mu14_L1eEM18L_MU8F) {
  unsigned int year = getRunYear(runNumber);
  bool DLT_2015 = HLT_mu18_mu8noL1 || HLT_2e12_lhloose_L12EM10VH || HLT_e17_lhloose_mu14;
  bool DLT_2016 = HLT_mu22_mu8noL1 || HLT_2e17_lhvloose_nod0 || HLT_e17_lhloose_nod0_mu14;
  bool DLT_201718 = HLT_mu22_mu8noL1 || HLT_2e24_lhvloose_nod0 || HLT_e17_lhloose_nod0_mu14;
  bool DLT_2022 = HLT_mu22_mu8noL1_L1MU14FCH || HLT_2e24_lhvloose_L12EM20VH || HLT_e17_lhloose_mu14_L1EM15VH_MU8F;
  bool DLT_202324 = HLT_mu22_mu8noL1_L1MU14FCH || HLT_2e24_lhvloose_L12eEM24L || HLT_e17_lhloose_mu14_L1eEM18L_MU8F;
  if (year == 2015) {
    return DLT_2015;
  } else if (year == 2016) {
    return DLT_2016;
  } else if (year == 2017 || year == 2018) {
    return DLT_201718;
  } else if (year == 2022) {
    return DLT_2022;
  } else if (year == 2023 || year == 2024) {
    return DLT_202324;
  }
  return false;
}

bool TauXHelpers::getSTTflag(std::vector<TauXParticles::Tau> tau,
                             unsigned int runNumber,
                             bool HLT_tau80_medium1_tracktwo_L1TAU60,
                             bool HLT_tau125_medium1_tracktwo,
                             bool HLT_tau160_medium1_tracktwo,
                             bool HLT_tau160_medium1_tracktwo_L1TAU100,
                             bool HLT_tau160_medium1_tracktwoEF_L1TAU100,
                             bool HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100,
                             bool HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140,
                             bool isTriggerDecision) {
  if (tau.size() < 1)
    return false;
  bool trigger_decision = false;
  bool trigger_offlineCut = false;
  unsigned int RunYear = getRunYear(runNumber);
  auto taus_pt_0 = tau[0].pt();
  if (taus_pt_0 > ((80 + 20) * 1000) && (RunYear == 2015 || (RunYear == 2016 && (runNumber >= 296939 && runNumber <= 300287)))) {
    trigger_offlineCut = true;
    if (HLT_tau80_medium1_tracktwo_L1TAU60 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((125 + 15) * 1000) && RunYear == 2016 && (runNumber >= 300345 && runNumber <= 302872)) {
    trigger_offlineCut = true;
    if (HLT_tau125_medium1_tracktwo == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((160 + 20) * 1000) && ((RunYear == 2016 && (runNumber >= 302919)) || (RunYear == 2017 && (runNumber <= 326695)))) {
    trigger_offlineCut = true;
    if (HLT_tau160_medium1_tracktwo == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((160 + 20) * 1000) && RunYear == 2017 && (runNumber >= 326834)) {
    trigger_offlineCut = true;
    if (HLT_tau160_medium1_tracktwo_L1TAU100 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((160 + 20) * 1000) && RunYear == 2018) {
    trigger_offlineCut = true;
    if (runNumber >= 355529 && runNumber <= 364485) {
      if ((HLT_tau160_medium1_tracktwoEF_L1TAU100 == 1) || (HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 == 1)) {
        trigger_decision = true;
      }
    } else {
      if (HLT_tau160_medium1_tracktwoEF_L1TAU100 == 1) {
        trigger_decision = true;
      }
    }
  } else if (taus_pt_0 > ((160 + 20) * 1000) && RunYear == 2022) {
    trigger_offlineCut = true;
    if (HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((160 + 20) * 1000) && RunYear == 2023) {
    trigger_offlineCut = true;
    if (runNumber >= 450360 && runNumber < 451896) {  // before 2023 first 2400bunches
      if (HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 == 1) {
        trigger_decision = true;
      }
    } else {
      if (HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140 == 1) {
        trigger_decision = true;
      }
    }
  }
  if (isTriggerDecision) {
    return trigger_decision;
  } else {
    return trigger_offlineCut;
  }
}

bool TauXHelpers::getDTTflag(std::vector<TauXParticles::Tau> tau,
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
                             bool HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25) {
  if (tau.size() < 2)
    return false;
  bool trigger_decision = false;
  unsigned int RunYear = getRunYear(runNumber);
  auto DRtautau01 = tau[0].DeltaR(tau[1]);
  float taus_pt_0 = tau[0].pt();
  float taus_pt_1 = tau[1].pt();
  float jet_pt_0 = 0;
  if (jet.size() >= 1)
    jet_pt_0 = jet[0].pt();
  float jet_pt_1 = 0;
  if (jet.size() >= 2)
    jet_pt_1 = jet[1].pt();
  if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 80 * 1000 && RunYear == 2015) {
    if (HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((80 + 15) * 1000) && taus_pt_1 > ((50 + 10) * 1000) &&
             ((RunYear == 2016 && runNumber >= 302919) || (RunYear == 2017 && runNumber <= 327490))) {  // begin tau80 (no DTT1J)
    if (HLT_tau80_medium1_tracktwo_L1TAU60_tau50_medium1_tracktwo_L1TAU12 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((80 + 15) * 1000) && taus_pt_1 > ((60 + 15) * 1000) && RunYear == 2017 && runNumber >= 327582) {
    if (HLT_tau80_medium1_tracktwo_L1TAU60_tau60_medium1_tracktwo_L1TAU40 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((80 + 15) * 1000) && taus_pt_1 > ((60 + 15) * 1000) && RunYear == 2018) {
    if (runNumber >= 355529 && runNumber <= 364485) {
      if ((HLT_tau80_medium1_tracktwoEF_L1TAU60_tau60_medium1_tracktwoEF_L1TAU40 == 1) || (HLT_tau80_mediumRNN_tracktwoMVA_L1TAU60_tau60_mediumRNN_tracktwoMVA_L1TAU40 == 1)) {
        trigger_decision = true;
      }
    } else if (HLT_tau80_medium1_tracktwoEF_L1TAU60_tau60_medium1_tracktwoEF_L1TAU40 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((80 + 15) * 1000) && taus_pt_1 > ((60 + 15) * 1000) && (RunYear == 2022 || RunYear == 2023)) {
    if (HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1TAU60_2TAU40 == 1) {
      trigger_decision = true;
    }
  }  // end tau80 (no DTT1J)
  else if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 80 * 1000 &&
           (RunYear == 2016 || (RunYear == 2017 && (runNumber >= 324320 && runNumber <= 326695)))) {
    if (HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 80 * 1000 && DRtautau01 < 2.5 && RunYear == 2017 && runNumber > 326695) {
    if (HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1DR_TAU20ITAU12I_J25 == 1) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 80 * 1000 && DRtautau01 < 2.5 && RunYear == 2018) {
    if (runNumber >= 355529 && runNumber <= 364485) {
      if ((HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1DR_TAU20ITAU12I_J25 == 1) ||
          (HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1DR_TAU20ITAU12I_J25 == 1)) {
        trigger_decision = true;
      }
    } else if (HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1DR_TAU20ITAU12I_J25 == 1) {
      trigger_decision = true;
    }
  }
  else if (taus_pt_0 > ((35+5)*1000) && taus_pt_1 > ((25+5)*1000) && jet_pt_0 > 45*1000 && jet_pt_1 > 45*1000 &&
  RunYear == 2017) {
      if (HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM_4J12 == 1) { trigger_decision = true;
      }
  }
  else if (taus_pt_0 > ((35+5)*1000) && taus_pt_1 > ((25+5)*1000) && jet_pt_0 > 45*1000 && jet_pt_1 > 45*1000 &&
  RunYear == 2018) {
      if (runNumber >= 355529 && runNumber <= 364485) {
        if ((HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1TAU20IM_2TAU12IM_4J12p0ETA23 == 1) ||
        (HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1TAU20IM_2TAU12IM_4J12p0ETA23 == 1)) {
        trigger_decision = true; }
      }
      else if (HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1TAU20IM_2TAU12IM_4J12p0ETA23 == 1) {
      trigger_decision = true; }
  }
  else if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 80 * 1000 && DRtautau01 < 2.5 && (RunYear == 2022 || RunYear == 2023)) {
    if ((HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1DR_TAU20ITAU12I_J25 == 1)) {
      trigger_decision = true;
    }
  } else if (taus_pt_0 > ((35 + 5) * 1000) && taus_pt_1 > ((25 + 5) * 1000) && jet_pt_0 > 45 * 1000 && jet_pt_1 > 45 * 1000 && (RunYear == 2022 || RunYear == 2023)) {
    if ((HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25 == 1)) {
      trigger_decision = true;
    }
  }

  return trigger_decision;
}

ROOT::RDF::RNode TauXHelpers::add_lepton_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame) {

  auto AddObjVector = [](const std::vector<TauXParticles::Electron>& electrons, const std::vector<TauXParticles::Muon>& muons) {
    std::vector<TauXParticles::Lepton> leptons;

    for ( auto &el : electrons){
      leptons.push_back(TauXParticles::Lepton(el));
    }

    for ( auto &mu : muons){
      leptons.push_back(TauXParticles::Lepton(mu));
    }

    sort(leptons.begin(), leptons.end(), [](const TauXParticles::Lepton& a, const TauXParticles::Lepton& b) { return a.Pt() > b.Pt(); });
    return leptons;
  };

  mainNode = frame->systematicRedefine(mainNode,
                                     "Leptons_NOSYS",                      // name of the new column
                                     AddObjVector,                         // functor (function that is called)
                                     {"Electrons_NOSYS", "Muons_NOSYS"});  // what it depends on

  return mainNode;
};


ROOT::RDF::RNode TauXHelpers::add_met(ROOT::RDF::RNode mainNode, std::string wpSet, TauXFastFrame* frame) {

  auto AddMET = [](const float& met_met,
		   const float& met_phi,
		   const float& met_significance,
		   const float& met_sumet
		   ) {
    
    TauXParticles::MET met(met_met, met_phi);
    met.set_sumEt( met_sumet );
    met.set_significance( met_significance );

    return met;
  };

  mainNode = frame->systematicRedefine(mainNode,
                                     "MET_NOSYS",
                                     AddMET,     
                                     {"MET_"+wpSet+"_met_NOSYS",
				      "MET_"+wpSet+"_phi_NOSYS",
				      "MET_"+wpSet+"_significance_NOSYS",
				      "MET_"+wpSet+"_sumet_NOSYS"
				     });

  return mainNode;
};

ROOT::RDF::RNode TauXHelpers::addHNLtDNNOutput(ROOT::RDF::RNode mainNode, TauXFastFrame* frame) {
    
  // Add a new column with the ONNX score
  // take tau and jet as input
  auto AddNNScore = [frame](
    const std::vector<ROOT::Math::PtEtaPhiEVector>& tau_tlvVec,
    const std::vector<ROOT::Math::PtEtaPhiEVector>& jet_tlvVec) {
    if (tau_tlvVec.size() < 1 || jet_tlvVec.size() < 2) {
      return float(-1.);
    }
    // Prepare the input feature vector from tau properties
    std::vector<float> X;

    // for (size_t i = 0; i < tau_tlvVec.size(); ++i) {
    // std::cout<< "tau_tlvVec size: " << tau_tlvVec.size() << std::endl;
        auto tau = tau_tlvVec[0];
        auto jet0 = jet_tlvVec[0];
        auto jet1 = jet_tlvVec[1];
        X.push_back(tau.Pt());
        X.push_back(jet0.Pt());
        X.push_back(jet1.Pt());
    // }

    // Define shape for ONNX model input
    std::vector<int64_t> shape = {1, static_cast<int64_t>(X.size())};

    // Create ONNX inference instance
    ONNXWrapper::Inference infer = frame->m_onnx->createInferenceInstance();
    infer.addInputs(X, shape);

    // Evaluate model
    frame->m_onnx->evaluate(infer, 0);

    // Extract the output score
    float score = infer.getOutputs<std::array<float, 1>>(0)->at(0);

    return score;
  };

  mainNode = frame->systematicRedefine(mainNode,"DNN_CUSTOMCLASS_NOSYS", AddNNScore,
    {"tau_TLV_NOSYS",
     "jet_TLV_NOSYS"});

  return mainNode;
}


