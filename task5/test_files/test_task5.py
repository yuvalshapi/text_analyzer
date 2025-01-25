import json
import os
import pandas as pd
import general_files.general_test_functions as gtf
from task5.task5 import ContextFinder

if __name__ == '__main__':

    # Test logic
    base_dir = ""
    nums = [3, 4, 5, 4]
    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q5_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, f"test{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = ContextFinder(s_path, p_path, w_path, False, nums[i - 1])
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
