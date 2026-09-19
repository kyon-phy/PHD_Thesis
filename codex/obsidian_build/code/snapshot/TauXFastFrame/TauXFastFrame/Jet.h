// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#pragma once
#include "Math/Vector4D.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {
class Jet : public Particle {
 public:
  Jet(){};
  Jet(const ROOT::Math::PtEtaPhiEVector &p4);
  void set_GN2v01_Continuous_quantile(int value);
  int GN2v01_Continuous_quantile() const;

  void set_GN2v01_FixedCutBEff_65_select(char value);
  bool GN2v01_FixedCutBEff_65_select() const;

  void set_GN2v01_FixedCutBEff_70_select(char value);
  bool GN2v01_FixedCutBEff_70_select() const;

  void set_GN2v01_FixedCutBEff_77_select(char value);
  bool GN2v01_FixedCutBEff_77_select() const;

  void set_GN2v01_FixedCutBEff_85_select(char value);
  bool GN2v01_FixedCutBEff_85_select() const;

  void set_HadronConeExclExtendedTruthLabelID(int value);
  int HadronConeExclExtendedTruthLabelID() const;

  void set_HadronConeExclTruthLabelID(int value);
  int HadronConeExclTruthLabelID() const;

  void set_PartonTruthLabelID(int value);
  int PartonTruthLabelID() const;

  void set_jvtEfficiency_NOSYS(float value);
  float jvtEfficiency_NOSYS() const;

  void set_select_GN2v01_FixedCutBEff_65_NOSYS(char value);
  bool select_GN2v01_FixedCutBEff_65_NOSYS() const;

  void set_select_GN2v01_FixedCutBEff_70_NOSYS(char value);
  bool select_GN2v01_FixedCutBEff_70_NOSYS() const;

  void set_select_GN2v01_FixedCutBEff_77_NOSYS(char value);
  bool select_GN2v01_FixedCutBEff_77_NOSYS() const;

  void set_select_GN2v01_FixedCutBEff_85_NOSYS(char value);
  bool select_GN2v01_FixedCutBEff_85_NOSYS() const;

  void set_select_baselineFJvt_NOSYS(char value);
  bool select_baselineFJvt_NOSYS() const;

  void set_select_baselineJvt_NOSYS(char value);
  bool select_baselineJvt_NOSYS() const;

  void set_select_wpSet0_NOSYS(char value);
  bool select_wpSet0_NOSYS() const;

  void set_select_wpSet1_NOSYS(char value);
  bool select_wpSet1_NOSYS() const;

  void set_select_wpSet2_NOSYS(char value);
  bool select_wpSet2_NOSYS() const;

  void set_select_wpSet3_NOSYS(char value);
  bool select_wpSet3_NOSYS() const;

 private:
  int m_GN2v01_Continuous_quantile = -9999;
  bool m_GN2v01_FixedCutBEff_65_select = false;
  bool m_GN2v01_FixedCutBEff_70_select = false;
  bool m_GN2v01_FixedCutBEff_77_select = false;
  bool m_GN2v01_FixedCutBEff_85_select = false;
  int m_HadronConeExclExtendedTruthLabelID = -9999;
  int m_HadronConeExclTruthLabelID = -9999;
  int m_PartonTruthLabelID = -9999;
  float m_jvtEfficiency_NOSYS = -9999;
  bool m_select_GN2v01_FixedCutBEff_65_NOSYS = false;
  bool m_select_GN2v01_FixedCutBEff_70_NOSYS = false;
  bool m_select_GN2v01_FixedCutBEff_77_NOSYS = false;
  bool m_select_GN2v01_FixedCutBEff_85_NOSYS = false;
  bool m_select_baselineFJvt_NOSYS = false;
  bool m_select_baselineJvt_NOSYS = false;
  bool m_select_wpSet0_NOSYS = false;
  bool m_select_wpSet1_NOSYS = false;
  bool m_select_wpSet2_NOSYS = false;
  bool m_select_wpSet3_NOSYS = false;
};  // Jet
}  // namespace TauXParticles