// Class include
#include "TRExFitter/MultiFit.h"

// Framework includes
#include "TRExFitter/ConfigParser.h"
#include "TRExFitter/ConfigReaderMulti.h"
#include "TRExFitter/StatusLogbook.h"
#include "TRExFitter/TRExFit.h"

// ROOT includes
#include "TSystem.h"

// c++ includes
#include <algorithm>

#define _STRINGIZE(x) #x
#define STRINGIZE(x) _STRINGIZE(x)

//_______________________________________________________________________________________
//
ConfigReaderMulti::ConfigReaderMulti(MultiFit *multiFitter) :
    fMultiFitter(multiFitter),
    fGlobalSuffix(""),
    fRunLHscan(true),
    fLHscanVariable(""),
    fLHscanStep(-1),
    fLHscanStepY(-1){
    WriteInfoStatus("ConfigReaderMulti::ConfigReaderMulti", "Started reading the config for multifit");
}

//_______________________________________________________________________________________
//
int ConfigReaderMulti::ReadFullConfig(const std::string& fileName, const std::string& opt, const std::string& option){
    // initialize ConfigParser for the actual config
    fParser.ReadFile(fileName);

    // initialize checker COnfigParser to cross check the input
    ConfigParser refConfig;
    TString homeArea(gSystem->Getenv("TREXFITTER_HOME") ? "$TREXFITTER_HOME" : "$DATAPATH");
#ifdef TREXFITTER_HOME
    homeArea = std::string(STRINGIZE(TREXFITTER_HOME));
#endif
    TString file = "multiFitSchema.config";
    auto* expandPath = gSystem->ExpandPathName(homeArea+":./");
    gSystem->FindFile(expandPath,file);
    if (file == "") {
        WriteErrorStatus("ConfigReaderMulti::ReadFullConfig", "jobSchema.config not found. Are you running from the main working directory?");
        exit(EXIT_FAILURE);
    }
    delete [] expandPath;
    refConfig.ReadFile(static_cast<std::string>(file.Data()));
    int sc = fParser.CheckSyntax(&refConfig);

    if (sc != 0) return sc;

    // syntax of the config is ok
    // read different types of settings
    if (option != ""){
        sc+= ReadCommandLineOptions(option);
    }

    sc+= ReadJobOptions();

    sc+= ReadLimitOptions();

    sc+= ReadSignificanceOptions();

    sc+= ReadFitOptions(opt, option);

    if (option != ""){
        sc+= ReadCommandLineOptions(option);
    }

    sc += PostConfig();

    // make directory
    gSystem->mkdir(fMultiFitter->fOutDir.c_str());

    return sc;
}

//_______________________________________________________________________________________
//
int ConfigReaderMulti::ReadCommandLineOptions(const std::string &option){
    // Read options (to skip stuff, or include only some regions, samples, systs...)
    // Syntax: .. .. Regions=ge4jge2b:Exclude=singleTop,wjets
    std::map< std::string,std::string > optMap;

    int sc(0);

    std::vector< std::string > optVec = Common::Vectorize(option,':');
    for(const std::string& iopt : optVec){
        std::vector< std::string > optPair;
        optPair = Common::Vectorize(iopt,'=');
        if (optPair.size() < 2){
            WriteErrorStatus("ConfigReaderMulti::ReadCommandLineOptions", "Cannot read your command line option, please check this!");
            ++sc;
        } else {
            optMap[optPair[0]] = optPair[1];
        }
    }

    if(optMap["Ranking"]!=""){
        fMultiFitter->fRankingOnly = optMap["Ranking"];
    }
    if(optMap["GroupedImpact"]!=""){
        fMultiFitter->fGroupedImpactCategory = optMap["GroupedImpact"];
    }

    if(optMap["Suffix"]!=""){
        fGlobalSuffix = optMap["Suffix"];
    }

    if(optMap["RunLHscan"]!="" && optMap["RunLHscan"]=="FALSE"){
        fRunLHscan = false;
    }
    if(optMap["LHscanVariable"]!=""){
        fLHscanVariable = optMap["LHscanVariable"];
    }
    if(optMap["LHscanStep"] != ""){
        fLHscanStep = atoi(optMap["LHscanStep"].c_str());
    }
    if(optMap["LHscanStepY"] != ""){
        fLHscanStepY = atoi(optMap["LHscanStepY"].c_str());
    }

    if(optMap["Regions"]!=""){
        fMultiFitter->fOnlyRegions = Common::Vectorize(optMap["Regions"],',');
    }
    if(optMap["BlindedParameters"]!=""){
        fMultiFitter->fBlindedParams = Common::Vectorize(optMap["BlindedParameters"],',');
    }
    if(optMap["NumCPU"]!=""){
        try {
            fMultiFitter->fCPU = std::stoi(optMap["NumCPU"]);
            if (fMultiFitter->fCPU <= 0) {
                WriteErrorStatus("ConfigReaderMulti::ReadCommandLineOptions", "NumCPU must be a positive integer!");
                ++sc;
            }
        }
        catch (const std::invalid_argument & e) {
            WriteErrorStatus("ConfigReaderMulti::ReadCommandLineOptions", "NumCPU must be an integer!");
            ++sc;
        }
    } else if (optMap["SignificanceToysSeed"] != "") {
        try {
            fMultiFitter->fSignificanceToysSeed = std::stoi(optMap["SignificanceToysSeed"]);
        }
        catch (const std::invalid_argument & e) {
            WriteErrorStatus("ConfigReaderMulti::ReadCommandLineOptions", "SignificanceToysSeed must be an int!");
            ++sc;
        }
    } else if (optMap["LimitToysSeed"] != "") {
        try {
            fMultiFitter->fLimitToysSeed = std::stoi(optMap["LimitToysSeed"]);
        }
        catch (const std::invalid_argument & e) {
            WriteErrorStatus("ConfigReaderMulti::ReadCommandLineOptions", "LimitToysSeed must be an int!");
            ++sc;
        }
    } else if(optMap["ToysSeed"] != ""){
         fMultiFitter->fToysSeed = std::stoi(optMap["ToysSeed"]);
    }

    return sc;
}

