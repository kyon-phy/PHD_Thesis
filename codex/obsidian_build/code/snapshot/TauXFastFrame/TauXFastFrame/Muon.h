// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#pragma once
#include "Math/Vector4D.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {
class Muon : public Particle {
 public:
  Muon(){};
  Muon(const ROOT::Math::PtEtaPhiEVector &p4);
  void set_IFFtype(int value);
  int IFFtype() const;

  void set_NinnPixHits(int value);
  int NinnPixHits() const;

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

  void set_vz(float value);
  float vz() const;

  void set_z0(float value);
  float z0() const;

  void set_BadMuonVeto_effSF_HighPt_NonIso_NOSYS(float value);
  float BadMuonVeto_effSF_HighPt_NonIso_NOSYS() const;

  void set_TTVA_effSF_HighPt_NonIso_NOSYS(float value);
  float TTVA_effSF_HighPt_NonIso_NOSYS() const;

  void set_TTVA_effSF_Loose_Loose_VarRad_NOSYS(float value);
  float TTVA_effSF_Loose_Loose_VarRad_NOSYS() const;

  void set_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS(float value);
  float TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS() const;

  void set_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS(float value);
  float TTVA_effSF_Loose_PflowTight_VarRad_NOSYS() const;

  void set_TTVA_effSF_Loose_Tight_VarRad_NOSYS(float value);
  float TTVA_effSF_Loose_Tight_VarRad_NOSYS() const;

  void set_TTVA_effSF_Medium_Tight_VarRad_NOSYS(float value);
  float TTVA_effSF_Medium_Tight_VarRad_NOSYS() const;

  void set_TTVA_effSF_Medium_NonIso_NOSYS(float value);
  float TTVA_effSF_Medium_NonIso_NOSYS() const;

  void set_TTVA_effSF_Tight_NonIso_NOSYS(float value);
  float TTVA_effSF_Tight_NonIso_NOSYS() const;

  void set_isol_effSF_Loose_Loose_VarRad_NOSYS(float value);
  float isol_effSF_Loose_Loose_VarRad_NOSYS() const;

  void set_isol_effSF_Loose_PflowLoose_VarRad_NOSYS(float value);
  float isol_effSF_Loose_PflowLoose_VarRad_NOSYS() const;

  void set_isol_effSF_Loose_PflowTight_VarRad_NOSYS(float value);
  float isol_effSF_Loose_PflowTight_VarRad_NOSYS() const;

  void set_isol_effSF_Loose_Tight_VarRad_NOSYS(float value);
  float isol_effSF_Loose_Tight_VarRad_NOSYS() const;

  void set_isol_effSF_Medium_Tight_VarRad_NOSYS(float value);
  float isol_effSF_Medium_Tight_VarRad_NOSYS() const;

  void set_reco_effSF_HighPt_NonIso_NOSYS(float value);
  float reco_effSF_HighPt_NonIso_NOSYS() const;

  void set_reco_effSF_Loose_Loose_VarRad_NOSYS(float value);
  float reco_effSF_Loose_Loose_VarRad_NOSYS() const;

  void set_reco_effSF_Loose_PflowLoose_VarRad_NOSYS(float value);
  float reco_effSF_Loose_PflowLoose_VarRad_NOSYS() const;

  void set_reco_effSF_Loose_PflowTight_VarRad_NOSYS(float value);
  float reco_effSF_Loose_PflowTight_VarRad_NOSYS() const;

  void set_reco_effSF_Loose_Tight_VarRad_NOSYS(float value);
  float reco_effSF_Loose_Tight_VarRad_NOSYS() const;

  void set_reco_effSF_Medium_Tight_VarRad_NOSYS(float value);
  float reco_effSF_Medium_Tight_VarRad_NOSYS() const;

  void set_reco_effSF_Medium_NonIso_NOSYS(float value);
  float reco_effSF_Medium_NonIso_NOSYS() const;

  void set_reco_effSF_Tight_NonIso_NOSYS(float value);
  float reco_effSF_Tight_NonIso_NOSYS() const;

  void set_select_HighPt_NonIso_NOSYS(char value);
  bool select_HighPt_NonIso_NOSYS() const;

  void set_select_Loose_Loose_VarRad_NOSYS(char value);
  bool select_Loose_Loose_VarRad_NOSYS() const;

