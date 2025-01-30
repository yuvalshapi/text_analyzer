import os
import json
import general_files.general_test_functions as gtf
from task1.textprocessor import TextPreprocessor
import data_analyzer.connection_finder as cf

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

    # Define parameters for each task
    w_sizes = [[4, 3, 5, 5], [5, 3, 5, 5], [3, 3, 3]]  # Window sizes for Task 6
    thresholds = [[4, 2, 2, 1], [2, 2, 1, 2], [2, 2, 2]]  # Thresholds for Task 6
    fixed_lengths = [2, 3, 8]  # Fixed lengths (None for Task 7, int for Task 8)

    # Directory to store output results
    output_results_dir = os.path.join("output_results")
    os.makedirs(output_results_dir, exist_ok=True)

    # Path to remove words file
    w_path = os.path.join("1_data", "data", "REMOVEWORDS.csv")

    # Loop through each task (6, 7, 8)
    for task_num, task_folder in enumerate(["Q6_examples", "Q7_examples", "Q8_examples"], start=6):
        for i in range(1, 5 if task_num != 8 else 4):  # ✅ Task 8 has only 3 tests, so range is (1,4)
            print(f"\n=== Running Tests for Task {task_num}, File Set {i} ===")

            # File paths
            s_path = os.path.join(base_dir, task_folder, f"example_{i}", f"sentences_small_{i}.csv")
            p_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_small_{i}.csv")
            conn_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_connections_{i}.json")
            preprocessed_input_path = os.path.join(base_dir, task_folder, f"example_{i}", f"preprocessed_input{i}.json")

            # ✅ **Set Expected Result File Paths According to the Given Naming Convention**
            if task_num == 6:
                expected_result_filename = f"Q6_result{i}_w{w_sizes[0][i - 1]}_t{thresholds[0][i - 1]}.json"
            elif task_num == 7:
                expected_result_filename = f"Q7_result{i}_w{w_sizes[1][i - 1]}_t{thresholds[1][i - 1]}.json"
            else:  # Task 8 (which has only 3 tests)
                expected_result_filename = f"Q8_example_{i}_w_{w_sizes[2][i - 1]}_threshold_{thresholds[2][i - 1]}_fixed_length_{fixed_lengths[i - 1]}.json"

            expected_result_path = os.path.join(base_dir, task_folder, f"example_{i}", expected_result_filename)

            ### ✅ **Test Non-Preprocessed Data (RAW INPUT)**
            print(f"Preprocessing input for Task {task_num}, File Set {i}...")
            text_preprocessor = TextPreprocessor(s_path, p_path, w_path, False, task_num)
            preprocessed_data = json.loads(text_preprocessor.get_json_format())

            print(f"Initializing ConnectionFinder for Task {task_num}, File Set {i} (RAW INPUT)...")
            connection_finder = cf.ConnectionFinder(
                processed_data=text_preprocessor,
                w_size=w_sizes[task_num - 6][i - 1],
                threshold=thresholds[task_num - 6][i - 1],
                fixed_len=fixed_lengths[i - 1] if task_num == 8 else None,
                people_connections_path=conn_path if task_num in [7, 8] else None
            )

            print(f"Running Task {task_num} for File Set {i} (RAW INPUT)...")
            if task_num == 6:
                processed_result_raw = json.loads(connection_finder.find_connections())
            else:
                processed_result_raw = json.loads(connection_finder.check_connections())

            output_path_raw = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output_raw.json")
            with open(output_path_raw, 'w') as output_file:
                json.dump(processed_result_raw, output_file, indent=4)
            print(f"Processed results saved to {output_path_raw}")

            ### ✅ **Save Preprocessed Data to a File**
            with open(preprocessed_input_path, 'w') as outfile:
                json.dump(preprocessed_data, outfile, indent=4)
            print(f"Preprocessed input saved to {preprocessed_input_path}")

            ### ✅ **Test Preprocessed Data**
            print(f"Initializing ConnectionFinder for Task {task_num}, File Set {i} (PREPROCESSED INPUT)...")
            connection_finder_preprocessed = cf.ConnectionFinder(
                processed_data=TextPreprocessor(preprocessed_input_path, None, None, True, task_num),
                w_size=w_sizes[task_num - 6][i - 1],
                threshold=thresholds[task_num - 6][i - 1],
                fixed_len=fixed_lengths[i - 1] if task_num == 8 else None,
                people_connections_path=conn_path if task_num in [7, 8] else None
            )

            print(f"Running Task {task_num} for File Set {i} (PREPROCESSED INPUT)...")
            if task_num == 6:
                processed_result_preprocessed = json.loads(connection_finder_preprocessed.find_connections())
            else:
                processed_result_preprocessed = json.loads(connection_finder_preprocessed.check_connections())

            output_path_preprocessed = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output_preprocessed.json")
            with open(output_path_preprocessed, 'w') as output_file:
                json.dump(processed_result_preprocessed, output_file, indent=4)
            print(f"Processed results saved to {output_path_preprocessed}")

            ### ✅ **Compare Processed Results with Expected Output**
            with open(expected_result_path, 'r') as file:
                expected_result = json.load(file)

            result_raw = "PASS" if processed_result_raw == expected_result else "FAIL"
            result_preprocessed = "PASS" if processed_result_preprocessed == expected_result else "FAIL"

            test_results.append((f"Task {task_num} - File Set {i} (RAW)", result_raw))
            test_results.append((f"Task {task_num} - File Set {i} (PREPROCESSED)", result_preprocessed))

    print("\n✅ All Tests Completed ✅")

    ### ✅ **Summary of test results**
    print("\n=== Test Summary ===")
    for test, result in test_results:
        color = Colors.GREEN if result == "PASS" else Colors.RED
        print(f"{color}{test}: {result}{Colors.RESET}")
