import pandas as pd
import json
import os
import general_files.general_test_functions as gtf
from task4.task4 import KseqEngine
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
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        kseq_path = os.path.join(base_dir, f"test{i}", f"kseq_query_keys_{i}.json")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q4_result{i}.json")

        # Output JSON file for processed result
        output_path_not_processed = os.path.join(base_dir, f"test{i}", f"processed_result{i}_not_processed.json")
        output_path_processed = os.path.join(base_dir, f"test{i}", f"processed_result{i}_processed.json")
        preprocessed_input_path = os.path.join(base_dir, f"test{i}", f"preprocessed_input{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Test KseqEngine with not processed input
        print(f"Running KseqEngine test with raw input for File Set {i}...")
        T = KseqEngine(s_path, w_path, kseq_path, False)
        processed_result_not_processed = json.loads(T.get_json_format())

        # Save processed result to a file
        with open(output_path_not_processed, 'w') as outfile:
            json.dump(processed_result_not_processed, outfile, indent=4)
        print(f"Processed result (not processed) saved to {output_path_not_processed}")

        # Compare and print results
        if processed_result_not_processed == expected_result:
            print(f"{Colors.GREEN}Test {i} (not processed): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (not processed): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result_not_processed, expected_result, sentences_file=s_path)

        # Preprocess input for KseqEngine (processed case)
        print(f"Generating preprocessed input for File Set {i}...")
        text_preprocessor = TextPreprocessor(s_path, None, w_path, 1)
        preprocessed_json = json.loads(text_preprocessor.get_json_format())

        # Save the preprocessed JSON to a file
        with open(preprocessed_input_path, 'w') as outfile:
            json.dump(preprocessed_json, outfile, indent=4)
        print(f"Preprocessed input saved to {preprocessed_input_path}")

        # Test KseqEngine with preprocessed input
        print(f"Running KseqEngine test with preprocessed input for File Set {i}...")
        P = KseqEngine(preprocessed_input_path, None, kseq_path, True)
        processed_result_processed = json.loads(P.get_json_format())

        # Save processed result to a file
        with open(output_path_processed, 'w') as outfile:
            json.dump(processed_result_processed, outfile, indent=4)
        print(f"Processed result (processed) saved to {output_path_processed}")

        # Compare and print results
        if processed_result_processed == expected_result:
            print(f"{Colors.GREEN}Test {i} (processed): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (processed): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result_processed, expected_result, sentences_file=s_path)
