"""!Script for smearing original ATLAS data or MC samples, to be able to use them in public CI tests.

Usage:
    python3 python/development/smear_input_root_file.py <input_root_file> <output_root_file>
"""

from sys import argv
from ROOT import TFile, TTree, RDataFrame, vector, gROOT
import uproot
import numpy as np
from copy import deepcopy
import random

def copy_other_objects_to_output_tfile(input_file_address : str, output_file : TFile, object_to_skip : list[str]) -> None:
    input_file = TFile(input_file_address, "READ")
    types_to_copy = ["TH1", "TTree"]
    list_of_keys = input_file.GetListOfKeys()
    for key in list_of_keys:
        object_name = key.GetName()
        if object_name in object_to_skip:
            continue

        this_class = gROOT.GetClass(key.GetClassName())
        is_type_to_copy = any([this_class.InheritsFrom(type_to_copy) for type_to_copy in types_to_copy])
        if not is_type_to_copy:
            continue
        object = input_file.Get(object_name)
        output_file.cd()
        object.Write()
    input_file.Close()

def get_list_of_trees(root_file_address : str) -> list[str]:
    root_file = TFile(root_file_address, "READ")
    selected_trees = ["truth", "reco", "particleLevel"]
    list_of_trees = [key.GetName() for key in root_file.GetListOfKeys() if key.GetClassName() == "TTree" and key.GetName() in selected_trees]
    root_file.Close()
    return list_of_trees

def get_selected_branches_for_smearing(branches : list[str]):
    keywords = set(["_eta", "_phi", "_pt", "_E_", "_e_", "_m_", "met_met"])
    selected_branches = [branch for branch in branches if any(keyword in branch for keyword in keywords)]
    return selected_branches

def apply_gaussian_smearing(array, mean=1, stddev=0.2):
    return array*np.random.normal(mean, stddev, array.shape)

def get_branches_types(file_address : str, tree_name : str) -> dict[str,str]:
    rdf = RDataFrame(tree_name, file_address)
    branches = rdf.GetColumnNames()
    branches_types = {}
    for branch in branches:
        type_string = rdf.GetColumnType(branch)
        type_string = type_string.replace("ROOT::VecOps::RVec", "std::vector")
        type_string = type_string.replace("Float_t", "float")
        type_string = type_string.replace("Int_t", "int")
        type_string = type_string.replace("Double_t", "double")
        type_string = type_string.replace("Long64_t", "long long")
        type_string = type_string.replace("Bool_t", "bool")
        type_string = type_string.replace("Char_t", "char")
        type_string = type_string.replace("Uint", "unsigned int")
        type_string = type_string.replace("Ulong long", "unsigned long long")
        branch_name = str(branch)

        branches_types[branch_name] = type_string
    return branches_types

def get_vector_type(string_type : str) -> str:
    return string_type[string_type.find("<")+1:string_type.find(">")]

def copy_array_to_vector(numpy_array, vec : vector) -> None:
    vec.clear()
    for element in numpy_array:
        if type(element) == np.int32:
            element = int(element) # I have no idea why this is needed ...
        if type(element) == np.uint32:
            element = int(element) # I have no idea why this is needed ...

        vec.push_back(element)

def get_type_one_char(type_string : str) -> str:
    if type_string == "float":
        return "F"
    if type_string == "int":
        return "I"
    if type_string == "double":
        return "D"
    if type_string == "long long":
        return "L"
    if type_string == "bool":
        return "O"
    if type_string == "char":
        return "C"
    if type_string == "unsigned int":
        return "i"
    if type_string == "unsigned long long":
        return "l"
    return "F"


def smear_file(input_address : str, output_address : str) -> None:
    list_of_trees = get_list_of_trees(input_root_file)

    input_file_uproot = uproot.open(input_address)
    output_file = TFile(output_address, "RECREATE")
    copy_other_objects_to_output_tfile(input_address, output_file, list_of_trees)
    for tree in list_of_trees:
        input_tree = input_file_uproot[tree]
        output_file.cd()
        output_tree = TTree(tree, tree)


        branch_name_to_type = get_branches_types(input_address, tree)
        branches = list(branch_name_to_type.keys())
        branches.sort()
        selected_branches_to_smear = get_selected_branches_for_smearing(branches)
        selected_branches_to_smear = set(selected_branches_to_smear)

        vector_dictionary = {}
        event_arrays_dictionary = {}
        #selected_branches = ["met_met_NOSYS"]
        for branch_name in branches:
            this_array = input_tree[branch_name].array()
            first_element_copy = deepcopy(this_array[0:1])
            type_string = branch_name_to_type[branch_name]

            one_char_type = get_type_one_char(type_string)
            if "vector" in type_string:
                vector_type = get_vector_type(type_string)
                this_vector = vector(vector_type)()
                vector_dictionary[branch_name] = this_vector
                output_tree.Branch(branch_name, this_vector)
            else:
                output_tree.Branch(branch_name, first_element_copy, branch_name + "/" + one_char_type)

            # now smear the branch if needed
            if branch_name in selected_branches_to_smear:
                this_array = apply_gaussian_smearing(this_array)
            event_arrays_dictionary[branch_name] = (first_element_copy,this_array)



        for i_event in range(input_tree.numentries):
            if i_event % 10 == 0:
                print(f"event: {i_event}/{input_tree.numentries}")
            for branch_name in event_arrays_dictionary:
                first_element, this_array = event_arrays_dictionary[branch_name]
                if "vector" in branch_name_to_type[branch_name]:
                    copy_array_to_vector(this_array[i_event], vector_dictionary[branch_name])
                else:
                    first_element[0] = this_array[i_event]
            output_tree.Fill()

        output_tree.Write()
    output_file.Close()


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python smear_input_root_file.py <input_root_file> <output_root_file>")
        exit(1)

    input_root_file = argv[1]
    output_root_file = argv[2]

    smear_file(input_root_file, output_root_file)
