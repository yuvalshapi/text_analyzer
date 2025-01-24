import json
import os
import pandas as pd

from task3.task3 import NamesCounter


def print_differences_and_find_sources(processed, expected, path="", sentences_file=None):
    """
    Recursively compares two dictionaries or lists, prints detailed differences,
    and locates the source of discrepancies in the source file if applicable.

    :param processed: The processed result (dict, list, or value).
    :param expected: The expected result (dict, list, or value).
    :param path: The path to the current key being compared (for context in nested structures).
    :param sentences_file: Path to the source file for locating discrepancies.
    """
    if isinstance(processed, dict) and isinstance(expected, dict):
        processed_keys = set(processed.keys())
        expected_keys = set(expected.keys())

        for key in processed_keys - expected_keys:
            print(f"Extra key at {path}/{key}: {processed[key]}")
        for key in expected_keys - processed_keys:
            print(f"Missing key at {path}/{key}: {expected[key]}")

        for key in processed_keys & expected_keys:
            print_differences_and_find_sources(processed[key], expected[key], path=f"{path}/{key}",
                                               sentences_file=sentences_file)

    elif isinstance(processed, list) and isinstance(expected, list):
        min_length = min(len(processed), len(expected))
        for i in range(min_length):
            print_differences_and_find_sources(processed[i], expected[i], path=f"{path}[{i}]",
                                               sentences_file=sentences_file)
        if len(processed) > len(expected):
            for i in range(len(expected), len(processed)):
                print(f"Extra item at {path}[{i}]: {processed[i]}")
                if sentences_file and "Processed Sentences" in path:
                    locate_sentence_in_file(sentences_file, i)
        elif len(expected) > len(processed):
            for i in range(len(processed), len(expected)):
                print(f"Missing item at {path}[{i}]: {expected[i]}")

    else:
        if processed != expected:
            print(f"Difference at {path}:")
            print(f"  Processed: {processed}")
            print(f"  Expected:  {expected}")


def locate_sentence_in_file(sentences_file, index):
    """
    Finds and prints the source of a discrepancy in the sentences file based on the index.

    :param sentences_file: Path to the sentences CSV file.
    :param index: The index in the processed result that contains the discrepancy.
    """
    try:
        df = pd.read_csv(sentences_file)

        if index >= len(df):
            print(f"Index {index} is out of bounds for the file with {len(df)} entries.")
            return

        raw_sentence = df.iloc[index].tolist()
        print(f"Source sentence for discrepancy at index {index}: {raw_sentence}")
    except Exception as e:
        print(f"Error reading file {sentences_file}: {e}")

if __name__ == '__main__':

    # Test logic
    base_dir = ""
    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 5):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, f"test{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, f"test{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, f"test{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir , f"test{i}", f"Q3_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir,f"test{i}",f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = NamesCounter(s_path, p_path, w_path, False)
        processed_result = json.loads(T._to_json())

        # Save processed result to a file
        with open(output_path, 'w') as outfile:
            json.dump(processed_result, outfile, indent=4)
        print(f"Processed result saved to {output_path}")

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"File set {i}: PASS")
        else:
            print(f"File set {i}: FAIL")
            print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)
