import json
import pandas as pd
from text_analayzer_project_final.general_files import general_functions as gf
from typing import Optional, List, Dict


class TextPreprocessor:
    """
    A class used to preprocess and prepare input text data for further analysis.
    It can either process raw input data or load preprocessed data from a JSON file.
    """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: Optional[str] = None,
                 common_words_file_path: Optional[str] = None,
                 is_processed: bool = False,
                 prog_num: int = 1) -> None:
        """
        Initializes the TextPreprocessor class.
        """
        self.prog_num = prog_num

        # If data is already processed, just load it
        if is_processed:
            self._load_preprocessed_data(sentences_file_path)
        else:
            self._process_raw_data(sentences_file_path, name_file_path, common_words_file_path)

    def _load_preprocessed_data(self, json_file_path: str) -> None:
        """
        Loads preprocessed data from a JSON file.
        """
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            self.sentences_list: List[List[str]] = data[f"Question {self.prog_num}"]["Processed Sentences"]
            self.names_list: List[List[str]] = [name_data[0] for name_data in data[f"Question {self.prog_num}"]["Processed Names"]]
            self.other_names_list: List[List[str]] = [name_data[1] for name_data in data[f"Question {self.prog_num}"]["Processed Names"]]

        except Exception as e:
            raise ValueError(f"Error loading preprocessed data: {e}")

    def _process_raw_data(self,
                          sentences_file_path: str,
                          name_file_path: Optional[str],
                          common_words_file_path: Optional[str]) -> None:
        """
        Processes raw input data from CSV files and prepares structured data.
        """
        # Load the sentences data
        self.sentences_data = pd.read_csv(sentences_file_path)
        self.sentences_list: List[str] = self.sentences_data[self.sentences_data.columns[0]].tolist()

        # Load and process names data
        if name_file_path:
            self.people_names_data = pd.read_csv(name_file_path)
            self.other_names_list: List[str] = self.people_names_data[self.people_names_data.columns[0]].tolist()
            self.names_list: List[str] = self.people_names_data[self.people_names_data.columns[1]].tolist()
        else:
            self.people_names_data = None
            self.other_names_list = []
            self.names_list = []

        # Load and process common words data
        if common_words_file_path:
            self.common_words = pd.read_csv(common_words_file_path)
            self.words_to_remove: List[str] = self.common_words[self.common_words.columns[0]].dropna().str.strip().tolist()
        else:
            self.common_words = None
            self.words_to_remove = []

        # Process names and sentences if applicable
        if self.people_names_data is not None and not self.people_names_data.empty:
            self._process_names()
        self._process_data_inputs()

    def get_processed_sentences(self) -> List[List[str]]:
        """
        Retrieves the processed sentences as a list of lists.
        """
        return self.sentences_list

    def get_processed_names(self) -> List[List[str]]:
        """
        Retrieves the processed names as a list.
        """
        return self.names_list

    def get_dict_of_names(self) -> Dict[str, List[str]]:
        """
        Constructs a dictionary where each key is a cleaned name, and its value is a list of cleaned nicknames.
        """
        return {
            " ".join(name): [" ".join(nickname) for nickname in nicknames]
            for name, nicknames in zip(self.names_list, self.other_names_list)
        }

    def _process_data_inputs(self) -> None:
        """
        Processes the input sentences by cleaning, tokenizing, and removing stop words.
        """
        self.sentences_list = [item for s in self.sentences_list for item in s.split("\n")]
        self.sentences_list = [s for s in self.sentences_list if s.strip()]
        self.sentences_list = [gf.clean_text(text) for text in self.sentences_list]
        self.sentences_list = [sentence.split() for sentence in self.sentences_list]
        self.sentences_list = gf.remove_words(self.sentences_list, self.words_to_remove)
        self.sentences_list = [s for s in self.sentences_list if s]

    def _process_names(self) -> None:
        """
        Processes names and their variations by cleaning and removing unwanted words.
        """
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

    def __str__(self) -> str:
        """
        Returns a JSON representation of the processed data.
        """
        return self._to_json()

    def _to_json(self) -> str:
        """
        Converts the processed sentences and names into a structured JSON format.
        """
        processed_sentences = self.sentences_list
        processed_names = [[self.names_list[i], self.other_names_list[i]] for i in range(len(self.names_list))]

        output = {
            f"Question {self.prog_num}": {
                "Processed Sentences": processed_sentences,
                "Processed Names": processed_names,
            }
        }

        return json.dumps(output, indent=4)

    def get_json_format(self) -> str:
        """
        Public method to get the formatted JSON structure.
        """
        return self._to_json()

    def get_task_num(self) -> int:
        return self.prog_num

    def get_task_method(self) -> Optional[int]:
        if 0 < self.prog_num < 6:
            return 1
        elif 5 < self.prog_num < 9:
            return 2
        else:
            print("wrong number")
            return None
