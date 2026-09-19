// Class include
#include "TRExFitter/ConfigParser.h"

// Framework includes
#include "TRExFitter/Common.h"
#include "TRExFitter/StatusLogbook.h"

// c++ includes
#include <algorithm>
#include <exception>
#include <filesystem>
#include <fstream>
#include <iostream>


// using namespace std;

//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
// -- Functions --
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------


//__________________________________________________________________________________
// Removes leading and trailing white spaces, removes everything after "%", removes '"'
std::string Fix(const std::string& s){
    if(s=="") return "";
    std::string ss = s.substr( 0, s.find_first_of('%') );
    replace( ss.begin(), ss.end(), '"', ' ');
    if (ss.find_first_not_of(' ')>=std::string::npos){
        ss = "";
    }
    else if (ss.find_first_not_of(' ')>0){
        ss=ss.substr(ss.find_first_not_of(' '),ss.find_last_not_of(' '));
    }
    else{
        ss=ss.substr(ss.find_first_not_of(' '),ss.find_last_not_of(' ')+1);
    }
    return ss;
}

//__________________________________________________________________________________
//
std::string First(const std::string& s){
    std::string first;
    first = s.substr( 0, s.find_first_of(':') );
    return Fix(first);
}

//__________________________________________________________________________________
//
std::string Second(const std::string& s){
    std::string second;
    second = s.substr( s.find_first_of(':')+1,std::string::npos );
    second = Common::RemoveComments(second);
    if(second==""){
        WriteErrorStatus("ConfigParser","No value set for parameter "+First(s)+" in the config.");
        exit(EXIT_FAILURE);
    }
    return second;
}

//_______________________________________________________________________________________
//
void ReplaceStringInPlace(std::string& subject, const std::string& search,
                                                const std::string& replace) {
    size_t pos = 0;
    while((pos = subject.find(search, pos)) != std::string::npos) {
        subject.replace(pos, search.length(), replace);
        pos += replace.length();
    }
}

//_______________________________________________________________________________________
// used to pre-read a config file to check single option values
std::string ReadValueFromConfig(const std::string& fileName,const std::string& option){
    std::string value = "";
    std::ifstream file(fileName.c_str());
    if(!file.is_open()) return value;
    std::string str;
    while(true){
        file >> str;
        if(!file.good()) break;
        if(str==(option+":")){
            file >> value;
            break;
        }
    }
    file.close();
    file.clear();
    return value;
}

//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
// -- Classes --
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------

//----------------------------------------------------------------------------------
// Config
//----------------------------------------------------------------------------------

//__________________________________________________________________________________
//
Config::Config() :
    fName(""),
    fValue("") {
}

//----------------------------------------------------------------------------------
// ConfigSet
//----------------------------------------------------------------------------------

//__________________________________________________________________________________
//
ConfigSet::ConfigSet() :
    fN(0),
    fName(""),
    fValue("") {
}

//__________________________________________________________________________________
//
void ConfigSet::SetConfig(const std::string& name,const std::string& value){
    // check if is name is there
    bool isThere = false;
    int index = -1;
    for(int i=0;i<fN;i++){
        if(fConfig[i].fName == name){
            isThere = true;
            index = i;
        }
    }
    if(!isThere){
        fConfig.emplace_back();
        fConfig.back().fName = name;
        fConfig.back().fValue = value;
        fN++;
    }
    else{
        fConfig[index].fName = name;
        fConfig[index].fValue = value;
    }
}

//__________________________________________________________________________________
//
std::string ConfigSet::Get(const std::string& name) const{
    for(int i=0;i<fN;i++){
        if(fConfig[i].fName == name){
            return fConfig[i].fValue;
        }
    }
    return "";
}

//__________________________________________________________________________________
//
std::string ConfigSet::operator[](const std::string& name) const{
    return Get(name);
}

//__________________________________________________________________________________
//
const Config& ConfigSet::GetConfig(int i) const{
    return fConfig[i];
}

//__________________________________________________________________________________
//
const std::string& ConfigSet::GetConfigName(int i) const{
    return fConfig[i].fName;
}

//__________________________________________________________________________________
//
const std::string& ConfigSet::GetConfigValue(int i) const{
    return fConfig[i].fValue;
}

//__________________________________________________________________________________
//
int ConfigSet::GetN() const{
    return fN;
}

