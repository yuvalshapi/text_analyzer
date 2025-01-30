import os
import json
import pytest
import tempfile
from text_analayzer_project_final.connection_finder.connection_finder import ConnectionFinder
from task1.textprocessor import TextPreprocessor

# Define test parameters
import os

# Automatically locate the `2_examples` directory relative to the test script's location
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "2_examples")
W_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "1_data", "data", "REMOVEWORDS.csv")

# Define parameters for each task
W_SIZES = [[4, 3, 5, 5], [5, 3, 5, 5], [3, 3, 3]]  # Window sizes for Task 6
THRESHOLDS = [[4, 2, 2, 1], [2, 2, 1, 2], [2, 2, 2]]  # Thresholds for Task 6
FIXED_LENGTHS = [2, 3, 8]  # Fixed lengths (None for Task 7, int for Task 8)

TASKS = [
    ("Q6_examples", 6, W_SIZES[0], THRESHOLDS[0], None, 4),  # Task 6 (4 tests)
    ("Q7_examples", 7, W_SIZES[1], THRESHOLDS[1], None, 4),  # Task 7 (4 tests)
    ("Q8_examples", 8, W_SIZES[2], THRESHOLDS[2], FIXED_LENGTHS, 3)  # Task 8 (3 tests)
]

# Create test cases dynamically
test_cases = []
for task_folder, task_num, w_sizes, thresholds, fixed_lens, max_tests in TASKS:
    for file_set in range(1, max_tests + 1):
        test_cases.append((task_folder, task_num, w_sizes, thresholds, fixed_lens, file_set))


@pytest.mark.parametrize("task_folder, task_num, w_sizes, thresholds, fixed_lens, file_set", test_cases)
def test_connection_finder_raw(task_folder, task_num, w_sizes, thresholds, fixed_lens, file_set):
    """
    Test ConnectionFinder for tasks 6-8 using only RAW CSV input.
    """

    # File paths for raw input
    s_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"sentences_small_{file_set}.csv")
    p_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_small_{file_set}.csv")
    conn_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_connections_{file_set}.json")

    # ✅ **Set Expected Result File Paths According to the Given Naming Convention**
    if task_num == 6:
        expected_result_filename = f"Q6_result{file_set}_w{w_sizes[file_set - 1]}_t{thresholds[file_set - 1]}.json"
    elif task_num == 7:
        expected_result_filename = f"Q7_result{file_set}_w{w_sizes[file_set - 1]}_t{thresholds[file_set - 1]}.json"
    else:  # Task 8 (which has only 3 tests)
        expected_result_filename = f"Q8_example_{file_set}_w_{w_sizes[file_set - 1]}_threshold_{thresholds[file_set - 1]}_fixed_length_{fixed_lens[file_set - 1]}.json"

    expected_result_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", expected_result_filename)

    # ✅ **Test Non-Preprocessed Data (RAW)**
    text_preprocessor = TextPreprocessor(s_path, p_path, W_PATH, False, task_num)

    connection_finder = ConnectionFinder(
        processed_data=text_preprocessor,
        w_size=w_sizes[file_set - 1],
        threshold=thresholds[file_set - 1],
        fixed_len=fixed_lens[file_set - 1] if fixed_lens else None,
        people_connections_path=conn_path if task_num in [7, 8] else None
    )

    # ✅ **Run the corresponding function based on the task number**
    if task_num == 6:
        processed_result_raw = json.loads(connection_finder.find_connections())
    else:
        processed_result_raw = json.loads(connection_finder.check_connections())

    # ✅ **Compare Processed Results with Expected Output**
    with open(expected_result_path, 'r') as file:
        expected_result = json.load(file)

    # ✅ **Assertions for Pytest**
    assert processed_result_raw == expected_result, f"Task {task_num}, File Set {file_set} (RAW) FAILED"


@pytest.mark.parametrize("task_folder, task_num, w_sizes, thresholds, fixed_lens, file_set", test_cases)
def test_connection_finder_preprocessed(task_folder, task_num, w_sizes, thresholds, fixed_lens, file_set):
    """
    Test ConnectionFinder for tasks 6-8 using PREPROCESSED input from a temporary file.
    """

    # File paths for raw input
    s_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"sentences_small_{file_set}.csv")
    p_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_small_{file_set}.csv")
    conn_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_connections_{file_set}.json")

    # ✅ **Set Expected Result File Paths According to the Given Naming Convention**
    if task_num == 6:
        expected_result_filename = f"Q6_result{file_set}_w{w_sizes[file_set - 1]}_t{thresholds[file_set - 1]}.json"
    elif task_num == 7:
        expected_result_filename = f"Q7_result{file_set}_w{w_sizes[file_set - 1]}_t{thresholds[file_set - 1]}.json"
    else:  # Task 8 (which has only 3 tests)
        expected_result_filename = f"Q8_example_{file_set}_w_{w_sizes[file_set - 1]}_threshold_{thresholds[file_set - 1]}_fixed_length_{fixed_lens[file_set - 1]}.json"

    expected_result_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", expected_result_filename)

    # ✅ **Create a Temporary File for Preprocessed Input**
    text_preprocessor = TextPreprocessor(s_path, p_path, W_PATH, False, task_num)
    preprocessed_data = json.loads(text_preprocessor.get_json_format())

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as temp_file:
        json.dump(preprocessed_data, temp_file, indent=4)
        temp_filename = temp_file.name  # Store temp file path

    # ✅ **Use Preprocessed Input from the Temporary File**
    connection_finder = ConnectionFinder(
        processed_data=TextPreprocessor(temp_filename, None, None, True, task_num),
        w_size=w_sizes[file_set - 1],
        threshold=thresholds[file_set - 1],
        fixed_len=fixed_lens[file_set - 1] if fixed_lens else None,
        people_connections_path=conn_path if task_num in [7, 8] else None
    )

    # ✅ **Run the corresponding function based on the task number**
    if task_num == 6:
        processed_result_preprocessed = json.loads(connection_finder.find_connections())
    else:
        processed_result_preprocessed = json.loads(connection_finder.check_connections())

    # ✅ **Compare Processed Results with Expected Output**
    with open(expected_result_path, 'r') as file:
        expected_result = json.load(file)

    # ✅ **Assertions for Pytest**
    assert processed_result_preprocessed == expected_result, f"Task {task_num}, File Set {file_set} (PREPROCESSED) FAILED"

    # ✅ **Cleanup Temporary File**
    os.remove(temp_filename)
