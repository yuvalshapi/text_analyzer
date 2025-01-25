import copy
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
        self.names_sentences = {}
        # Call the private method to compute the appearances
        self._appearances_counter()

    def _appearances_counter(self):
        """
        Counts the appearances of each name (full name or other names) in the text,
        updates `app_dict` with occurrence counts, and records the sentences in which each name appears.

        This method performs the following tasks:
        1. Iterates over the list of processed sentences to identify mentions of each person.
        2. For each full name (and its nicknames), counts its appearances in each sentence.
        3. Maintains a dictionary (`app_dict`) with the total count of appearances for each name.
        4. Maintains another dictionary (`person_sentences`) to store sentences where each name appears.
        :return None
        """
        # Temporary dictionaries to store counts and sentences
        app_dict = {}
        person_sentences = {name: [] for name in self.names_dict.keys()}  # Initialize for each name

        # Iterate through each sentence in the processed sentences list
        for sentence in self.sentences_list:
            # Convert the sentence (list of words) into a single string
            sentence_str = " ".join(sentence)

            # Check for mentions of each person in the sentence
            for name in self.names_dict.keys():
                num_of_apps = 0  # Counter for this name in the current sentence

                # Create variations of the name (split full name + include nicknames)
                name_variations = name.split()
                name_variations.extend(self.names_dict[name])

                # Use a temporary copy of the sentence for counting occurrences
                temp_sentence_str = copy.deepcopy(sentence_str)

                # Count occurrences for each variation of the name
                for variation in name_variations:
                    count_app, _ = gf.count_and_remove(temp_sentence_str, variation)
                    num_of_apps += count_app  # Increment the count with the occurrences of the variation

                # If the name appeared in this sentence, update counts and store the sentence
                if num_of_apps > 0:
                    # Update total count in app_dict
                    app_dict[name] = app_dict.get(name, 0) + num_of_apps

                    # Add the sentence to the person's context if not already added
                    if sentence_str not in person_sentences[name]:
                        person_sentences[name].append(sentence_str)

        # Remove names with zero appearances from the app_dict
        app_dict = {name: count for name, count in app_dict.items() if count > 0}

        # Update instance variables with the results
        self.app_dict = {name: app_dict[name] for name in sorted(app_dict.keys())}
        self.names_sentences = {name: person_sentences[name] for name in person_sentences.keys()}

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

    def get_names_sentences(self):
        """
        Public method to get the person sentences.
        :return:
        dict - containing names as keys and sentences as values.
        """
        return self.names_sentences

    def get_json_format(self):
        """
        Public method to get the formatted JSON structure.

        Returns:
        -------
        str
            The JSON string output of the `_to_json` method.
        """
        return self._to_json()

    def get_sentences(self):
        """
        Public method to get the cleaned sentences

        Returns:
        -------
        list of lists
            list of sentces contains list of words
        """
        return self.sentences_list