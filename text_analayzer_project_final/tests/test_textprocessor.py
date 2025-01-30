import os
import json
import pytest
import text_analayzer_project_final.general_files.general_test_functions as gtf
from text_analayzer_project_final.textprocessor.textprocessor import TextPreprocessor

# Define test parameters (base directory and remove words file)
BASE_DIR = os.path.join("2_examples", "Q1_examples")
W_PATH = os.path.join("1_data", "data", "REMOVEWORDS.csv")


@pytest.mark.parametrize("file_set", [1, 2, 3])
def test_text_preprocessor(file_set):
    """
    Pytest function to test the TextPreprocessor against expected Q1 results.

    :param file_set: The test case number (1, 2, or 3).
    """
    print(f"\n=== Running Test for File Set {file_set} ===")

    # File paths for the current iteration
    p_path = os.path.join(BASE_DIR, f"example_{file_set}", f"people_small_{file_set}.csv")
    s_path = os.path.join(BASE_DIR, f"example_{file_set}", f"sentences_small_{file_set}.csv")
    e_path = os.path.join(BASE_DIR, f"example_{file_set}", f"Q1_result{file_set}.json")

    # Load the expected JSON result
    with open(e_path, 'r') as file:
        expected_result = json.load(file)

    # Instantiate TextPreprocessor and get the processed result
    text_processor = TextPreprocessor(s_path, p_path, W_PATH, False, 1)
    processed_result = json.loads(text_processor.get_json_format())

    # Assert if the results match
    assert processed_result == expected_result, gtf.print_differences_and_find_sources(
        processed_result, expected_result, sentences_file=s_path
    )
