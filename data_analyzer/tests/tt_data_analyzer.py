import os
import json
import general_files.general_test_functions as gtf
from task1.textprocessor import TextPreprocessor
import data_analyzer.data_analyzer as da

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

if __name__ == '__main__':

    # Store results
    test_results = []

    # Base directory containing test data
    base_dir = os.path.join("2_examples")
    w_path = os.path.join("1_data", "data", "REMOVEWORDS.csv")

    # Parameters for tasks
    seq_lengths = [3, 4, 5]  # For sequence counting (Task 2)
    context_sizes = [3, 4, 5, 4]  # For context extraction (Task 5)

    # Directory to store output results
    output_results_dir = os.path.join("output_results")
    os.makedirs(output_results_dir, exist_ok=True)

    # Loop through each task (2-5)
    for task_num, task_folder in enumerate(["Q2_examples", "Q3_examples", "Q4_examples", "Q5_examples"], start=2):
        for i in range(1, 5 if task_num > 2 else 4):  # Task 2 has 3 tests, Task 3-5 have 4 tests
            print(f"\n=== Running Tests for Task {task_num}, File Set {i} ===")

            # File paths
            s_path = os.path.join(base_dir, task_folder, f"example_{i}", f"sentences_small_{i}.csv")
            preprocessed_input_path = os.path.join(base_dir, task_folder, f"example_{i}", f"preprocessed_input{i}.json")

            if task_num == 4:
                p_path = None
                k_path = os.path.join(base_dir, task_folder, f"example_{i}", f"kseq_query_keys_{i}.json")
            else:
                p_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_small_{i}.csv")
                k_path = None

            expected_result_path = os.path.join(base_dir, task_folder, f"example_{i}", f"Q{task_num}_result{i}.json")

            # ✅ **Test Raw Data**
            print(f"Preprocessing input for Task {task_num}, File Set {i} (RAW INPUT)...")
            text_preprocessor = TextPreprocessor(s_path, p_path, w_path, False, 1)
            preprocessed_data = json.loads(text_preprocessor.get_json_format())

            print(f"Initializing DataAnalyzer for Task {task_num}, File Set {i} (RAW INPUT)...")

            if task_num == 2:
                data_analyzer = da.DataAnalyzer(text_preprocessor, seq_lengths[i - 1], k_path)
            elif task_num == 5:
                data_analyzer = da.DataAnalyzer(text_preprocessor, context_sizes[i - 1], k_path)
            else:
                data_analyzer = da.DataAnalyzer(text_preprocessor, 1, k_path)

            print(f"Running Task {task_num} for File Set {i} (RAW INPUT)...")
            if task_num == 2:
                processed_result_raw = json.loads(data_analyzer.sequence_counter())
            elif task_num == 3:
                processed_result_raw = json.loads(data_analyzer.names_counter())
            elif task_num == 4:
                processed_result_raw = json.loads(data_analyzer.kseqengine())
            else:
                processed_result_raw = json.loads(data_analyzer.find_context())

            output_path_raw = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output_raw.json")
            with open(output_path_raw, 'w') as output_file:
                json.dump(processed_result_raw, output_file, indent=4)
            print(f"Processed results saved to {output_path_raw}")

            # ✅ **Save Preprocessed Data to a File**
            with open(preprocessed_input_path, 'w') as outfile:
                json.dump(preprocessed_data, outfile, indent=4)
            print(f"Preprocessed input saved to {preprocessed_input_path}")

            # ✅ **Test Preprocessed Data**
            print(f"Initializing DataAnalyzer for Task {task_num}, File Set {i} (PREPROCESSED INPUT)...")
            preprocessed_text = TextPreprocessor(preprocessed_input_path, None, None, True, 1)

            if task_num == 2:
                data_analyzer_preprocessed = da.DataAnalyzer(preprocessed_text, seq_lengths[i - 1], k_path)
            elif task_num == 5:
                data_analyzer_preprocessed = da.DataAnalyzer(preprocessed_text, context_sizes[i - 1], k_path)
            else:
                data_analyzer_preprocessed = da.DataAnalyzer(preprocessed_text, 1, k_path)

            print(f"Running Task {task_num} for File Set {i} (PREPROCESSED INPUT)...")
            if task_num == 2:
                processed_result_preprocessed = json.loads(data_analyzer_preprocessed.sequence_counter())
            elif task_num == 3:
                processed_result_preprocessed = json.loads(data_analyzer_preprocessed.names_counter())
            elif task_num == 4:
                processed_result_preprocessed = json.loads(data_analyzer_preprocessed.kseqengine())
            else:
                processed_result_preprocessed = json.loads(data_analyzer_preprocessed.find_context())

            output_path_preprocessed = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output_preprocessed.json")
            with open(output_path_preprocessed, 'w') as output_file:
                json.dump(processed_result_preprocessed, output_file, indent=4)
            print(f"Processed results saved to {output_path_preprocessed}")

            # ✅ **Compare Processed Results with Expected Output**
            with open(expected_result_path, 'r') as file:
                expected_result = json.load(file)

            result_raw = "PASS" if processed_result_raw == expected_result else "FAIL"
            result_preprocessed = "PASS" if processed_result_preprocessed == expected_result else "FAIL"

            test_results.append((f"Task {task_num} - File Set {i} (RAW)", result_raw))
            test_results.append((f"Task {task_num} - File Set {i} (PREPROCESSED)", result_preprocessed))

    print("\n✅ All Tests Completed ✅")

    # ✅ **Summary of test results**
    print("\n=== Test Summary ===")
    for test, result in test_results:
        color = Colors.GREEN if result == "PASS" else Colors.RED
        print(f"{color}{test}: {result}{Colors.RESET}")
