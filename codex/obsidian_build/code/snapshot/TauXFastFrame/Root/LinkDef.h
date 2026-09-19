#include "TauXFastFrame/Electron.h"
#include "TauXFastFrame/Jet.h"
#include "TauXFastFrame/Lepton.h"
#include "TauXFastFrame/Muon.h"
#include "TauXFastFrame/Particle.h"
#include "TauXFastFrame/Tau.h"
#include "TauXFastFrame/TauXFastFrame.h"
#ifdef __CINT__

#pragma extra_include "TauXFastFrame/TauXFastFrame.h";
#pragma extra_include "TauXFastFrame/Tau.h";
#pragma extra_include "TauXFastFrame/Jet.h";
#pragma extra_include "TauXFastFrame/Muon.h";
#pragma extra_include "TauXFastFrame/Met.h";
#pragma extra_include "TauXFastFrame/Electron.h";
#pragma extra_include "TauXFastFrame/Lepton.h";
#pragma extra_include "TauXFastFrame/Particle.h";
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclass;
#pragma link C++ class TauXFastFrame + ;
#pragma link C++ class TauXParticles::Tau + ;
#pragma link C++ class TauXParticles::Jet + ;
#pragma link C++ class TauXParticles::Muon + ;
#pragma link C++ class TauXParticles::MET + ;
#pragma link C++ class TauXParticles::Electron + ;
#pragma link C++ class TauXParticles::Lepton + ;
#pragma link C++ class TauXParticles::Particle + ;

#endif
