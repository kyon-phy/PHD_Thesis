// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#include "../TauXFastFrame/Electron.h"

#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"

using TauXParticles::Electron;

Electron::Electron(const ROOT::Math::PtEtaPhiEVector &p4) : Particle(p4){};

void Electron::set_AmbiguityType(unsigned char value) {
  this->m_AmbiguityType = (unsigned char)value;
}

unsigned char Electron::AmbiguityType() const {
  return this->m_AmbiguityType;
}

void Electron::set_DFCommonAddAmbiguity(int value) {
  this->m_DFCommonAddAmbiguity = (int)value;
}

int Electron::DFCommonAddAmbiguity() const {
  return this->m_DFCommonAddAmbiguity;
}

void Electron::set_FirstEgMotherPdgId(int value) {
  this->m_FirstEgMotherPdgId = (int)value;
}

int Electron::FirstEgMotherPdgId() const {
  return this->m_FirstEgMotherPdgId;
}

void Electron::set_FirstEgMotherTruthOrigin(int value) {
  this->m_FirstEgMotherTruthOrigin = (int)value;
}

int Electron::FirstEgMotherTruthOrigin() const {
  return this->m_FirstEgMotherTruthOrigin;
}

void Electron::set_FirstEgMotherTruthType(int value) {
  this->m_FirstEgMotherTruthType = (int)value;
}

int Electron::FirstEgMotherTruthType() const {
  return this->m_FirstEgMotherTruthType;
}

void Electron::set_IFFtype(int value) {
  this->m_IFFtype = (int)value;
}

int Electron::IFFtype() const {
  return this->m_IFFtype;
}

void Electron::set_NinnPixHits(int value) {
  this->m_NinnPixHits = (int)value;
}

int Electron::NinnPixHits() const {
  return this->m_NinnPixHits;
}

void Electron::set_NtrackParticles(int value) {
  this->m_NtrackParticles = (int)value;
}

int Electron::NtrackParticles() const {
  return this->m_NtrackParticles;
}

void Electron::set_charge(float value) {
  this->m_charge = (float)value;
}

float Electron::charge() const {
  return this->m_charge;
}

void Electron::set_d0(float value) {
  this->m_d0 = (float)value;
}

float Electron::d0() const {
  return this->m_d0;
}

void Electron::set_d0sig(float value) {
  this->m_d0sig = (float)value;
}

float Electron::d0sig() const {
  return this->m_d0sig;
}

void Electron::set_deltaz0(float value) {
  this->m_deltaz0 = (float)value;
}

float Electron::deltaz0() const {
  return this->m_deltaz0;
}

void Electron::set_deltaz0sinTheta(float value) {
  this->m_deltaz0sinTheta = (float)value;
}

float Electron::deltaz0sinTheta() const {
  return this->m_deltaz0sinTheta;
}

void Electron::set_vz(float value) {
  this->m_vz = (float)value;
}

float Electron::vz() const {
  return this->m_vz;
}

void Electron::set_z0(float value) {
  this->m_z0 = (float)value;
}

float Electron::z0() const {
  return this->m_z0;
}

// (Jiaqi hack) el SFs
void Electron::set_id_effSF_TightLH_HighPtCaloOnly_NOSYS(float value) {
  this->m_id_effSF_TightLH_HighPtCaloOnly_NOSYS = (float)value;
}

float Electron::id_effSF_TightLH_HighPtCaloOnly_NOSYS() const {
  return this->m_id_effSF_TightLH_HighPtCaloOnly_NOSYS;
}

void Electron::set_isol_effSF_TightLH_HighPtCaloOnly_NOSYS(float value) {
  this->m_isol_effSF_TightLH_HighPtCaloOnly_NOSYS = (float)value;
}

float Electron::isol_effSF_TightLH_HighPtCaloOnly_NOSYS() const {
  return this->m_isol_effSF_TightLH_HighPtCaloOnly_NOSYS;
}

void Electron::set_reco_effSF_TightLH_HighPtCaloOnly_NOSYS(float value) {
  this->m_reco_effSF_TightLH_HighPtCaloOnly_NOSYS = (float)value;
}

