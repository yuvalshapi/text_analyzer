import os
import json
import pandas as pd
from task1.task1 import TextPreprocessor
from task2.task2 import SequenceCounter
import general_files.general_test_functions as gtf

if __name__ == '__main__':

    # Test logic
    base_dir = ""
    n1 = [3, 4, 5]
    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 4):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q2_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, f"test{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Test SequenceCounter with not processed input
        print(f"Running SequenceCounter test with raw input for File Set {i}...")
        T = SequenceCounter(s_path, w_path, False, n1[i - 1])
        processed_result = json.loads(T.get_json_format())

        # Save processed result to a file
        with open(output_path, 'w') as outfile:
            json.dump(processed_result, outfile, indent=4)
        print(f"Processed result (raw input) saved to {output_path}")

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"Test {i} (not processed): SUCCESS")
        else:
            print(f"Test {i} (not processed): FAIL")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

        # Generate preprocessed input for SequenceCounter
        d_path = os.path.join(base_dir, f"test{i}", f"input_data.json")
        fd_path = os.path.join(base_dir, f"test{i}", f"processed_data.json")

        print(f"Generating preprocessed input for File Set {i}...")
        text_preprocessor = TextPreprocessor(s_path,p_path, w_path,1)
        preprocessed_json = json.loads(text_preprocessor.get_json_format())

        # Save the preprocessed JSON to a file
        with open(d_path, 'w') as outfile:
            json.dump(preprocessed_json, outfile, indent=4)
        print(f"Preprocessed input saved to {d_path}")

        # Test SequenceCounter with preprocessed input
        print(f"Running SequenceCounter test with preprocessed input for File Set {i}...")
        P = SequenceCounter(d_path, None, True, n1[i - 1])
        processed_result_preprocessed = json.loads(P.get_json_format())

        # Save processed result to a file
        with open(fd_path, 'w') as outfile:
            json.dump(processed_result_preprocessed, outfile, indent=4)
        print(f"Processed result (preprocessed input) saved to {fd_path}")

        # Compare the outputs
        if processed_result_preprocessed == expected_result:
            print(f"Test {i} (processed): SUCCESS")
        else:
            print(f"Test {i} (processed): FAIL")
            gtf.print_differences_and_find_sources(processed_result_preprocessed, expected_result, sentences_file=s_path)
