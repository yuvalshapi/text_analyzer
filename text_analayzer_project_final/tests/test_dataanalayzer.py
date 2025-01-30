import os
import json
import pytest
from text_analayzer_project_final.textprocessor.textprocessor import TextPreprocessor
from text_analayzer_project_final.data_analyzer.data_analyzer import DataAnalyzer


# Define test parameters
BASE_DIR = os.path.join("2_examples")
W_PATH = os.path.join("1_data", "data", "REMOVEWORDS.csv")

SEQ_LENGTHS = [3, 4, 5]  # Task 2 sequence lengths
CONTEXT_SIZES = [3, 4, 5, 4]  # Task 5 context extraction sizes

TASKS = [
    ("Q2_examples", 2, SEQ_LENGTHS, 3),  # Task 2 (3 tests only)
    ("Q3_examples", 3, None, 4),  # Task 3 (4 tests)
    ("Q4_examples", 4, None, 4),  # Task 4 (4 tests)
    ("Q5_examples", 5, CONTEXT_SIZES, 4)  # Task 5 (4 tests)
]

# Create test cases dynamically (removes extra test from Task 2)
test_cases = []
for task_folder, task_num, param_list, max_tests in TASKS:
    for file_set in range(1, max_tests + 1):  # Use max_tests to filter Task 2
        test_cases.append((task_folder, task_num, param_list, file_set))

# Test cases for tasks 2-5 with correct file set count
@pytest.mark.parametrize("task_folder, task_num, param_list, file_set", test_cases)
def test_data_analyzer_raw(task_folder, task_num, param_list, file_set):
    """
    Test DataAnalyzer tasks (2-5) with raw CSV input only (no preprocessed JSON).
    Ensures Task 2 runs only 3 tests, while others run 4.
    """

    # File paths
    s_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"sentences_small_{file_set}.csv")

    if task_num == 4:
        p_path = None
        k_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"kseq_query_keys_{file_set}.json")
    else:
        p_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"people_small_{file_set}.csv")
        k_path = None

    expected_result_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"Q{task_num}_result{file_set}.json")

    # ✅ **Test Raw Data**
    text_preprocessor = TextPreprocessor(s_path, p_path, W_PATH, False, 1)

    if task_num == 2:
        data_analyzer = DataAnalyzer(text_preprocessor, param_list[file_set - 1], k_path)
    elif task_num == 5:
        data_analyzer = DataAnalyzer(text_preprocessor, param_list[file_set - 1], k_path)
    else:
        data_analyzer = DataAnalyzer(text_preprocessor, 1, k_path)

    if task_num == 2:
        processed_result_raw = json.loads(data_analyzer.sequence_counter())
    elif task_num == 3:
        processed_result_raw = json.loads(data_analyzer.names_counter())
    elif task_num == 4:
        processed_result_raw = json.loads(data_analyzer.kseqengine())
    else:
        processed_result_raw = json.loads(data_analyzer.find_context())

    # ✅ **Compare Processed Results with Expected Output**
    with open(expected_result_path, 'r') as file:
        expected_result = json.load(file)

    # ✅ **Assertions for Pytest**
    assert processed_result_raw == expected_result, f"Task {task_num}, File Set {file_set} (RAW) FAILED"