  void set_select_Loose_PflowLoose_VarRad_NOSYS(char value);
  bool select_Loose_PflowLoose_VarRad_NOSYS() const;

  void set_select_Loose_PflowTight_VarRad_NOSYS(char value);
  bool select_Loose_PflowTight_VarRad_NOSYS() const;

  void set_select_Loose_Tight_VarRad_NOSYS(char value);
  bool select_Loose_Tight_VarRad_NOSYS() const;

  void set_select_Medium_Tight_VarRad_NOSYS(char value);
  bool select_Medium_Tight_VarRad_NOSYS() const;

  void set_select_LowPtEfficiency_NonIso_NOSYS(char value);
  bool select_LowPtEfficiency_NonIso_NOSYS() const;

  void set_select_Medium_NonIso_NOSYS(char value);
  bool select_Medium_NonIso_NOSYS() const;

  void set_select_Tight_NonIso_NOSYS(char value);
  bool select_Tight_NonIso_NOSYS() const;

  void set_select_wpSet0_NOSYS(char value);
  bool select_wpSet0_NOSYS() const;

  void set_select_wpSet1_NOSYS(char value);
  bool select_wpSet1_NOSYS() const;

  void set_select_wpSet2_NOSYS(char value);
  bool select_wpSet2_NOSYS() const;

  void set_select_wpSet3_NOSYS(char value);
  bool select_wpSet3_NOSYS() const;

 private:
  int m_IFFtype = -9999;
  int m_NinnPixHits = -9999;
  float m_charge = -9999;
  float m_d0 = -9999;
  float m_d0sig = -9999;
  float m_deltaz0 = -9999;
  float m_deltaz0sinTheta = -9999;
  float m_vz = -9999;
  float m_z0 = -9999;
  float m_BadMuonVeto_effSF_HighPt_NonIso_NOSYS = 1;
  float m_TTVA_effSF_HighPt_NonIso_NOSYS = 1;
  float m_TTVA_effSF_Loose_Loose_VarRad_NOSYS = 1;
  float m_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS = 1;
  float m_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS = 1;
  float m_TTVA_effSF_Loose_Tight_VarRad_NOSYS = 1;
  float m_TTVA_effSF_Medium_Tight_VarRad_NOSYS = 1;
  float m_TTVA_effSF_Medium_NonIso_NOSYS = 1;
  float m_TTVA_effSF_Tight_NonIso_NOSYS = 1;
  float m_isol_effSF_Loose_Loose_VarRad_NOSYS = 1;
  float m_isol_effSF_Loose_PflowLoose_VarRad_NOSYS = 1;
  float m_isol_effSF_Loose_PflowTight_VarRad_NOSYS = 1;
  float m_isol_effSF_Loose_Tight_VarRad_NOSYS = 1;
  float m_isol_effSF_Medium_Tight_VarRad_NOSYS = 1;
  float m_reco_effSF_HighPt_NonIso_NOSYS = 1;
  float m_reco_effSF_Loose_Loose_VarRad_NOSYS = 1;
  float m_reco_effSF_Loose_PflowLoose_VarRad_NOSYS = 1;
  float m_reco_effSF_Loose_PflowTight_VarRad_NOSYS = 1;
  float m_reco_effSF_Loose_Tight_VarRad_NOSYS = 1;
  float m_reco_effSF_Medium_Tight_VarRad_NOSYS = 1;
  float m_reco_effSF_Medium_NonIso_NOSYS = 1;
  float m_reco_effSF_Tight_NonIso_NOSYS = 1;
  bool m_select_HighPt_NonIso_NOSYS = false;
  bool m_select_Loose_Loose_VarRad_NOSYS = false;
  bool m_select_Loose_PflowLoose_VarRad_NOSYS = false;
  bool m_select_Loose_PflowTight_VarRad_NOSYS = false;
  bool m_select_Loose_Tight_VarRad_NOSYS = false;
  bool m_select_Medium_Tight_VarRad_NOSYS = false;
  bool m_select_LowPtEfficiency_NonIso_NOSYS = false;
  bool m_select_Medium_NonIso_NOSYS = false;
  bool m_select_Tight_NonIso_NOSYS = false;
  bool m_select_wpSet0_NOSYS = false;
  bool m_select_wpSet1_NOSYS = false;
  bool m_select_wpSet2_NOSYS = false;
  bool m_select_wpSet3_NOSYS = false;
};  // Muon
}  // namespace TauXParticles