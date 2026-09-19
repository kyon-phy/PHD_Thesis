// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#include "../TauXFastFrame/Tau.h"

#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"

using TauXParticles::Tau;

Tau::Tau(const ROOT::Math::PtEtaPhiEVector &p4) : Particle(p4){};

void Tau::set_IsTauFlags(unsigned int value) {
  this->m_IsTauFlags = (unsigned int)value;
}

unsigned int Tau::IsTauFlags() const {
  return this->m_IsTauFlags;
}

void Tau::set_NNDecayMode(int value) {
  this->m_NNDecayMode = (int)value;
}

int Tau::NNDecayMode() const {
  return this->m_NNDecayMode;
}

void Tau::set_PanTauDecayMode(int value) {
  this->m_PanTauDecayMode = (int)value;
}

int Tau::PanTauDecayMode() const {
  return this->m_PanTauDecayMode;
}

void Tau::set_RNNJetScore(float value) {
  this->m_RNNJetScore = (float)value;
}

float Tau::RNNJetScore() const {
  return this->m_RNNJetScore;
}

void Tau::set_RNNJetScoreSigTrans(float value) {
  this->m_RNNJetScoreSigTrans = (float)value;
}

float Tau::RNNJetScoreSigTrans() const {
  return this->m_RNNJetScoreSigTrans;
}

void Tau::set_charge(float value) {
  this->m_charge = (float)value;
}

float Tau::charge() const {
  return this->m_charge;
}

void Tau::set_d0(float value) {
  this->m_d0 = (float)value;
}

float Tau::d0() const {
  return this->m_d0;
}

void Tau::set_d0sig(float value) {
  this->m_d0sig = (float)value;
}

float Tau::d0sig() const {
  return this->m_d0sig;
}

void Tau::set_deltaz0(float value) {
  this->m_deltaz0 = (float)value;
}

float Tau::deltaz0() const {
  return this->m_deltaz0;
}

void Tau::set_deltaz0sinTheta(float value) {
  this->m_deltaz0sinTheta = (float)value;
}

float Tau::deltaz0sinTheta() const {
  return this->m_deltaz0sinTheta;
}

void Tau::set_nTracks(int value) {
  this->m_nTracks = (int)value;
}

int Tau::nTracks() const {
  return this->m_nTracks;
}

void Tau::set_trackPt(float value) {
  this->m_trackPt = (float)value;
}

float Tau::trackPt() const {
  return this->m_trackPt;
}

void Tau::set_truth_DecayMode(float value) {
  this->m_truth_DecayMode = (float)value;
}

float Tau::truth_DecayMode() const {
  return this->m_truth_DecayMode;
}

void Tau::set_truth_IsHadronicTau(char value) {
  this->m_truth_IsHadronicTau = (bool)value;
}

bool Tau::truth_IsHadronicTau() const {
  return this->m_truth_IsHadronicTau;
}

void Tau::set_truth_ParticleType(float value) {
  this->m_truth_ParticleType = (float)value;
}

float Tau::truth_ParticleType() const {
  return this->m_truth_ParticleType;
}

void Tau::set_truth_PartonTruthLabelID(float value) {
  this->m_truth_PartonTruthLabelID = (float)value;
}

float Tau::truth_PartonTruthLabelID() const {
  return this->m_truth_PartonTruthLabelID;
}

void Tau::set_truth_eta_vis(float value) {
  this->m_truth_eta_vis = (float)value;
}

float Tau::truth_eta_vis() const {
  return this->m_truth_eta_vis;
}

void Tau::set_truth_m_vis(float value) {
  this->m_truth_m_vis = (float)value;
}

float Tau::truth_m_vis() const {
  return this->m_truth_m_vis;
}

void Tau::set_truth_origin(unsigned int value) {
  this->m_truth_origin = (unsigned int)value;
}

unsigned int Tau::truth_origin() const {
  return this->m_truth_origin;
}

