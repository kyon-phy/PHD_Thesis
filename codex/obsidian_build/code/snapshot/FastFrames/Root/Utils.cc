/**
 * @file Utils.cc
 * @brief Helper functions
 *
 */

#include "FastFrames/Utils.h"

#include "FastFrames/Logger.h"
#include "FastFrames/Sample.h"

#include "TChain.h"
#include "TTreeIndex.h"

#include <algorithm>
#include <exception>
#include <regex>

std::unique_ptr<TChain> Utils::chainFromFiles(const std::string& treeName,
                                              const std::vector<std::string>& files,
                                              const bool checkTree) {

    std::unique_ptr<TChain> chain = std::make_unique<TChain>(treeName.c_str());

    for (const auto& ifile : files) {
        if (checkTree) {
            const bool exists = Utils::checkTreeExists(ifile, treeName);
            if (!exists) {
                LOG(INFO) << "Skipping path: " << ifile << " as it does not have tree: " << treeName << "\n";
                continue;
            }
        }
        chain->AddFile(ifile.c_str());
    }

    return chain;
}

std::vector<double> fromRegularToEdges(const Variable& v){
    // We create a TH1D just as a proxy to get the bin edges
    TH1D histo("", "", v.axisNbins(), v.axisMin(), v.axisMax());
    std::vector<double> binEdges{};


    // Add each bin edge one by one
    std::size_t nBins = static_cast<std::size_t>(histo.GetNbinsX());
    for(std::size_t i = 1; i <= nBins; ++i) {
        binEdges.push_back(histo.GetXaxis()->GetBinLowEdge(i));
    }
    // Add the last bin edge
    binEdges.push_back(histo.GetXaxis()->GetBinUpEdge(nBins));

    return binEdges;
}

ROOT::RDF::TH2DModel Utils::histoModel2D(const Variable& v1, const Variable& v2) {
    if (v1.hasRegularBinning() && v2.hasRegularBinning()) {
        return ROOT::RDF::TH2DModel("", "", v1.axisNbins(), v1.axisMin(), v1.axisMax(), v2.axisNbins(), v2.axisMin(), v2.axisMax());
    }
    if (v1.hasRegularBinning() && !v2.hasRegularBinning()) {
        const std::vector<double>& binEdges2 = v2.binEdges();
        return ROOT::RDF::TH2DModel("", "", v1.axisNbins(), v1.axisMin(), v1.axisMax(), binEdges2.size() - 1, binEdges2.data());
    }
    if (!v1.hasRegularBinning() && v2.hasRegularBinning()) {
        const std::vector<double>& binEdges1 = v1.binEdges();
        return ROOT::RDF::TH2DModel("", "", binEdges1.size() -1, binEdges1.data(), v2.axisNbins(), v2.axisMin(), v2.axisMax());
    }
    const std::vector<double>& binEdges1 = v1.binEdges();
    const std::vector<double>& binEdges2 = v2.binEdges();
    return ROOT::RDF::TH2DModel("", "", binEdges1.size() -1, binEdges1.data(), binEdges2.size() - 1, binEdges2.data());
}

ROOT::RDF::TProfile1DModel Utils::histoModelProfile(const Variable& v1, const Variable& v2) {
    if (v1.hasRegularBinning()) {
        return ROOT::RDF::TProfile1DModel("", "", v1.axisNbins(), v1.axisMin(), v1.axisMax(), v2.axisMin(), v2.axisMax());
    } else {
        const std::vector<double>& binEdges1 = v1.binEdges();
        return ROOT::RDF::TProfile1DModel("", "", binEdges1.size() -1, binEdges1.data(), v2.axisMin(), v2.axisMax());
    }
}