//__________________________________________________________________________________
//
int ConfigSet::size() const{
    return fN;
}

//__________________________________________________________________________________
//
void ConfigSet::Set(const std::string& name,const std::string& value){
    fName = name;
    fValue = value;
}

//__________________________________________________________________________________
//
const std::string& ConfigSet::GetName() const{
    return fName;
}

//__________________________________________________________________________________
//
const std::string& ConfigSet::GetValue() const{
    return fValue;
}

//----------------------------------------------------------------------------------
// ConfigParser
//----------------------------------------------------------------------------------

//__________________________________________________________________________________
//
ConfigParser::ConfigParser() :
    fN(0) {
}

void ConfigParser::ResolvePath(std::string *config_address) {
    std::vector<std::string> elements = Common::SplitString(*config_address, "/");
    if (elements.size() == 0)   {
        return;
    }
    const bool absolute_path = elements[0] == "";

    for (unsigned int i = 0; i < elements.size(); )  {
        if (elements[i] == "" || elements[i] == ".")    {
            elements.erase(elements.begin() + i);
            if (i > 0)  {
                i--;
            }
            continue;
        }

        if (elements[i] != "..")    {
            if (i+1 < elements.size())  {
                if (elements[i+1] == "..")  {
                    elements.erase(elements.begin() + i);
                    elements.erase(elements.begin() + i);
                    if (i > 0)  {
                        i--;
                    }
                    continue;
                }
            }
        }
        i++;
    }
    *config_address = Common::join_strings(elements, "/");
    if (absolute_path)  {
        *config_address = "/" + *config_address;
    }
}

void ConfigParser::ReplaceFromReplacementFile(std::string* line, const std::map<std::string,std::string>& fReplacement){
    std::map<std::string,std::string>::const_iterator itr=fReplacement.begin();
    for ( ;itr!=fReplacement.end();++itr) {
        std::string oldV=itr->first;
        std::string newV=itr->second;
        ReplaceStringInPlace(*line, oldV, newV);
    }
}

std::map<std::string,std::string> ConfigParser::ParseReplacements(const std::vector<std::string>& lines_of_config, const std::string& fileName){
    std::string str;
    std::map<std::string,std::string> fReplacement;
    std::string replacementFileName="";
    // loop over the file once to automatically find the replacement fileName

    for (const std::string &line : lines_of_config) {
        str = line;
        replace( str.begin(), str.end(), '\n', ' ');
        replace( str.begin(), str.end(), '\r', ' ');
        replace( str.begin(), str.end(), '\t', ' ');
        if (str.find_first_not_of(' ') != std::string::npos) {
            if (str[str.find_first_not_of(' ')] == '%') continue;
            if (str[str.find_first_not_of(' ')] == '#') continue;
        }
        if ( str.find("ReplacementFile")==std::string::npos ) continue;
        replacementFileName=Second(str);
        break;
    }
    if (replacementFileName!="" && (fileName.find("jobSchema.config") == std::string::npos)) {
        WriteInfoStatus("ConfigParser::ReadFile", "Opening replacement file: " + replacementFileName + " to fill the map");
        replacementFileName = Common::RemoveQuotes(replacementFileName);
        std::ifstream fileR(replacementFileName.c_str());
        if(!fileR.is_open()){
            WriteErrorStatus("ConfigParser::ReadFile", "The replacement file: " + replacementFileName + " cannot be opened!");
            exit(-1);
        }
        while (getline(fileR, str)){
            replace( str.begin(), str.end(), '\n', ' ');
            replace( str.begin(), str.end(), '\r', ' ');
            replace( str.begin(), str.end(), '\t', ' ');
            if ( str.find("%")!=std::string::npos || str.find("#")!=std::string::npos) continue;
            if (str.find_first_not_of(' ') == std::string::npos)    continue;
            WriteInfoStatus("ConfigParser::ReadFile", "putting in the map: [" + First(str) + "]=" + Second(str));
            fReplacement[First(str)]=Second(str);
        }
        fileR.close();
    }
    return fReplacement;
}

