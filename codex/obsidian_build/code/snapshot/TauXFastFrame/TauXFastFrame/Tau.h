// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#pragma once
#include "Math/Vector4D.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {
class Tau : public Particle {
 public:
  Tau(){};
  Tau(const ROOT::Math::PtEtaPhiEVector &p4);
  void set_IsTauFlags(unsigned int value);
  unsigned int IsTauFlags() const;

  void set_NNDecayMode(int value);
  int NNDecayMode() const;

  void set_PanTauDecayMode(int value);
  int PanTauDecayMode() const;

  void set_RNNJetScore(float value);
  float RNNJetScore() const;

  void set_RNNJetScoreSigTrans(float value);
  float RNNJetScoreSigTrans() const;

  void set_charge(float value);
  float charge() const;

  void set_d0(float value);
  float d0() const;

  void set_d0sig(float value);
  float d0sig() const;

  void set_deltaz0(float value);
  float deltaz0() const;

  void set_deltaz0sinTheta(float value);
  float deltaz0sinTheta() const;

  void set_nTracks(int value);
  int nTracks() const;

  void set_trackPt(float value);
  float trackPt() const;

  void set_truth_DecayMode(float value);
  float truth_DecayMode() const;

  void set_truth_IsHadronicTau(char value);
  bool truth_IsHadronicTau() const;

  void set_truth_ParticleType(float value);
  float truth_ParticleType() const;

  void set_truth_PartonTruthLabelID(float value);
  float truth_PartonTruthLabelID() const;

  void set_truth_eta_vis(float value);
  float truth_eta_vis() const;

  void set_truth_m_vis(float value);
  float truth_m_vis() const;

  void set_truth_origin(unsigned int value);
  unsigned int truth_origin() const;

  void set_truth_pdgId(int value);
  int truth_pdgId() const;

  void set_truth_phi_vis(float value);
  float truth_phi_vis() const;

  void set_truth_pt_vis(float value);
  float truth_pt_vis() const;

  void set_truth_type(unsigned int value);
  unsigned int truth_type() const;

  void set_vz(float value);
  float vz() const;

  void set_z0(float value);
  float z0() const;

  void set_EvetoFakeTau_effSF_Baseline_NOSYS(float value);
  float EvetoFakeTau_effSF_Baseline_NOSYS() const;

  void set_EvetoFakeTau_effSF_LooseRNN_NOSYS(float value);
  float EvetoFakeTau_effSF_LooseRNN_NOSYS() const;

  void set_EvetoFakeTau_effSF_MediumRNN_NOSYS(float value);
  float EvetoFakeTau_effSF_MediumRNN_NOSYS() const;

  void set_EvetoFakeTau_effSF_TightRNN_NOSYS(float value);
  float EvetoFakeTau_effSF_TightRNN_NOSYS() const;

  void set_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS(float value);
  float EvetoFakeTau_effSF_VeryLooseRNN_NOSYS() const;

  void set_EvetoTrueTau_effSF_Baseline_NOSYS(float value);
  float EvetoTrueTau_effSF_Baseline_NOSYS() const;

  void set_EvetoTrueTau_effSF_LooseRNN_NOSYS(float value);
  float EvetoTrueTau_effSF_LooseRNN_NOSYS() const;

  void set_EvetoTrueTau_effSF_MediumRNN_NOSYS(float value);
  float EvetoTrueTau_effSF_MediumRNN_NOSYS() const;

  void set_EvetoTrueTau_effSF_TightRNN_NOSYS(float value);
  float EvetoTrueTau_effSF_TightRNN_NOSYS() const;

  void set_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS(float value);
  float EvetoTrueTau_effSF_VeryLooseRNN_NOSYS() const;

  void set_ID_effSF_LooseRNN_NOSYS(float value);
  float ID_effSF_LooseRNN_NOSYS() const;

  void set_ID_effSF_LooseRNN_noElVeto_NOSYS(float value);
  float ID_effSF_LooseRNN_noElVeto_NOSYS() const;

  void set_ID_effSF_MediumRNN_NOSYS(float value);
  float ID_effSF_MediumRNN_NOSYS() const;

  void set_ID_effSF_MediumRNN_noElVeto_NOSYS(float value);
  float ID_effSF_MediumRNN_noElVeto_NOSYS() const;

  void set_ID_effSF_TightRNN_NOSYS(float value);
  float ID_effSF_TightRNN_NOSYS() const;

