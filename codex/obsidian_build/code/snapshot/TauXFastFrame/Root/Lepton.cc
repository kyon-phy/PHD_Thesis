#include "../TauXFastFrame/Lepton.h"

#include "Math/Vector4D.h"
#include "Math/VectorUtil.h"
#include "TauXFastFrame/Electron.h"
#include "TauXFastFrame/Muon.h"

using TauXParticles::Electron;
using TauXParticles::Lepton;
using TauXParticles::Muon;

Lepton::Lepton(const ROOT::Math::PtEtaPhiEVector& p4) : Particle(p4){};


Lepton::Lepton(const TauXParticles::Electron& el) : Particle(static_cast<const ROOT::Math::PtEtaPhiEVector&>(el)) {
  this->set_electron(el);
}


Lepton::Lepton(const TauXParticles::Muon& mu) : Particle(static_cast<const ROOT::Math::PtEtaPhiEVector&>(mu)) {
  this->set_muon(mu);
}


void Lepton::set_electron(Electron el) {
  m_el = el;
  m_charge = el.charge();
  m_pdgId = 11;
};

Electron& Lepton::El() {
  return m_el;
};

void Lepton::set_muon(Muon mu) {
  m_mu = mu;
  m_charge = mu.charge();
  m_pdgId = 13;
};

Muon& Lepton::Mu() {
  return m_mu;
};

bool Lepton::is_electron() {
  return m_pdgId == 11;
};

bool Lepton::is_muon() {
  return m_pdgId == 13;
};

bool Lepton::SF(Lepton& p) {
  return this->m_pdgId == p.m_pdgId;
};

int Lepton::charge() {
  return m_charge;
};