void Tau::set_truth_pdgId(int value) {
  this->m_truth_pdgId = (int)value;
}

int Tau::truth_pdgId() const {
  return this->m_truth_pdgId;
}

void Tau::set_truth_phi_vis(float value) {
  this->m_truth_phi_vis = (float)value;
}

float Tau::truth_phi_vis() const {
  return this->m_truth_phi_vis;
}

void Tau::set_truth_pt_vis(float value) {
  this->m_truth_pt_vis = (float)value;
}

float Tau::truth_pt_vis() const {
  return this->m_truth_pt_vis;
}

void Tau::set_truth_type(unsigned int value) {
  this->m_truth_type = (unsigned int)value;
}

unsigned int Tau::truth_type() const {
  return this->m_truth_type;
}

void Tau::set_vz(float value) {
  this->m_vz = (float)value;
}

float Tau::vz() const {
  return this->m_vz;
}

void Tau::set_z0(float value) {
  this->m_z0 = (float)value;
}

float Tau::z0() const {
  return this->m_z0;
}

void Tau::set_EvetoFakeTau_effSF_Baseline_NOSYS(float value) {
  this->m_EvetoFakeTau_effSF_Baseline_NOSYS = (float)value;
}

float Tau::EvetoFakeTau_effSF_Baseline_NOSYS() const {
  return this->m_EvetoFakeTau_effSF_Baseline_NOSYS;
}

void Tau::set_EvetoFakeTau_effSF_LooseRNN_NOSYS(float value) {
  this->m_EvetoFakeTau_effSF_LooseRNN_NOSYS = (float)value;
}

float Tau::EvetoFakeTau_effSF_LooseRNN_NOSYS() const {
  return this->m_EvetoFakeTau_effSF_LooseRNN_NOSYS;
}

void Tau::set_EvetoFakeTau_effSF_MediumRNN_NOSYS(float value) {
  this->m_EvetoFakeTau_effSF_MediumRNN_NOSYS = (float)value;
}

float Tau::EvetoFakeTau_effSF_MediumRNN_NOSYS() const {
  return this->m_EvetoFakeTau_effSF_MediumRNN_NOSYS;
}

void Tau::set_EvetoFakeTau_effSF_TightRNN_NOSYS(float value) {
  this->m_EvetoFakeTau_effSF_TightRNN_NOSYS = (float)value;
}

float Tau::EvetoFakeTau_effSF_TightRNN_NOSYS() const {
  return this->m_EvetoFakeTau_effSF_TightRNN_NOSYS;
}

void Tau::set_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS(float value) {
  this->m_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS = (float)value;
}

float Tau::EvetoFakeTau_effSF_VeryLooseRNN_NOSYS() const {
  return this->m_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS;
}

void Tau::set_EvetoTrueTau_effSF_Baseline_NOSYS(float value) {
  this->m_EvetoTrueTau_effSF_Baseline_NOSYS = (float)value;
}

float Tau::EvetoTrueTau_effSF_Baseline_NOSYS() const {
  return this->m_EvetoTrueTau_effSF_Baseline_NOSYS;
}

void Tau::set_EvetoTrueTau_effSF_LooseRNN_NOSYS(float value) {
  this->m_EvetoTrueTau_effSF_LooseRNN_NOSYS = (float)value;
}

float Tau::EvetoTrueTau_effSF_LooseRNN_NOSYS() const {
  return this->m_EvetoTrueTau_effSF_LooseRNN_NOSYS;
}

void Tau::set_EvetoTrueTau_effSF_MediumRNN_NOSYS(float value) {
  this->m_EvetoTrueTau_effSF_MediumRNN_NOSYS = (float)value;
}

float Tau::EvetoTrueTau_effSF_MediumRNN_NOSYS() const {
  return this->m_EvetoTrueTau_effSF_MediumRNN_NOSYS;
}

