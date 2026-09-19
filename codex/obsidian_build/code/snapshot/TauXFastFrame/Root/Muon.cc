// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#include "../TauXFastFrame/Muon.h"

#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"

using TauXParticles::Muon;

Muon::Muon(const ROOT::Math::PtEtaPhiEVector &p4) : Particle(p4){};

void Muon::set_IFFtype(int value) {
  this->m_IFFtype = (int)value;
}

int Muon::IFFtype() const {
  return this->m_IFFtype;
}

void Muon::set_NinnPixHits(int value) {
  this->m_NinnPixHits = (int)value;
}

int Muon::NinnPixHits() const {
  return this->m_NinnPixHits;
}

void Muon::set_charge(float value) {
  this->m_charge = (float)value;
}

float Muon::charge() const {
  return this->m_charge;
}

void Muon::set_d0(float value) {
  this->m_d0 = (float)value;
}

float Muon::d0() const {
  return this->m_d0;
}

void Muon::set_d0sig(float value) {
  this->m_d0sig = (float)value;
}

float Muon::d0sig() const {
  return this->m_d0sig;
}

void Muon::set_deltaz0(float value) {
  this->m_deltaz0 = (float)value;
}

float Muon::deltaz0() const {
  return this->m_deltaz0;
}

void Muon::set_deltaz0sinTheta(float value) {
  this->m_deltaz0sinTheta = (float)value;
}

float Muon::deltaz0sinTheta() const {
  return this->m_deltaz0sinTheta;
}

void Muon::set_vz(float value) {
  this->m_vz = (float)value;
}

float Muon::vz() const {
  return this->m_vz;
}

void Muon::set_z0(float value) {
  this->m_z0 = (float)value;
}

float Muon::z0() const {
  return this->m_z0;
}

void Muon::set_BadMuonVeto_effSF_HighPt_NonIso_NOSYS(float value) {
  this->m_BadMuonVeto_effSF_HighPt_NonIso_NOSYS = (float)value;
}

float Muon::BadMuonVeto_effSF_HighPt_NonIso_NOSYS() const {
  return this->m_BadMuonVeto_effSF_HighPt_NonIso_NOSYS;
}

void Muon::set_TTVA_effSF_HighPt_NonIso_NOSYS(float value) {
  this->m_TTVA_effSF_HighPt_NonIso_NOSYS = (float)value;
}

float Muon::TTVA_effSF_HighPt_NonIso_NOSYS() const {
  return this->m_TTVA_effSF_HighPt_NonIso_NOSYS;
}

