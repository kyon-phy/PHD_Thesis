// Auto-generated code from class_patcher.py
// Based on Tau+X ntuple branch names

#include <vector>

#include "TauXFastFrame/Electron.h"
#include "TauXFastFrame/Jet.h"
#include "TauXFastFrame/Lepton.h"
#include "TauXFastFrame/Muon.h"
#include "TauXFastFrame/Tau.h"
#include "TauXFastFrame/TauXHelpers.h"
ROOT::RDF::RNode TauXHelpers::add_el_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData) {

  auto AddObjVectorMC = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                           const std::vector<unsigned char>& el_AmbiguityType,
                           const std::vector<int>& el_DFCommonAddAmbiguity,
                           const std::vector<int>& el_FirstEgMotherPdgId,
                           const std::vector<int>& el_FirstEgMotherTruthOrigin,
                           const std::vector<int>& el_FirstEgMotherTruthType,
                           const std::vector<int>& el_IFFtype,
                           const std::vector<int>& el_NinnPixHits,
                           const std::vector<int>& el_NtrackParticles,
                           const std::vector<float>& el_charge,
                           const std::vector<float>& el_d0,
                           const std::vector<float>& el_d0sig,
                           const std::vector<float>& el_deltaz0,
                           const std::vector<float>& el_deltaz0sinTheta,
                           const std::vector<float>& el_vz,
                           const std::vector<float>& el_z0,
                           const std::vector<float>& el_id_effSF_TightLH_HighPtCaloOnly_NOSYS,
                           const std::vector<float>& el_isol_effSF_TightLH_HighPtCaloOnly_NOSYS,
                           const std::vector<float>& el_reco_effSF_TightLH_HighPtCaloOnly_NOSYS,
                           const std::vector<char>& el_select_LooseBLayerLH_NonIso_NOSYS,
                           const std::vector<char>& el_select_LooseDNN_NonIso_NOSYS,
                           const std::vector<char>& el_select_MediumDNN_NonIso_NOSYS,
                           const std::vector<char>& el_select_TightDNN_NonIso_NOSYS,
                           const std::vector<char>& el_select_TightLH_HighPtCaloOnly_NOSYS,
                           const std::vector<char>& el_select_TightLH_Loose_VarRad_NOSYS,
                           const std::vector<char>& el_select_TightLH_TightTrackOnly_FixedRad_NOSYS,
                           const std::vector<char>& el_select_TightLH_TightTrackOnly_VarRad_NOSYS,
                           const std::vector<char>& el_select_TightLH_Tight_VarRad_NOSYS,
                           const std::vector<char>& el_select_wpSet0_NOSYS,
                          //  const std::vector<char>& el_select_wpSet1_NOSYS,
                          //  const std::vector<char>& el_select_wpSet2_NOSYS,
                          //  const std::vector<char>& el_select_wpSet3_NOSYS,
                           const ROOT::VecOps::RVec<int>& selected,
                           const ROOT::VecOps::RVec<float>& scaleFactor) {
    std::vector<TauXParticles::Electron> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Electron";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Electron(tlvVec[i]));
      objVec[j].set_AmbiguityType(el_AmbiguityType[i]);
      objVec[j].set_DFCommonAddAmbiguity(el_DFCommonAddAmbiguity[i]);
      objVec[j].set_FirstEgMotherPdgId(el_FirstEgMotherPdgId[i]);
      objVec[j].set_FirstEgMotherTruthOrigin(el_FirstEgMotherTruthOrigin[i]);
      objVec[j].set_FirstEgMotherTruthType(el_FirstEgMotherTruthType[i]);
      objVec[j].set_IFFtype(el_IFFtype[i]);
      objVec[j].set_NinnPixHits(el_NinnPixHits[i]);
      objVec[j].set_NtrackParticles(el_NtrackParticles[i]);
      objVec[j].set_charge(el_charge[i]);
      objVec[j].set_d0(el_d0[i]);
      objVec[j].set_d0sig(el_d0sig[i]);
      objVec[j].set_deltaz0(el_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(el_deltaz0sinTheta[i]);
      objVec[j].set_vz(el_vz[i]);
      objVec[j].set_z0(el_z0[i]);
      objVec[j].set_id_effSF_TightLH_HighPtCaloOnly_NOSYS(el_id_effSF_TightLH_HighPtCaloOnly_NOSYS[i]);
      objVec[j].set_isol_effSF_TightLH_HighPtCaloOnly_NOSYS(el_isol_effSF_TightLH_HighPtCaloOnly_NOSYS[i]);
      objVec[j].set_reco_effSF_TightLH_HighPtCaloOnly_NOSYS(el_reco_effSF_TightLH_HighPtCaloOnly_NOSYS[i]);
      objVec[j].set_select_LooseBLayerLH_NonIso_NOSYS(el_select_LooseBLayerLH_NonIso_NOSYS[i]);
      objVec[j].set_select_LooseDNN_NonIso_NOSYS(el_select_LooseDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_MediumDNN_NonIso_NOSYS(el_select_MediumDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_TightDNN_NonIso_NOSYS(el_select_TightDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_TightLH_HighPtCaloOnly_NOSYS(el_select_TightLH_HighPtCaloOnly_NOSYS[i]);
      objVec[j].set_select_TightLH_Loose_VarRad_NOSYS(el_select_TightLH_Loose_VarRad_NOSYS[i]);
      objVec[j].set_select_TightLH_TightTrackOnly_FixedRad_NOSYS(el_select_TightLH_TightTrackOnly_FixedRad_NOSYS[i]);
      objVec[j].set_select_TightLH_TightTrackOnly_VarRad_NOSYS(el_select_TightLH_TightTrackOnly_VarRad_NOSYS[i]);
      objVec[j].set_select_TightLH_Tight_VarRad_NOSYS(el_select_TightLH_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(el_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(el_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(el_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(el_select_wpSet3_NOSYS[i]);
      objVec[j].set_sf(scaleFactor[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Electron& a, const TauXParticles::Electron& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorMC;
  auto AddObjVectorData = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                             const std::vector<unsigned char>& el_AmbiguityType,
                             const std::vector<int>& el_DFCommonAddAmbiguity,
                             const std::vector<int>& el_NinnPixHits,
                             const std::vector<int>& el_NtrackParticles,
                             const std::vector<float>& el_charge,
                             const std::vector<float>& el_d0,
                             const std::vector<float>& el_d0sig,
                             const std::vector<float>& el_deltaz0,
                             const std::vector<float>& el_deltaz0sinTheta,
                             const std::vector<float>& el_vz,
                             const std::vector<float>& el_z0,
                             const std::vector<char>& el_select_LooseBLayerLH_NonIso_NOSYS,
                             const std::vector<char>& el_select_LooseDNN_NonIso_NOSYS,
                             const std::vector<char>& el_select_MediumDNN_NonIso_NOSYS,
                             const std::vector<char>& el_select_TightDNN_NonIso_NOSYS,
                             const std::vector<char>& el_select_TightLH_HighPtCaloOnly_NOSYS,
                             const std::vector<char>& el_select_TightLH_Loose_VarRad_NOSYS,
                             const std::vector<char>& el_select_TightLH_TightTrackOnly_FixedRad_NOSYS,
                             const std::vector<char>& el_select_TightLH_TightTrackOnly_VarRad_NOSYS,
                             const std::vector<char>& el_select_TightLH_Tight_VarRad_NOSYS,
                             const std::vector<char>& el_select_wpSet0_NOSYS,
                            //  const std::vector<char>& el_select_wpSet1_NOSYS,
                            //  const std::vector<char>& el_select_wpSet2_NOSYS,
                            //  const std::vector<char>& el_select_wpSet3_NOSYS,
                             const ROOT::VecOps::RVec<int>& selected) {
    std::vector<TauXParticles::Electron> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Electron";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Electron(tlvVec[i]));
      objVec[j].set_AmbiguityType(el_AmbiguityType[i]);
      objVec[j].set_DFCommonAddAmbiguity(el_DFCommonAddAmbiguity[i]);
      objVec[j].set_NinnPixHits(el_NinnPixHits[i]);
      objVec[j].set_NtrackParticles(el_NtrackParticles[i]);
      objVec[j].set_charge(el_charge[i]);
      objVec[j].set_d0(el_d0[i]);
      objVec[j].set_d0sig(el_d0sig[i]);
      objVec[j].set_deltaz0(el_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(el_deltaz0sinTheta[i]);
      objVec[j].set_vz(el_vz[i]);
      objVec[j].set_z0(el_z0[i]);
      objVec[j].set_select_LooseBLayerLH_NonIso_NOSYS(el_select_LooseBLayerLH_NonIso_NOSYS[i]);
      objVec[j].set_select_LooseDNN_NonIso_NOSYS(el_select_LooseDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_MediumDNN_NonIso_NOSYS(el_select_MediumDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_TightDNN_NonIso_NOSYS(el_select_TightDNN_NonIso_NOSYS[i]);
      objVec[j].set_select_TightLH_HighPtCaloOnly_NOSYS(el_select_TightLH_HighPtCaloOnly_NOSYS[i]);
      objVec[j].set_select_TightLH_Loose_VarRad_NOSYS(el_select_TightLH_Loose_VarRad_NOSYS[i]);
      objVec[j].set_select_TightLH_TightTrackOnly_FixedRad_NOSYS(el_select_TightLH_TightTrackOnly_FixedRad_NOSYS[i]);
      objVec[j].set_select_TightLH_TightTrackOnly_VarRad_NOSYS(el_select_TightLH_TightTrackOnly_VarRad_NOSYS[i]);
      objVec[j].set_select_TightLH_Tight_VarRad_NOSYS(el_select_TightLH_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(el_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(el_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(el_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(el_select_wpSet3_NOSYS[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Electron& a, const TauXParticles::Electron& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorData;

  mainNode = frame->systematicStringRedefine(mainNode, "el_filter_NOSYS", presel);

  if (!isData) {
    mainNode = frame->systematicStringRedefine(mainNode, "el_SF_NOSYS", scaleFactorDef);
    mainNode = frame->systematicRedefine(mainNode,
                                         "Electrons_NOSYS",
                                         AddObjVectorMC,
                                         {"el_TLV_NOSYS",
                                          "el_AmbiguityType",
                                          "el_DFCommonAddAmbiguity",
                                          "el_FirstEgMotherPdgId",
                                          "el_FirstEgMotherTruthOrigin",
                                          "el_FirstEgMotherTruthType",
                                          "el_IFFtype",
                                          "el_NinnPixHits",
                                          "el_NtrackParticles",
                                          "el_charge",
                                          "el_d0",
                                          "el_d0sig",
                                          "el_deltaz0",
                                          "el_deltaz0sinTheta",
                                          "el_vz",
                                          "el_z0",
                                          "el_id_effSF_TightLH_HighPtCaloOnly_NOSYS",
                                          "el_isol_effSF_TightLH_HighPtCaloOnly_NOSYS",
                                          "el_reco_effSF_TightLH_HighPtCaloOnly_NOSYS",
                                          "el_select_LooseBLayerLH_NonIso_NOSYS",
                                          "el_select_LooseDNN_NonIso_NOSYS",
                                          "el_select_MediumDNN_NonIso_NOSYS",
                                          "el_select_TightDNN_NonIso_NOSYS",
                                          "el_select_TightLH_HighPtCaloOnly_NOSYS",
                                          "el_select_TightLH_Loose_VarRad_NOSYS",
                                          "el_select_TightLH_TightTrackOnly_FixedRad_NOSYS",
                                          "el_select_TightLH_TightTrackOnly_VarRad_NOSYS",
                                          "el_select_TightLH_Tight_VarRad_NOSYS",
                                          "el_select_wpSet0_NOSYS",
                                          // "el_select_wpSet1_NOSYS",
                                          // "el_select_wpSet2_NOSYS",
                                          // "el_select_wpSet3_NOSYS",
                                          "el_filter_NOSYS",
                                          "el_SF_NOSYS"});
  }
  if (isData) {
    mainNode = frame->systematicRedefine(mainNode,
                                         "Electrons_NOSYS",
                                         AddObjVectorData,
                                         {"el_TLV_NOSYS",
                                          "el_AmbiguityType",
                                          "el_DFCommonAddAmbiguity",
                                          "el_NinnPixHits",
                                          "el_NtrackParticles",
                                          "el_charge",
                                          "el_d0",
                                          "el_d0sig",
                                          "el_deltaz0",
                                          "el_deltaz0sinTheta",
                                          "el_vz",
                                          "el_z0",
                                          "el_select_LooseBLayerLH_NonIso_NOSYS",
                                          "el_select_LooseDNN_NonIso_NOSYS",
                                          "el_select_MediumDNN_NonIso_NOSYS",
                                          "el_select_TightDNN_NonIso_NOSYS",
                                          "el_select_TightLH_HighPtCaloOnly_NOSYS",
                                          "el_select_TightLH_Loose_VarRad_NOSYS",
                                          "el_select_TightLH_TightTrackOnly_FixedRad_NOSYS",
                                          "el_select_TightLH_TightTrackOnly_VarRad_NOSYS",
                                          "el_select_TightLH_Tight_VarRad_NOSYS",
                                          "el_select_wpSet0_NOSYS",
                                          // "el_select_wpSet1_NOSYS",
                                          // "el_select_wpSet2_NOSYS",
                                          // "el_select_wpSet3_NOSYS",
                                          "el_filter_NOSYS"});
  }

  return mainNode;
};

ROOT::RDF::RNode TauXHelpers::add_mu_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData) {

  auto AddObjVectorMC = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                           const std::vector<int>& mu_IFFtype,
                           const std::vector<int>& mu_NinnPixHits,
                           const std::vector<float>& mu_charge,
                           const std::vector<float>& mu_d0,
                           const std::vector<float>& mu_d0sig,
                           const std::vector<float>& mu_deltaz0,
                           const std::vector<float>& mu_deltaz0sinTheta,
                           const std::vector<float>& mu_vz,
                           const std::vector<float>& mu_z0,
                           const std::vector<float>& mu_BadMuonVeto_effSF_HighPt_NonIso_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_HighPt_NonIso_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Loose_Loose_VarRad_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Loose_Tight_VarRad_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Medium_NonIso_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Medium_Tight_VarRad_NOSYS,
                           const std::vector<float>& mu_TTVA_effSF_Tight_NonIso_NOSYS,
                           const std::vector<float>& mu_isol_effSF_Loose_Loose_VarRad_NOSYS,
                           const std::vector<float>& mu_isol_effSF_Loose_PflowLoose_VarRad_NOSYS,
                           const std::vector<float>& mu_isol_effSF_Loose_PflowTight_VarRad_NOSYS,
                           const std::vector<float>& mu_isol_effSF_Loose_Tight_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_HighPt_NonIso_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Loose_Loose_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Loose_PflowLoose_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Loose_PflowTight_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Loose_Tight_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Medium_NonIso_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Medium_Tight_VarRad_NOSYS,
                           const std::vector<float>& mu_reco_effSF_Tight_NonIso_NOSYS,
                           const std::vector<char>& mu_select_HighPt_NonIso_NOSYS,
                           const std::vector<char>& mu_select_Loose_Loose_VarRad_NOSYS,
                           const std::vector<char>& mu_select_Loose_PflowLoose_VarRad_NOSYS,
                           const std::vector<char>& mu_select_Loose_PflowTight_VarRad_NOSYS,
                           const std::vector<char>& mu_select_Loose_Tight_VarRad_NOSYS,
                           const std::vector<char>& mu_select_LowPtEfficiency_NonIso_NOSYS,
                           const std::vector<char>& mu_select_Medium_NonIso_NOSYS,
                           const std::vector<char>& mu_select_Medium_Tight_VarRad_NOSYS,
                           const std::vector<char>& mu_select_Tight_NonIso_NOSYS,
                           const std::vector<char>& mu_select_wpSet0_NOSYS,
                          //  const std::vector<char>& mu_select_wpSet1_NOSYS,
                          //  const std::vector<char>& mu_select_wpSet2_NOSYS,
                          //  const std::vector<char>& mu_select_wpSet3_NOSYS,
                           const ROOT::VecOps::RVec<int>& selected,
                           const ROOT::VecOps::RVec<float>& scaleFactor) {
    std::vector<TauXParticles::Muon> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Muon";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Muon(tlvVec[i]));
      objVec[j].set_IFFtype(mu_IFFtype[i]);
      objVec[j].set_NinnPixHits(mu_NinnPixHits[i]);
      objVec[j].set_charge(mu_charge[i]);
      objVec[j].set_d0(mu_d0[i]);
      objVec[j].set_d0sig(mu_d0sig[i]);
      objVec[j].set_deltaz0(mu_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(mu_deltaz0sinTheta[i]);
      objVec[j].set_vz(mu_vz[i]);
      objVec[j].set_z0(mu_z0[i]);
      objVec[j].set_BadMuonVeto_effSF_HighPt_NonIso_NOSYS(mu_BadMuonVeto_effSF_HighPt_NonIso_NOSYS[i]);
      objVec[j].set_TTVA_effSF_HighPt_NonIso_NOSYS(mu_TTVA_effSF_HighPt_NonIso_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Loose_Loose_VarRad_NOSYS(mu_TTVA_effSF_Loose_Loose_VarRad_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS(mu_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS(mu_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Loose_Tight_VarRad_NOSYS(mu_TTVA_effSF_Loose_Tight_VarRad_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Medium_NonIso_NOSYS(mu_TTVA_effSF_Medium_NonIso_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Medium_Tight_VarRad_NOSYS(mu_TTVA_effSF_Medium_Tight_VarRad_NOSYS[i]);
      objVec[j].set_TTVA_effSF_Tight_NonIso_NOSYS(mu_TTVA_effSF_Tight_NonIso_NOSYS[i]);
      objVec[j].set_isol_effSF_Loose_Loose_VarRad_NOSYS(mu_isol_effSF_Loose_Loose_VarRad_NOSYS[i]);
      objVec[j].set_isol_effSF_Loose_PflowLoose_VarRad_NOSYS(mu_isol_effSF_Loose_PflowLoose_VarRad_NOSYS[i]);
      objVec[j].set_isol_effSF_Loose_PflowTight_VarRad_NOSYS(mu_isol_effSF_Loose_PflowTight_VarRad_NOSYS[i]);
      objVec[j].set_isol_effSF_Loose_Tight_VarRad_NOSYS(mu_isol_effSF_Loose_Tight_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_HighPt_NonIso_NOSYS(mu_reco_effSF_HighPt_NonIso_NOSYS[i]);
      objVec[j].set_reco_effSF_Loose_Loose_VarRad_NOSYS(mu_reco_effSF_Loose_Loose_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_Loose_PflowLoose_VarRad_NOSYS(mu_reco_effSF_Loose_PflowLoose_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_Loose_PflowTight_VarRad_NOSYS(mu_reco_effSF_Loose_PflowTight_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_Loose_Tight_VarRad_NOSYS(mu_reco_effSF_Loose_Tight_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_Medium_NonIso_NOSYS(mu_reco_effSF_Medium_NonIso_NOSYS[i]);
      objVec[j].set_reco_effSF_Medium_Tight_VarRad_NOSYS(mu_reco_effSF_Medium_Tight_VarRad_NOSYS[i]);
      objVec[j].set_reco_effSF_Tight_NonIso_NOSYS(mu_reco_effSF_Tight_NonIso_NOSYS[i]);
      objVec[j].set_select_HighPt_NonIso_NOSYS(mu_select_HighPt_NonIso_NOSYS[i]);
      objVec[j].set_select_Loose_Loose_VarRad_NOSYS(mu_select_Loose_Loose_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_PflowLoose_VarRad_NOSYS(mu_select_Loose_PflowLoose_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_PflowTight_VarRad_NOSYS(mu_select_Loose_PflowTight_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_Tight_VarRad_NOSYS(mu_select_Loose_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_LowPtEfficiency_NonIso_NOSYS(mu_select_LowPtEfficiency_NonIso_NOSYS[i]);
      objVec[j].set_select_Medium_NonIso_NOSYS(mu_select_Medium_NonIso_NOSYS[i]);
      objVec[j].set_select_Medium_Tight_VarRad_NOSYS(mu_select_Medium_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_Tight_NonIso_NOSYS(mu_select_Tight_NonIso_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(mu_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(mu_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(mu_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(mu_select_wpSet3_NOSYS[i]);
      objVec[j].set_sf(scaleFactor[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Muon& a, const TauXParticles::Muon& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorMC;
  auto AddObjVectorData = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                             const std::vector<int>& mu_NinnPixHits,
                             const std::vector<float>& mu_charge,
                             const std::vector<float>& mu_d0,
                             const std::vector<float>& mu_d0sig,
                             const std::vector<float>& mu_deltaz0,
                             const std::vector<float>& mu_deltaz0sinTheta,
                             const std::vector<float>& mu_vz,
                             const std::vector<float>& mu_z0,
                             const std::vector<char>& mu_select_HighPt_NonIso_NOSYS,
                             const std::vector<char>& mu_select_Loose_Loose_VarRad_NOSYS,
                             const std::vector<char>& mu_select_Loose_PflowLoose_VarRad_NOSYS,
                             const std::vector<char>& mu_select_Loose_PflowTight_VarRad_NOSYS,
                             const std::vector<char>& mu_select_Loose_Tight_VarRad_NOSYS,
                             const std::vector<char>& mu_select_LowPtEfficiency_NonIso_NOSYS,
                             const std::vector<char>& mu_select_Medium_NonIso_NOSYS,
                             const std::vector<char>& mu_select_Medium_Tight_VarRad_NOSYS,
                             const std::vector<char>& mu_select_Tight_NonIso_NOSYS,
                             const std::vector<char>& mu_select_wpSet0_NOSYS,
                            //  const std::vector<char>& mu_select_wpSet1_NOSYS,
                            //  const std::vector<char>& mu_select_wpSet2_NOSYS,
                            //  const std::vector<char>& mu_select_wpSet3_NOSYS,
                             const ROOT::VecOps::RVec<int>& selected) {
    std::vector<TauXParticles::Muon> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Muon";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Muon(tlvVec[i]));
      objVec[j].set_NinnPixHits(mu_NinnPixHits[i]);
      objVec[j].set_charge(mu_charge[i]);
      objVec[j].set_d0(mu_d0[i]);
      objVec[j].set_d0sig(mu_d0sig[i]);
      objVec[j].set_deltaz0(mu_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(mu_deltaz0sinTheta[i]);
      objVec[j].set_vz(mu_vz[i]);
      objVec[j].set_z0(mu_z0[i]);
      objVec[j].set_select_HighPt_NonIso_NOSYS(mu_select_HighPt_NonIso_NOSYS[i]);
      objVec[j].set_select_Loose_Loose_VarRad_NOSYS(mu_select_Loose_Loose_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_PflowLoose_VarRad_NOSYS(mu_select_Loose_PflowLoose_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_PflowTight_VarRad_NOSYS(mu_select_Loose_PflowTight_VarRad_NOSYS[i]);
      objVec[j].set_select_Loose_Tight_VarRad_NOSYS(mu_select_Loose_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_LowPtEfficiency_NonIso_NOSYS(mu_select_LowPtEfficiency_NonIso_NOSYS[i]);
      objVec[j].set_select_Medium_NonIso_NOSYS(mu_select_Medium_NonIso_NOSYS[i]);
      objVec[j].set_select_Medium_Tight_VarRad_NOSYS(mu_select_Medium_Tight_VarRad_NOSYS[i]);
      objVec[j].set_select_Tight_NonIso_NOSYS(mu_select_Tight_NonIso_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(mu_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(mu_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(mu_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(mu_select_wpSet3_NOSYS[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Muon& a, const TauXParticles::Muon& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorData;

  mainNode = frame->systematicStringRedefine(mainNode, "mu_filter_NOSYS", presel);

  if (!isData) {
    mainNode = frame->systematicStringRedefine(mainNode, "mu_SF_NOSYS", scaleFactorDef);
    mainNode = frame->systematicRedefine(mainNode,
                                         "Muons_NOSYS",
                                         AddObjVectorMC,
                                         {"mu_TLV_NOSYS",
                                          "mu_IFFtype",
                                          "mu_NinnPixHits",
                                          "mu_charge",
                                          "mu_d0",
                                          "mu_d0sig",
                                          "mu_deltaz0",
                                          "mu_deltaz0sinTheta",
                                          "mu_vz",
                                          "mu_z0",
                                          "mu_BadMuonVeto_effSF_HighPt_NonIso_NOSYS",
                                          "mu_TTVA_effSF_HighPt_NonIso_NOSYS",
                                          "mu_TTVA_effSF_Loose_Loose_VarRad_NOSYS",
                                          "mu_TTVA_effSF_Loose_PflowLoose_VarRad_NOSYS",
                                          "mu_TTVA_effSF_Loose_PflowTight_VarRad_NOSYS",
                                          "mu_TTVA_effSF_Loose_Tight_VarRad_NOSYS",
                                          "mu_TTVA_effSF_Medium_NonIso_NOSYS",
                                          "mu_TTVA_effSF_Medium_Tight_VarRad_NOSYS",
                                          "mu_TTVA_effSF_Tight_NonIso_NOSYS",
                                          "mu_isol_effSF_Loose_Loose_VarRad_NOSYS",
                                          "mu_isol_effSF_Loose_PflowLoose_VarRad_NOSYS",
                                          "mu_isol_effSF_Loose_PflowTight_VarRad_NOSYS",
                                          "mu_isol_effSF_Loose_Tight_VarRad_NOSYS",
                                          "mu_reco_effSF_HighPt_NonIso_NOSYS",
                                          "mu_reco_effSF_Loose_Loose_VarRad_NOSYS",
                                          "mu_reco_effSF_Loose_PflowLoose_VarRad_NOSYS",
                                          "mu_reco_effSF_Loose_PflowTight_VarRad_NOSYS",
                                          "mu_reco_effSF_Loose_Tight_VarRad_NOSYS",
                                          "mu_reco_effSF_Medium_NonIso_NOSYS",
                                          "mu_reco_effSF_Medium_Tight_VarRad_NOSYS",
                                          "mu_reco_effSF_Tight_NonIso_NOSYS",
                                          "mu_select_HighPt_NonIso_NOSYS",
                                          "mu_select_Loose_Loose_VarRad_NOSYS",
                                          "mu_select_Loose_PflowLoose_VarRad_NOSYS",
                                          "mu_select_Loose_PflowTight_VarRad_NOSYS",
                                          "mu_select_Loose_Tight_VarRad_NOSYS",
                                          "mu_select_LowPtEfficiency_NonIso_NOSYS",
                                          "mu_select_Medium_NonIso_NOSYS",
                                          "mu_select_Medium_Tight_VarRad_NOSYS",
                                          "mu_select_Tight_NonIso_NOSYS",
                                          "mu_select_wpSet0_NOSYS",
                                          // "mu_select_wpSet1_NOSYS",
                                          // "mu_select_wpSet2_NOSYS",
                                          // "mu_select_wpSet3_NOSYS",
                                          "mu_filter_NOSYS",
                                          "mu_SF_NOSYS"});
  }
  if (isData) {
    mainNode = frame->systematicRedefine(mainNode,
                                         "Muons_NOSYS",
                                         AddObjVectorData,
                                         {"mu_TLV_NOSYS",
                                          "mu_NinnPixHits",
                                          "mu_charge",
                                          "mu_d0",
                                          "mu_d0sig",
                                          "mu_deltaz0",
                                          "mu_deltaz0sinTheta",
                                          "mu_vz",
                                          "mu_z0",
                                          "mu_select_HighPt_NonIso_NOSYS",
                                          "mu_select_Loose_Loose_VarRad_NOSYS",
                                          "mu_select_Loose_PflowLoose_VarRad_NOSYS",
                                          "mu_select_Loose_PflowTight_VarRad_NOSYS",
                                          "mu_select_Loose_Tight_VarRad_NOSYS",
                                          "mu_select_LowPtEfficiency_NonIso_NOSYS",
                                          "mu_select_Medium_NonIso_NOSYS",
                                          "mu_select_Medium_Tight_VarRad_NOSYS",
                                          "mu_select_Tight_NonIso_NOSYS",
                                          "mu_select_wpSet0_NOSYS",
                                          // "mu_select_wpSet1_NOSYS",
                                          // "mu_select_wpSet2_NOSYS",
                                          // "mu_select_wpSet3_NOSYS",
                                          "mu_filter_NOSYS"});
  }

  return mainNode;
};

ROOT::RDF::RNode TauXHelpers::add_tau_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData) {

  auto AddObjVectorMC = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                           //  const std::vector<unsigned int>& tau_IsTauFlags,
                           const std::vector<int>& tau_NNDecayMode,
                           const std::vector<int>& tau_PanTauDecayMode,
                           //  const std::vector<float>& tau_RNNJetScore,
                           const std::vector<float>& tau_RNNJetScoreSigTrans,
                           const std::vector<float>& tau_charge,
                           const std::vector<float>& tau_d0,
                           const std::vector<float>& tau_d0sig,
                           const std::vector<float>& tau_deltaz0,
                           const std::vector<float>& tau_deltaz0sinTheta,
                           const std::vector<int>& tau_nTracks,
                           const std::vector<float>& tau_trackPt,
                           const std::vector<float>& tau_truth_DecayMode,
                           const std::vector<char>& tau_truth_IsHadronicTau,
                           const std::vector<float>& tau_truth_ParticleType,
                           const std::vector<float>& tau_truth_PartonTruthLabelID,
                           const std::vector<float>& tau_truth_eta_vis,
                           const std::vector<float>& tau_truth_m_vis,
                           const std::vector<unsigned int>& tau_truth_origin,
                           const std::vector<int>& tau_truth_pdgId,
                           const std::vector<float>& tau_truth_phi_vis,
                           const std::vector<float>& tau_truth_pt_vis,
                           const std::vector<unsigned int>& tau_truth_type,
                           const std::vector<float>& tau_vz,
                           const std::vector<float>& tau_z0,
                           //  const std::vector<float>& tau_EvetoFakeTau_effSF_Baseline_NOSYS,
                           const std::vector<float>& tau_EvetoFakeTau_effSF_LooseRNN_NOSYS,
                           const std::vector<float>& tau_EvetoFakeTau_effSF_MediumRNN_NOSYS,
                           //  const std::vector<float>& tau_EvetoFakeTau_effSF_TightRNN_NOSYS,
                           //  const std::vector<float>& tau_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS,
                           //  const std::vector<float>& tau_EvetoTrueTau_effSF_Baseline_NOSYS,
                           const std::vector<float>& tau_EvetoTrueTau_effSF_LooseRNN_NOSYS,
                           const std::vector<float>& tau_EvetoTrueTau_effSF_MediumRNN_NOSYS,
                           //  const std::vector<float>& tau_EvetoTrueTau_effSF_TightRNN_NOSYS,
                           //  const std::vector<float>& tau_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS,
                           const std::vector<float>& tau_ID_effSF_LooseRNN_NOSYS,
                           const std::vector<float>& tau_ID_effSF_LooseRNN_noElVeto_NOSYS,
                           const std::vector<float>& tau_ID_effSF_MediumRNN_NOSYS,
                           const std::vector<float>& tau_ID_effSF_MediumRNN_noElVeto_NOSYS,
                           //  const std::vector<float>& tau_ID_effSF_TightRNN_NOSYS,
                           const std::vector<float>& tau_ID_effSF_TightRNN_noElVeto_NOSYS,
                           //  const std::vector<float>& tau_Reco_effSF_Baseline_NOSYS,
                           //  const std::vector<float>& tau_Reco_effSF_Baseline_noElVeto_NOSYS,
                           const std::vector<float>& tau_Reco_effSF_LooseRNN_NOSYS,
                           const std::vector<float>& tau_Reco_effSF_LooseRNN_noElVeto_NOSYS,
                           const std::vector<float>& tau_Reco_effSF_MediumRNN_NOSYS,
                           const std::vector<float>& tau_Reco_effSF_MediumRNN_noElVeto_NOSYS,
                           //  const std::vector<float>& tau_Reco_effSF_TightRNN_NOSYS,
                           const std::vector<float>& tau_Reco_effSF_TightRNN_noElVeto_NOSYS,
                           //  const std::vector<float>& tau_Reco_effSF_VeryLooseRNN_NOSYS,
                           //  const std::vector<float>& tau_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS,
                           //  const std::vector<char>& tau_select_Baseline_NOSYS,
                           //  const std::vector<char>& tau_select_Baseline_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_LooseGNTau_NOSYS,
                           const std::vector<char>& tau_select_LooseGNTau_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_LooseRNN_NOSYS,
                           const std::vector<char>& tau_select_LooseRNN_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_MediumGNTau_NOSYS,
                           const std::vector<char>& tau_select_MediumGNTau_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_MediumRNN_NOSYS,
                           const std::vector<char>& tau_select_MediumRNN_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_TightGNTau_NOSYS,
                           const std::vector<char>& tau_select_TightGNTau_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_TightRNN_NOSYS,
                           const std::vector<char>& tau_select_TightRNN_noElVeto_NOSYS,
                           //  const std::vector<char>& tau_select_VeryLooseGNTau_NOSYS,
                           //  const std::vector<char>& tau_select_VeryLooseGNTau_noElVeto_NOSYS,
                           //  const std::vector<char>& tau_select_VeryLooseRNN_NOSYS,
                           //  const std::vector<char>& tau_select_VeryLooseRNN_noElVeto_NOSYS,
                           const std::vector<char>& tau_select_wpSet0_NOSYS,
                           //  const std::vector<char>& tau_select_wpSet1_NOSYS,
                           //  const std::vector<char>& tau_select_wpSet2_NOSYS,
                           //  const std::vector<char>& tau_select_wpSet3_NOSYS,
                           const ROOT::VecOps::RVec<int>& selected,
                           const ROOT::VecOps::RVec<float>& scaleFactor) {
    std::vector<TauXParticles::Tau> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Tau";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Tau(tlvVec[i]));
      // objVec[j].set_IsTauFlags(tau_IsTauFlags[i]);
      objVec[j].set_NNDecayMode(tau_NNDecayMode[i]);
      objVec[j].set_PanTauDecayMode(tau_PanTauDecayMode[i]);
      // objVec[j].set_RNNJetScore(tau_RNNJetScore[i]);
      objVec[j].set_RNNJetScoreSigTrans(tau_RNNJetScoreSigTrans[i]);
      objVec[j].set_charge(tau_charge[i]);
      objVec[j].set_d0(tau_d0[i]);
      objVec[j].set_d0sig(tau_d0sig[i]);
      objVec[j].set_deltaz0(tau_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(tau_deltaz0sinTheta[i]);
      objVec[j].set_nTracks(tau_nTracks[i]);
      objVec[j].set_trackPt(tau_trackPt[i]);
      objVec[j].set_truth_DecayMode(tau_truth_DecayMode[i]);
      objVec[j].set_truth_IsHadronicTau(tau_truth_IsHadronicTau[i]);
      objVec[j].set_truth_ParticleType(tau_truth_ParticleType[i]);
      objVec[j].set_truth_PartonTruthLabelID(tau_truth_PartonTruthLabelID[i]);
      objVec[j].set_truth_eta_vis(tau_truth_eta_vis[i]);
      objVec[j].set_truth_m_vis(tau_truth_m_vis[i]);
      objVec[j].set_truth_origin(tau_truth_origin[i]);
      objVec[j].set_truth_pdgId(tau_truth_pdgId[i]);
      objVec[j].set_truth_phi_vis(tau_truth_phi_vis[i]);
      objVec[j].set_truth_pt_vis(tau_truth_pt_vis[i]);
      objVec[j].set_truth_type(tau_truth_type[i]);
      objVec[j].set_vz(tau_vz[i]);
      objVec[j].set_z0(tau_z0[i]);
      // objVec[j].set_EvetoFakeTau_effSF_Baseline_NOSYS(tau_EvetoFakeTau_effSF_Baseline_NOSYS[i]);
      objVec[j].set_EvetoFakeTau_effSF_LooseRNN_NOSYS(tau_EvetoFakeTau_effSF_LooseRNN_NOSYS[i]);
      objVec[j].set_EvetoFakeTau_effSF_MediumRNN_NOSYS(tau_EvetoFakeTau_effSF_MediumRNN_NOSYS[i]);
      // objVec[j].set_EvetoFakeTau_effSF_TightRNN_NOSYS(tau_EvetoFakeTau_effSF_TightRNN_NOSYS[i]);
      // objVec[j].set_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS(tau_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS[i]);
      // objVec[j].set_EvetoTrueTau_effSF_Baseline_NOSYS(tau_EvetoTrueTau_effSF_Baseline_NOSYS[i]);
      objVec[j].set_EvetoTrueTau_effSF_LooseRNN_NOSYS(tau_EvetoTrueTau_effSF_LooseRNN_NOSYS[i]);
      objVec[j].set_EvetoTrueTau_effSF_MediumRNN_NOSYS(tau_EvetoTrueTau_effSF_MediumRNN_NOSYS[i]);
      // objVec[j].set_EvetoTrueTau_effSF_TightRNN_NOSYS(tau_EvetoTrueTau_effSF_TightRNN_NOSYS[i]);
      // objVec[j].set_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS(tau_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS[i]);
      objVec[j].set_ID_effSF_LooseRNN_NOSYS(tau_ID_effSF_LooseRNN_NOSYS[i]);
      objVec[j].set_ID_effSF_LooseRNN_noElVeto_NOSYS(tau_ID_effSF_LooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_ID_effSF_MediumRNN_NOSYS(tau_ID_effSF_MediumRNN_NOSYS[i]);
      objVec[j].set_ID_effSF_MediumRNN_noElVeto_NOSYS(tau_ID_effSF_MediumRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_ID_effSF_TightRNN_NOSYS(tau_ID_effSF_TightRNN_NOSYS[i]);
      objVec[j].set_ID_effSF_TightRNN_noElVeto_NOSYS(tau_ID_effSF_TightRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_Reco_effSF_Baseline_NOSYS(tau_Reco_effSF_Baseline_NOSYS[i]);
      // objVec[j].set_Reco_effSF_Baseline_noElVeto_NOSYS(tau_Reco_effSF_Baseline_noElVeto_NOSYS[i]);
      objVec[j].set_Reco_effSF_LooseRNN_NOSYS(tau_Reco_effSF_LooseRNN_NOSYS[i]);
      objVec[j].set_Reco_effSF_LooseRNN_noElVeto_NOSYS(tau_Reco_effSF_LooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_Reco_effSF_MediumRNN_NOSYS(tau_Reco_effSF_MediumRNN_NOSYS[i]);
      objVec[j].set_Reco_effSF_MediumRNN_noElVeto_NOSYS(tau_Reco_effSF_MediumRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_Reco_effSF_TightRNN_NOSYS(tau_Reco_effSF_TightRNN_NOSYS[i]);
      objVec[j].set_Reco_effSF_TightRNN_noElVeto_NOSYS(tau_Reco_effSF_TightRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_Reco_effSF_VeryLooseRNN_NOSYS(tau_Reco_effSF_VeryLooseRNN_NOSYS[i]);
      // objVec[j].set_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS(tau_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_select_Baseline_NOSYS(tau_select_Baseline_NOSYS[i]);
      // objVec[j].set_select_Baseline_noElVeto_NOSYS(tau_select_Baseline_noElVeto_NOSYS[i]);
      objVec[j].set_select_LooseGNTau_NOSYS(tau_select_LooseGNTau_NOSYS[i]);
      objVec[j].set_select_LooseGNTau_noElVeto_NOSYS(tau_select_LooseGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_LooseRNN_NOSYS(tau_select_LooseRNN_NOSYS[i]);
      objVec[j].set_select_LooseRNN_noElVeto_NOSYS(tau_select_LooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_MediumGNTau_NOSYS(tau_select_MediumGNTau_NOSYS[i]);
      objVec[j].set_select_MediumGNTau_noElVeto_NOSYS(tau_select_MediumGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_MediumRNN_NOSYS(tau_select_MediumRNN_NOSYS[i]);
      objVec[j].set_select_MediumRNN_noElVeto_NOSYS(tau_select_MediumRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_TightGNTau_NOSYS(tau_select_TightGNTau_NOSYS[i]);
      objVec[j].set_select_TightGNTau_noElVeto_NOSYS(tau_select_TightGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_TightRNN_NOSYS(tau_select_TightRNN_NOSYS[i]);
      objVec[j].set_select_TightRNN_noElVeto_NOSYS(tau_select_TightRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_select_VeryLooseGNTau_NOSYS(tau_select_VeryLooseGNTau_NOSYS[i]);
      // objVec[j].set_select_VeryLooseGNTau_noElVeto_NOSYS(tau_select_VeryLooseGNTau_noElVeto_NOSYS[i]);
      // objVec[j].set_select_VeryLooseRNN_NOSYS(tau_select_VeryLooseRNN_NOSYS[i]);
      // objVec[j].set_select_VeryLooseRNN_noElVeto_NOSYS(tau_select_VeryLooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(tau_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(tau_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(tau_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(tau_select_wpSet3_NOSYS[i]);
      objVec[j].set_sf(scaleFactor[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Tau& a, const TauXParticles::Tau& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorMC;
  auto AddObjVectorData = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                             //  const std::vector<unsigned int>& tau_IsTauFlags,
                             const std::vector<int>& tau_NNDecayMode,
                             const std::vector<int>& tau_PanTauDecayMode,
                             //  const std::vector<float>& tau_RNNJetScore,
                             const std::vector<float>& tau_RNNJetScoreSigTrans,
                             const std::vector<float>& tau_charge,
                             const std::vector<float>& tau_d0,
                             const std::vector<float>& tau_d0sig,
                             const std::vector<float>& tau_deltaz0,
                             const std::vector<float>& tau_deltaz0sinTheta,
                             const std::vector<int>& tau_nTracks,
                             const std::vector<float>& tau_trackPt,
                             const std::vector<float>& tau_vz,
                             const std::vector<float>& tau_z0,
                             //  const std::vector<char>& tau_select_Baseline_NOSYS,
                             //  const std::vector<char>& tau_select_Baseline_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_LooseGNTau_NOSYS,
                             const std::vector<char>& tau_select_LooseGNTau_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_LooseRNN_NOSYS,
                             const std::vector<char>& tau_select_LooseRNN_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_MediumGNTau_NOSYS,
                             const std::vector<char>& tau_select_MediumGNTau_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_MediumRNN_NOSYS,
                             const std::vector<char>& tau_select_MediumRNN_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_TightGNTau_NOSYS,
                             const std::vector<char>& tau_select_TightGNTau_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_TightRNN_NOSYS,
                             const std::vector<char>& tau_select_TightRNN_noElVeto_NOSYS,
                             //  const std::vector<char>& tau_select_VeryLooseGNTau_NOSYS,
                             //  const std::vector<char>& tau_select_VeryLooseGNTau_noElVeto_NOSYS,
                             //  const std::vector<char>& tau_select_VeryLooseRNN_NOSYS,
                             //  const std::vector<char>& tau_select_VeryLooseRNN_noElVeto_NOSYS,
                             const std::vector<char>& tau_select_wpSet0_NOSYS,
                             //  const std::vector<char>& tau_select_wpSet1_NOSYS,
                             //  const std::vector<char>& tau_select_wpSet2_NOSYS,
                             //  const std::vector<char>& tau_select_wpSet3_NOSYS,
                             const ROOT::VecOps::RVec<int>& selected) {
    std::vector<TauXParticles::Tau> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Tau";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Tau(tlvVec[i]));
      // objVec[j].set_IsTauFlags(tau_IsTauFlags[i]);
      objVec[j].set_NNDecayMode(tau_NNDecayMode[i]);
      objVec[j].set_PanTauDecayMode(tau_PanTauDecayMode[i]);
      // objVec[j].set_RNNJetScore(tau_RNNJetScore[i]);
      objVec[j].set_RNNJetScoreSigTrans(tau_RNNJetScoreSigTrans[i]);
      objVec[j].set_charge(tau_charge[i]);
      objVec[j].set_d0(tau_d0[i]);
      objVec[j].set_d0sig(tau_d0sig[i]);
      objVec[j].set_deltaz0(tau_deltaz0[i]);
      objVec[j].set_deltaz0sinTheta(tau_deltaz0sinTheta[i]);
      objVec[j].set_nTracks(tau_nTracks[i]);
      objVec[j].set_trackPt(tau_trackPt[i]);
      objVec[j].set_vz(tau_vz[i]);
      objVec[j].set_z0(tau_z0[i]);
      // objVec[j].set_select_Baseline_NOSYS(tau_select_Baseline_NOSYS[i]);
      // objVec[j].set_select_Baseline_noElVeto_NOSYS(tau_select_Baseline_noElVeto_NOSYS[i]);
      objVec[j].set_select_LooseGNTau_NOSYS(tau_select_LooseGNTau_NOSYS[i]);
      objVec[j].set_select_LooseGNTau_noElVeto_NOSYS(tau_select_LooseGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_LooseRNN_NOSYS(tau_select_LooseRNN_NOSYS[i]);
      objVec[j].set_select_LooseRNN_noElVeto_NOSYS(tau_select_LooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_MediumGNTau_NOSYS(tau_select_MediumGNTau_NOSYS[i]);
      objVec[j].set_select_MediumGNTau_noElVeto_NOSYS(tau_select_MediumGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_MediumRNN_NOSYS(tau_select_MediumRNN_NOSYS[i]);
      objVec[j].set_select_MediumRNN_noElVeto_NOSYS(tau_select_MediumRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_TightGNTau_NOSYS(tau_select_TightGNTau_NOSYS[i]);
      objVec[j].set_select_TightGNTau_noElVeto_NOSYS(tau_select_TightGNTau_noElVeto_NOSYS[i]);
      objVec[j].set_select_TightRNN_NOSYS(tau_select_TightRNN_NOSYS[i]);
      objVec[j].set_select_TightRNN_noElVeto_NOSYS(tau_select_TightRNN_noElVeto_NOSYS[i]);
      // objVec[j].set_select_VeryLooseGNTau_NOSYS(tau_select_VeryLooseGNTau_NOSYS[i]);
      // objVec[j].set_select_VeryLooseGNTau_noElVeto_NOSYS(tau_select_VeryLooseGNTau_noElVeto_NOSYS[i]);
      // objVec[j].set_select_VeryLooseRNN_NOSYS(tau_select_VeryLooseRNN_NOSYS[i]);
      // objVec[j].set_select_VeryLooseRNN_noElVeto_NOSYS(tau_select_VeryLooseRNN_noElVeto_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(tau_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(tau_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(tau_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(tau_select_wpSet3_NOSYS[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Tau& a, const TauXParticles::Tau& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorData;

  mainNode = frame->systematicStringRedefine(mainNode, "tau_filter_NOSYS", presel);

  if (!isData) {
    mainNode = frame->systematicStringRedefine(mainNode, "tau_SF_NOSYS", scaleFactorDef);
    mainNode = frame->systematicRedefine(mainNode,
                                         "Taus_NOSYS",
                                         AddObjVectorMC,
                                         {"tau_TLV_NOSYS",
                                          // "tau_IsTauFlags",
                                          "tau_NNDecayMode",
                                          "tau_PanTauDecayMode",
                                          // "tau_RNNJetScore",
                                          "tau_RNNJetScoreSigTrans",
                                          "tau_charge",
                                          "tau_d0",
                                          "tau_d0sig",
                                          "tau_deltaz0",
                                          "tau_deltaz0sinTheta",
                                          "tau_nTracks",
                                          "tau_trackPt",
                                          "tau_truth_DecayMode",
                                          "tau_truth_IsHadronicTau",
                                          "tau_truth_ParticleType",
                                          "tau_truth_PartonTruthLabelID",
                                          "tau_truth_eta_vis",
                                          "tau_truth_m_vis",
                                          "tau_truth_origin",
                                          "tau_truth_pdgId",
                                          "tau_truth_phi_vis",
                                          "tau_truth_pt_vis",
                                          "tau_truth_type",
                                          "tau_vz",
                                          "tau_z0",
                                          // "tau_EvetoFakeTau_effSF_Baseline_NOSYS",
                                          "tau_EvetoFakeTau_effSF_LooseRNN_NOSYS",
                                          "tau_EvetoFakeTau_effSF_MediumRNN_NOSYS",
                                          // "tau_EvetoFakeTau_effSF_TightRNN_NOSYS",
                                          // "tau_EvetoFakeTau_effSF_VeryLooseRNN_NOSYS",
                                          // "tau_EvetoTrueTau_effSF_Baseline_NOSYS",
                                          "tau_EvetoTrueTau_effSF_LooseRNN_NOSYS",
                                          "tau_EvetoTrueTau_effSF_MediumRNN_NOSYS",
                                          // "tau_EvetoTrueTau_effSF_TightRNN_NOSYS",
                                          // "tau_EvetoTrueTau_effSF_VeryLooseRNN_NOSYS",
                                          "tau_ID_effSF_LooseRNN_NOSYS",
                                          "tau_ID_effSF_LooseRNN_noElVeto_NOSYS",
                                          "tau_ID_effSF_MediumRNN_NOSYS",
                                          "tau_ID_effSF_MediumRNN_noElVeto_NOSYS",
                                          // "tau_ID_effSF_TightRNN_NOSYS",
                                          "tau_ID_effSF_TightRNN_noElVeto_NOSYS",
                                          // "tau_Reco_effSF_Baseline_NOSYS",
                                          // "tau_Reco_effSF_Baseline_noElVeto_NOSYS",
                                          "tau_Reco_effSF_LooseRNN_NOSYS",
                                          "tau_Reco_effSF_LooseRNN_noElVeto_NOSYS",
                                          "tau_Reco_effSF_MediumRNN_NOSYS",
                                          "tau_Reco_effSF_MediumRNN_noElVeto_NOSYS",
                                          // "tau_Reco_effSF_TightRNN_NOSYS",
                                          "tau_Reco_effSF_TightRNN_noElVeto_NOSYS",
                                          // "tau_Reco_effSF_VeryLooseRNN_NOSYS",
                                          // "tau_Reco_effSF_VeryLooseRNN_noElVeto_NOSYS",
                                          // "tau_select_Baseline_NOSYS",
                                          // "tau_select_Baseline_noElVeto_NOSYS",
                                          "tau_select_LooseGNTau_NOSYS",
                                          "tau_select_LooseGNTau_noElVeto_NOSYS",
                                          "tau_select_LooseRNN_NOSYS",
                                          "tau_select_LooseRNN_noElVeto_NOSYS",
                                          "tau_select_MediumGNTau_NOSYS",
                                          "tau_select_MediumGNTau_noElVeto_NOSYS",
                                          "tau_select_MediumRNN_NOSYS",
                                          "tau_select_MediumRNN_noElVeto_NOSYS",
                                          "tau_select_TightGNTau_NOSYS",
                                          "tau_select_TightGNTau_noElVeto_NOSYS",
                                          "tau_select_TightRNN_NOSYS",
                                          "tau_select_TightRNN_noElVeto_NOSYS",
                                          // "tau_select_VeryLooseGNTau_NOSYS",
                                          // "tau_select_VeryLooseGNTau_noElVeto_NOSYS",
                                          // "tau_select_VeryLooseRNN_NOSYS",
                                          // "tau_select_VeryLooseRNN_noElVeto_NOSYS",
                                          "tau_select_wpSet0_NOSYS",
                                          // "tau_select_wpSet1_NOSYS",
                                          // "tau_select_wpSet2_NOSYS",
                                          // "tau_select_wpSet3_NOSYS",
                                          "tau_filter_NOSYS",
                                          "tau_SF_NOSYS"});
  }
  if (isData) {
    mainNode = frame->systematicRedefine(mainNode,
                                         "Taus_NOSYS",
                                         AddObjVectorData,
                                         {"tau_TLV_NOSYS",
                                          // "tau_IsTauFlags",
                                          "tau_NNDecayMode",
                                          "tau_PanTauDecayMode",
                                          // "tau_RNNJetScore",
                                          "tau_RNNJetScoreSigTrans",
                                          "tau_charge",
                                          "tau_d0",
                                          "tau_d0sig",
                                          "tau_deltaz0",
                                          "tau_deltaz0sinTheta",
                                          "tau_nTracks",
                                          "tau_trackPt",
                                          "tau_vz",
                                          "tau_z0",
                                          // "tau_select_Baseline_NOSYS",
                                          // "tau_select_Baseline_noElVeto_NOSYS",
                                          "tau_select_LooseGNTau_NOSYS",
                                          "tau_select_LooseGNTau_noElVeto_NOSYS",
                                          "tau_select_LooseRNN_NOSYS",
                                          "tau_select_LooseRNN_noElVeto_NOSYS",
                                          "tau_select_MediumGNTau_NOSYS",
                                          "tau_select_MediumGNTau_noElVeto_NOSYS",
                                          "tau_select_MediumRNN_NOSYS",
                                          "tau_select_MediumRNN_noElVeto_NOSYS",
                                          "tau_select_TightGNTau_NOSYS",
                                          "tau_select_TightGNTau_noElVeto_NOSYS",
                                          "tau_select_TightRNN_NOSYS",
                                          "tau_select_TightRNN_noElVeto_NOSYS",
                                          // "tau_select_VeryLooseGNTau_NOSYS",
                                          // "tau_select_VeryLooseGNTau_noElVeto_NOSYS",
                                          // "tau_select_VeryLooseRNN_NOSYS",
                                          // "tau_select_VeryLooseRNN_noElVeto_NOSYS",
                                          "tau_select_wpSet0_NOSYS",
                                          // "tau_select_wpSet1_NOSYS",
                                          // "tau_select_wpSet2_NOSYS",
                                          // "tau_select_wpSet3_NOSYS",
                                          "tau_filter_NOSYS"});
  }

  return mainNode;
};

ROOT::RDF::RNode TauXHelpers::add_jet_vector(ROOT::RDF::RNode mainNode, TauXFastFrame* frame, std::string presel, std::string scaleFactorDef, bool isData) {

  auto AddObjVectorMC = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                           const std::vector<int>& jet_GN2v01_Continuous_quantile,
                           const std::vector<char>& jet_GN2v01_FixedCutBEff_65_select,
                           const std::vector<char>& jet_GN2v01_FixedCutBEff_70_select,
                           const std::vector<char>& jet_GN2v01_FixedCutBEff_77_select,
                           const std::vector<char>& jet_GN2v01_FixedCutBEff_85_select,
                           const std::vector<int>& jet_HadronConeExclExtendedTruthLabelID,
                           const std::vector<int>& jet_HadronConeExclTruthLabelID,
                           const std::vector<int>& jet_PartonTruthLabelID,
                           const std::vector<float>& jet_jvtEfficiency_NOSYS,
                           const std::vector<char>& jet_select_GN2v01_FixedCutBEff_65_NOSYS,
                           const std::vector<char>& jet_select_GN2v01_FixedCutBEff_70_NOSYS,
                           const std::vector<char>& jet_select_GN2v01_FixedCutBEff_77_NOSYS,
                           const std::vector<char>& jet_select_GN2v01_FixedCutBEff_85_NOSYS,
                           const std::vector<char>& jet_select_baselineFJvt_NOSYS,
                           const std::vector<char>& jet_select_baselineJvt_NOSYS,
                           const std::vector<char>& jet_select_wpSet0_NOSYS,
                          //  const std::vector<char>& jet_select_wpSet1_NOSYS,
                          //  const std::vector<char>& jet_select_wpSet2_NOSYS,
                          //  const std::vector<char>& jet_select_wpSet3_NOSYS,
                           const ROOT::VecOps::RVec<int>& selected,
                           const ROOT::VecOps::RVec<float>& scaleFactor) {
    std::vector<TauXParticles::Jet> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Jet";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Jet(tlvVec[i]));
      objVec[j].set_GN2v01_Continuous_quantile(jet_GN2v01_Continuous_quantile[i]);
      objVec[j].set_GN2v01_FixedCutBEff_65_select(jet_GN2v01_FixedCutBEff_65_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_70_select(jet_GN2v01_FixedCutBEff_70_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_77_select(jet_GN2v01_FixedCutBEff_77_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_85_select(jet_GN2v01_FixedCutBEff_85_select[i]);
      objVec[j].set_HadronConeExclExtendedTruthLabelID(jet_HadronConeExclExtendedTruthLabelID[i]);
      objVec[j].set_HadronConeExclTruthLabelID(jet_HadronConeExclTruthLabelID[i]);
      objVec[j].set_PartonTruthLabelID(jet_PartonTruthLabelID[i]);
      objVec[j].set_jvtEfficiency_NOSYS(jet_jvtEfficiency_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_65_NOSYS(jet_select_GN2v01_FixedCutBEff_65_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_70_NOSYS(jet_select_GN2v01_FixedCutBEff_70_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_77_NOSYS(jet_select_GN2v01_FixedCutBEff_77_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_85_NOSYS(jet_select_GN2v01_FixedCutBEff_85_NOSYS[i]);
      objVec[j].set_select_baselineFJvt_NOSYS(jet_select_baselineFJvt_NOSYS[i]);
      objVec[j].set_select_baselineJvt_NOSYS(jet_select_baselineJvt_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(jet_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(jet_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(jet_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(jet_select_wpSet3_NOSYS[i]);
      objVec[j].set_sf(scaleFactor[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Jet& a, const TauXParticles::Jet& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorMC;
  auto AddObjVectorData = [](const std::vector<ROOT::Math::PtEtaPhiEVector>& tlvVec,
                             const std::vector<int>& jet_GN2v01_Continuous_quantile,
                             const std::vector<char>& jet_GN2v01_FixedCutBEff_65_select,
                             const std::vector<char>& jet_GN2v01_FixedCutBEff_70_select,
                             const std::vector<char>& jet_GN2v01_FixedCutBEff_77_select,
                             const std::vector<char>& jet_GN2v01_FixedCutBEff_85_select,
                             const std::vector<char>& jet_select_GN2v01_FixedCutBEff_65_NOSYS,
                             const std::vector<char>& jet_select_GN2v01_FixedCutBEff_70_NOSYS,
                             const std::vector<char>& jet_select_GN2v01_FixedCutBEff_77_NOSYS,
                             const std::vector<char>& jet_select_GN2v01_FixedCutBEff_85_NOSYS,
                             const std::vector<char>& jet_select_baselineFJvt_NOSYS,
                             const std::vector<char>& jet_select_baselineJvt_NOSYS,
                             const std::vector<char>& jet_select_wpSet0_NOSYS,
                            //  const std::vector<char>& jet_select_wpSet1_NOSYS,
                            //  const std::vector<char>& jet_select_wpSet2_NOSYS,
                            //  const std::vector<char>& jet_select_wpSet3_NOSYS,
                             const ROOT::VecOps::RVec<int>& selected) {
    std::vector<TauXParticles::Jet> objVec;
    if (tlvVec.size() != selected.size()) {
      LOG(ERROR) << "Vector for TLV and selected have different size when processing class Jet";
      exit(1);
    }

    unsigned int j = 0;
    for (unsigned int i = 0; i < tlvVec.size(); ++i) {
      if (!selected[i])
        continue;
      objVec.push_back(TauXParticles::Jet(tlvVec[i]));
      objVec[j].set_GN2v01_Continuous_quantile(jet_GN2v01_Continuous_quantile[i]);
      objVec[j].set_GN2v01_FixedCutBEff_65_select(jet_GN2v01_FixedCutBEff_65_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_70_select(jet_GN2v01_FixedCutBEff_70_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_77_select(jet_GN2v01_FixedCutBEff_77_select[i]);
      objVec[j].set_GN2v01_FixedCutBEff_85_select(jet_GN2v01_FixedCutBEff_85_select[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_65_NOSYS(jet_select_GN2v01_FixedCutBEff_65_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_70_NOSYS(jet_select_GN2v01_FixedCutBEff_70_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_77_NOSYS(jet_select_GN2v01_FixedCutBEff_77_NOSYS[i]);
      objVec[j].set_select_GN2v01_FixedCutBEff_85_NOSYS(jet_select_GN2v01_FixedCutBEff_85_NOSYS[i]);
      objVec[j].set_select_baselineFJvt_NOSYS(jet_select_baselineFJvt_NOSYS[i]);
      objVec[j].set_select_baselineJvt_NOSYS(jet_select_baselineJvt_NOSYS[i]);
      objVec[j].set_select_wpSet0_NOSYS(jet_select_wpSet0_NOSYS[i]);
      // objVec[j].set_select_wpSet1_NOSYS(jet_select_wpSet1_NOSYS[i]);
      // objVec[j].set_select_wpSet2_NOSYS(jet_select_wpSet2_NOSYS[i]);
      // objVec[j].set_select_wpSet3_NOSYS(jet_select_wpSet3_NOSYS[i]);
      j++;
    }

    sort(objVec.begin(), objVec.end(), [](const TauXParticles::Jet& a, const TauXParticles::Jet& b) { return a.Pt() > b.Pt(); });
    return objVec;
  };  // AddObjVectorData;

  mainNode = frame->systematicStringRedefine(mainNode, "jet_filter_NOSYS", presel);

  if (!isData) {
    mainNode = frame->systematicStringRedefine(mainNode, "jet_SF_NOSYS", scaleFactorDef);
    mainNode = frame->systematicRedefine(mainNode,
                                         "Jets_NOSYS",
                                         AddObjVectorMC,
                                         {"jet_TLV_NOSYS",
                                          "jet_GN2v01_Continuous_quantile",
                                          "jet_GN2v01_FixedCutBEff_65_select",
                                          "jet_GN2v01_FixedCutBEff_70_select",
                                          "jet_GN2v01_FixedCutBEff_77_select",
                                          "jet_GN2v01_FixedCutBEff_85_select",
                                          "jet_HadronConeExclExtendedTruthLabelID",
                                          "jet_HadronConeExclTruthLabelID",
                                          "jet_PartonTruthLabelID",
                                          "jet_jvtEfficiency_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_65_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_70_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_77_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_85_NOSYS",
                                          "jet_select_baselineFJvt_NOSYS",
                                          "jet_select_baselineJvt_NOSYS",
                                          "jet_select_wpSet0_NOSYS",
                                          // "jet_select_wpSet1_NOSYS",
                                          // "jet_select_wpSet2_NOSYS",
                                          // "jet_select_wpSet3_NOSYS",
                                          "jet_filter_NOSYS",
                                          "jet_SF_NOSYS"});
  }
  if (isData) {
    mainNode = frame->systematicRedefine(mainNode,
                                         "Jets_NOSYS",
                                         AddObjVectorData,
                                         {"jet_TLV_NOSYS",
                                          "jet_GN2v01_Continuous_quantile",
                                          "jet_GN2v01_FixedCutBEff_65_select",
                                          "jet_GN2v01_FixedCutBEff_70_select",
                                          "jet_GN2v01_FixedCutBEff_77_select",
                                          "jet_GN2v01_FixedCutBEff_85_select",
                                          "jet_select_GN2v01_FixedCutBEff_65_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_70_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_77_NOSYS",
                                          "jet_select_GN2v01_FixedCutBEff_85_NOSYS",
                                          "jet_select_baselineFJvt_NOSYS",
                                          "jet_select_baselineJvt_NOSYS",
                                          "jet_select_wpSet0_NOSYS",
                                          // "jet_select_wpSet1_NOSYS",
                                          // "jet_select_wpSet2_NOSYS",
                                          // "jet_select_wpSet3_NOSYS",
                                          "jet_filter_NOSYS"});
  }

  return mainNode;
};