ROOT::RDF::TH3DModel Utils::histoModel3D(const Variable& v1, const Variable& v2, const Variable& v3) {
    const std::vector<double> binEdges1 = v1.hasRegularBinning() ? fromRegularToEdges(v1) : v1.binEdges();
    const std::vector<double> binEdges2 = v2.hasRegularBinning() ? fromRegularToEdges(v2) : v2.binEdges();
    const std::vector<double> binEdges3 = v3.hasRegularBinning() ? fromRegularToEdges(v3) : v3.binEdges();
    return ROOT::RDF::TH3DModel("", "", binEdges1.size() -1, binEdges1.data(), binEdges2.size() - 1, binEdges2.data(), binEdges3.size() - 1, binEdges3.data());
}

std::unique_ptr<TH1D> Utils::copyHistoFromVariableHistos(const std::vector<VariableHisto>& histos,
                                                         const std::string& name) {

    auto itr = std::find_if(histos.begin(), histos.end(), [&name](const auto& element){return element.name() == name;});
    if (itr == histos.end()) {
        LOG(ERROR) << "Cannot find histogram: " << name << "\n";
        throw std::runtime_error("");
    }

    std::unique_ptr<TH1D> result(static_cast<TH1D*>(itr->histoUniquePtr()->Clone()));
    result->SetDirectory(nullptr);

    return result;
}

std::unique_ptr<TH2D> Utils::copyHistoFromVariableHistos2D(const std::vector<VariableHisto2D>& histos,
                                                           const std::string& name) {

    auto itr = std::find_if(histos.begin(), histos.end(), [&name](const auto& element){return element.name() == name;});
    if (itr == histos.end()) {
        LOG(ERROR) << "Cannot find histogram: " << name << "\n";
        throw std::runtime_error("");
    }

    std::unique_ptr<TH2D> result(static_cast<TH2D*>(itr->histoUniquePtr()->Clone()));
    result->SetDirectory(nullptr);

    return result;
}

std::vector<std::string> Utils::selectedFileList(const std::vector<std::string>& fileList,
                                                 const int split,
                                                 const int index) {

    if (index < 0) {
        LOG(ERROR) << "Index < 0, cannot proceed\n";
        throw std::invalid_argument("");
    }

    std::vector<std::string> result;
    for (std::size_t i = 0; i < fileList.size(); ++i) {
        static int totalIndex(0);
        if ((int)totalIndex % split == index) {
            LOG(DEBUG) << "Split N: " << split << ", index: " << index << ", adding file: " << fileList.at(i) << "\n";
            result.emplace_back(fileList.at(i));
        }
        ++totalIndex;
    }

    return result;
}

void Utils::capHisto0And1(TH1D* h, const std::string& name) {
    for (int ibin = 0; ibin <= h->GetNbinsX(); ++ibin) {
        const double content = h->GetBinContent(ibin);
        if (content < 0) {
            h->SetBinContent(ibin, 0.);
            LOG(VERBOSE) << "Negative bin content of " << content << " found in " << ibin << " bin of " << name << " histogram, setting it to 0\n";
        }
        if (content > 1.) {
            h->SetBinContent(ibin, 1.);
            LOG(VERBOSE) << "Bin content of " << content << " found in " << ibin << " bin of " << name << " histogram, setting it to 1\n";
        }
    }
}

const Variable& Utils::getVariableByName(const std::vector<std::shared_ptr<Region> >& regions,
                                         const std::string& regionName,
                                         const std::string& variableName) {

    // first find the region
    auto itrReg = std::find_if(regions.begin(), regions.end(), [&regionName](const auto& element){return element->name() == regionName;});
    if (itrReg == regions.end()) {
        LOG(ERROR) << "Cannot find region: " << regionName << "\n";
        throw std::runtime_error("");
    }

    auto itrVar = std::find_if((*itrReg)->variables().begin(), (*itrReg)->variables().end(),
                                [&variableName](const auto& element){return element.name() == variableName;});

    if (itrVar == (*itrReg)->variables().end()) {
        LOG(ERROR) << "Cannot find variable: " << variableName << " in region: " << regionName <<"\n";
        throw std::runtime_error("");
    }

    return *itrVar;
}

