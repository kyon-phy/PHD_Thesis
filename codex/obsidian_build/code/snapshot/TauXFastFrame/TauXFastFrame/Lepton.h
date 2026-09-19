#pragma once

#include "Math/Vector4D.h"
#include "TauXFastFrame/Electron.h"
#include "TauXFastFrame/Muon.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {

class Lepton : public Particle {
 public:
  Lepton(const ROOT::Math::PtEtaPhiEVector& p4);
  Lepton(const TauXParticles::Electron& el);
  Lepton(const TauXParticles::Muon& mu);

  bool is_electron();
  void set_electron(Electron el);

  bool is_muon();
  void set_muon(Muon mu);

  int charge();

  Electron& El();
  Muon& Mu();

  // Returns true if Same flavour
  bool SF(Lepton& p);

 private:
  int m_pdgId;
  int m_charge;
  Electron m_el;
  Muon m_mu;
};
}  // namespace TauXParticles