//_______________________________________________________________________________________
//
int ConfigReaderMulti::ReadJobOptions() {

    int sc(0);

    std::string param = "";
    const ConfigSet *confSet = fParser.GetConfigSet("MultiFit");
    if (confSet == nullptr){
        WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "Cannot find 'MultiFit' in your config which is required. Please check this!");
        ++sc;
        return sc;
    }

    fMultiFitter->fName = Common::CheckName(confSet->GetValue());

    // Set POIName
    param = confSet->Get("POIName");
    if( param != "" ) {
        const auto tmp =  Common::Vectorize(param, ',');
        for (const auto& i : tmp) {
            fMultiFitter->AddPOI(i);
        }
    }

    // Set OutputDir
    param = confSet->Get("OutputDir");
    if(param !=""){
        fMultiFitter->fDir = Common::CheckName(param);
        if(fMultiFitter->fDir.back() != '/') fMultiFitter->fDir += '/';
        fMultiFitter->fOutDir = fMultiFitter->fDir + fMultiFitter->fName;
        gSystem->mkdir((fMultiFitter->fOutDir).c_str(), true);
    }
    else{
        fMultiFitter->fOutDir = "./" + fMultiFitter->fName;
    }

    // Set Label
    param = confSet->Get("Label");
    if( param != "") fMultiFitter->fLabel = Common::RemoveQuotes(param);

    // Set LumiLabel
    param = confSet->Get("LumiLabel");
    if( param != "") fMultiFitter->fLumiLabel = Common::RemoveQuotes(param);

    // Set CmeLabel
    param = confSet->Get("CmeLabel");
    if( param != "") fMultiFitter->fCmeLabel = Common::RemoveQuotes(param);

    // Set Label of combination
    param = confSet->Get("CombiLabel");
    if( param != "") fMultiFitter->fCombiLabel = Common::RemoveQuotes(param);

    // Set SaveSuf
    param = confSet->Get("SaveSuf");
    if( param != "") fMultiFitter->fSaveSuf = Common::RemoveQuotes(param);
    else fMultiFitter->fSaveSuf             = fGlobalSuffix;

    // Set ShowObserved
    param = confSet->Get("ShowObserved");
    if( param != ""){
        fMultiFitter->fShowObserved = Common::StringToBoolean(param);
    }

    // Set LimitTitle
    param = confSet->Get("LimitTitle");
    if( param != "") fMultiFitter->fLimitTitle = Common::RemoveQuotes(param);
    // --- these lines should be removed at some point, since now we protect the text inside ""
    if(fMultiFitter->fLimitTitle.find("95CL")!=std::string::npos){
         fMultiFitter->fLimitTitle.replace(fMultiFitter->fLimitTitle.find("95CL"),4,"95% CL");
    }
    // ---

    // Ser POITitle
    param = confSet->Get("POITitle");
    if (param != "") {
        const auto vec = Common::Vectorize(param, ',');
        if (vec.size () != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POITitle' option but you didn't pass the same number of parameters as the number of POIs. Please check this!");
            ++sc;
        }
        fMultiFitter->fPOITitle = vec;
     } else {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fPOITitle.emplace_back("#mu");
        }
     }

    // Set CompareLimits
    param = confSet->Get("CompareLimits");
    if( param != ""){
        fMultiFitter->fCompareLimits = Common::StringToBoolean(param);
    }

    // Ser ComparePOI
    param = confSet->Get("ComparePOI");
    if( param != ""){
        fMultiFitter->fComparePOI = Common::StringToBoolean(param);
    }

    // Ser CompareEFT
    param = confSet->Get("CompareEFT");
    if( param != ""){
        fMultiFitter->fCompareEFT = Common::StringToBoolean(param);
    }

    // Set ComparePulls
    param = confSet->Get("ComparePulls");
    if( param != "" ){
        fMultiFitter->fComparePulls = Common::StringToBoolean(param);
    }

    // Set PlotCombCorrMatrix
    param = confSet->Get("PlotCombCorrMatrix");
    if (param != ""){
        fMultiFitter->fPlotCombCorrMatrix = Common::StringToBoolean(param);
    }

    // Set CorrelationThreshold
    param = confSet->Get("CorrelationThreshold");
    if( param != ""){
        TRExFitter::CORRELATIONTHRESHOLD = atof(param.c_str());
    }

    // Set UseGammasForCorr
    param = confSet->Get("UseGammasForCorr");
    if( param != ""){
        fMultiFitter->fUseGammasForCorr = Common::StringToBoolean(param);
    }

    // Set Combine
    param = confSet->Get("Combine");
    if( param != ""){
        fMultiFitter->fCombine = Common::StringToBoolean(param);
    }

    // Set Compare
    param = confSet->Get("Compare");
    if( param != ""){
        fMultiFitter->fCompare = Common::StringToBoolean(param);
    }

    // Set StatOnly
    param = confSet->Get("StatOnly");
    if( param != "" ){
        fMultiFitter->fStatOnly = Common::StringToBoolean(param);
        WriteWarningStatus("ConfigReaderMulti::ReadJobOtions", "StatOnlyFit option is deprecated for obtaining stat-only uncertainty. Please, use the covariance matrix breakdown");
    }

    // Set IncludeStatOnly
    param = confSet->Get("IncludeStatOnly");
    if( param != ""){
        fMultiFitter->fIncludeStatOnly = Common::StringToBoolean(param);
        if (fMultiFitter->fIncludeStatOnly) {
            fMultiFitter->fUnfoldingShowStat = true;
        }
    }

    // Set POILabel
    param = confSet->Get("POILabel");
    if (param != "") {
        const auto vec = Common::Vectorize(param, ',');
        if (vec.size () != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POILabel' option but you didn't pass the same number of parameters as the number of POIs. Please check this!");
            ++sc;
        }
        fMultiFitter->fPOIName = vec;
     } else {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fPOIName.emplace_back("#mu");
        }
     }

    // Set POINominal
    param = confSet->Get("POINominal");
    if (param != "") {
        const auto vec = Common::Vectorize(param, ',');
        if (vec.size () != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POINominal' option but you didn't pass the same number of parameters as the number of POIs. Please check this!");
            ++sc;
        }
        for (const auto& ivec : vec) {
            fMultiFitter->fPOINominal.emplace_back(std::stof(ivec));
        }
     } else {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fPOINominal.emplace_back(1);
        }
     }

    // Set POIRange
    param = confSet->Get("POIRange");
    if( param != ""){
        const auto tmp = Common::Vectorize(param, ',');
        if (tmp.size() != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POIRange' option but you didn't pass the same number of parametrs as the number of POIs. Please check this!");
            ++sc;
        }
        for (const auto& irange : tmp) {
            const auto vec = Common::Vectorize(irange,':');
            if (vec.size()==2 ) {
                fMultiFitter->fPOIMin.emplace_back(atof( vec[0].c_str() ));
                fMultiFitter->fPOIMax.emplace_back(atof( vec[1].c_str() ));
            } else {
                WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POIRange' option but you didn't provide valid setting. Please check this!");
                ++sc;
            }
        }
    }

    // Set LimitMax
    param = confSet->Get("LimitMax");
    if( param != "" ) {
        fMultiFitter->fLimitMax = atof( param.c_str() );
    }

    // Set POIPrecision
    param = confSet->Get("POIPrecision");
    if( param != "" ) {
        const auto tmp = Common::Vectorize(param, ',');
        if (tmp.size() != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POIPrecision' option but you didn't pass the same number of parametrs as the number of POIs. Please check this!");
            ++sc;
        }
        for (const auto& i : tmp) {
            fMultiFitter->fPOIPrecision.emplace_back(Common::RemoveQuotes(i).c_str());
        }
    }

    //Set DataName
    param = confSet->Get("DataName");
    if( param != "" ) fMultiFitter->fDataName = Common::RemoveQuotes(param);

    // Set FitType
    param = confSet->Get("FitType");
    if( param != "" ){
        std::transform(param.begin(), param.end(), param.begin(), ::toupper);
        if(param=="SPLUSB")      fMultiFitter->fFitType = 1;
        else if(param=="BONLY")  fMultiFitter->fFitType = 2;
        else if(param=="UNFOLDING")  fMultiFitter->fFitType = 3;
        else {
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'FitType' option but you didn't provide valid setting. Using default (SPLUSB)");
            fMultiFitter->fFitType = 1;
        }
    }

    // Set NPCategories
    param = confSet->Get("NPCategories");
    if( param != "" ) {
        std::vector<std::string> categ = Common::Vectorize(param,',');
        for(const std::string &icat : categ)
            fMultiFitter->fNPCategories.push_back(icat);
    }

    // Set SetRandomInitialNPval
    param = confSet->Get("SetRandomInitialNPval");
    if( param != ""){
        fMultiFitter->fUseRnd = true;
        fMultiFitter->fRndRange = atof(param.c_str());
    }

    // Set SetRandomInitialNPvalSeed
    param = confSet->Get("SetRandomInitialNPvalSeed");
    if( param != ""){
        fMultiFitter->fRndSeed = atol(param.c_str());
    }

    // Set NumCPU
    param = confSet->Get("NumCPU");
    if( param != "" ){
        fMultiFitter->fCPU = atoi( param.c_str());
        if (fMultiFitter->fCPU <= 0) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "NumCPU must be a positive integer!");
            ++sc;
        }
    }

    // Set FastFit
    param = confSet->Get("FastFit");
    if (param != ""){
        fMultiFitter->fFastFit = Common::StringToBoolean(param);
    }

    // Set FastFitForRanking
    param = confSet->Get("FastFitForRanking");
    if (param != ""){
        fMultiFitter->fFastFitForRanking = Common::StringToBoolean(param);
    }

    // Set NuisParListFile
    param = confSet->Get("NuisParListFile");
    if( param != "" ) fMultiFitter->fNuisParListFile = Common::RemoveQuotes(param);

    // Set PlotSoverB
    param = confSet->Get("PlotSoverB");
    if (param != ""){
        fMultiFitter->fPlotSoverB = Common::StringToBoolean(param);
    }

    // Set SignalTitle
    param = confSet->Get("SignalTitle");
    if( param != "" ) fMultiFitter->fSignalTitle = Common::RemoveQuotes(param);

    // Set FitResultsFile
    param = confSet->Get("FitResultsFile");
    if( param != "" ) fMultiFitter->fFitResultsFile = Common::RemoveQuotes(param);

    // Set LimitsFile
    param = confSet->Get("LimitsFile");
    if( param != "" ) fMultiFitter->fLimitsFile = Common::RemoveQuotes(param);

    // Set BonlySuffix
    param = confSet->Get("BonlySuffix");
    if( param != "" ) fMultiFitter->fBonlySuffix = Common::RemoveQuotes(param);

    // Set ShowSystForPOI
    param = confSet->Get("ShowSystForPOI");
    if( param != ""){
        fMultiFitter->fShowSystForPOI = Common::StringToBoolean(param);
    }

    // Set doLHscan
    param = confSet->Get("doLHscan");
    if( fRunLHscan && param != "" ){
        if (fLHscanVariable==""){
            fMultiFitter->fVarNameLH = Common::Vectorize(param,',');
        } else {
            fMultiFitter->fVarNameLH.emplace_back(fLHscanVariable);
        }
    }

    // Set do2DLHscan
    param = confSet->Get("do2DLHscan");
    if( param != "" ){
        const std::vector<std::string> tmp = Common::Vectorize(param,':');
        for (const auto& ivec : tmp){
            const std::vector<std::string> v = Common::Vectorize(ivec,',');
            if (v.size() == 2){
                fMultiFitter->fVarName2DLH.emplace_back(v);
            } else {
                WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'do2DLHscan' option but did not provide correct input. Ignoring");
            }
        }
    }

    // Set LHscanMin
    param = confSet->Get("LHscanMin");
    if ( fRunLHscan && param != "" ) {
        if (fMultiFitter->fVarNameLH.size() == 0 && fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanMin' option but did not set doLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanMin = std::stof(param);
        }
    }

    // Set LHscanMax
    param = confSet->Get("LHscanMax");
    if ( fRunLHscan && param != "" ) {
        if (fMultiFitter->fVarNameLH.size() == 0 && fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanMax' option but did not set doLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanMax = std::stof(param);
        }
    }
    // Set LHscanMin for second variable
    param = confSet->Get("LHscanMinY");
    if ( param != "" ) {
        if (fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanMinY' option but did not set do2DLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanMinY = std::stof(param);
        }
    }

    // Set LHscanMax for second variable
    param = confSet->Get("LHscanMaxY");
    if ( param != "" ) {
        if (fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanMaxY' option but did not set do2DLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanMaxY = std::stof(param);
        }
    }


    // Set LHscanSteps
    param = confSet->Get("LHscanSteps");
    if ( param != "" ) {
        if (fMultiFitter->fVarNameLH.size() == 0 && fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanSteps' option but did not set doLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanSteps = std::stoi(param);
            if(fMultiFitter->fLHscanSteps < 3 || fMultiFitter->fLHscanSteps > 100){
                WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "LHscanSteps is smaller than 3 or larger than 100, setting to defaut (30)");
                fMultiFitter->fLHscanSteps = 30;
            }
        }
    }

    // Set LHscanSteps for second variable
    param = confSet->Get("LHscanStepsY");
    if ( param != "" ) {
        if (fMultiFitter->fVarName2DLH.size() == 0){
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'LHscanStepsY' option but did not set do2DLHscan. Ignoring");
        } else {
            fMultiFitter->fLHscanStepsY = std::stoi(param);
            if(fMultiFitter->fLHscanStepsY < 3 || fMultiFitter->fLHscanStepsY > 100){
                WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "LHscanStepsY is smaller than 3 or larger than 100, setting to LHscanSteps");
                fMultiFitter->fLHscanStepsY = fMultiFitter->fLHscanSteps;
            }
        }
    }
    else {
        fMultiFitter->fLHscanStepsY = fMultiFitter->fLHscanSteps;
    }



    // Set LHscanStep (-1 = process all points, otherwise process the single point only)
    if (fLHscanStep != -1) {
        if (fLHscanStep < -1 || fLHscanStep >= fMultiFitter->fLHscanSteps) {
            ++sc;
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "Invalid command line option for LHscanStep, please check!");
        }
        fMultiFitter->fLHscanStep = fLHscanStep;
    }

    if (fLHscanStepY != -1) {
        if (fLHscanStepY < -1 || fLHscanStepY >= fMultiFitter->fLHscanStepsY) {
            ++sc;
            WriteErrorStatus("ConfigReaderMulti::ReadFitOptions", "Invalid command line option for LHscanStepY, please check!");
        }
        fMultiFitter->fLHscanStepY = fLHscanStepY;
    }

    // Set ShowTotalOnly
    param = confSet->Get("ShowTotalOnly");
    if ( param != "" ) {
        fMultiFitter->fShowTotalOnly = Common::StringToBoolean(param);
    }

    // Set PlotOptions
    param = confSet->Get("PlotOptions");
    if( param != ""){
        std::vector<std::string> vec = Common::Vectorize(param,',');
        if( std::find(vec.begin(), vec.end(), "PREFITONPOSTFIT")   !=vec.end() )  TRExFitter::PREFITONPOSTFIT= true;
    }

    // Set POIAsimovl
    param = confSet->Get("POIAsimov");
    if( param != "" ) {
        const auto tmp = Common::Vectorize(param, ',');
        if (tmp.size() != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "You specified 'POIAsimov' option but you didn't pass the same number of parametrs as the number of POIs. Please check this!");
            ++sc;
        }
        for (const auto& i : tmp) {
            fMultiFitter->fPOIAsimov.emplace_back(std::stof(i));
        }
    } else {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fPOIAsimov.emplace_back(1);
        }
    }

    // Set POIInitial
    param = confSet->Get("POIInitial");
    if( param != ""){
        const std::vector<std::string> tmp = Common::Vectorize(param, ',');
        if (tmp.size() != fMultiFitter->fPOIs.size()) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "Number of POI initial values does not match the number of POIs");
            return 1;
        }

        for (std::size_t i = 0; i < tmp.size(); ++i) {
            double value(0);
            try {
                value = std::stof(tmp.at(i));
            } catch (...) {
                WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "Cannot convert POIInitial element to float");
                return 1;
            }
            fMultiFitter->fPOIInitials.emplace_back(fMultiFitter->fPOIs.at(i), value);
        }
    }

    // Set HEPDataFormat
    param = confSet->Get("HEPDataFormat");
    if( param != ""){
        fMultiFitter->fHEPDataFormat = Common::StringToBoolean(param);
    }

    // Set UheppFormat
    param = confSet->Get("UheppFormat");
    if( param != ""){
        fMultiFitter->fUheppFormat = Common::StringToBoolean(param);
    }

    // Set FitStrategy
    param = confSet->Get("FitStrategy");
    if (param != "") {
        fMultiFitter->fFitStrategy = std::stoi(param);
        if (fMultiFitter->fFitStrategy > 3) {
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "FitStrategy > 3, setting to default (-1)");
            fMultiFitter->fFitStrategy = -1;
        }
    }

    // Set BinnedLikelihoodOptimization
    param = confSet->Get("BinnedLikelihoodOptimization");
    if (param != "") {
        fMultiFitter->fBinnedLikelihood = Common::StringToBoolean(param);
    }

    // Set UseHesseBeforeMigrad
    param = confSet->Get("UseHesseBeforeMigrad");
    if (param != "") {
        fMultiFitter->fUseHesseBeforeMigrad = Common::StringToBoolean(param);
    }

    // Set UsePOISinRanking
    param = confSet->Get("UsePOISinRanking");
    if (param != "") {
        fMultiFitter->fUsePOISinRanking = Common::StringToBoolean(param);
    }

    // Set Regions
    param = confSet->Get("Regions");
    if (param != "") {
        fMultiFitter->fOnlyRegions = Common::Vectorize(param,',');
    }

    param = confSet->Get("MultiStageFit");
    if (param != "") {
        fMultiFitter->fSpeedUpFit = Common::StringToBoolean(param);
    }

    param = confSet->Get("NPCutOff");
    if (param != "") {
        fMultiFitter->fNPCutOff = std::stof(param);
        if (fMultiFitter->fNPCutOff < 0. || fMultiFitter->fNPCutOff > 1.0) {
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "NPCutOff is < 0 or > 1, this is not a valid option, setting to default (0.3)");
            fMultiFitter->fNPCutOff = 0.3;
        }
    }

    param = confSet->Get("PlotUnfoldedData");
    if (param != "") {
        fMultiFitter->fPlotUnfoldedData = Common::StringToBoolean(param);
        if (fMultiFitter->fPlotUnfoldedData && fMultiFitter->fFitType != 3) {
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "PlotUnfoldedData set to TRUE, but the FitType is not UNFOLDING, ignoring");
            fMultiFitter->fPlotUnfoldedData = false;
        }
    }

    param = confSet->Get("UnfoldingShowStatOnlyError");
    if (param != "") {
        fMultiFitter->fUnfoldingShowStat = Common::StringToBoolean(param);
    }

    param = confSet->Get("UnfoldingShowUncertaintyBreakdown");
    if (param != "") {
        fMultiFitter->fUnfoldingShowUncertaintyBreakdown = Common::StringToBoolean(param);
    }

    param = confSet->Get("UnfoldingUncertaintyBreakdownTotal");
    if (param != "") {
        fMultiFitter->fUnfoldingUncertaintyBreakdownTotal = Common::StringToBoolean(param);
    }

    param = confSet->Get("PlotGammas");
    if (param != "") {
        fMultiFitter->fPlotGammas = Common::StringToBoolean(param);
    }

    param = confSet->Get("BlindedParameters");
    if( param != "" ){
        const std::vector<std::string> tmp = Common::Vectorize( param,',');
        fMultiFitter->fBlindedParams = std::move(tmp);
    }

    param = confSet->Get("RankingPOIName");
    if( param != ""){
        fMultiFitter->fRankingPOIName = Common::Vectorize(param, ',');
    }

    param = confSet->Get("ToleranceScale");
    if( param != ""){
        fMultiFitter->fToleranceScale = std::stod(param);
    }

    param = confSet->Get("ShiftGlobalObservablesInRanking");
    if (param != ""){
        fMultiFitter->fShiftGlobalObservablesInRanking = Common::StringToBoolean(param);
    }

    // Set RankingUpperAxisNdivision
    param = confSet->Get("RankingUpperAxisNdivision");
    if( param != ""){
        const auto tmp = Common::Vectorize(param, ',');
        std::vector<int> v;
        for (const auto& i : tmp) {
            v.emplace_back(std::stoi(i));
        }
        fMultiFitter->fRankingUpperAxisNdivision = v;
    }

    // Set RankingPOIAxisScale
    param = confSet->Get("RankingPOIAxisScale");
    if( param != ""){
        const auto tmp = Common::Vectorize(param, ',');
        std::vector<double> v;
        for (const auto& i : tmp) {
            v.emplace_back(std::stof(i));
        }
        fMultiFitter->fRankingPOIAxisScale = v;
    }

    param = confSet->Get("RankingNPfraction");
    if (param != "") {
        const double fraction = std::stof(param);
        if (fraction < 0. || fraction > 1.) {
            WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "RankingNPfraction < 0 or > 1");
            ++sc;
            return sc;
        }
        fMultiFitter->fRankingNpFraction = fraction;
    }

    param = confSet->Get("MaximumNumberFCNcalls");
    if (param != "") {
        const int max = std::stoi(param);
        if (max < 0) {
            WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", "\"MaximumNumberFCNcalls\" is < 0. Ignoring the option");
        } else {
            fMultiFitter->fMaximumNumberFCNcalls = max;
        }
    }

    param = confSet->Get("UseModularL");
    if (param != ""){
        fMultiFitter->fUseModularL = Common::StringToBoolean(param);
    }

    param = confSet->Get("NLLOffset");
    if (param != "") {
        // Ensure lowercase to match RooFit documentation
        std::transform(param.begin(), param.end(), param.begin(), ::tolower);
        fMultiFitter->fNLLOffset = param;
    }

    param = confSet->Get("FitToys");
    if (param != ""){
        fMultiFitter->fFitToys = std::stoi(param);
    }

    param = confSet->Get("ToysSeed");
    if (param != ""){
        fMultiFitter->fToysSeed = std::stoi(param);
    }

    param = confSet->Get("ToysHistoNbins");
    if (param != ""){
        fMultiFitter->fToysHistoNbins = std::stoi(param);
    }

    param = confSet->Get("ToysOnlyStatFluctuation");
    if (param != ""){
        fMultiFitter->fToysSetStatOnlyFluctuation = Common::StringToBoolean(param);
    }

    param = confSet->Get("FitToysRandomInitialNormFactorValues");
    if (param != "") {
        const std::vector<std::string> singleParam = Common::Vectorize(param, ',');
        for (const auto& iparam : singleParam) {
            const std::vector<std::string> values = Common::Vectorize(iparam, ':');
            if (values.size() != 3) {
                WriteErrorStatus("ConfigReaderMulti::ReadJonOptions", "Wrong input for \"FitToysRandomInitialNormFactorValues\"");
                return ++sc;
            }
            const std::string& nfName = values.at(0);
            const double min = std::stod(values.at(1));
            const double max = std::stod(values.at(2));

            auto itr = fMultiFitter->fToysRandomPOIStartingValues.find(nfName);
            if (itr != fMultiFitter->fToysRandomPOIStartingValues.end()) {
                WriteWarningStatus("ConfigReaderMulti::ReadJobOptions", nfName + " already set in the config for \"FitToysRandomInitialNormFactorValues\", ignoring");
            } else {
                fMultiFitter->fToysRandomPOIStartingValues.insert({nfName, std::make_pair(min, max)});
            }
        }
    }

    param = confSet->Get("ToysLHScanForAll");
    if (param != ""){
        fMultiFitter->fToysLHScanForAll = Common::StringToBoolean(param);
    }

    param = confSet->Get("FitToysLHscanCondition");
    if (param != "") {
        const std::vector<std::string> singleParam = Common::Vectorize(param, ',');
        for (const auto& iparam : singleParam) {
            const std::vector<std::string> values = Common::Vectorize(iparam, ':');
            if (values.size() != 3) {
                WriteErrorStatus("ConfigReaderMulti::ReadJobOptions", "Wrong input for \"FitToysLHscanCondition\"");
                return ++sc;
            }
            const std::string& nfName = values.at(0);
            const double min = std::stod(values.at(1));
            const double max = std::stod(values.at(2));

            fMultiFitter->fToysLHScanCondition.insert({nfName, std::make_pair(min, max)});
        }
    }

    return sc;
}

