// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#pragma once
#include "Math/Vector4D.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {
class Electron : public Particle {
 public:
  Electron(){};
  Electron(const ROOT::Math::PtEtaPhiEVector &p4);
  void set_AmbiguityType(unsigned char value);
  unsigned char AmbiguityType() const;

  void set_DFCommonAddAmbiguity(int value);
  int DFCommonAddAmbiguity() const;

  void set_FirstEgMotherPdgId(int value);
  int FirstEgMotherPdgId() const;

  void set_FirstEgMotherTruthOrigin(int value);
  int FirstEgMotherTruthOrigin() const;

  void set_FirstEgMotherTruthType(int value);
  int FirstEgMotherTruthType() const;

  void set_IFFtype(int value);
  int IFFtype() const;

  void set_NinnPixHits(int value);
  int NinnPixHits() const;

  void set_NtrackParticles(int value);
  int NtrackParticles() const;

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

  // (Jiaqi hack) el SFs
  void set_id_effSF_TightLH_HighPtCaloOnly_NOSYS(float value);
  float id_effSF_TightLH_HighPtCaloOnly_NOSYS() const;

  void set_isol_effSF_TightLH_HighPtCaloOnly_NOSYS(float value);
  float isol_effSF_TightLH_HighPtCaloOnly_NOSYS() const;

  void set_reco_effSF_TightLH_HighPtCaloOnly_NOSYS(float value);
  float reco_effSF_TightLH_HighPtCaloOnly_NOSYS() const;
  // (Jiaqi hack) el SFs

  void set_select_LooseBLayerLH_NonIso_NOSYS(char value);
  bool select_LooseBLayerLH_NonIso_NOSYS() const;

  void set_select_LooseDNN_NonIso_NOSYS(char value);
  bool select_LooseDNN_NonIso_NOSYS() const;

  void set_select_MediumDNN_NonIso_NOSYS(char value);
  bool select_MediumDNN_NonIso_NOSYS() const;

  void set_select_TightDNN_NonIso_NOSYS(char value);
  bool select_TightDNN_NonIso_NOSYS() const;

  void set_select_TightLH_HighPtCaloOnly_NOSYS(char value);
  bool select_TightLH_HighPtCaloOnly_NOSYS() const;

  void set_select_TightLH_Loose_VarRad_NOSYS(char value);
  bool select_TightLH_Loose_VarRad_NOSYS() const;

  void set_select_TightLH_TightTrackOnly_FixedRad_NOSYS(char value);
  bool select_TightLH_TightTrackOnly_FixedRad_NOSYS() const;

  void set_select_TightLH_TightTrackOnly_VarRad_NOSYS(char value);
  bool select_TightLH_TightTrackOnly_VarRad_NOSYS() const;

  void set_select_TightLH_Tight_VarRad_NOSYS(char value);
  bool select_TightLH_Tight_VarRad_NOSYS() const;

  void set_select_wpSet0_NOSYS(char value);
  bool select_wpSet0_NOSYS() const;

  void set_select_wpSet1_NOSYS(char value);
  bool select_wpSet1_NOSYS() const;

  void set_select_wpSet2_NOSYS(char value);
  bool select_wpSet2_NOSYS() const;

  void set_select_wpSet3_NOSYS(char value);
  bool select_wpSet3_NOSYS() const;

 private:
  unsigned char m_AmbiguityType = -15;
  int m_DFCommonAddAmbiguity = -9999;
  int m_FirstEgMotherPdgId = -9999;
  int m_FirstEgMotherTruthOrigin = -9999;
  int m_FirstEgMotherTruthType = -9999;
  int m_IFFtype = -9999;
  int m_NinnPixHits = -9999;
  int m_NtrackParticles = -9999;
  float m_charge = -9999;
  float m_d0 = -9999;
  float m_d0sig = -9999;
  float m_deltaz0 = -9999;
  float m_deltaz0sinTheta = -9999;
  float m_vz = -9999;
  float m_z0 = -9999;
  // (Jiaqi hack) el SFs
  float m_id_effSF_TightLH_HighPtCaloOnly_NOSYS = 1;
  float m_isol_effSF_TightLH_HighPtCaloOnly_NOSYS = 1;
  float m_reco_effSF_TightLH_HighPtCaloOnly_NOSYS = 1;
  // (Jiaqi hack) el SFs
  bool m_select_LooseBLayerLH_NonIso_NOSYS = false;
  bool m_select_LooseDNN_NonIso_NOSYS = false;
  bool m_select_MediumDNN_NonIso_NOSYS = false;
  bool m_select_TightDNN_NonIso_NOSYS = false;
  bool m_select_TightLH_HighPtCaloOnly_NOSYS = false;
  bool m_select_TightLH_Loose_VarRad_NOSYS = false;
  bool m_select_TightLH_TightTrackOnly_FixedRad_NOSYS = false;
  bool m_select_TightLH_TightTrackOnly_VarRad_NOSYS = false;
  bool m_select_TightLH_Tight_VarRad_NOSYS = false;
  bool m_select_wpSet0_NOSYS = false;
  bool m_select_wpSet1_NOSYS = false;
  bool m_select_wpSet2_NOSYS = false;
  bool m_select_wpSet3_NOSYS = false;
};  // Electron
}  // namespace TauXParticles