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

    # Test logic
    base_dir = os.path.join("2_examples")

    # Define parameters for each task
    w_sizes = [[4, 3, 5, 5],[5,3,5,5],[3,3,3]]  # Window sizes for Task 6
    thresholds = [[4, 2, 2, 1],[2,2,1,2],[2,2,2]]  # Thresholds for Task 6
    fixed_lengths = [2, 3, 8]  # Fixed lengths (None for Task 7, int for Task 8)

    output_results_dir = os.path.join("output_results")
    os.makedirs(output_results_dir, exist_ok=True)

    w_path = os.path.join("1_data","data", f"REMOVEWORDS.csv")
    for task_num, task_folder in enumerate(["Q6_examples", "Q7_examples", "Q8_examples"], start=6):
        for i in range(1, 5 if task_num != 8 else 4):  # ✅ Task 8 has only 3 tests, so range is (1,4)
            print(f"\n=== Running Tests for Task {task_num}, File Set {i} ===")

            # File paths
            s_path = os.path.join(base_dir, task_folder, f"example_{i}", f"sentences_small_{i}.csv")
            p_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_small_{i}.csv")
            conn_path = os.path.join(base_dir, task_folder, f"example_{i}", f"people_connections_{i}.json")

            # ✅ **Set Expected Result File Paths According to the Given Naming Convention**
            if task_num == 6:
                expected_result_filename = f"Q6_result{i}_w{w_sizes[0][i-1]}_t{thresholds[0][i-1]}.json"
            elif task_num == 7:
                expected_result_filename = f"Q7_result{i}_w{w_sizes[1][i-1]}_t{thresholds[1][i-1]}.json"
            else:  # Task 8 (which has only 3 tests)
                expected_result_filename = f"Q8_example_{i}_w_{w_sizes[2][i-1]}_threshold_{thresholds[2][i-1]}_fixed_length_{fixed_lengths[i-1]}.json"

            expected_result_path = os.path.join(base_dir, task_folder, f"example_{i}", expected_result_filename)

            # ✅ **Initialize TextPreprocessor**
            print(f"Preprocessing input for Task {task_num}, File Set {i}...")
            text_preprocessor = TextPreprocessor(s_path, p_path, w_path, False, task_num)
            preprocessed_data = json.loads(text_preprocessor.get_json_format())

            # ✅ **Initialize ConnectionFinder with the correct parameters**
            print(f"Initializing ConnectionFinder for Task {task_num}, File Set {i}...")
            connection_finder = cf.ConnectionFinder(
                processed_data=text_preprocessor,
                w_size=w_sizes[task_num - 6][i - 1],
                threshold=thresholds[task_num - 6][i - 1],
                fixed_len=fixed_lengths[i - 1] if task_num == 8 else None,
                people_connections_path=conn_path if task_num in [7, 8] else None  # Only needed for Task 7 and 8
            )

            # ✅ **Run the correct function based on the task number**
            print(f"Running Task {task_num} for File Set {i}...")
            if task_num == 6:
                processed_result = json.loads(connection_finder.find_connections())
            else:  # Task 7 and 8 (same function, different fixed_len values)
                processed_result = json.loads(connection_finder.check_connections())

            # ✅ **Save Processed Results to File**
            output_path = os.path.join(output_results_dir, f"task_{task_num}_file_set_{i}_output.json")
            with open(output_path, 'w') as output_file:
                json.dump(processed_result, output_file, indent=4)
            print(f"Processed results saved to {output_path}")

            # ✅ **Compare Processed Results with Expected Output**
            with open(expected_result_path, 'r') as file:
                expected_result = json.load(file)

            result = "PASS" if processed_result == expected_result else "FAIL"
            test_results.append((f"Task {task_num} - File Set {i}", result))

    print("\n✅ All Tests Completed ✅")

    # ✅ **Summary of test results**
    print("\n=== Test Summary ===")
    for test, result in test_results:
        color = Colors.GREEN if result == "PASS" else Colors.RED
        print(f"{color}{test}: {result}{Colors.RESET}")