Variable Utils::getVariableByNameTruth(const std::shared_ptr<Sample>& sample,
                                       const std::string& variableName) {

    for (const auto& itruth : sample->truths()) {
        const auto vars = itruth->variables();
        auto itr = std::find_if(vars.begin(), vars.end(), [&itruth,&variableName](const auto& element){return variableName == (itruth->name() + "_" + element.name());});

        if (itr != vars.end()) {
            return *itr;
        }
    }

    // this should not happen
    LOG(ERROR) << "Cannot find the corresponding truth variable for: " << variableName << "\n";
    throw std::runtime_error("");
}


std::pair<Variable, Variable> Utils::get2DVariablesByName(const std::shared_ptr<Sample>& sample,
                                                          const std::string& regionName,
                                                          const std::string& variableName) {

    // first find the region
    auto itrReg = std::find_if(sample->regions().begin(), sample->regions().end(), [&regionName](const auto& element){return element->name() == regionName;});
    if (itrReg == sample->regions().end()) {
        LOG(ERROR) << "Cannot find region: " << regionName << "\n";
        throw std::runtime_error("");
    }

    const auto vars = (*itrReg)->variables();

    auto itrVar1 = std::find_if(vars.begin(), vars.end(),
        [&variableName](const auto& element){return StringOperations::stringStartsWith(variableName, (element.name()+"_vs"));});

    std::unique_ptr<Variable> var1(nullptr);

    if (itrVar1 == vars.end()) {
        // check truth
        for (const auto& itruth : sample->truths()) {
            const auto& truthVars = itruth->variables();
            auto itrTruth1 = std::find_if(truthVars.begin(), truthVars.end(),
                [&variableName, &itruth](const auto& element){return StringOperations::stringStartsWith(variableName, (itruth->name() + "_" + element.name()+"_vs"));});

            if (itrTruth1 != truthVars.end()) {
                var1 = std::make_unique<Variable>(*itrTruth1);
            }
        }
    } else {
        var1 = std::make_unique<Variable>(*itrVar1);
    }

    auto itrVar2 = std::find_if(vars.begin(), vars.end(),
        [&variableName, &regionName](const auto& element){return StringOperations::stringEndsWith(variableName, ("vs_"+element.name()+"_" + regionName));});

    std::unique_ptr<Variable> var2(nullptr);

    if (itrVar2 == vars.end()) {
        // check truth
        for (const auto& itruth : sample->truths()) {
            const auto& truthVars = itruth->variables();
            auto itrTruth2 = std::find_if(truthVars.begin(), truthVars.end(),
                [&variableName, &itruth, &regionName](const auto& element){return StringOperations::stringEndsWith(variableName, ("vs_" + itruth->name() + "_" + element.name()+"_" + regionName));});

            if (itrTruth2 != truthVars.end()) {
                var2 = std::make_unique<Variable>(*itrTruth2);
            }
        }
    } else {
        var2 = std::make_unique<Variable>(*itrVar2);
    }

    if (!var1 || !var2) {
        LOG(ERROR) << "Cannot split 2D histogram into variables: " << variableName << "\n";
        throw std::runtime_error("");
    }

    return std::make_pair(std::move(*var1), std::move(*var2));
}


bool Utils::compareDoubles(const double a, const double b, const double relative_precision) {
    return std::abs(a - b) < relative_precision * std::max(std::abs(a), std::abs(b));
};

std::vector<std::string> Utils::selectedNotExcludedElements(const std::vector<std::string>& all,
                                                            const std::vector<std::string>& selected,
                                                            const std::vector<std::string>& excluded) {

    std::vector<std::string> result;

    if (selected.empty() && excluded.empty()) {
        return all;
    }

    for (const auto& ibranch : all) {
        bool isSelected(false);
        for (const auto& imatch : selected) {
            std::regex match(imatch);
            if (std::regex_match(ibranch, match)) {
                isSelected = true;
                break;
            }
        }

        // if not selected, skip
        if (!isSelected) continue;

        // if selected check if it is not excluded
        for (const auto& imatch : excluded) {
            std::regex match(imatch);
            if (std::regex_match(ibranch, match)) {
                isSelected = false;
                break;
            }
        }

        if (isSelected) {
            result.emplace_back(ibranch);
        }
    }

    return result;
}