void Tau::set_EvetoTrueTau_effSF_TightRNN_NOSYS(float value) {
  this->m_EvetoTrueTau_effSF_TightRNN_NOSYS = (float)value;
}

float Tau::EvetoTrueTau_effSF_TightRNN_NOSYS() const {
  return this->m_EvetoTrueTau_effSF_TightRNN_NOSYS;
}

void Tau::set_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS(float value) {
  this->m_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS = (float)value;
}

float Tau::EvetoTrueTau_effSF_VeryLooseRNN_NOSYS() const {
  return this->m_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS;
}

void Tau::set_ID_effSF_LooseRNN_NOSYS(float value) {
  this->m_ID_effSF_LooseRNN_NOSYS = (float)value;
}

float Tau::ID_effSF_LooseRNN_NOSYS() const {
  return this->m_ID_effSF_LooseRNN_NOSYS;
}

void Tau::set_ID_effSF_LooseRNN_noElVeto_NOSYS(float value) {
  this->m_ID_effSF_LooseRNN_noElVeto_NOSYS = (float)value;
}

float Tau::ID_effSF_LooseRNN_noElVeto_NOSYS() const {
  return this->m_ID_effSF_LooseRNN_noElVeto_NOSYS;
}

void Tau::set_ID_effSF_MediumRNN_NOSYS(float value) {
  this->m_ID_effSF_MediumRNN_NOSYS = (float)value;
}

float Tau::ID_effSF_MediumRNN_NOSYS() const {
  return this->m_ID_effSF_MediumRNN_NOSYS;
}

void Tau::set_ID_effSF_MediumRNN_noElVeto_NOSYS(float value) {
  this->m_ID_effSF_MediumRNN_noElVeto_NOSYS = (float)value;
}

float Tau::ID_effSF_MediumRNN_noElVeto_NOSYS() const {
  return this->m_ID_effSF_MediumRNN_noElVeto_NOSYS;
}

void Tau::set_ID_effSF_TightRNN_NOSYS(float value) {
  this->m_ID_effSF_TightRNN_NOSYS = (float)value;
}

float Tau::ID_effSF_TightRNN_NOSYS() const {
  return this->m_ID_effSF_TightRNN_NOSYS;
}

void Tau::set_ID_effSF_TightRNN_noElVeto_NOSYS(float value) {
  this->m_ID_effSF_TightRNN_noElVeto_NOSYS = (float)value;
}

float Tau::ID_effSF_TightRNN_noElVeto_NOSYS() const {
  return this->m_ID_effSF_TightRNN_noElVeto_NOSYS;
}

void Tau::set_Reco_effSF_Baseline_NOSYS(float value) {
  this->m_Reco_effSF_Baseline_NOSYS = (float)value;
}

float Tau::Reco_effSF_Baseline_NOSYS() const {
  return this->m_Reco_effSF_Baseline_NOSYS;
}

void Tau::set_Reco_effSF_Baseline_noElVeto_NOSYS(float value) {
  this->m_Reco_effSF_Baseline_noElVeto_NOSYS = (float)value;
}

float Tau::Reco_effSF_Baseline_noElVeto_NOSYS() const {
  return this->m_Reco_effSF_Baseline_noElVeto_NOSYS;
}

void Tau::set_Reco_effSF_LooseRNN_NOSYS(float value) {
  this->m_Reco_effSF_LooseRNN_NOSYS = (float)value;
}

float Tau::Reco_effSF_LooseRNN_NOSYS() const {
  return this->m_Reco_effSF_LooseRNN_NOSYS;
}

void Tau::set_Reco_effSF_LooseRNN_noElVeto_NOSYS(float value) {
  this->m_Reco_effSF_LooseRNN_noElVeto_NOSYS = (float)value;
}

float Tau::Reco_effSF_LooseRNN_noElVeto_NOSYS() const {
  return this->m_Reco_effSF_LooseRNN_noElVeto_NOSYS;
}

