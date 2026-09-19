#pragma once

#include "Math/Vector4D.h"
#include "TauXFastFrame/Particle.h"

namespace TauXParticles {

class MET : public Particle {
 public:
  MET(){};
  MET(float met, float phi);

  float met();

  float sumEt();
  void set_sumEt(float val);

  float significance();
  void set_significance(float val);
    
 private:
  float m_sumEt;
  float m_significance;
};
}  // namespace TauXParticles