float Electron::reco_effSF_TightLH_HighPtCaloOnly_NOSYS() const {
  return this->m_reco_effSF_TightLH_HighPtCaloOnly_NOSYS;
}
// (Jiaqi hack) el SFs

void Electron::set_select_LooseBLayerLH_NonIso_NOSYS(char value) {
  this->m_select_LooseBLayerLH_NonIso_NOSYS = (bool)value;
}

bool Electron::select_LooseBLayerLH_NonIso_NOSYS() const {
  return this->m_select_LooseBLayerLH_NonIso_NOSYS;
}

void Electron::set_select_LooseDNN_NonIso_NOSYS(char value) {
  this->m_select_LooseDNN_NonIso_NOSYS = (bool)value;
}

bool Electron::select_LooseDNN_NonIso_NOSYS() const {
  return this->m_select_LooseDNN_NonIso_NOSYS;
}

void Electron::set_select_MediumDNN_NonIso_NOSYS(char value) {
  this->m_select_MediumDNN_NonIso_NOSYS = (bool)value;
}

bool Electron::select_MediumDNN_NonIso_NOSYS() const {
  return this->m_select_MediumDNN_NonIso_NOSYS;
}

void Electron::set_select_TightDNN_NonIso_NOSYS(char value) {
  this->m_select_TightDNN_NonIso_NOSYS = (bool)value;
}

bool Electron::select_TightDNN_NonIso_NOSYS() const {
  return this->m_select_TightDNN_NonIso_NOSYS;
}

void Electron::set_select_TightLH_HighPtCaloOnly_NOSYS(char value) {
  this->m_select_TightLH_HighPtCaloOnly_NOSYS = (bool)value;
}

bool Electron::select_TightLH_HighPtCaloOnly_NOSYS() const {
  return this->m_select_TightLH_HighPtCaloOnly_NOSYS;
}

void Electron::set_select_TightLH_Loose_VarRad_NOSYS(char value) {
  this->m_select_TightLH_Loose_VarRad_NOSYS = (bool)value;
}

bool Electron::select_TightLH_Loose_VarRad_NOSYS() const {
  return this->m_select_TightLH_Loose_VarRad_NOSYS;
}

void Electron::set_select_TightLH_TightTrackOnly_FixedRad_NOSYS(char value) {
  this->m_select_TightLH_TightTrackOnly_FixedRad_NOSYS = (bool)value;
}

bool Electron::select_TightLH_TightTrackOnly_FixedRad_NOSYS() const {
  return this->m_select_TightLH_TightTrackOnly_FixedRad_NOSYS;
}

void Electron::set_select_TightLH_TightTrackOnly_VarRad_NOSYS(char value) {
  this->m_select_TightLH_TightTrackOnly_VarRad_NOSYS = (bool)value;
}

bool Electron::select_TightLH_TightTrackOnly_VarRad_NOSYS() const {
  return this->m_select_TightLH_TightTrackOnly_VarRad_NOSYS;
}

void Electron::set_select_TightLH_Tight_VarRad_NOSYS(char value) {
  this->m_select_TightLH_Tight_VarRad_NOSYS = (bool)value;
}

bool Electron::select_TightLH_Tight_VarRad_NOSYS() const {
  return this->m_select_TightLH_Tight_VarRad_NOSYS;
}

void Electron::set_select_wpSet0_NOSYS(char value) {
  this->m_select_wpSet0_NOSYS = (bool)value;
}

bool Electron::select_wpSet0_NOSYS() const {
  return this->m_select_wpSet0_NOSYS;
}

void Electron::set_select_wpSet1_NOSYS(char value) {
  this->m_select_wpSet1_NOSYS = (bool)value;
}

bool Electron::select_wpSet1_NOSYS() const {
  return this->m_select_wpSet1_NOSYS;
}

void Electron::set_select_wpSet2_NOSYS(char value) {
  this->m_select_wpSet2_NOSYS = (bool)value;
}

bool Electron::select_wpSet2_NOSYS() const {
  return this->m_select_wpSet2_NOSYS;
}

void Electron::set_select_wpSet3_NOSYS(char value) {
  this->m_select_wpSet3_NOSYS = (bool)value;
}

bool Electron::select_wpSet3_NOSYS() const {
  return this->m_select_wpSet3_NOSYS;
}