void Tau::set_Reco_effSF_MediumRNN_NOSYS(float value) {
  this->m_Reco_effSF_MediumRNN_NOSYS = (float)value;
}

float Tau::Reco_effSF_MediumRNN_NOSYS() const {
  return this->m_Reco_effSF_MediumRNN_NOSYS;
}

void Tau::set_Reco_effSF_MediumRNN_noElVeto_NOSYS(float value) {
  this->m_Reco_effSF_MediumRNN_noElVeto_NOSYS = (float)value;
}

float Tau::Reco_effSF_MediumRNN_noElVeto_NOSYS() const {
  return this->m_Reco_effSF_MediumRNN_noElVeto_NOSYS;
}

void Tau::set_Reco_effSF_TightRNN_NOSYS(float value) {
  this->m_Reco_effSF_TightRNN_NOSYS = (float)value;
}

float Tau::Reco_effSF_TightRNN_NOSYS() const {
  return this->m_Reco_effSF_TightRNN_NOSYS;
}

void Tau::set_Reco_effSF_TightRNN_noElVeto_NOSYS(float value) {
  this->m_Reco_effSF_TightRNN_noElVeto_NOSYS = (float)value;
}

float Tau::Reco_effSF_TightRNN_noElVeto_NOSYS() const {
  return this->m_Reco_effSF_TightRNN_noElVeto_NOSYS;
}

void Tau::set_Reco_effSF_VeryLooseRNN_NOSYS(float value) {
  this->m_Reco_effSF_VeryLooseRNN_NOSYS = (float)value;
}

float Tau::Reco_effSF_VeryLooseRNN_NOSYS() const {
  return this->m_Reco_effSF_VeryLooseRNN_NOSYS;
}

void Tau::set_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS(float value) {
  this->m_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS = (float)value;
}

float Tau::Reco_effSF_VeryLooseRNN_noElVeto_NOSYS() const {
  return this->m_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS;
}

void Tau::set_select_Baseline_NOSYS(char value) {
  this->m_select_Baseline_NOSYS = (bool)value;
}

bool Tau::select_Baseline_NOSYS() const {
  return this->m_select_Baseline_NOSYS;
}