//__________________________________________________________________________________
//
int ConfigReaderMulti::ReadLimitOptions(){

    int sc(0);

    std::string param = "";

    const ConfigSet* confSet = fParser.GetConfigSet("Limit");
    if (confSet == nullptr){
        WriteDebugStatus("ConfigReader::ReadLimitOptions", "You do not have Limit option in the config. It is ok, we just want to let you know.");
        return 0; // it is ok to not have Fit set up
    }

    // Set POI
    param = confSet->Get("POI");
    if( param != "" ){
        fMultiFitter->fPOIforLimit = Common::RemoveQuotes(param);
        fMultiFitter->AddPOI(Common::RemoveQuotes(param));
    }

    // Set LimitType
    param = confSet->Get("LimitType");
    if( param != "" ){
        std::transform(param.begin(), param.end(), param.begin(), ::toupper);
        if( param == "ASYMPTOTIC" ){
            fMultiFitter->SetLimitType(TRExFit::LimitType::ASYMPTOTIC);
        }
        else if( param == "TOYS" ){
            fMultiFitter->SetLimitType(TRExFit::LimitType::TOYS);
        }
        else{
            WriteErrorStatus("ConfigReaderMulti::ReadLimitOptions", "Unknown LimitType argument : " + confSet->Get("LimitType"));
            ++sc;
        }
    }

    // Set LimitBlind
    param = confSet->Get("LimitBlind");
    if( param != "" ){
        fMultiFitter->fLimitIsBlind = Common::StringToBoolean(param);
    }

    // Set SignalInjection
    param = confSet->Get("SignalInjection");
    if( param != "" ){
        fMultiFitter->fSignalInjection = Common::StringToBoolean(param);
    }

    // Set SignalInjectionValue
    param = confSet->Get("SignalInjectionValue");
    if( param != "" ){
        fMultiFitter->fSignalInjectionValue = std::stof(param);
    }

    param = confSet->Get("ParamName");
    if( param != "" ){
        fMultiFitter->fLimitParamName = param;
    }

    param = confSet->Get("ParamValue");
    if( param != "" ){
        fMultiFitter->fLimitParamValue = std::stof(param);
    }

    param = confSet->Get("OutputPrefixName");
    if( param != "" ){
        fMultiFitter->fLimitOutputPrefixName = param;
    }

    param = confSet->Get("ConfidenceLevel");
    if( param != "" ){
        double conf = std::stod(param);
        if (conf <= 0. || conf >= 1.){
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "Confidence level is <= 0 or >=1. Setting to default 0.95");
            conf = 0.95;
        }
        fMultiFitter->fLimitsConfidence = conf;
    }

    param = confSet->Get("SplusBToys");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "SplusBToys is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitToysStepsSplusB = std::stoi(param);
        }
    }

    param = confSet->Get("BonlyToys");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "BonlyToys is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitToysStepsB = std::stoi(param);
        }
    }

    param = confSet->Get("ScanSteps");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "ScanSteps is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitToysScanSteps = std::stoi(param);
        }
    }

    param = confSet->Get("ScanMin");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "ScanMin is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitToysScanMin = std::stof(param);
        }
    }

    param = confSet->Get("ScanMax");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "ScanMax is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitToysScanMax = std::stof(param);
        }
    }

    param = confSet->Get("LimitPlot");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "LimitPlot is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitPlot = Common::StringToBoolean(param);
        }
    }

    param = confSet->Get("LimitFile");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "LimitFile is available only when TOYS are used");
        } else {
            fMultiFitter->fLimitFile = Common::StringToBoolean(param);
        }
    }

    param = confSet->Get("FitStrategy");
    if( param != "" ) {
        if (fMultiFitter->fLimitType != TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "FitStrategy is available only when ASYMPTOTIC limits are used");
        } else {
            fMultiFitter->fLimitFitStrategy = std::stoi(param);
        }
    }

    param = confSet->Get("ToysSeed");
    if (param != ""){
        fMultiFitter->fLimitToysSeed = std::stoi(param);
    }

    param = confSet->Get("UseNLLwithoutOffsetInLHscan");
    if (param != "") {
        fMultiFitter->fUseNllInLHscan = Common::StringToBoolean(param);
    }

    param = confSet->Get("UseHesse");
    if (param != "") {
        fMultiFitter->fUseHesse = Common::StringToBoolean(param);
    }

    param = confSet->Get("ToysUsexRooFit");
    if( param != "" ) {
        if (fMultiFitter->fLimitType == TRExFit::LimitType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadLimitOptions", "ToysUsexRooFit is available only when TOYS are used");
        } else {
	    std::transform(param.begin(), param.end(), param.begin(), ::toupper);
	    if (param == "FALSE") {
		fMultiFitter->fLimitToysUsexRooFit = TRExFit::ToysUsexRooFit::FALSE;
	    } else if (param == "TRUE") {
		fMultiFitter->fLimitToysUsexRooFit = TRExFit::ToysUsexRooFit::TRUE;
	    } else if (param == "AUTO") {
		fMultiFitter->fLimitToysUsexRooFit = TRExFit::ToysUsexRooFit::AUTO;
	    } else {
		WriteErrorStatus("ConfigReaderMulti::ReadLimitOptions", "Unknown ToysUsexRooFit argument : " + confSet->Get("ToysUsexRooFit"));
		++sc;
	    }
        }
    }


    return sc;
}

