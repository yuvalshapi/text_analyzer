import pandas as pd
import json
import re
import os
import general_files.general_test_functions as gtf
from task4.task4 import *

if __name__ == '__main__':

    # Test logic
    base_dir = ""
    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        kseq_path = os.path.join(base_dir, f"test{i}", f"kseq_query_keys_{i}.json")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q4_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, f"test{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = KseqEngine(s_path, w_path, kseq_path, False)
        processed_result = json.loads(T.get_json_format())

        # Save processed result to a file
        with open(output_path, 'w') as outfile:
            json.dump(processed_result, outfile, indent=4)
        print(f"Processed result saved to {output_path}")

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"File set {i}: PASS")
        else:
            print(f"File set {i}: FAIL")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)
