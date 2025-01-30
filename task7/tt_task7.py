import json
import os
import text_analayzer_project_final.general_files.general_test_functions as gtf
import task6.task6 as task6
import task7.task7 as task7

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

if __name__ == '__main__':
    # Test logic
    base_dir = ""
    window_size = [5, 3, 5, 5]
    thresholds = [2, 2, 1, 2]
    w_path = os.path.join(f'../../', f'../', f"text_analyzer", f"1_data", f"data", "REMOVEWORDS.csv")

    # Iterate through 1, 2, 3, and 4 for file sets
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        e_path = os.path.join(base_dir, f"test{i}", f"Q7_result{i}_w{window_size[i - 1]}_t{thresholds[i - 1]}.json")
        pc_path = os.path.join(base_dir, f"test{i}", f"people_connections_{i}.json")

        # Output JSON files
        output_path_task6 = os.path.join(base_dir, f"test{i}", f"task6_output{i}.json")
        output_path_task7_not_processed = os.path.join(base_dir, f"test{i}", f"task7_result{i}_not_processed.json")
        output_path_task7_preprocessed = os.path.join(base_dir, f"test{i}", f"task7_result{i}_preprocessed.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # **Task 7 with non-preprocessed input**
        print(f"Running Task 7 with raw input for File Set {i}...")
        task7_non_preprocessed = task7.IndirectConnector(
            s_path, p_path, w_path, pc_path, False, window_size[i - 1], thresholds[i - 1]
        )
        task7_non_preprocessed_result = json.loads(task7_non_preprocessed.get_json_format())

        # Save non-preprocessed result to a file
        with open(output_path_task7_not_processed, 'w') as outfile:
            json.dump(task7_non_preprocessed_result, outfile, indent=4)
        print(f"Task 7 (not processed) result saved to {output_path_task7_not_processed}")

        # Compare non-preprocessed results
        if task7_non_preprocessed_result == expected_result:
            print(f"{Colors.GREEN}Test {i} (Task 7 with raw input): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (Task 7 with raw input): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(task7_non_preprocessed_result, expected_result, sentences_file=s_path)

        # **Task 6: Create preprocessed input for Task 7**
        print(f"Running Task 6 to create preprocessed input for Task 7 for File Set {i}...")
        connection_finder = task6.ConnectionFinder(
            s_path, p_path, w_path, False, window_size[i - 1], thresholds[i - 1]
        )
        task6_output = json.loads(connection_finder.get_json_format())

        # Save Task 6 output to a file
        with open(output_path_task6, 'w') as outfile:
            json.dump(task6_output, outfile, indent=4)
        print(f"Task 6 output saved to {output_path_task6}")

        # **Task 7 with preprocessed input**
        print(f"Running Task 7 with preprocessed input for File Set {i}...")
        task7_preprocessed = task7.IndirectConnector(
            output_path_task6, None, None, pc_path, True, window_size[i - 1], thresholds[i - 1]
        )
        task7_preprocessed_result = json.loads(task7_preprocessed.get_json_format())

        # Save preprocessed result to a file
        with open(output_path_task7_preprocessed, 'w') as outfile:
            json.dump(task7_preprocessed_result, outfile, indent=4)
        print(f"Task 7 (preprocessed) result saved to {output_path_task7_preprocessed}")

        # Compare preprocessed results
        if task7_preprocessed_result == expected_result:
            print(f"{Colors.GREEN}Test {i} (Task 7 with preprocessed input): SUCCESS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Test {i} (Task 7 with preprocessed input): FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(task7_preprocessed_result, expected_result, sentences_file=s_path)