void ConfigParser::ExpandConfigs(std::string config_address, std::vector<std::string> *lines_of_config,
                                std::vector<std::string> *included_configs, std::map<std::string,std::string>& fReplacement,
                                bool doIncludes)    {

    ResolvePath(&config_address);
    if (std::count(included_configs->begin(), included_configs->end(), config_address))    {
        const std::string configs = Common::join_strings(*included_configs, " -> ") + " -> " + config_address;
        WriteErrorStatus("ConfigParser::ExpandConfigs", std::string("Detected circular include of configs: ") + configs);
        exit(EXIT_FAILURE);
    }
    included_configs->push_back(config_address);

    std::ifstream input_file (config_address);
    if (input_file.is_open())    {
        std::string line;
        while ( getline (input_file,line) )        {
            Common::StripString(&line, "");

            std::string stripped_line = line;
            Common::StripString(&stripped_line);
            if (Common::StartsWith(stripped_line, "INCLUDE:")) {
                if ((line.find("XXX") != std::string::npos) && (!fReplacement.empty())) {
                    ReplaceFromReplacementFile(&line, fReplacement);
                }
                line = Common::RemoveQuotes(line);
                if (!doIncludes)   continue;
                std::vector<std::string> current_config_address_elements = Common::SplitAndStripString(config_address, "/");
                current_config_address_elements.pop_back();

                std::string new_config = line.substr(8);
                Common::StripString(&new_config);

                std::vector<std::string> new_config_elements = Common::SplitString(new_config, "/");
                if (new_config_elements.size() == 0)   {
                    WriteErrorStatus("ConfigParser::ExpandConfigs", "INCLUDE flag must be followed by a path");
                    exit(EXIT_FAILURE);
                }
                if ((current_config_address_elements.size() == 0)) {current_config_address_elements = {"."};}
                const bool absolute_path = new_config_elements[0] == "";


                if (!absolute_path)  {
                     new_config =  (Common::join_strings(current_config_address_elements, "/")) + "/" + new_config;
                }
                ExpandConfigs(new_config, lines_of_config, included_configs, fReplacement);
            }
            else {
                lines_of_config->push_back(line);
            }
        }
    }
    else    {
        WriteErrorStatus("ConfigParser::ExpandConfigs", "Unable to open config file \"" + config_address + "\"");
        exit(EXIT_FAILURE);
    }
    included_configs->pop_back();
}

//__________________________________________________________________________________
//

void ConfigParser::ReadFile(const std::string& fileName){
    if (!std::filesystem::is_regular_file(fileName)) {
        WriteErrorStatus("ConfigParser::ReadFile", "Path: " + fileName + " is not a regular file path");
        exit(EXIT_FAILURE);
    }
    WriteInfoStatus("ConfigParser::ReadFile", "Reading config file: " + fileName);
    std::vector<std::string> tmp_lines_of_config, lines_of_config, included_configs;
    std::string val;

    // If a replacement file is given in main config, not via an include, then parse it before parsing INCLUDES
    // this allows using replaced strings in INCLUDE: lines within the config
    std::map<std::string,std::string> fReplacement;
    // Expand the main config only, without expanding included configs
    // At this point, fReplacement is empty, no replacements are made
    ExpandConfigs(fileName, &tmp_lines_of_config, &included_configs, fReplacement, false);
    // If a replacement file was found in main config, create replacement mapping from it
    // If a replacement file was notfound in main config, it may be in an included config
    fReplacement = ParseReplacements(tmp_lines_of_config, fileName);

    // Expand all included configs -- if fReplacement was defined from main config
    // all lines willl be replaced on the fly as included configs are parsed
    ExpandConfigs(fileName, &lines_of_config, &included_configs, fReplacement);

    // if fReplacement was not defined from main config, we can look for it again
    // after we have expanded all includes
    if (fReplacement.empty())   fReplacement = ParseReplacements(lines_of_config, fileName);
    // at this point, if fReplacement is empty, there is no replacment file within main and nested configs
    // if fReplacement is not empty, it will be used to replace XXX in the fully expanded config.

    bool reading = false;
    int n = 1;
    int k = 0;
    for (std::string line : lines_of_config) {
        replace( line.begin(), line.end(), '\n', ' ');
        replace( line.begin(), line.end(), '\r', ' ');
        replace( line.begin(), line.end(), '\t', ' ');
        if (line.find_first_not_of(' ') != std::string::npos) {
            if(line[line.find_first_not_of(' ')]=='%') continue;
            if(line[line.find_first_not_of(' ')]=='#') continue;
        }
        //
        if (line.find("XXX")!=std::string::npos) {
            WriteInfoStatus("ConfigParser::ReadFile", "BEFORE replacement: " + line);
            ReplaceFromReplacementFile(&line, fReplacement);
            WriteInfoStatus("ConfigParser::ReadFile", " AFTER replacement: " + line);
        }
        //
        if(line.find_first_not_of(' ')==std::string::npos){
            reading = false;
        }
        else{
            const std::vector<std::string> valVec = Common::Vectorize(Second(line),';',false);
            if(!reading){
                n = valVec.size();
                for(k=0;k<n;k++){
                    fConfSets.emplace_back(std::make_unique<ConfigSet>());
                    fConfSets[fN]->Set( First(line),Common::RemoveSpaces(valVec[k]) );
                    fN++;
                }
                reading = true;
            }
            else{
                for(k=0;k<n;k++){
                    if (valVec.empty()) {
                        val = "";
                    } else {
                        if(k>=(int)valVec.size()) val = valVec[valVec.size()-1];
                        else                      val = valVec[k];
                    }
                    fConfSets[fN-n+k]->SetConfig(First(line),Common::RemoveSpaces(val) );
                }
            }
        }
    }
}