//__________________________________________________________________________________
//
int ConfigReaderMulti::ReadSignificanceOptions(){

    int sc(0);

    std::string param = "";

    const ConfigSet* confSet = fParser.GetConfigSet("Significance");
    if (confSet == nullptr){
        WriteDebugStatus("ConfigReaderMulti::ReadSignificanceOptions", "You do not have Significance option in the config. It is ok, we just want to let you know.");
        return 0; // it is ok to not have Fit set up
    }

    // Set POI
    param = confSet->Get("POI");
    if( param != "" ){
        fMultiFitter->fPOIforSig = Common::RemoveQuotes(param);
        fMultiFitter->AddPOI(Common::RemoveQuotes(param));
    }

    // Set SignificanceType
    param = confSet->Get("SignificanceType");
    if( param != "" ){
        std::transform(param.begin(), param.end(), param.begin(), ::toupper);
        if(param == "ASYMPTOTIC"){
            fMultiFitter->SetSignificanceType(TRExFit::SignificanceType::ASYMPTOTIC);
        }
        else if(param == "TOYS"){
            fMultiFitter->SetSignificanceType(TRExFit::SignificanceType::TOYS);
        }
        else{
            WriteErrorStatus("ConfigReaderMulti::ReadSignificanceOptions", "Unknown SignificanceType argument : " + confSet->Get("SignificanceType"));
            ++sc;
        }
    }

    param = confSet->Get("SplusBToys");
    if( param != "" ) {
        if (fMultiFitter->fSignificanceType == TRExFit::SignificanceType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadSignificanceOptions", "SplusBToys is available only when TOYS are used");
        } else {
            fMultiFitter->fSignificanceToysStepsSplusB = std::stoi(param);
        }
    }

    param = confSet->Get("BonlyToys");
    if( param != "" ) {
        if (fMultiFitter->fSignificanceType == TRExFit::SignificanceType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadSignificanceOptions", "BonlyToys is available only when TOYS are used");
        } else {
            fMultiFitter->fSignificanceToysStepsB = std::stoi(param);
        }
    }

    param = confSet->Get("SignificancePlot");
    if( param != "" ) {
        if (fMultiFitter->fSignificanceType == TRExFit::SignificanceType::ASYMPTOTIC) {
            WriteWarningStatus("ConfigReaderMulti::ReadSignificanceOptions", "SignificancePlot is available only when TOYS are used");
        } else {
            fMultiFitter->fSignificancePlot = Common::StringToBoolean(param);
        }
    }

    // Set SignificanceBlind
    param = confSet->Get("SignificanceBlind");
    if( param != "" ){
        fMultiFitter->fSignificanceIsBlind = Common::StringToBoolean(param);
    }

    // Set POIAsimov
    param = confSet->Get("POIAsimov");
    if( param != "" ){
        fMultiFitter->fSignificancePOIAsimov = atof(param.c_str());
        fMultiFitter->fSignificanceDoInj = true;
    }

    param = confSet->Get("ParamName");
    if( param != "" ){
        fMultiFitter->fSignificanceParamName = param;
    }

    param = confSet->Get("ParamValue");
    if( param != "" ){
        fMultiFitter->fSignificanceParamValue = std::stof(param);
    }

    param = confSet->Get("OutputPrefixName");
    if( param != "" ){
        fMultiFitter->fSignificanceOutputPrefixName = param;
    }

    param = confSet->Get("ToysSeed");
    if (param != ""){
        fMultiFitter->fSignificanceToysSeed = std::stoi(param);
    }

    return sc;
}