std::vector<std::string> Utils::requestedNotPresentElements(const std::vector<std::string>& all,
                                                            const std::vector<std::string>& requested) {

    std::vector<std::string> result;

    for (const auto& irequested : requested) {
        std::regex match(irequested);

        auto itr = std::find_if(all.begin(), all.end(), [&match](const auto& element){return std::regex_match(element, match);});

        if (itr == all.end()) {
            result.emplace_back(irequested);
        }
    }

    return result;
}

std::map<std::string, std::string> Utils::variablesWithFormulaReco(ROOT::RDF::RNode node,
                                                                   const std::shared_ptr<Sample>& sample,
                                                                   const std::vector<std::string>& truthTrees) {

    std::map<std::string, std::string> result;

    const std::vector<std::string>& columns = node.GetColumnNames();

    const std::vector<std::string>& variableNames = sample->variables();
    for (const auto& iregion : sample->regions()) {
        for (const auto& ivariable : iregion->variables()) {

            // check of it is not of a form "truthTree."
            bool isTruth(false);
            for (const auto& itruthTree : truthTrees) {
                if (StringOperations::stringStartsWith(ivariable.name(), itruthTree+".")) {
                    LOG(DEBUG) << "Variable: " << ivariable.name() << " contains \"treeName.\" prefix, will not consider it as a formula.\n";
                    isTruth = true;
                    break;
                }
            }

            if (isTruth) continue;

            auto itrVar = std::find(variableNames.begin(), variableNames.end(), ivariable.name());
            if (itrVar == variableNames.end()) continue;

            const std::string& definition = ivariable.definition();

            // skip if the column exists (is not a formula)
            auto itrColumns = std::find(columns.begin(), columns.end(), definition);
            if (itrColumns != columns.end()) continue;

            // skip if it is already added
            auto itrMap = result.find(definition);
            if (itrMap != result.end()) continue;


            const std::string newName = "internal_FastFrames_" + iregion->name() + "_" + std::to_string(result.size()) + "_NOSYS";
            result.insert({definition, newName});
        }
    }

    return result;
}

std::map<std::string, std::string>Utils::variablesWithFormulaTruth(ROOT::RDF::RNode node,
                                                                   const std::shared_ptr<Sample>& sample,
                                                                   const std::string& treeName) {

    std::map<std::string, std::string> result;
    const std::vector<std::string>& columns = node.GetColumnNames();

    for (const auto& itruth : sample->truths()) {
        const std::string truthTreeName = itruth->truthTreeName();
        if (truthTreeName != treeName) continue;

        for (const auto& ivariable : itruth->variables()) {
            const std::string definition = ivariable.definition();

            if (StringOperations::stringStartsWith(definition, treeName+".")) {
                LOG(DEBUG) << "Variable: " << definition << " contains \"treeName.\" prefix, will not consider it as a formula\n";
                continue;
            }

            // skip if the column exists (is not a formula)
            auto itrColumns = std::find(columns.begin(), columns.end(), definition);
            if (itrColumns != columns.end()) continue;

            itrColumns = std::find(columns.begin(), columns.end(), treeName+"."+definition);
            if (itrColumns != columns.end()) continue;

            // skip if it is already added
            auto itrMap = result.find(definition);
            if (itrMap != result.end()) continue;

            const std::string newName = "internal_FastFrames_" + itruth->name() + "_" + std::to_string(result.size());
            result.insert({definition, newName});
        }
    }

    return result;
}