  void set_ID_effSF_TightRNN_noElVeto_NOSYS(float value);
  float ID_effSF_TightRNN_noElVeto_NOSYS() const;

  void set_Reco_effSF_Baseline_NOSYS(float value);
  float Reco_effSF_Baseline_NOSYS() const;

  void set_Reco_effSF_Baseline_noElVeto_NOSYS(float value);
  float Reco_effSF_Baseline_noElVeto_NOSYS() const;

  void set_Reco_effSF_LooseRNN_NOSYS(float value);
  float Reco_effSF_LooseRNN_NOSYS() const;

  void set_Reco_effSF_LooseRNN_noElVeto_NOSYS(float value);
  float Reco_effSF_LooseRNN_noElVeto_NOSYS() const;

  void set_Reco_effSF_MediumRNN_NOSYS(float value);
  float Reco_effSF_MediumRNN_NOSYS() const;

  void set_Reco_effSF_MediumRNN_noElVeto_NOSYS(float value);
  float Reco_effSF_MediumRNN_noElVeto_NOSYS() const;

  void set_Reco_effSF_TightRNN_NOSYS(float value);
  float Reco_effSF_TightRNN_NOSYS() const;

  void set_Reco_effSF_TightRNN_noElVeto_NOSYS(float value);
  float Reco_effSF_TightRNN_noElVeto_NOSYS() const;

  void set_Reco_effSF_VeryLooseRNN_NOSYS(float value);
  float Reco_effSF_VeryLooseRNN_NOSYS() const;

  void set_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS(float value);
  float Reco_effSF_VeryLooseRNN_noElVeto_NOSYS() const;

  void set_select_Baseline_NOSYS(char value);
  bool select_Baseline_NOSYS() const;

  void set_select_Baseline_noElVeto_NOSYS(char value);
  bool select_Baseline_noElVeto_NOSYS() const;

  void set_select_LooseGNTau_NOSYS(char value);
  bool select_LooseGNTau_NOSYS() const;

  void set_select_LooseGNTau_noElVeto_NOSYS(char value);
  bool select_LooseGNTau_noElVeto_NOSYS() const;

  void set_select_LooseRNN_NOSYS(char value);
  bool select_LooseRNN_NOSYS() const;

  void set_select_LooseRNN_noElVeto_NOSYS(char value);
  bool select_LooseRNN_noElVeto_NOSYS() const;

  void set_select_MediumGNTau_NOSYS(char value);
  bool select_MediumGNTau_NOSYS() const;

  void set_select_MediumGNTau_noElVeto_NOSYS(char value);
  bool select_MediumGNTau_noElVeto_NOSYS() const;

  void set_select_MediumRNN_NOSYS(char value);
  bool select_MediumRNN_NOSYS() const;

  void set_select_MediumRNN_noElVeto_NOSYS(char value);
  bool select_MediumRNN_noElVeto_NOSYS() const;

  void set_select_TightGNTau_NOSYS(char value);
  bool select_TightGNTau_NOSYS() const;

  void set_select_TightGNTau_noElVeto_NOSYS(char value);
  bool select_TightGNTau_noElVeto_NOSYS() const;

  void set_select_TightRNN_NOSYS(char value);
  bool select_TightRNN_NOSYS() const;

  void set_select_TightRNN_noElVeto_NOSYS(char value);
  bool select_TightRNN_noElVeto_NOSYS() const;

  void set_select_VeryLooseGNTau_NOSYS(char value);
  bool select_VeryLooseGNTau_NOSYS() const;

  void set_select_VeryLooseGNTau_noElVeto_NOSYS(char value);
  bool select_VeryLooseGNTau_noElVeto_NOSYS() const;

  void set_select_VeryLooseRNN_NOSYS(char value);
  bool select_VeryLooseRNN_NOSYS() const;

  void set_select_VeryLooseRNN_noElVeto_NOSYS(char value);
  bool select_VeryLooseRNN_noElVeto_NOSYS() const;

  void set_select_wpSet0_NOSYS(char value);
  bool select_wpSet0_NOSYS() const;

  void set_select_wpSet1_NOSYS(char value);
  bool select_wpSet1_NOSYS() const;

  void set_select_wpSet2_NOSYS(char value);
  bool select_wpSet2_NOSYS() const;

  void set_select_wpSet3_NOSYS(char value);
  bool select_wpSet3_NOSYS() const;

