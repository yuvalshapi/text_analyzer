import os
import json
import pytest
from text_analayzer_project_final.main.main import readargs, process_task  # Import functions from main.py

# Base directory where test data is stored
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "2_examples")
REMOVE_WORDS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "1_data", "data", "REMOVEWORDS.csv")

# Define test parameters for tasks
TASKS = [
    ("Q1_examples", 1, {}, 3),  # Task 1 (3 tests)
    ("Q2_examples", 2, {"maxk": [3, 4, 5]}, 3),  # Task 2 (3 tests)
    ("Q3_examples", 3, {}, 4),  # Task 3 (4 tests)
    ("Q4_examples", 4, {"qsek_query_path": True}, 4),  # Task 4 (4 tests)
    ("Q5_examples", 5, {"maxk": [3, 4, 5, 4]}, 4),  # Task 5 (4 tests)
    ("Q6_examples", 6, {"windowsize": [4, 3, 5, 5], "threshold": [4, 2, 2, 1]}, 4),  # Task 6 (4 tests)
    ("Q7_examples", 7, {"windowsize": [5, 3, 5, 5], "threshold": [2, 2, 1, 2], "pairs": True}, 4),  # Task 7 (4 tests)
    ("Q8_examples", 8, {"windowsize": [3, 3, 3], "threshold": [2, 2, 2], "fixed_length": [2, 3, 8], "pairs": True}, 3),  # Task 8 (3 tests)
]

# Dynamically generate test cases
test_cases = []
for task_folder, task_num, params, max_tests in TASKS:
    for file_set in range(1, max_tests + 1):
        test_cases.append((task_folder, task_num, params, file_set))


@pytest.mark.parametrize("task_folder, task_num, params, file_set", test_cases)
def test_main_raw(task_folder, task_num, params, file_set) -> None:
    """
    Test `process_task` in `main.py` using raw CSV/JSON input.
    """

    # Define file paths
    s_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"sentences_small_{file_set}.csv")
    p_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_small_{file_set}.csv")
    k_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"kseq_query_keys_{file_set}.json")
    pairs_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_connections_{file_set}.json")  # For Task 7 & 8

    # ✅ **Set Expected Result File Paths According to Task Format**
    if task_num == 6:
        expected_result_filename = f"Q6_result{file_set}_w{params['windowsize'][file_set - 1]}_t{params['threshold'][file_set - 1]}.json"
    elif task_num == 7:
        expected_result_filename = f"Q7_result{file_set}_w{params['windowsize'][file_set - 1]}_t{params['threshold'][file_set - 1]}.json"
    elif task_num == 8:
        expected_result_filename = f"Q8_example_{file_set}_w_{params['windowsize'][file_set - 1]}_threshold_{params['threshold'][file_set - 1]}_fixed_length_{params['fixed_length'][file_set - 1]}.json"
    else:
        expected_result_filename = f"Q{task_num}_result{file_set}.json"

    expected_result_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", expected_result_filename)

    # Ensure required files exist
    assert os.path.exists(s_path), f"Missing file: {s_path}"
    assert os.path.exists(expected_result_path), f"Missing expected result file: {expected_result_path}"

    # ✅ **Build command-line argument list**
    args_list = ["--task", str(task_num), "--sentences", s_path, "--removewords", REMOVE_WORDS_PATH]

    # Add names file if needed (all tasks except Q4)
    if task_num != 4:
        args_list.extend(["--names", p_path])

    # Add query path if needed (Task 4)
    if "qsek_query_path" in params:
        args_list.extend(["--qsek_query_path", k_path])

    # Add pairs_to_check path if needed (Tasks 7 & 8)
    if "pairs" in params:
        args_list.extend(["--pairs", pairs_path])

    # Add task-specific parameters (e.g., window size, threshold)
    for param, values in params.items():
        if values is True:  # Special case for query paths or pairs_to_check
            continue
        args_list.extend([f"--{param}", str(values[file_set - 1])])

    # ✅ **Run the function with simulated arguments**
    args = readargs(args_list)
    output_json = process_task(args)

    # ✅ **Load Expected Result**
    with open(expected_result_path, "r") as file:
        expected_json = json.load(file)

    # ✅ **Assertions**
    assert json.loads(output_json) == expected_json, (
        f"\nTask {task_num}, File Set {file_set} FAILED"
        f"\nExpected: {json.dumps(expected_json, indent=2)}"
        f"\nGot: {json.dumps(json.loads(output_json), indent=2)}"
    )