void Tau::set_select_Baseline_noElVeto_NOSYS(char value) {
  this->m_select_Baseline_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_Baseline_noElVeto_NOSYS() const {
  return this->m_select_Baseline_noElVeto_NOSYS;
}

void Tau::set_select_LooseGNTau_NOSYS(char value) {
  this->m_select_LooseGNTau_NOSYS = (bool)value;
}

bool Tau::select_LooseGNTau_NOSYS() const {
  return this->m_select_LooseGNTau_NOSYS;
}

void Tau::set_select_LooseGNTau_noElVeto_NOSYS(char value) {
  this->m_select_LooseGNTau_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_LooseGNTau_noElVeto_NOSYS() const {
  return this->m_select_LooseGNTau_noElVeto_NOSYS;
}

void Tau::set_select_LooseRNN_NOSYS(char value) {
  this->m_select_LooseRNN_NOSYS = (bool)value;
}

bool Tau::select_LooseRNN_NOSYS() const {
  return this->m_select_LooseRNN_NOSYS;
}

void Tau::set_select_LooseRNN_noElVeto_NOSYS(char value) {
  this->m_select_LooseRNN_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_LooseRNN_noElVeto_NOSYS() const {
  return this->m_select_LooseRNN_noElVeto_NOSYS;
}

void Tau::set_select_MediumGNTau_NOSYS(char value) {
  this->m_select_MediumGNTau_NOSYS = (bool)value;
}

bool Tau::select_MediumGNTau_NOSYS() const {
  return this->m_select_MediumGNTau_NOSYS;
}

void Tau::set_select_MediumGNTau_noElVeto_NOSYS(char value) {
  this->m_select_MediumGNTau_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_MediumGNTau_noElVeto_NOSYS() const {
  return this->m_select_MediumGNTau_noElVeto_NOSYS;
}

void Tau::set_select_MediumRNN_NOSYS(char value) {
  this->m_select_MediumRNN_NOSYS = (bool)value;
}

bool Tau::select_MediumRNN_NOSYS() const {
  return this->m_select_MediumRNN_NOSYS;
}

void Tau::set_select_MediumRNN_noElVeto_NOSYS(char value) {
  this->m_select_MediumRNN_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_MediumRNN_noElVeto_NOSYS() const {
  return this->m_select_MediumRNN_noElVeto_NOSYS;
}

void Tau::set_select_TightGNTau_NOSYS(char value) {
  this->m_select_TightGNTau_NOSYS = (bool)value;
}

bool Tau::select_TightGNTau_NOSYS() const {
  return this->m_select_TightGNTau_NOSYS;
}

void Tau::set_select_TightGNTau_noElVeto_NOSYS(char value) {
  this->m_select_TightGNTau_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_TightGNTau_noElVeto_NOSYS() const {
  return this->m_select_TightGNTau_noElVeto_NOSYS;
}

void Tau::set_select_TightRNN_NOSYS(char value) {
  this->m_select_TightRNN_NOSYS = (bool)value;
}

bool Tau::select_TightRNN_NOSYS() const {
  return this->m_select_TightRNN_NOSYS;
}

void Tau::set_select_TightRNN_noElVeto_NOSYS(char value) {
  this->m_select_TightRNN_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_TightRNN_noElVeto_NOSYS() const {
  return this->m_select_TightRNN_noElVeto_NOSYS;
}

void Tau::set_select_VeryLooseGNTau_NOSYS(char value) {
  this->m_select_VeryLooseGNTau_NOSYS = (bool)value;
}

bool Tau::select_VeryLooseGNTau_NOSYS() const {
  return this->m_select_VeryLooseGNTau_NOSYS;
}

void Tau::set_select_VeryLooseGNTau_noElVeto_NOSYS(char value) {
  this->m_select_VeryLooseGNTau_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_VeryLooseGNTau_noElVeto_NOSYS() const {
  return this->m_select_VeryLooseGNTau_noElVeto_NOSYS;
}

void Tau::set_select_VeryLooseRNN_NOSYS(char value) {
  this->m_select_VeryLooseRNN_NOSYS = (bool)value;
}

bool Tau::select_VeryLooseRNN_NOSYS() const {
  return this->m_select_VeryLooseRNN_NOSYS;
}

void Tau::set_select_VeryLooseRNN_noElVeto_NOSYS(char value) {
  this->m_select_VeryLooseRNN_noElVeto_NOSYS = (bool)value;
}

bool Tau::select_VeryLooseRNN_noElVeto_NOSYS() const {
  return this->m_select_VeryLooseRNN_noElVeto_NOSYS;
}

void Tau::set_select_wpSet0_NOSYS(char value) {
  this->m_select_wpSet0_NOSYS = (bool)value;
}

bool Tau::select_wpSet0_NOSYS() const {
  return this->m_select_wpSet0_NOSYS;
}

void Tau::set_select_wpSet1_NOSYS(char value) {
  this->m_select_wpSet1_NOSYS = (bool)value;
}

bool Tau::select_wpSet1_NOSYS() const {
  return this->m_select_wpSet1_NOSYS;
}

void Tau::set_select_wpSet2_NOSYS(char value) {
  this->m_select_wpSet2_NOSYS = (bool)value;
}

bool Tau::select_wpSet2_NOSYS() const {
  return this->m_select_wpSet2_NOSYS;
}

void Tau::set_select_wpSet3_NOSYS(char value) {
  this->m_select_wpSet3_NOSYS = (bool)value;
}

bool Tau::select_wpSet3_NOSYS() const {
  return this->m_select_wpSet3_NOSYS;
}