//__________________________________________________________________________________
// Returns the i-th configSet
const ConfigSet *ConfigParser::GetConfigSet(int i){
    return fConfSets[i].get();
}

//__________________________________________________________________________________
// Returns the i-th configSet with given name
const ConfigSet *ConfigParser::GetConfigSet(const std::string& name,int i){
    int k = 0;
    for(int j=0;j<fN;j++){
        if(fConfSets[j]->GetName() == name){
            if(i==k) return fConfSets[j].get();
            k++;
        }
    }
    return nullptr;
}

//__________________________________________________________________________________
//
int ConfigParser::CheckSyntax(ConfigParser *refConfigParser){
    int exitStatus = 0;
    // loop on all the confic sets
    for(int i_cs = 0; i_cs<fN; i_cs++){
        ConfigSet *cs = fConfSets[i_cs].get();
        // check if the same exists in the reference
        for (int i_c = 0; i_c < cs->fN; i_c++){
            const Config& c = cs->fConfig[i_c];
            exitStatus+= SettingIsValid(cs, refConfigParser, cs->fName, c.fName);
        }
    }
    return exitStatus;
}

//_______________________________________________________________________________________
//
int ConfigParser::SettingIsValid(const ConfigSet *cs, ConfigParser *refConfigParser, const std::string &setting_set, const std::string &setting) const{
    if (refConfigParser == nullptr){
        WriteErrorStatus("ConfigParser::SettingIsPresentAndValid", "Invalid pointer to the reference ConfigParser. Please check this!");
        exit(EXIT_FAILURE);
    }
    const ConfigSet *cs_ref = nullptr;
    bool refIsFound = false;
    // check if the setting type exists in the reference
    for (int i_cs =0; i_cs < refConfigParser->fN; i_cs++){
        cs_ref = refConfigParser->fConfSets[i_cs].get();
        if (cs_ref->fName == setting_set){
            refIsFound = true;
            break;
        }
    }
    //
    // config set is not present in the reference
    if (!refIsFound){
        WriteErrorStatus("ConfigParser::SettingIsValid", "Cannot find config set '" + setting_set + "' in reference config. Please check this!");
        return 1;
    }
    //
    // check the validity of the single setting
    if(CheckSingleSetting(cs, cs_ref, setting_set, setting)) return 1;
    return 0;
}

