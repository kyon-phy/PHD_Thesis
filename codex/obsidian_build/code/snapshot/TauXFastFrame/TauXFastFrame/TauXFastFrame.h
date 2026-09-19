#pragma once

#include <memory>

#include "FastFrames/ConfigSetting.h"
#include "FastFrames/MainFrame.h"
#include "FastFrames/Sample.h"
#include "FastFrames/UniqueSampleID.h"
#include "Math/Vector4D.h"
#include "ROOT/RDataFrame.hxx"
#include "TClass.h"
#include "FastFrames/ONNXWrapper.h" 

using TLV = ROOT::Math::PtEtaPhiEVector;
using RNode = ROOT::RDF::RNode;

class UniqueSampleID;

class TauXFastFrame : public MainFrame {
 public:
  explicit TauXFastFrame() = default;

  virtual ~TauXFastFrame() = default;

  virtual void init() override final {
    MainFrame::init();
    std::string NNpath = m_config->customOptions().getOption<std::string>("NNpath", "");
    if (!NNpath.empty()){
      m_onnx = new ONNXWrapper("My ML model", {
      NNpath
      });
    }
  }
  

  virtual RNode defineVariables(RNode mainNode, const std::shared_ptr<Sample>& sample, const UniqueSampleID& id) override final;

  virtual RNode defineVariablesNtuple(RNode mainNode, const std::shared_ptr<Sample>& sample, const UniqueSampleID& id) override final;

  virtual RNode defineVariablesTruth(RNode node, const std::string& truth, const std::shared_ptr<Sample>& sample, const UniqueSampleID& sampleID) override final;

  virtual RNode defineVariablesNtupleTruth(RNode node, const std::string& treeName, const std::shared_ptr<Sample>& sample, const UniqueSampleID& sampleID) override final;

    
 private:
  std::string getWP(const std::shared_ptr<ConfigSetting>& m_config);
  
  ClassDefOverride(TauXFastFrame, 1);

  ONNXWrapper *m_onnx;
};
