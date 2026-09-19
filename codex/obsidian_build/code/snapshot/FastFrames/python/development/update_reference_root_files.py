"""!Script for automated updates of the reference files for output ROOT comparison tests.
The script has to be run from the root directory of the project.

Usage:
    python3 python/development/update_reference_root_files.py
"""

import yaml
import os
from sys import path

path.append("test/python")

from DevelopmentCommon.DevelopmentFunctions import get_keyboard_bool
from compare_two_root_files import test_compare_files

class RootFilesComparisonTest:
    def __init__(self):
        self.produce_inputs_command = ""
        self.pairs_output_file_and_reference_file = []
    def valid_test(self):
        return self.produce_inputs_command and self.pairs_output_file_and_reference_file

def get_from_dict(test_dict : dict) -> RootFilesComparisonTest:
    if type(test_dict) != dict:
        return
    if test_dict.get("stage", "") != "compare_results":
        return
    script = test_dict.get("script", [])
    result = RootFilesComparisonTest()
    for command in script:
        command = command.strip()
        if command.startswith("python3 python/FastFrames.py"):
            if (result.produce_inputs_command):
                print("Cannot read test from CI test confing: ", test_dict)
            result.produce_inputs_command = command
        elif command.startswith("python3 test/python/compare_two_root_files.py"):
            elements = command.split()
            if len(elements) < 4:
                print("Cannot read test from CI test confing: ", test_dict)
            result.pairs_output_file_and_reference_file.append((elements[2], elements[3]))
    if result.valid_test():
        return result


if __name__ == "__main__":
    with open(".gitlab-ci.yml", "r") as f:
        data_full = yaml.load(f, Loader=yaml.FullLoader)

        for test_name in data_full:
            test_dict = data_full[test_name]
            test = get_from_dict(test_dict)
            if test == None:
                continue
            os.system(test.produce_inputs_command)
            for pair_to_compare in test.pairs_output_file_and_reference_file:
                comparison_result = test_compare_files(pair_to_compare[0], pair_to_compare[1])

                if comparison_result:
                    print(f"Files{pair_to_compare[0]} and {pair_to_compare[1]} are different:")
                    print("\t", comparison_result)
                    want_to_update = get_keyboard_bool("Do you want to update the reference file? (y/n): ")
                    if want_to_update:
                        os.system(f"cp {pair_to_compare[0]} {pair_to_compare[1]}")