//_______________________________________________________________________________________
//
int ConfigParser::CheckSingleSetting(const ConfigSet *cs, const ConfigSet *cs_ref, const std::string &setting_set, const std::string &setting) const {
    std::string param = cs->Get(setting);
    std::string ref_param = cs_ref->Get(setting);
    //
    // this option used to exist, write a message informing the user of the new syntax
    if (setting == "TtresSmoothing"){
        WriteErrorStatus("ConfigParser::CheckSingleSetting", "The TtresSmoothing option is deprecated, use SmoothingOption: TTBARRESONANCE instead.");
        return 1;
    }
    else if (ref_param == ""){
        WriteErrorStatus("ConfigParser::CheckSingleSetting", "Cannot find setting '" + setting + "' for setting set " + setting_set +  " in reference config. Please check this!");
        return 1;
    }
    //
    // there is nothing to check if the reference setting is simply 'std::string'
    if (ref_param == "string") return 0;
    //
    // need to check the consistency of the provided settings
    // first check the number of provided parameters
    std::vector<std::string> current_settings = Common::Vectorize(param,',');
    std::vector<std::string> possible_settings = Common::Vectorize(ref_param,'/');
    std::vector<unsigned int> possible_sizes;
    //
    for (const std::string &ioption : possible_settings){
        possible_sizes.push_back( Common::Vectorize(ioption,',').size() );
    }
    unsigned int current_setting_size = current_settings.size();
    //
    // search the vector for the possible sizes
    auto it = std::find(possible_sizes.begin(), possible_sizes.end(), current_setting_size);
    if (it == possible_sizes.end()){
        WriteErrorStatus("ConfigParser::CheckSingleSetting", "You provided " + std::to_string(current_setting_size) +" parameters, for setting set '" + setting_set + "' and setting '" + setting + "'");
        std::string tmp = "Possible setting sizes are: ";
        for (const unsigned int& i : possible_sizes){
            tmp+= std::to_string(i) + " ";
        }
        tmp+= ". Please check this!";
        WriteErrorStatus("ConfigParser::CheckSingleSetting", tmp );
        return 1;
    }
    //
    // sizes are correct, not we need to check the actual input
    if(CheckParameters(param, possible_settings, setting_set, setting)) return 1;
    return 0;
}

//_______________________________________________________________________________________
//
int ConfigParser::CheckParameters(std::string current, const std::vector<std::string> &possible_settings, const std::string &setting_set, const std::string &setting) const{
    if (possible_settings.size() == 1){
        if(!SettingMultipleParamIsOK(setting_set, setting, current, possible_settings.at(0))) return 1;
    }
    else {
        // multiple settings are possible
        bool isFound = false;
        std::transform(current.begin(), current.end(), current.begin(), ::toupper);
        for (const std::string& isetting : possible_settings){
            // for std::string
            if(SettingMultipleParamIsOK(setting_set, setting, current, isetting)){
                isFound = true;
                break;
            }
        }
        if (!isFound){
            WriteErrorStatus("ConfigParser::CheckParameters", "Parameter " + current +" is not valid, for setting set '" + setting_set + "' and setting '" + setting );
            std::string tmp = "Possible values: ";
            for (const std::string &i : possible_settings){
                tmp+= i + " ";
            }
            tmp+= ". Please check this!";
            WriteErrorStatus("ConfigParser::CheckParameters", tmp );
            return 1;
        }
    }
    return 0;
}

//_______________________________________________________________________________________
//
bool ConfigParser::SettingMultipleParamIsOK(const std::string& setting_set, const std::string& setting, const std::string& current, const std::string& possible, const char delimiter) const{
    const std::vector<std::string> current_vec = Common::Vectorize(current, delimiter);
    const std::vector<std::string> possible_vec = Common::Vectorize(possible, delimiter);
    if (current_vec.size() != possible_vec.size()) return false;
    //
    // check setting by setting
    for (std::size_t iparam = 0; iparam < possible_vec.size(); iparam++){
        if (possible_vec.at(iparam) == "string"){
            continue; // nothing to check
        } else if (possible_vec.at(iparam) == "int"){
            try {
                // cppcheck-suppress ignoredReturnValue
                std::stoi(current_vec.at(iparam));
            } catch (std::exception &e){
                WriteErrorStatus("ConfigParser::SettingMultipleParamIsOK", "Parameter " + current_vec.at(iparam) + " is not valid, for setting set '" + setting_set + "' and setting '" + setting + ", for parameter number " + std::to_string(iparam+1) + ". Please check this!" );
                return false;
            }
        } else if (possible_vec.at(iparam) == "float"){
            try {
                // cppcheck-suppress ignoredReturnValue
                std::stod(current_vec.at(iparam));
            } catch (std::exception &e){
                WriteErrorStatus("ConfigParser::SettingMultipleParamIsOK", "Parameter " + current_vec.at(iparam) + " is not valid, for setting set '" + setting_set + "' and setting '" + setting + ", for parameter number " + std::to_string(iparam+1) + ". Please check this!" );
                return false;
            }
        } else {
            if (current_vec.at(iparam) != possible_vec.at(iparam)){
                return false;
            }
        }
    }
    return true;
}