 private:
  unsigned int m_IsTauFlags = -9999;
  int m_NNDecayMode = -9999;
  int m_PanTauDecayMode = -9999;
  float m_RNNJetScore = -9999;
  float m_RNNJetScoreSigTrans = -9999;
  float m_charge = -9999;
  float m_d0 = -9999;
  float m_d0sig = -9999;
  float m_deltaz0 = -9999;
  float m_deltaz0sinTheta = -9999;
  int m_nTracks = -9999;
  float m_trackPt = -9999;
  float m_truth_DecayMode = -9999;
  bool m_truth_IsHadronicTau = false;
  float m_truth_ParticleType = -9999;
  float m_truth_PartonTruthLabelID = -9999;
  float m_truth_eta_vis = -9999;
  float m_truth_m_vis = -9999;
  unsigned int m_truth_origin = -9999;
  int m_truth_pdgId = -9999;
  float m_truth_phi_vis = -9999;
  float m_truth_pt_vis = -9999;
  unsigned int m_truth_type = -9999;
  float m_vz = -9999;
  float m_z0 = -9999;
  float m_EvetoFakeTau_effSF_Baseline_NOSYS = 1;
  float m_EvetoFakeTau_effSF_LooseRNN_NOSYS = 1;
  float m_EvetoFakeTau_effSF_MediumRNN_NOSYS = 1;
  float m_EvetoFakeTau_effSF_TightRNN_NOSYS = 1;
  float m_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS = 1;
  float m_EvetoTrueTau_effSF_Baseline_NOSYS = 1;
  float m_EvetoTrueTau_effSF_LooseRNN_NOSYS = 1;
  float m_EvetoTrueTau_effSF_MediumRNN_NOSYS = 1;
  float m_EvetoTrueTau_effSF_TightRNN_NOSYS = 1;
  float m_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS = 1;
  float m_ID_effSF_LooseRNN_NOSYS = 1;
  float m_ID_effSF_LooseRNN_noElVeto_NOSYS = 1;
  float m_ID_effSF_MediumRNN_NOSYS = 1;
  float m_ID_effSF_MediumRNN_noElVeto_NOSYS = 1;
  float m_ID_effSF_TightRNN_NOSYS = 1;
  float m_ID_effSF_TightRNN_noElVeto_NOSYS = 1;
  float m_Reco_effSF_Baseline_NOSYS = 1;
  float m_Reco_effSF_Baseline_noElVeto_NOSYS = 1;
  float m_Reco_effSF_LooseRNN_NOSYS = 1;
  float m_Reco_effSF_LooseRNN_noElVeto_NOSYS = 1;
  float m_Reco_effSF_MediumRNN_NOSYS = 1;
  float m_Reco_effSF_MediumRNN_noElVeto_NOSYS = 1;
  float m_Reco_effSF_TightRNN_NOSYS = 1;
  float m_Reco_effSF_TightRNN_noElVeto_NOSYS = 1;
  float m_Reco_effSF_VeryLooseRNN_NOSYS = 1;
  float m_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS = 1;
  bool m_select_Baseline_NOSYS = false;
  bool m_select_Baseline_noElVeto_NOSYS = false;
  bool m_select_LooseGNTau_NOSYS = false;
  bool m_select_LooseGNTau_noElVeto_NOSYS = false;
  bool m_select_LooseRNN_NOSYS = false;
  bool m_select_LooseRNN_noElVeto_NOSYS = false;
  bool m_select_MediumGNTau_NOSYS = false;
  bool m_select_MediumGNTau_noElVeto_NOSYS = false;
  bool m_select_MediumRNN_NOSYS = false;
  bool m_select_MediumRNN_noElVeto_NOSYS = false;
  bool m_select_TightGNTau_NOSYS = false;
  bool m_select_TightGNTau_noElVeto_NOSYS = false;
  bool m_select_TightRNN_NOSYS = false;
  bool m_select_TightRNN_noElVeto_NOSYS = false;
  bool m_select_VeryLooseGNTau_NOSYS = false;
  bool m_select_VeryLooseGNTau_noElVeto_NOSYS = false;
  bool m_select_VeryLooseRNN_NOSYS = false;
  bool m_select_VeryLooseRNN_noElVeto_NOSYS = false;
  bool m_select_wpSet0_NOSYS = false;
  bool m_select_wpSet1_NOSYS = false;
  bool m_select_wpSet2_NOSYS = false;
  bool m_select_wpSet3_NOSYS = false;
};  // Tau
}  // namespace TauXParticles