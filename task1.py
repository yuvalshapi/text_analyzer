import string
import re
import os
import json
import pandas as pd
import general_functions as gf


class TextPreprocessor:
    """
    A class used to preprocess and prepare input text data for further analysis.
    The class supports reading input data, processing sentences, cleaning names,
    and removing unwanted words. Outputs are structured in a JSON format.
    """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 common_words_file_path: str = None,
                 prog_num: int = 1):
        """
        Initializes the TextPreprocessor class with input file paths and optional parameters.

        :param sentences_file_path: Path to the input sentences file.
        :param name_file_path: (Optional) Path to the file containing names data.
        :param common_words_file_path: (Optional) Path to the file containing common words to remove.
        :param prog_num: (Optional) An integer representing the task/question number. Default is 1.
        """
        # Load the sentences data from the provided file path
        self.sentences_data = pd.read_csv(sentences_file_path)

        # Extract the first column as the list of sentences
        self.sentences_list = self.sentences_data[self.sentences_data.columns[0]].tolist()

        # If a names file is provided, load and process it
        if name_file_path:
            self.people_names_data = pd.read_csv(name_file_path)

            # Extract 'Name' and 'Other Names' columns
            self.other_names_list = self.people_names_data[self.people_names_data.columns[0]].tolist()
            self.names_list = self.people_names_data[self.people_names_data.columns[1]].tolist()
        else:
            # Initialize empty structures if no names file is provided
            self.people_names_data = None
            self.other_names_list = []
            self.names_list = []

        # If a common words file is provided, load and process it
        if common_words_file_path:
            self.common_words = pd.read_csv(common_words_file_path)

            # Extract the list of words to remove from the first column
            self.words_to_remove = self.common_words[self.common_words.columns[0]].dropna().str.strip().tolist()
        else:
            # Initialize an empty list if no common words file is provided
            self.common_words = None
            self.words_to_remove = []

        # Store the program number for output formatting
        self.prog_num = prog_num

        # Automatically process names and sentences if optional files are provided
        if self.people_names_data is not None and not self.people_names_data.empty:
            self._process_names()
        self._process_data_inputs()

    def get_processed_sentences(self):
        """
        Retrieves the processed sentences as a list of lists.

        :return: List of processed sentences, where each sentence is represented as a list of words.
        """
        return self.sentences_list

    def get_processed_names(self):
        """
        Retrieves the processed names as a list.

        :return: List of cleaned and processed names.
        """
        return self.names_list

    def _process_data_inputs(self):
        """
        Processes the input sentences by performing the following steps:
        1. Splits sentences by new lines.
        2. Removes empty sentences.
        3. Cleans sentences (removes punctuation, converts to lowercase).
        4. Converts sentences into lists of words.
        5. Removes common words from the sentences.
        6. Removes any resulting empty lists.
        """
        # Split sentences into smaller strings based on new line characters
        self.sentences_list = [item for s in self.sentences_list for item in s.split("\n")]

        # Remove any empty strings caused by splitting or blank lines in the input
        self.sentences_list = [s for s in self.sentences_list if s.strip()]

        # Clean each sentence by removing punctuation, extra spaces, and converting to lowercase
        self.sentences_list = [gf.clean_text(text) for text in self.sentences_list]

        # Split cleaned sentences into lists of words
        self.sentences_list = [sentence.split() for sentence in self.sentences_list]

        # Remove common words (e.g., stop words) from the sentences
        self.sentences_list = gf.remove_words(self.sentences_list, self.words_to_remove)

        # Remove any empty lists caused by removing all words from a sentence
        self.sentences_list = [s for s in self.sentences_list if s]

    def _process_names(self):
        """
        Processes names and other names by performing the following steps:
        1. Cleans and removes duplicates while preserving the original structure of the DataFrame.
        2. Splits the 'Name' and 'Other Names' columns into lists of words.
        3. Separates 'names' and 'other names' into distinct lists.
        4. Removes unwanted words from the names and other names.
        """
        # Clean and split the 'Name' column into lists of words
        self.people_names_data[self.people_names_data.columns[0]] = (
            self.people_names_data[self.people_names_data.columns[0]]
            .dropna()  # Remove any null values
            .apply(lambda x: gf.clean_text(x.strip()).split())  # Clean and split into words
        )

        # Clean and split the 'Other Names' column into lists of lists of words
        self.people_names_data[self.people_names_data.columns[1]] = (
            self.people_names_data[self.people_names_data.columns[1]]
            .fillna("")  # Replace null values with empty strings
            .apply(lambda x: [gf.clean_text(name.strip()).split() for name in x.split(",") if name.strip()])
        )

        # Extract processed 'Name' and 'Other Names' columns into separate lists
        self.names_list = self.people_names_data[self.people_names_data.columns[0]].tolist()
        self.other_names_list = self.people_names_data[self.people_names_data.columns[1]].tolist()

        # Remove common words from the 'names' list
        self.names_list = gf.remove_words(self.names_list, self.words_to_remove)

        # Remove common words from the 'other names' list
        self.other_names_list = gf.remove_words(self.other_names_list, self.words_to_remove)

    def __str__(self):
        """
        Returns a JSON representation of the processed data.

        :return: JSON string representation of the processed sentences and names.
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts the processed sentences and names into a structured JSON format.

        :return: JSON string containing processed sentences and names.
        """
        # Prepare processed sentences
        processed_sentences = self.sentences_list

        # Pair each name with its corresponding list of other names
        processed_names = [
            [self.names_list[i], self.other_names_list[i]]
            for i in range(len(self.names_list))
        ]

        # Construct the output dictionary in the required format
        output = {
            f"Question {self.prog_num}": {
                "Processed Sentences": processed_sentences,
                "Processed Names": processed_names,
            }
        }

        # Return the JSON string representation of the output
        return json.dumps(output, indent=4)


if __name__ == '__main__':

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


    # Test logic
    base_dir = "text_analyzer"

    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 4):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, "2_examples", "Q1_examples", f"example_{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, "2_examples", "Q1_examples", f"example_{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, "1_data", "data", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, "2_examples", "Q1_examples", f"example_{i}", f"q1_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, "2_examples", "Q1_examples", f"example_{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = TextPreprocessor(s_path, p_path, w_path, 1)
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
