import string
import re
import os
import json
import pandas as pd
import general_functions as gf

class TextPreprocessor:
    """
    A class which used to make the preparations on the input text.
    The class parses the input paths and change the input data according to the various inputs
    """
    def __init__(self,
                 sentences_file_path:str,
                 name_file_path:str,
                 common_words_file_path:str,
                 prog_num:int):
        """
        A constructor for a TextPreprocessor object.
        :param sentences_file_path: A string holding the path to the actual "data" file.
        :param name_file_path: A string holding the path to the list of the names file.
        :param common_words_file_path: A string holding the path to the  common words file we should remove.
        :param prog_num: An integer that represents the program number output is expected.
        """
        self.sentences_data = pd.read_csv(sentences_file_path)
        #Converting the sentences from DF
        self.sentences_list = self.sentences_data[self.sentences_data.columns[0]].tolist()
        self.people_names_data = pd.read_csv(name_file_path)
        self.other_names_list  = self.people_names_data[self.people_names_data.columns[0]].tolist()
        self.names_list = self.people_names_data[self.people_names_data.columns[1]].tolist()
        self.common_words = pd.read_csv(common_words_file_path)
        self.words_to_remove = self.common_words[self.common_words.columns[0]].dropna().str.strip().tolist()
        self.prog_num = prog_num
        self._process_names()
        self._process_data_inputs()

    def _process_data_inputs(self):
        """
        Function which gets a TextPreprocessor object and processes it:
        1. Splitting the data according to new lines.
        2. Removing all punctuation.
        3. Converting all to lower case.
        4. Removing all common words.
        """
        # Splitting the strings by new lines
        self.sentences_list = [item for s in self.sentences_list for item in s.split("\n")]

        # Remove empty sentences from the list (action 'i')
        self.sentences_list = [s for s in self.sentences_list if s.strip()]

        # Clean the text
        self.sentences_list = [gf.clean_text(text) for text in self.sentences_list]

        # Splitting the string into lists of words, making sentences become lists of lists ('h)
        self.sentences_list = [sentence.split() for sentence in self.sentences_list]

        # Remove common words
        self.sentences_list = gf.remove_words(self.sentences_list, self.words_to_remove)

        # Remove any empty lists
        self.sentences_list = [s for s in self.sentences_list if s]

    def _process_names(self):
        """
        Processes the names and other names:
        1. Cleans and removes duplicates while preserving the original structure of the DataFrame.
        2. Processes the 'Name' and 'Other Names' columns by splitting and converting them to lists of words.
        3. Ensures `names` and `other names` are stored as two separate lists.
        4. Groups multiple "other names" into separate lists.
        """
        # Clean and process 'Name' column into a list of words
        self.people_names_data[self.people_names_data.columns[0]] = (
            self.people_names_data[self.people_names_data.columns[0]]
            .dropna()
            .apply(lambda x: gf.clean_text(x.strip()).split())  # Clean and split into words
        )

        # Clean and process 'Other Names' column into lists of words
        self.people_names_data[self.people_names_data.columns[1]] = (
            self.people_names_data[self.people_names_data.columns[1]]
            .fillna("")
            .apply(lambda x: [gf.clean_text(name.strip()).split() for name in x.split(",") if name.strip()])
        # Split names and words
        )

        # Separate 'Name' and 'Other Names' into distinct lists
        self.names_list = self.people_names_data[self.people_names_data.columns[0]].tolist()
        self.other_names_list = self.people_names_data[self.people_names_data.columns[1]].tolist()

        # Remove common words
        self.names_list = gf.remove_words(self.names_list, self.words_to_remove)
        self.other_names_list = gf.remove_words(self.other_names_list, self.words_to_remove)

    def __str__(self):
        """
        print the object ath the format asked
        :return:
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts the processed data and names into a JSON format as described.
        :return: JSON string representation of the processed data.
        """
        processed_sentences = self.sentences_list
        processed_names = [
            [self.names_list[i], self.other_names_list[i]]
            for i in range(len(self.names_list))
        ]

        # Format the output
        output = {
            f"Question {self.prog_num}": {
                "Processed Sentences": processed_sentences,
                "Processed Names": processed_names,
            }
        }

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
