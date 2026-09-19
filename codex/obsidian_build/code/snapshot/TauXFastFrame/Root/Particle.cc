#include "../TauXFastFrame/Particle.h"

#include "Math/VectorUtil.h"
#include "TVector3.h"

using TauXParticles::Particle;

Particle::Particle(const ROOT::Math::PtEtaPhiEVector &p4) {
  this->SetCoordinates(p4.Pt(), p4.Eta(), p4.Phi(), p4.E());
};

double Particle::InvM(const Particle &l) const {
  return ((ROOT::Math::PtEtaPhiEVector)(*this) + (ROOT::Math::PtEtaPhiEVector)l).M();
}

double Particle::InvM(const float &p1, const float &p2, const float &p3, const float &p4) const {
  ROOT::Math::PtEtaPhiEVector TLV(p1, p2, p3, p4);
  return ((ROOT::Math::PtEtaPhiEVector)(*this) + (ROOT::Math::PtEtaPhiEVector)TLV).M();
}

double Particle::DeltaR(const Particle &l) const {
  return ROOT::Math::VectorUtil::DeltaR((ROOT::Math::PtEtaPhiEVector)(*this), (ROOT::Math::PtEtaPhiEVector)l);
}

double Particle::DeltaR(const float &p1, const float &p2, const float &p3, const float &p4) const {
  ROOT::Math::PtEtaPhiEVector TLV(p1, p2, p3, p4);
  return ROOT::Math::VectorUtil::DeltaR((ROOT::Math::PtEtaPhiEVector)(*this), (ROOT::Math::PtEtaPhiEVector)TLV);
}

double Particle::DeltaRy(const Particle &l) const {
  return ROOT::Math::VectorUtil::DeltaRapidityPhi((ROOT::Math::PtEtaPhiEVector)(*this), (ROOT::Math::PtEtaPhiEVector)l);
}

void Particle::set_sf(float f) {
  this->m_sf = (float)f;
}

float Particle::sf() const {
  return this->m_sf;
}

double Particle::DeltaPhi(const Particle &l) const {
  return ROOT::Math::VectorUtil::DeltaPhi((ROOT::Math::PtEtaPhiEVector)(*this), (ROOT::Math::PtEtaPhiEVector)l);
}

double Particle::DeltaPhi(const float &p1, const float &p2, const float &p3, const float &p4) const {
  ROOT::Math::PtEtaPhiEVector TLV(p1, p2, p3, p4);
  return ROOT::Math::VectorUtil::DeltaPhi((ROOT::Math::PtEtaPhiEVector)(*this), (ROOT::Math::PtEtaPhiEVector)TLV);
}

double Particle::mT(const Particle &l) const {
  double deltaPhi_met = this->DeltaPhi(l);
  return sqrt(2 * this->Pt() * l.Pt() * (1 - cos(deltaPhi_met)));
}

double Particle::mT(const float &p1, const float &p2, const float &p3, const float &p4) const {
  ROOT::Math::PtEtaPhiEVector TLV(p1, p2, p3, p4);
  double deltaPhi_met = this->DeltaPhi(TLV);
  return sqrt(2 * this->Pt() * p1 * (1 - cos(deltaPhi_met)));
}

// Get the vector sum of the two particles' Et
double Particle::VecSumEt(const Particle &l) const {
  ROOT::Math::PtEtaPhiEVector vec_sum = (ROOT::Math::PtEtaPhiEVector)(*this) + (ROOT::Math::PtEtaPhiEVector)l;
  return vec_sum.Et();
}

// Get the vector sum of the two particles' pt
double Particle::VecSumPt(const Particle &l) const {
  ROOT::Math::PtEtaPhiEVector vec_sum = (ROOT::Math::PtEtaPhiEVector)(*this) + (ROOT::Math::PtEtaPhiEVector)l;
  return vec_sum.Pt();
}

