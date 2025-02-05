import os
import json
import pytest
from text_analayzer_project_final.textprocessor.textprocessor import TextPreprocessor
from text_analayzer_project_final.connection_finder.connection_finder import ConnectionFinder

# ✅ Define test parameters
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "2_examples")
W_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "1_data", "data", "REMOVEWORDS.csv")

# ✅ Define parameters for Task 9
TASK_FOLDER = "Q9_examples"
TASK_NUM = 9

# ✅ Correct thresholds for each test case
TEST_CASES = [
    (TASK_FOLDER, TASK_NUM, 1, 1),  # Test 1: Threshold = 1
    (TASK_FOLDER, TASK_NUM, 3, 2),  # Test 2: Threshold = 3
    (TASK_FOLDER, TASK_NUM, 6, 3)   # Test 3: Threshold = 6
]

@pytest.mark.parametrize("task_folder, task_num, threshold, file_set", TEST_CASES)
def test_task9(task_folder, task_num, threshold, file_set):
    """
    Test Task 9 using only RAW CSV input.
    """

    # Set File Paths for RAW Input
    s_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", f"sentences_small_{file_set}.csv")

    # Set Expected Result File Paths
    expected_result_filename = f"Q9_result{file_set}.json"
    expected_result_path = os.path.join(BASE_DIR, task_folder, f"example_{file_set}", expected_result_filename)
    print(s_path)
    # Test Non-Preprocessed Data (RAW)
    text_preprocessor = TextPreprocessor(s_path, None, W_PATH, False, task_num)  # 🚨 No "people_small_{file_set}.csv"

    connection_finder = ConnectionFinder(
        processed_data=text_preprocessor,
        w_size=None,  # 🚨 Task 9 does NOT use window size
        threshold=threshold,
        fixed_len=None,  # 🚨 Task 9 does NOT use fixed length
        people_connections_path=None  # 🚨 Task 9 does NOT need people connections
    )

    # Run Task 9 Function
    processed_result_raw = json.loads(connection_finder.group_sentences())  # 🚨 Task 9 uses `group_sentences()`

    # Compare Processed Results with Expected Output
    with open(expected_result_path, 'r') as file:
        expected_result = json.load(file)

    assert processed_result_raw == expected_result, f"Task 9, File Set {file_set} (RAW) FAILED"