std::vector<std::string> Utils::matchingBranchesFromChains(const std::unique_ptr<TChain>& reco,
                                                           const std::unique_ptr<TChain>& truth,
                                                           const std::vector<std::string>& toCheck) {

    std::vector<std::string> matches;

    const TObjArray* const recoBranchList = reco->GetListOfBranches();
    const TObjArray* const truthBranchList = truth->GetListOfBranches();

    const std::size_t recoBranchSize = reco->GetNbranches();
    const std::size_t truthBranchSize = truth->GetNbranches();

    std::vector<std::string> recoMatch;
    std::vector<std::string> truthMatch;

    for (std::size_t ibranch = 0; ibranch < recoBranchSize; ++ibranch) {
        const std::string name = recoBranchList->At(ibranch)->GetName();
        for (const auto& check : toCheck) {
            std::regex re(check);
            if (std::regex_match(name, re)) {
                recoMatch.emplace_back(name);
            }
        }
    }

    for (std::size_t ibranch = 0; ibranch < truthBranchSize; ++ibranch) {
        const std::string name = truthBranchList->At(ibranch)->GetName();
        for (const auto& check : toCheck) {
            std::regex re(check);
            if (std::regex_match(name, re)) {
                truthMatch.emplace_back(name);
            }
        }
    }

    for (const auto& ireco : recoMatch) {
        auto itr = std::find(truthMatch.begin(), truthMatch.end(), ireco);
        if (itr != truthMatch.end()) {
            matches.emplace_back(ireco);
        }
    }

    return matches;
}

std::vector<std::string> Utils::getColumnsFromString(const std::string& formula,
                                                     const std::string& truthTreeName,
                                                     ROOT::RDF::RNode& node) {

    const std::vector<std::string> allColumns = node.GetColumnNames();

    std::vector<std::string> result;

    for (const auto& icolumn : allColumns) {
        std::string toCheck("");
        const auto strip = StringOperations::splitAndStripString(icolumn, ".");
        if ((strip.size() == 2) && (strip.at(0) == truthTreeName)) {
            toCheck = strip.at(1);
        }
        if (!toCheck.empty() && formula.find(toCheck) != std::string::npos) {
            result.emplace_back(toCheck);
        }
    }

    return result;
}

void Utils::mergeUnderOverFlow(TH1D* histo, const UnderOverFlowType& type) {
    if (type == UnderOverFlowType::NO_UNDER_OVER_FLOW_MERGE) return;

    const int bins = histo->GetNbinsX();

    if (type == UnderOverFlowType::MERGE_BOTH || type == UnderOverFlowType::MERGE_UNDERFLOW) {
        const double valueUnder = histo->GetBinContent(0);
        const double errorUnder = histo->GetBinError(0);
        const double valueFirst = histo->GetBinContent(1);
        const double errorFirst = histo->GetBinError(1);

        histo->SetBinContent(1, valueUnder + valueFirst);
        histo->SetBinError(1, std::hypot(errorUnder, errorFirst));

        histo->SetBinContent(0, 0);
        histo->SetBinError(0, 0);
    }
    if (type == UnderOverFlowType::MERGE_BOTH || type == UnderOverFlowType::MERGE_OVERFLOW) {

        const double valueOver = histo->GetBinContent(bins+1);
        const double errorOver = histo->GetBinError(bins+1);
        const double valueLast = histo->GetBinContent(bins);
        const double errorLast = histo->GetBinError(bins);

        histo->SetBinContent(bins, valueOver + valueLast);
        histo->SetBinError(bins, std::hypot(errorOver, errorLast));

        histo->SetBinContent(bins+1, 0);
        histo->SetBinError(bins+1, 0);
    }
}

