import pytest
import sys
import json
from text_analayzer_project_final.main.main import readargs, validate_args


### **🚀 Helper Function**
def run_with_invalid_args(args_list, capfd):
    """
    Helper function to run `validate_args` with invalid arguments and check that it exits.
    """
    with pytest.raises(SystemExit) as exc_info:
        args = readargs(args_list)
        validate_args(args)

    assert exc_info.value.code == 1, "Expected sys.exit(1)"


### **🚀 Test Cases for Missing Required Arguments**
def test_missing_sentences_or_preprocessed(capfd):
    """ Test case where neither --sentences nor --preprocessed is provided. """
    args_list = ["--task", "1", "--removewords", "remove.csv"]
    run_with_invalid_args(args_list, capfd)


def test_missing_removewords(capfd):
    """ Test case where --removewords is missing. """
    args_list = ["--task", "1", "--sentences", "sentences.csv"]
    run_with_invalid_args(args_list, capfd)


def test_task_2_missing_maxk(capfd):
    """ Test case where Task 2 is missing --maxk. """
    args_list = ["--task", "2", "--sentences", "sentences.csv", "--removewords", "remove.csv"]
    run_with_invalid_args(args_list, capfd)


def test_task_4_missing_qsek_query_path(capfd):
    """ Test case where Task 4 is missing --qsek_query_path. """
    args_list = ["--task", "4", "--sentences", "sentences.csv", "--removewords", "remove.csv"]
    run_with_invalid_args(args_list, capfd)


def test_task_6_missing_windowsize_threshold(capfd):
    """ Test case where Task 6 is missing --windowsize and --threshold. """
    args_list = ["--task", "6", "--sentences", "sentences.csv", "--removewords", "remove.csv"]
    run_with_invalid_args(args_list, capfd)


def test_task_7_missing_pairs(capfd):
    """ Test case where Task 7 is missing --pairs. """
    args_list = ["--task", "7", "--sentences", "sentences.csv", "--removewords", "remove.csv", "--windowsize", "5", "--threshold", "2"]
    run_with_invalid_args(args_list, capfd)


def test_task_8_missing_fixed_length(capfd):
    """ Test case where Task 8 is missing --fixed_length. """
    args_list = ["--task", "8", "--sentences", "sentences.csv", "--removewords", "remove.csv", "--windowsize", "3", "--threshold", "2", "--pairs", "pairs.json"]
    run_with_invalid_args(args_list, capfd)


def test_invalid_task_number(capfd):
    """ Test case where an invalid task number is given. """
    args_list = ["--task", "99", "--sentences", "sentences.csv", "--removewords", "remove.csv"]
    run_with_invalid_args(args_list, capfd)
