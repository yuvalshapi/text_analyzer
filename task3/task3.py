import pandas as pd
import json
from general_files import general_functions as gf
from task1.task1 import TextPreprocessor
import os


class NamesCounter:
    """
    A class to count occurrences of full names and their nicknames in a text corpus.

    Attributes:
        sentences_list (list): List of sentences (each sentence is a list of words).
        names_dict (dict): Dictionary mapping full names to their respective nicknames.
        app_dict (dict): Dictionary containing the count of occurrences for each name.
    """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 remove_words_file_path: str = None,
                 is_processed: bool = False):
        """
        Initializes the NamesCounter instance and processes the input data.

        Args:
            sentences_file_path (str): Path to the file containing sentences.
            name_file_path (str, optional): Path to the file containing names and nicknames. Defaults to None.
            remove_words_file_path (str, optional): Path to the file containing words to be ignored. Defaults to None.
            is_processed (bool, optional): Indicates if the input data is already preprocessed. Defaults to False.
        """
        # If the input data is preprocessed, load it directly
        if is_processed:
            self.sentences_list, self.names_dict = gf.parse_json_to_lists(sentences_file_path)
        else:
            # If not preprocessed, use TextPreprocessor to prepare the data
            data = TextPreprocessor(sentences_file_path, name_file_path, remove_words_file_path)
            self.sentences_list = data.get_processed_sentences()  # Get the processed sentences
            self.names_dict = data.get_dict_of_names()  # Get the dictionary of names and nicknames

        # Initialize an empty dictionary to store appearance counts
        self.app_dict = {}

        # Call the private method to compute the appearances
        self._appearances_counter()

    def _appearances_counter(self):
        """
        Counts the appearances of each name (full name or other names) in the text and updates `app_dict`.

        The function iterates over the list of processed sentences and counts the occurrences of each full name
        and their associated nicknames. The occurrences are tracked and stored in `app_dict`.

        :return: None
        """
        app_dict = {}  # Temporary dictionary to store counts during computation

        # Iterate through each sentence in the processed sentences list
        for sentence in self.sentences_list:
            # Convert the sentence (list of words) into a single string
            sentence_str = " ".join(sentence)

            # Iterate through each full name in the names dictionary
            for name in self.names_dict.keys():
                num_of_apps = 0  # Initialize the count for this name in the current sentence

                # Generate all substrings of the full name
                name_variations = gf.generate_substrings(name)

                # Include associated nicknames in the variations
                name_variations.extend(self.names_dict[name])

                # Count and remove occurrences of each name variation
                for variation in name_variations:
                    count_app, sentence_str = gf.count_and_remove(sentence_str, variation)
                    num_of_apps += count_app  # Increment the count with the occurrences of the variation

                # Update the overall appearance count in app_dict
                app_dict[name] = app_dict.get(name, 0) + num_of_apps

        # Remove entries with zero appearances
        app_dict = {name: count for name, count in app_dict.items() if count > 0}

        # Store the result in the instance variable for further use
        self.app_dict = {name: app_dict[name] for name in sorted(app_dict.keys())}

    def __str__(self):
        """
        Converts the instance's data into a JSON string representation.

        This is called when the instance is printed.

        :return: JSON string representation of the appearances counter.
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts the data from the appearances counter into the required JSON format.

        The format is:
        {
            "Question 3": {
                "Name Mentions": [
                    ["Name1", Number],
                    ["Name2", Number],
                    ...
                ]
            }
        }

        :return: JSON string with the specified structure.
        """
        # Ensure `app_dict` exists and has been computed
        if not hasattr(self, "app_dict"):
            raise AttributeError("The appearances counter has not been run. Call `_appearances_counter` first.")

        # Prepare the name mentions list (convert dictionary to list of lists)
        name_mentions = [[name, count] for name, count in self.app_dict.items()]

        # Structure the output dictionary
        output = {
            "Question 3": {
                "Name Mentions": name_mentions
            }
        }

        # Convert the dictionary to a formatted JSON string
        return json.dumps(output, indent=4)


    def get_json_format(self):
        """
        Public method to get the formatted JSON structure.

        Returns:
        -------
        str
            The JSON string output of the `_to_json` method.
        """
        return self._to_json()