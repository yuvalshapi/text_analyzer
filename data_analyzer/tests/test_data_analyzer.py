import os
import json
import subprocess
import  general_files.general_test_functions as gtf
from task1.textprocessor import TextPreprocessor
import data_analyzer

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

import data_analyzer.data_analyzer as da
if __name__ == '__main__':

    # Test logic
    base_dir = "tests/2_examples"
    w_path = os.path.join("tests","1_data", "data", "REMOVEWORDS.csv")

    # Parameters for tasks
    seq_lengths = [3, 4, 5]  # For sequence counting (Task 2)
    context_sizes = [3, 4, 5, 4]  # For context extraction (Task 5)

    for i in range(1, 5):  # Tasks 2-5 use up to 4 test sets
        print(f"\n=== Running Tests for File Set {i} ===")

        # File paths
        s_path = os.path.join(base_dir, f"Q{i}_examples", f"example_{i}", f"sentences_small_{i}.csv")
        p_path = os.path.join(base_dir, f"Q{i}_examples", f"example_{i}", f"people_small_{i}.csv")
        e_path_task2 = os.path.join(base_dir, f"Q2_examples", f"example_{i}", f"Q2_result{i}.json")
        e_path_task3 = os.path.join(base_dir, f"Q3_examples", f"example_{i}", f"Q3_result{i}.json")
        e_path_task4 = os.path.join(base_dir, f"Q4_examples", f"example_{i}", f"Q4_result{i}.json")
        e_path_task5 = os.path.join(base_dir, f"Q5_examples", f"example_{i}", f"Q5_result{i}.json")

        # Paths for optional inputs
        kseq_path = os.path.join(base_dir, f"Q4_examples", f"example_{i}", f"kseq_query_keys_{i}.json")

        # Output paths for processed data
        preprocessed_output_path = os.path.join(base_dir, f"Q{i}_examples", f"example_{i}",
                                                f"preprocessed_data_{i}.json")

        # ✅ **Step 1: Preprocess Input**
        print(f"Preprocessing input for File Set {i}...")
        text_preprocessor = TextPreprocessor(s_path, p_path, w_path, 1)
        preprocessed_data = json.loads(text_preprocessor.get_json_format())

        # Save preprocessed data
        with open(preprocessed_output_path, 'w') as outfile:
            json.dump(preprocessed_data, outfile, indent=4)
        print(f"Preprocessed data saved to {preprocessed_output_path}")

        # ✅ **Step 2: Initialize DataAnalyzer with Preprocessed Data**
        print(f"Initializing DataAnalyzer for File Set {i}...")
        if i<= 3:
            data_analyzer = da.DataAnalyzer(text_preprocessor, seq_lengths[i - 1],kseq_path)
        else:
            data_analyzer = da.DataAnalyzer(text_preprocessor, None,kseq_path)

        # ✅ **Step 3: Run Tasks and Compare Outputs**

        # 🔹 **Task 2: Sequence Counter**
        if i <= 3:  # Task 2 only has 3 test cases
            print(f"Running Task 2 (Sequence Counter) for File Set {i}...")
            processed_result = json.loads(data_analyzer.sequence_counter())
            print(processed_result)
            with open(e_path_task2, 'r') as file:
                expected_result = json.load(file)

            if processed_result == expected_result:
                print(f"{Colors.GREEN}Task 2, File Set {i}: PASS{Colors.RESET}")
            else:
                print(f"{Colors.RED}Task 2, File Set {i}: FAIL{Colors.RESET}")
                gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

        # 🔹 **Task 3: Name Counter**
        print(f"Running Task 3 (Name Counter) for File Set {i}...")
        processed_result = json.loads(data_analyzer.names_counter())
        with open(e_path_task3, 'r') as file:
            expected_result = json.load(file)

        if processed_result == expected_result:
            print(f"{Colors.GREEN}Task 3, File Set {i}: PASS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Task 3, File Set {i}: FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

        # 🔹 **Task 4: K-Seq Engine**
        if i <= 4:  # Task 4 has 4 test cases
            print(f"Running Task 4 (K-Seq Engine) for File Set {i}...")
            processed_result = json.loads(data_analyzer.kseqengine())
            with open(e_path_task4, 'r') as file:
                expected_result = json.load(file)

            if processed_result == expected_result:
                print(f"{Colors.GREEN}Task 4, File Set {i}: PASS{Colors.RESET}")
            else:
                print(f"{Colors.RED}Task 4, File Set {i}: FAIL{Colors.RESET}")
                gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

        # 🔹 **Task 5: Context Finder**
        print(f"Running Task 5 (Context Finder) for File Set {i}...")
        processed_result = json.loads(data_analyzer.find_context())
        with open(e_path_task5, 'r') as file:
            expected_result = json.load(file)

        if processed_result == expected_result:
            print(f"{Colors.GREEN}Task 5, File Set {i}: PASS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Task 5, File Set {i}: FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

    print("\n✅ All Tests Completed ✅")