void Muon::set_TTVA_effSF_Loose_Loose_VarRad_NOSYS(float value) {
  this->m_TTVA_effSF_Loose_Loose_VarRad_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Loose_Loose_VarRad_NOSYS() const {
  return this->m_TTVA_effSF_Loose_Loose_VarRad_NOSYS;
}

void Muon::set_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS(float value) {
  this->m_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS() const {
  return this->m_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS;
}

void Muon::set_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS(float value) {
  this->m_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Loose_PflowTight_VarRad_NOSYS() const {
  return this->m_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS;
}

void Muon::set_TTVA_effSF_Loose_Tight_VarRad_NOSYS(float value) {
  this->m_TTVA_effSF_Loose_Tight_VarRad_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Loose_Tight_VarRad_NOSYS() const {
  return this->m_TTVA_effSF_Loose_Tight_VarRad_NOSYS;
}

void Muon::set_TTVA_effSF_Medium_Tight_VarRad_NOSYS(float value) {
  this->m_TTVA_effSF_Medium_Tight_VarRad_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Medium_Tight_VarRad_NOSYS() const {
  return this->m_TTVA_effSF_Medium_Tight_VarRad_NOSYS;
}

void Muon::set_TTVA_effSF_Medium_NonIso_NOSYS(float value) {
  this->m_TTVA_effSF_Medium_NonIso_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Medium_NonIso_NOSYS() const {
  return this->m_TTVA_effSF_Medium_NonIso_NOSYS;
}

void Muon::set_TTVA_effSF_Tight_NonIso_NOSYS(float value) {
  this->m_TTVA_effSF_Tight_NonIso_NOSYS = (float)value;
}

float Muon::TTVA_effSF_Tight_NonIso_NOSYS() const {
  return this->m_TTVA_effSF_Tight_NonIso_NOSYS;
}

void Muon::set_isol_effSF_Loose_Loose_VarRad_NOSYS(float value) {
  this->m_isol_effSF_Loose_Loose_VarRad_NOSYS = (float)value;
}

float Muon::isol_effSF_Loose_Loose_VarRad_NOSYS() const {
  return this->m_isol_effSF_Loose_Loose_VarRad_NOSYS;
}

void Muon::set_isol_effSF_Loose_PflowLoose_VarRad_NOSYS(float value) {
  this->m_isol_effSF_Loose_PflowLoose_VarRad_NOSYS = (float)value;
}

float Muon::isol_effSF_Loose_PflowLoose_VarRad_NOSYS() const {
  return this->m_isol_effSF_Loose_PflowLoose_VarRad_NOSYS;
}

void Muon::set_isol_effSF_Loose_PflowTight_VarRad_NOSYS(float value) {
  this->m_isol_effSF_Loose_PflowTight_VarRad_NOSYS = (float)value;
}

float Muon::isol_effSF_Loose_PflowTight_VarRad_NOSYS() const {
  return this->m_isol_effSF_Loose_PflowTight_VarRad_NOSYS;
}

void Muon::set_isol_effSF_Loose_Tight_VarRad_NOSYS(float value) {
  this->m_isol_effSF_Loose_Tight_VarRad_NOSYS = (float)value;
}

float Muon::isol_effSF_Loose_Tight_VarRad_NOSYS() const {
  return this->m_isol_effSF_Loose_Tight_VarRad_NOSYS;
}

void Muon::set_isol_effSF_Medium_Tight_VarRad_NOSYS(float value) {
  this->m_isol_effSF_Medium_Tight_VarRad_NOSYS = (float)value;
}

float Muon::isol_effSF_Medium_Tight_VarRad_NOSYS() const {
  return this->m_isol_effSF_Medium_Tight_VarRad_NOSYS;
}

void Muon::set_reco_effSF_HighPt_NonIso_NOSYS(float value) {
  this->m_reco_effSF_HighPt_NonIso_NOSYS = (float)value;
}

float Muon::reco_effSF_HighPt_NonIso_NOSYS() const {
  return this->m_reco_effSF_HighPt_NonIso_NOSYS;
}

void Muon::set_reco_effSF_Loose_Loose_VarRad_NOSYS(float value) {
  this->m_reco_effSF_Loose_Loose_VarRad_NOSYS = (float)value;
}

float Muon::reco_effSF_Loose_Loose_VarRad_NOSYS() const {
  return this->m_reco_effSF_Loose_Loose_VarRad_NOSYS;
}

void Muon::set_reco_effSF_Loose_PflowLoose_VarRad_NOSYS(float value) {
  this->m_reco_effSF_Loose_PflowLoose_VarRad_NOSYS = (float)value;
}

float Muon::reco_effSF_Loose_PflowLoose_VarRad_NOSYS() const {
  return this->m_reco_effSF_Loose_PflowLoose_VarRad_NOSYS;
}

void Muon::set_reco_effSF_Loose_PflowTight_VarRad_NOSYS(float value) {
  this->m_reco_effSF_Loose_PflowTight_VarRad_NOSYS = (float)value;
}

float Muon::reco_effSF_Loose_PflowTight_VarRad_NOSYS() const {
  return this->m_reco_effSF_Loose_PflowTight_VarRad_NOSYS;
}

void Muon::set_reco_effSF_Loose_Tight_VarRad_NOSYS(float value) {
  this->m_reco_effSF_Loose_Tight_VarRad_NOSYS = (float)value;
}

float Muon::reco_effSF_Loose_Tight_VarRad_NOSYS() const {
  return this->m_reco_effSF_Loose_Tight_VarRad_NOSYS;
}

void Muon::set_reco_effSF_Medium_Tight_VarRad_NOSYS(float value) {
  this->m_reco_effSF_Medium_Tight_VarRad_NOSYS = (float)value;
}

float Muon::reco_effSF_Medium_Tight_VarRad_NOSYS() const {
  return this->m_reco_effSF_Medium_Tight_VarRad_NOSYS;
}

void Muon::set_reco_effSF_Medium_NonIso_NOSYS(float value) {
  this->m_reco_effSF_Medium_NonIso_NOSYS = (float)value;
}

float Muon::reco_effSF_Medium_NonIso_NOSYS() const {
  return this->m_reco_effSF_Medium_NonIso_NOSYS;
}

void Muon::set_reco_effSF_Tight_NonIso_NOSYS(float value) {
  this->m_reco_effSF_Tight_NonIso_NOSYS = (float)value;
}

float Muon::reco_effSF_Tight_NonIso_NOSYS() const {
  return this->m_reco_effSF_Tight_NonIso_NOSYS;
}

void Muon::set_select_HighPt_NonIso_NOSYS(char value) {
  this->m_select_HighPt_NonIso_NOSYS = (bool)value;
}

bool Muon::select_HighPt_NonIso_NOSYS() const {
  return this->m_select_HighPt_NonIso_NOSYS;
}

void Muon::set_select_Loose_Loose_VarRad_NOSYS(char value) {
  this->m_select_Loose_Loose_VarRad_NOSYS = (bool)value;
}

bool Muon::select_Loose_Loose_VarRad_NOSYS() const {
  return this->m_select_Loose_Loose_VarRad_NOSYS;
}

void Muon::set_select_Loose_PflowLoose_VarRad_NOSYS(char value) {
  this->m_select_Loose_PflowLoose_VarRad_NOSYS = (bool)value;
}

bool Muon::select_Loose_PflowLoose_VarRad_NOSYS() const {
  return this->m_select_Loose_PflowLoose_VarRad_NOSYS;
}

void Muon::set_select_Loose_PflowTight_VarRad_NOSYS(char value) {
  this->m_select_Loose_PflowTight_VarRad_NOSYS = (bool)value;
}

bool Muon::select_Loose_PflowTight_VarRad_NOSYS() const {
  return this->m_select_Loose_PflowTight_VarRad_NOSYS;
}

void Muon::set_select_Loose_Tight_VarRad_NOSYS(char value) {
  this->m_select_Loose_Tight_VarRad_NOSYS = (bool)value;
}

bool Muon::select_Loose_Tight_VarRad_NOSYS() const {
  return this->m_select_Loose_Tight_VarRad_NOSYS;
}

void Muon::set_select_Medium_Tight_VarRad_NOSYS(char value) {
  this->m_select_Medium_Tight_VarRad_NOSYS = (bool)value;
}

bool Muon::select_Medium_Tight_VarRad_NOSYS() const {
  return this->m_select_Medium_Tight_VarRad_NOSYS;
}

void Muon::set_select_LowPtEfficiency_NonIso_NOSYS(char value) {
  this->m_select_LowPtEfficiency_NonIso_NOSYS = (bool)value;
}

bool Muon::select_LowPtEfficiency_NonIso_NOSYS() const {
  return this->m_select_LowPtEfficiency_NonIso_NOSYS;
}

void Muon::set_select_Medium_NonIso_NOSYS(char value) {
  this->m_select_Medium_NonIso_NOSYS = (bool)value;
}

bool Muon::select_Medium_NonIso_NOSYS() const {
  return this->m_select_Medium_NonIso_NOSYS;
}

void Muon::set_select_Tight_NonIso_NOSYS(char value) {
  this->m_select_Tight_NonIso_NOSYS = (bool)value;
}

bool Muon::select_Tight_NonIso_NOSYS() const {
  return this->m_select_Tight_NonIso_NOSYS;
}

void Muon::set_select_wpSet0_NOSYS(char value) {
  this->m_select_wpSet0_NOSYS = (bool)value;
}

bool Muon::select_wpSet0_NOSYS() const {
  return this->m_select_wpSet0_NOSYS;
}

void Muon::set_select_wpSet1_NOSYS(char value) {
  this->m_select_wpSet1_NOSYS = (bool)value;
}

bool Muon::select_wpSet1_NOSYS() const {
  return this->m_select_wpSet1_NOSYS;
}

void Muon::set_select_wpSet2_NOSYS(char value) {
  this->m_select_wpSet2_NOSYS = (bool)value;
}

bool Muon::select_wpSet2_NOSYS() const {
  return this->m_select_wpSet2_NOSYS;
}

void Muon::set_select_wpSet3_NOSYS(char value) {
  this->m_select_wpSet3_NOSYS = (bool)value;
}

bool Muon::select_wpSet3_NOSYS() const {
  return this->m_select_wpSet3_NOSYS;
}
