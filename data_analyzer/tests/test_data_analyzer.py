import os
import json
import subprocess
import general_files.general_test_functions as gtf
from task1.textprocessor import TextPreprocessor
import data_analyzer

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

import data_analyzer.data_analyzer as da

if __name__ == '__main__':

    # Store results
    test_results = []

    # Test logic
    base_dir = os.path.join("2_examples")
    w_path = os.path.join("1_data", "data", "REMOVEWORDS.csv")

    # Parameters for tasks
    seq_lengths = [3, 4, 5]  # For sequence counting (Task 2)
    context_sizes = [3, 4, 5, 4]  # For context extraction (Task 5)

    output_results_dir = os.path.join("output_results")
    os.makedirs(output_results_dir, exist_ok=True)

    for task_num, task_folder in enumerate(["Q2_examples", "Q3_examples", "Q4_examples", "Q5_examples"], start=2):
        for i in range(1, 5 if task_num > 2 else 4):  # Task 2 has 3 tests, Task 3-5 have 4 tests
            print(f"\n=== Running Tests for Task {task_num}, File Set {i} ===")

            s_path = os.path.join(base_dir, task_folder, f"example_{i}", f"sentences_small_{i}.csv")

            if task_num == 4:
                p_path = None
                k_path = os.path.join(base_dir, task_folder, f"example_{i}", f"kseq_query_keys_{i}.json")
            else:
                p_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_small_{i}.csv")
                k_path = None

            # ✅ **Initialize TextPreprocessor with Correct Files**
            print(f"Preprocessing input for Task {task_num}, File Set {i}...")
            text_preprocessor = TextPreprocessor(s_path, p_path, w_path, False, 1)
            preprocessed_data = json.loads(text_preprocessor.get_json_format())

            # ✅ **Initialize DataAnalyzer with Preprocessed Data**
            print(f"Initializing DataAnalyzer for Task {task_num}, File Set {i}...")

            if task_num == 2:
                data_analyzer = da.DataAnalyzer(text_preprocessor, seq_lengths[i - 1], k_path)
            elif task_num == 5:
                data_analyzer = da.DataAnalyzer(text_preprocessor, context_sizes[i - 1], k_path)
            else:
                data_analyzer = da.DataAnalyzer(text_preprocessor, 1, k_path)

            # ✅ **Step 3: Run Tasks and Compare Outputs**
            print(f"Running Task {task_num} for File Set {i}...")
            if task_num == 2:
                processed_result = json.loads(data_analyzer.sequence_counter())
            elif task_num == 3:
                processed_result = json.loads(data_analyzer.names_counter())
            elif task_num == 4:
                processed_result = json.loads(data_analyzer.kseqengine())
            else:
                processed_result = json.loads(data_analyzer.find_context())

            # ✅ **Save Processed Results to File**
            output_file_path = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output.json")
            with open(output_file_path, 'w') as output_file:
                json.dump(processed_result, output_file, indent=4)
            print(f"Processed results saved to {output_file_path}")

            expected_result_path = os.path.join(base_dir, task_folder, f"example_{i}", f"Q{task_num}_result{i}.json")
            with open(expected_result_path, 'r') as file:
                expected_result = json.load(file)

            result = "PASS" if processed_result == expected_result else "FAIL"
            test_results.append((f"Task {task_num} - File Set {i}", result))

    print("\n✅ All Tests Completed ✅")

    # Summary of test results
    print("\n=== Test Summary ===")
    for test, result in test_results:
        color = Colors.GREEN if result == "PASS" else Colors.RED
        print(f"{color}{test}: {result}{Colors.RESET}")
