// -*- c++ -*-
#pragma once

#include "Math/Vector4D.h"
#include "TVector3.h"

namespace TauXParticles {

/// Particle class, base class for other object types
class Particle : public ROOT::Math::PtEtaPhiEVector {
 public:
  Particle(){};
  Particle(const ROOT::Math::PtEtaPhiEVector &p4);

  // Rapidity-based DeltaR between this and another particle
  double DeltaRy(const Particle &p1) const;

  double DeltaR(const Particle &p1) const;

  double DeltaR(const float &p1, const float &p2, const float &p3, const float &p4) const;

  double InvM(const Particle &p1) const;

  double InvM(const float &p1, const float &p2, const float &p3, const float &p4) const;

  double DeltaPhi(const Particle &l) const;

  double DeltaPhi(const float &p1, const float &p2, const float &p3, const float &p4) const;

  double mT(const Particle &l) const;

  double mT(const float &p1, const float &p2, const float &p3, const float &p4) const;

  double VecSumEt(const Particle &l) const;

  double VecSumPt(const Particle &l) const;

  // Generic obj-level Scale Factor
  void set_sf(float f);
  float sf() const;

  /// Comparison operators for sorting, etc.
  inline bool operator>(const Particle &other) const {
    return this->Pt() > other.Pt();
  }
  inline bool operator<(const Particle &other) const {
    return this->Pt() < other.Pt();
  }

 private:
  float m_sf = 1.;
  
};

}  // namespace TauXParticles