//_______________________________________________________________________________________
//
int ConfigReaderMulti::ReadFitOptions(const std::string& opt, const std::string& options){

    int sc(0);

    int nFit = 0;

    while(true){
        const ConfigSet *confSet = fParser.GetConfigSet("Fit", nFit);
        if (confSet == nullptr) break;
        nFit++;

        // Set Options
        std::string fullOptions;
        std::string param = confSet->Get("Options");
        if(param!="" && options!="") fullOptions = options+";"+Common::RemoveQuotes(param);
        else if(param!="") fullOptions = Common::RemoveQuotes(param);
        else fullOptions = options;

        // name
        fMultiFitter->fFitNames.push_back(Common::CheckName(confSet->GetValue()));

        // Set Label
        param = confSet->Get("Label");
        std::string label = Common::CheckName(confSet->GetValue());
        if(param!="") label = Common::RemoveQuotes(param);

        // Set suf
        param = confSet->Get("LoadSuf");
        std::string loadSuf = "";
        if(param!="") loadSuf = Common::RemoveQuotes(param);
        else          loadSuf = fGlobalSuffix;

        // config file
        std::string confFile = "";
        param = confSet->Get("ConfigFile");
        if(param!="") confFile = Common::RemoveQuotes(param);

        // workspace
        std::string wsFile = "";
        param = confSet->Get("Workspace");
        if(param!="") wsFile = Common::RemoveQuotes(param);

        bool useInFit(true);
        param = confSet->Get("UseInFit");
        if (param != "") {
            std::transform(param.begin(), param.end(), param.begin(), ::toupper);
            if(param=="FALSE") {
                useInFit = false;
            }
        }

        bool useInComparison(true);
        param = confSet->Get("UseInComparison");
        if (param != "") {
            std::transform(param.begin(), param.end(), param.begin(), ::toupper);
            if(param=="FALSE") {
                useInComparison = false;
            }
        }


        fMultiFitter->AddFitFromConfig(confFile, opt, fullOptions, label, loadSuf, wsFile, useInFit, useInComparison);

        // Set FitResultsFile
        param = confSet->Get("FitResultsFile");
        if( param != "" ) fMultiFitter->fFitList[fMultiFitter->fFitList.size()-1]->fFitResultsFile = Common::RemoveQuotes(param);
        fMultiFitter->fLimitsFiles.push_back("");

        // Set LimitsFile
        param = confSet->Get("LimitsFile");
        if( param != "" ) fMultiFitter->fLimitsFiles[fMultiFitter->fFitList.size()-1] = Common::RemoveQuotes(param);

        // Set POIName
        param = confSet->Get("POIName");
        if (param != "") {
            const std::vector<std::string> vec = Common::Vectorize(param, ',');
            for (const auto& i : vec) {
                fMultiFitter->AddPOI(i);
            }
        }

        // Set Directory
        param = confSet->Get("Directory");
        if( param != "" ) fMultiFitter->fFitList[fMultiFitter->fFitList.size()-1]->fName = Common::RemoveQuotes(param);

        // Set InputName
        param = confSet->Get("InputName");
        if( param != "" ) fMultiFitter->fFitList[fMultiFitter->fFitList.size()-1]->fInputName = Common::RemoveQuotes(param);

        // Set EFTFitType
        param = confSet->Get("EFTFitType");
        if( param != "" ) fMultiFitter->fFitList[fMultiFitter->fFitList.size()-1]->fEFTFitType = Common::RemoveQuotes(param);
   }

    if (nFit == 0){
        WriteErrorStatus("ConfigReaderMulti::ReadFitOptions", "You need to provide at least one 'Fit' option. Please check this!");
        ++sc;
    }

    return sc;
}

