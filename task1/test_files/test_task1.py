import os
import json
import pandas as pd
import general_files.general_test_functions as gtf
from task1.textprocessor import TextPreprocessor

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

if __name__ == '__main__':

    # Test logic
    base_dir = ""

    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 4):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q1_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, f"test{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = TextPreprocessor(s_path, p_path, w_path, 1)
        processed_result = json.loads(T.get_json_format())

        # Save processed result to a file
        with open(output_path, 'w') as outfile:
            json.dump(processed_result, outfile, indent=4)
        print(f"Processed result saved to {output_path}")

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"{Colors.GREEN}File set {i}: PASS{Colors.RESET}")
        else:
            print(f"{Colors.RED}File set {i}: FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)
