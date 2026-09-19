// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#include "../TauXFastFrame/Jet.h"

#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"

using TauXParticles::Jet;

Jet::Jet(const ROOT::Math::PtEtaPhiEVector &p4) : Particle(p4){};

void Jet::set_GN2v01_Continuous_quantile(int value) {
  this->m_GN2v01_Continuous_quantile = (int)value;
}

int Jet::GN2v01_Continuous_quantile() const {
  return this->m_GN2v01_Continuous_quantile;
}

void Jet::set_GN2v01_FixedCutBEff_65_select(char value) {
  this->m_GN2v01_FixedCutBEff_65_select = (bool)value;
}

bool Jet::GN2v01_FixedCutBEff_65_select() const {
  return this->m_GN2v01_FixedCutBEff_65_select;
}

void Jet::set_GN2v01_FixedCutBEff_70_select(char value) {
  this->m_GN2v01_FixedCutBEff_70_select = (bool)value;
}

bool Jet::GN2v01_FixedCutBEff_70_select() const {
  return this->m_GN2v01_FixedCutBEff_70_select;
}

void Jet::set_GN2v01_FixedCutBEff_77_select(char value) {
  this->m_GN2v01_FixedCutBEff_77_select = (bool)value;
}

bool Jet::GN2v01_FixedCutBEff_77_select() const {
  return this->m_GN2v01_FixedCutBEff_77_select;
}

void Jet::set_GN2v01_FixedCutBEff_85_select(char value) {
  this->m_GN2v01_FixedCutBEff_85_select = (bool)value;
}

bool Jet::GN2v01_FixedCutBEff_85_select() const {
  return this->m_GN2v01_FixedCutBEff_85_select;
}

void Jet::set_HadronConeExclExtendedTruthLabelID(int value) {
  this->m_HadronConeExclExtendedTruthLabelID = (int)value;
}

int Jet::HadronConeExclExtendedTruthLabelID() const {
  return this->m_HadronConeExclExtendedTruthLabelID;
}

void Jet::set_HadronConeExclTruthLabelID(int value) {
  this->m_HadronConeExclTruthLabelID = (int)value;
}

int Jet::HadronConeExclTruthLabelID() const {
  return this->m_HadronConeExclTruthLabelID;
}

void Jet::set_PartonTruthLabelID(int value) {
  this->m_PartonTruthLabelID = (int)value;
}

int Jet::PartonTruthLabelID() const {
  return this->m_PartonTruthLabelID;
}

void Jet::set_jvtEfficiency_NOSYS(float value) {
  this->m_jvtEfficiency_NOSYS = (float)value;
}

float Jet::jvtEfficiency_NOSYS() const {
  return this->m_jvtEfficiency_NOSYS;
}

void Jet::set_select_GN2v01_FixedCutBEff_65_NOSYS(char value) {
  this->m_select_GN2v01_FixedCutBEff_65_NOSYS = (bool)value;
}

bool Jet::select_GN2v01_FixedCutBEff_65_NOSYS() const {
  return this->m_select_GN2v01_FixedCutBEff_65_NOSYS;
}

void Jet::set_select_GN2v01_FixedCutBEff_70_NOSYS(char value) {
  this->m_select_GN2v01_FixedCutBEff_70_NOSYS = (bool)value;
}

bool Jet::select_GN2v01_FixedCutBEff_70_NOSYS() const {
  return this->m_select_GN2v01_FixedCutBEff_70_NOSYS;
}

void Jet::set_select_GN2v01_FixedCutBEff_77_NOSYS(char value) {
  this->m_select_GN2v01_FixedCutBEff_77_NOSYS = (bool)value;
}

bool Jet::select_GN2v01_FixedCutBEff_77_NOSYS() const {
  return this->m_select_GN2v01_FixedCutBEff_77_NOSYS;
}

void Jet::set_select_GN2v01_FixedCutBEff_85_NOSYS(char value) {
  this->m_select_GN2v01_FixedCutBEff_85_NOSYS = (bool)value;
}

bool Jet::select_GN2v01_FixedCutBEff_85_NOSYS() const {
  return this->m_select_GN2v01_FixedCutBEff_85_NOSYS;
}

void Jet::set_select_baselineFJvt_NOSYS(char value) {
  this->m_select_baselineFJvt_NOSYS = (bool)value;
}

bool Jet::select_baselineFJvt_NOSYS() const {
  return this->m_select_baselineFJvt_NOSYS;
}

void Jet::set_select_baselineJvt_NOSYS(char value) {
  this->m_select_baselineJvt_NOSYS = (bool)value;
}

bool Jet::select_baselineJvt_NOSYS() const {
  return this->m_select_baselineJvt_NOSYS;
}

void Jet::set_select_wpSet0_NOSYS(char value) {
  this->m_select_wpSet0_NOSYS = (bool)value;
}

bool Jet::select_wpSet0_NOSYS() const {
  return this->m_select_wpSet0_NOSYS;
}

void Jet::set_select_wpSet1_NOSYS(char value) {
  this->m_select_wpSet1_NOSYS = (bool)value;
}

bool Jet::select_wpSet1_NOSYS() const {
  return this->m_select_wpSet1_NOSYS;
}

void Jet::set_select_wpSet2_NOSYS(char value) {
  this->m_select_wpSet2_NOSYS = (bool)value;
}

bool Jet::select_wpSet2_NOSYS() const {
  return this->m_select_wpSet2_NOSYS;
}

void Jet::set_select_wpSet3_NOSYS(char value) {
  this->m_select_wpSet3_NOSYS = (bool)value;
}

bool Jet::select_wpSet3_NOSYS() const {
  return this->m_select_wpSet3_NOSYS;
}
