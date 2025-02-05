import json
import pandas as pd
import sys
from text_analayzer_project_final.general_files import general_functions as gf


class TextPreprocessor:
    class TextPreprocessor:
        """
        A class used to preprocess text data for further analysis.

        It supports:
        - Loading preprocessed data from a JSON file.
        - Processing raw data from CSV files.
        - Cleaning, tokenizing, and filtering sentences.
        - Extracting and formatting names and their variations.

        ### Methods:
        - `get_processed_sentences()`: Returns a list of processed sentences.
        - `get_processed_names()`: Returns a list of cleaned names.
        - `get_dict_of_names()`: Returns a dictionary mapping names to nicknames.
        - `get_json_format()`: Provides a JSON representation of processed data.
        - `get_task_num()`: Returns the current task number.

        """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 common_words_file_path: str = None,
                 is_processed: bool = False,
                 prog_num: int = 1):
        """
        Initializes the TextPreprocessor class and loads or processes data.

        ### Parameters:
        - `sentences_file_path` (str): Path to the CSV file containing sentences.
        - `name_file_path` (str, optional): Path to the CSV file containing names and nicknames.
        - `common_words_file_path` (str, optional): Path to a CSV file containing common words to remove.
        - `is_processed` (bool, default=False): If True, loads preprocessed data from a JSON file.
        - `prog_num` (int, default=1): Identifies the task number for tracking different analyses.

        """
        self.prog_num = prog_num

        if is_processed:
            self._load_preprocessed_data(sentences_file_path)
        else:
            self._process_raw_data(sentences_file_path, name_file_path, common_words_file_path)

    def _load_preprocessed_data(self, json_file_path):
        """ Loads preprocessed data from a JSON file. """
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, PermissionError):
            print(f"File '{json_file_path}' is invalid, try again.")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error while opening '{json_file_path}': {e}")
            sys.exit(1)

        self.sentences_list = data[f"Question 1"]["Processed Sentences"]
        self.names_list = [name_data[0] for name_data in data[f"Question 1"]["Processed Names"]]
        self.other_names_list = [name_data[1] for name_data in data[f"Question 1"]["Processed Names"]]

    def _process_raw_data(self, sentences_file_path, name_file_path, common_words_file_path):
        """ Processes raw input data from CSV files. """
        try:
            self.sentences_data = pd.read_csv(sentences_file_path)
        except (FileNotFoundError, PermissionError):
            print(f"File '{sentences_file_path}' is invalid, try again.")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error while opening '{sentences_file_path}': {e}")
            sys.exit(1)

        self.sentences_list = self.sentences_data[self.sentences_data.columns[0]].tolist()

        if name_file_path:
            try:
                self.people_names_data = pd.read_csv(name_file_path)
            except (FileNotFoundError, PermissionError):
                print(f"File '{name_file_path}' is invalid, try again.")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error while opening '{name_file_path}': {e}")
                sys.exit(1)

            self.other_names_list = self.people_names_data[self.people_names_data.columns[0]].tolist()
            self.names_list = self.people_names_data[self.people_names_data.columns[1]].tolist()
        else:
            self.people_names_data = None
            self.other_names_list = []
            self.names_list = []

        if common_words_file_path:
            try:
                self.common_words = pd.read_csv(common_words_file_path)
            except (FileNotFoundError, PermissionError):
                print(f"File '{common_words_file_path}' is invalid, try again.")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error while opening '{common_words_file_path}': {e}")
                sys.exit(1)

            self.words_to_remove = self.common_words[self.common_words.columns[0]].dropna().str.strip().tolist()
        else:
            self.common_words = None
            self.words_to_remove = []

        if self.people_names_data is not None and not self.people_names_data.empty:
            self._process_names()
        self._process_data_inputs()

    def get_processed_sentences(self):
        """ Retrieves the processed sentences as a list of lists. """
        return self.sentences_list

    def get_processed_names(self):
        """ Retrieves the processed names as a list. """
        return self.names_list

    def get_dict_of_names(self):
        """ Constructs a dictionary where each key is a cleaned name, and its value is a list of cleaned nicknames. """
        return {
            " ".join(name): [" ".join(nickname) for nickname in nicknames]
            for name, nicknames in zip(self.names_list, self.other_names_list)
        }

    def _process_data_inputs(self):
        """ Processes the input sentences by cleaning, tokenizing, and removing stop words. """
        self.sentences_list = [item for s in self.sentences_list for item in s.split("\n")]
        self.sentences_list = [s for s in self.sentences_list if s.strip()]
        self.sentences_list = [gf.clean_text(text) for text in self.sentences_list]
        self.sentences_list = [sentence.split() for sentence in self.sentences_list]
        self.sentences_list = gf.remove_words(self.sentences_list, self.words_to_remove)
        self.sentences_list = [s for s in self.sentences_list if s]

    def _process_names(self):
        """ Processes names and their variations by cleaning and removing unwanted words. """
        self.people_names_data[self.people_names_data.columns[0]] = (
            self.people_names_data[self.people_names_data.columns[0]]
            .dropna()
            .apply(lambda x: gf.clean_text(x.strip()).split())
        )

        self.people_names_data[self.people_names_data.columns[1]] = (
            self.people_names_data[self.people_names_data.columns[1]]
            .fillna("")
            .apply(lambda x: [gf.clean_text(name.strip()).split() for name in x.split(",") if name.strip()])
        )

        clean_data = [
            (row[self.people_names_data.columns[0]], row[self.people_names_data.columns[1]])
            for _, row in self.people_names_data.iterrows()
            if row[self.people_names_data.columns[0]]
        ]

        self.names_list = [entry[0] for entry in clean_data]
        self.other_names_list = [entry[1] for entry in clean_data]

        self.names_list = gf.remove_words(self.names_list, self.words_to_remove)
        self.other_names_list = gf.remove_words(self.other_names_list, self.words_to_remove)

    def __str__(self):
        """ Returns a JSON representation of the processed data. """
        return self._to_json()

    def _to_json(self):
        """ Converts the processed sentences and names into a structured JSON format. """
        processed_sentences = self.sentences_list
        processed_names = [[self.names_list[i], self.other_names_list[i]] for i in range(len(self.names_list))]

        output = {
            f"Question 1": {
                "Processed Sentences": processed_sentences,
                "Processed Names": processed_names,
            }
        }

        return json.dumps(output, indent=4)

    def get_json_format(self):
        """ Public method to get the formatted JSON structure. """
        return self._to_json()

    def get_task_num(self):
        return self.prog_num

    def get_task_method(self):
        if 6 > self.prog_num > 0:
            return 1
        elif 9 > self.prog_num > 5:
            return 2
        else:
            print("wrong number")
