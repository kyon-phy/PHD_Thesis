#include "TauXFastFrame/Met.h"

using TauXParticles::MET;

MET::MET(float met, float phi){
  this->SetCoordinates(met,0.,phi,met);
};

float MET::met(){
  return this->Pt();
}

float MET::sumEt(){
  return this->m_sumEt;
}

float MET::significance(){
  return this->m_significance;
}


void MET::set_sumEt(float val){
  this->m_sumEt = val;
}

void MET::set_significance(float val){
  this->m_significance = val;
}