void Utils::mergeUnderOverFlow2D(TH2D* histo, const UnderOverFlowType& type1, const UnderOverFlowType& type2) {
    if (type1 == UnderOverFlowType::NO_UNDER_OVER_FLOW_MERGE && type2 == UnderOverFlowType::NO_UNDER_OVER_FLOW_MERGE) return;

    const int binsX = histo->GetNbinsX();
    const int binsY = histo->GetNbinsY();

    for (int ibinX = 1; ibinX <= binsX; ++ibinX) {
        if (type2 == UnderOverFlowType::MERGE_BOTH || type2 == UnderOverFlowType::MERGE_UNDERFLOW) {
            const double valueUnder = histo->GetBinContent(ibinX, 0);
            const double errorUnder = histo->GetBinError(ibinX, 0);
            const double valueFirst = histo->GetBinContent(ibinX, 1);
            const double errorFirst = histo->GetBinError(ibinX, 1);

            histo->SetBinContent(ibinX, 1, valueUnder + valueFirst);
            histo->SetBinError(ibinX, 1, std::hypot(errorUnder, errorFirst));

            histo->SetBinContent(ibinX, 0, 0);
            histo->SetBinError(ibinX, 0, 0);
        }
        if (type2 == UnderOverFlowType::MERGE_BOTH || type2 == UnderOverFlowType::MERGE_OVERFLOW) {

            const double valueOver = histo->GetBinContent(ibinX, binsY+1);
            const double errorOver = histo->GetBinError(ibinX, binsY+1);
            const double valueLast = histo->GetBinContent(ibinX, binsY);
            const double errorLast = histo->GetBinError(ibinX, binsY);

            histo->SetBinContent(ibinX, binsY, valueOver + valueLast);
            histo->SetBinError(ibinX, binsY, std::hypot(errorOver, errorLast));

            histo->SetBinContent(ibinX, binsY+1, 0);
            histo->SetBinError(ibinX, binsY+1, 0);
        }
    }
    for (int ibinY = 1; ibinY <= binsY; ++ibinY) {
        if (type1 == UnderOverFlowType::MERGE_BOTH || type1 == UnderOverFlowType::MERGE_UNDERFLOW) {
            const double valueUnder = histo->GetBinContent(0, ibinY);
            const double errorUnder = histo->GetBinError(0, ibinY);
            const double valueFirst = histo->GetBinContent(1, ibinY);
            const double errorFirst = histo->GetBinError(1, ibinY);

            histo->SetBinContent(1, ibinY, valueUnder + valueFirst);
            histo->SetBinError(1, ibinY, std::hypot(errorUnder, errorFirst));

            histo->SetBinContent(0, ibinY, 0);
            histo->SetBinError(0, ibinY, 0);
        }
        if (type1 == UnderOverFlowType::MERGE_BOTH || type1 == UnderOverFlowType::MERGE_OVERFLOW) {

            const double valueOver = histo->GetBinContent(binsX+1, ibinY);
            const double errorOver = histo->GetBinError(binsX+1, ibinY);
            const double valueLast = histo->GetBinContent(binsX, ibinY);
            const double errorLast = histo->GetBinError(binsX, ibinY);

            histo->SetBinContent(binsX, ibinY, valueOver + valueLast);
            histo->SetBinError(binsX, ibinY, std::hypot(errorOver, errorLast));

            histo->SetBinContent(binsX+1, ibinY, 0);
            histo->SetBinError(binsX+1, ibinY, 0);
        }
    }
}

bool Utils::checkTreeExists(const std::string& path, const std::string& tree) {
    std::unique_ptr<TFile> f(TFile::Open(path.c_str(), "READ"));
    if (!f) return false;

    const bool result = f->GetListOfKeys()->Contains(tree.c_str());

    f->Close();

    return result;
}

std::vector<std::string> Utils::selectedPathsWithTree(const std::vector<std::string>& paths, const std::string& tree) {
    std::vector<std::string> result;
    for (const auto& ipath : paths) {
        if (!Utils::checkTreeExists(ipath, tree)) {
            LOG(INFO) << "Skipping path: " << ipath << " as it does not have tree: " << tree << "\n";
            continue;
        }

        result.emplace_back(ipath);
    }

    return result;
}