//_______________________________________________________________________________________
//
int ConfigReaderMulti::PostConfig() {

    int sc(0);

    if (fMultiFitter->fRankingPOIName.empty()) {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fRankingPOIName.emplace_back("#mu");
        }
    } else if (fMultiFitter->fRankingPOIName.size() != fMultiFitter->fPOIs.size()) {
        WriteErrorStatus("ConfigReaderMulti::PostConfig", "Sizes of RankingPOIName and POIs do not match");
        ++sc;
    }

    if (fMultiFitter->fRankingUpperAxisNdivision.empty()) {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fRankingUpperAxisNdivision.emplace_back(510);
        }
    } else if (fMultiFitter->fRankingUpperAxisNdivision.size() != fMultiFitter->fPOIs.size()) {
        WriteErrorStatus("ConfigReaderMulti::PostConfig", "Sizes of RankingUpperAxisNdivision and POIs do not match");
        ++sc;
    }

    if (fMultiFitter->fRankingPOIAxisScale.empty()) {
        for (std::size_t i = 0; i < fMultiFitter->fPOIs.size(); ++i) {
            fMultiFitter->fRankingPOIAxisScale.emplace_back(1.0);
        }
    } else if (fMultiFitter->fRankingPOIAxisScale.size() != fMultiFitter->fPOIs.size()) {
        WriteErrorStatus("ConfigReaderMulti::PostConfig", "Sizes of RankingPOIAxisScale and POIs do not match");
        ++sc;
    }

    return sc;
}
