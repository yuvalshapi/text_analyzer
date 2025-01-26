import json
import os
import pandas as pd
import general_files.general_test_functions as gtf
from task1.task1 import TextPreprocessor
from task3.task3 import NamesCounter

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

if __name__ == '__main__':

    # Test logic
    base_dir = ""
    # Iterate through 1, 2, 3, and 4 for file sets
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q3_result{i}.json")

        # Output JSON files for processed results
        output_path_not_processed = os.path.join(base_dir, f"test{i}", f"processed_result{i}_not_processed.json")
        output_path_preprocessed = os.path.join(base_dir, f"test{i}", f"processed_result{i}_preprocessed.json")
        preprocessed_input_path = os.path.join(base_dir, f"test{i}", f"preprocessed_input{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Test NamesCounter with not processed input
        print(f"Running NamesCounter test with raw input for File Set {i}...")
        T = NamesCounter(s_path, p_path, w_path, False)
        processed_result_not_processed = json.loads(T.get_json_format())

        # Save processed result to a file
        with open(output_path_not_processed, 'w') as outfile:
            json.dump(processed_result_not_processed, outfile, indent=4)
        print(f"Processed result (not processed) saved to {output_path_not_processed}")

        # Compare and print results for not processed input
        if processed_result_not_processed == expected_result:
            print(f"{Colors.GREEN}Test {i} (not processed): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (not processed): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result_not_processed, expected_result, sentences_file=s_path)

        # Preprocess the input data for NamesCounter (processed case)
        print(f"Generating preprocessed input for File Set {i}...")
        text_preprocessor = TextPreprocessor(s_path, p_path, w_path, 1)
        preprocessed_json = json.loads(text_preprocessor.get_json_format())

        # Save the preprocessed input to a file
        with open(preprocessed_input_path, 'w') as outfile:
            json.dump(preprocessed_json, outfile, indent=4)
        print(f"Preprocessed input saved to {preprocessed_input_path}")

        # Test NamesCounter with preprocessed input
        print(f"Running NamesCounter test with preprocessed input for File Set {i}...")
        P = NamesCounter(preprocessed_input_path, None, None, True)
        processed_result_preprocessed = json.loads(P.get_json_format())

        # Save processed result to a file
        with open(output_path_preprocessed, 'w') as outfile:
            json.dump(processed_result_preprocessed, outfile, indent=4)
        print(f"Processed result (preprocessed) saved to {output_path_preprocessed}")

        # Compare the outputs for preprocessed input
        if processed_result_preprocessed == expected_result:
            print(f"{Colors.GREEN}Test {i} (preprocessed): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (preprocessed): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result_preprocessed, expected_result, sentences_file=s_path)
