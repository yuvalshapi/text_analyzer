import pandas as pd
import json
import os
import string
import task3.task3 as task3
import task1.task1 as task1
import task2.task2 as task2
import general_files.general_functions as gf

class ConnectionFinder:
    """
    This class finds connections between people based on their mentions in the same sentence windows.
    It creates a graph where people are nodes and edges are based on shared windows.
    """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 remove_words_file_path: str = None,
                 is_processed: bool = False,
                 window_size: int = 1,
                 threshold: int = 2):
        """
        Initializes the ConnectionFinder with input data and parameters.

        :param sentences_file_path: Path to the sentences file (CSV or preprocessed JSON).
        :param name_file_path: Path to the names file (optional).
        :param remove_words_file_path: Path to the file with words to remove (optional).
        :param is_processed: If True, assumes the input is already preprocessed.
        :param window_size: The size of the sentence window to check.
        :param threshold: Minimum number of shared windows to create a connection.
        """
        if is_processed:
            # If data is preprocessed, load it
            self.sentences_list, self.names_dict = gf.parse_json_to_lists(sentences_file_path)
        else:
            # Otherwise, process the data using TextPreprocessor
            data = task1.TextPreprocessor(sentences_file_path, name_file_path, remove_words_file_path)
            self.sentences_list = data.get_processed_sentences()
            self.names_dict = data.get_dict_of_names()

        self.window_size = window_size
        self.threshold = threshold
        self.windows_list = []  # List of sentence windows
        self.people_windows_dict = {}  # Which windows each person appears in
        self.people_connection_list = []  # Connections between people
        self._create_windows_dict()
        self._find_connections()

    def _create_windows_dict(self):
        """
        Creates a dictionary where each person maps to the windows they appear in.

        A window is a list of consecutive sentences determined by the window size.
        This checks all variations of a name (including nicknames).
        """
        windows_list = gf.create_all_sublists(self.sentences_list, self.window_size)
        for window in windows_list:
            for name in self.names_dict:
                # Create variations of the name and nicknames as lists of words
                name_variations = [[word] for word in name.split()]  # Words from full name
                name_variations.extend([nickname.split() for nickname in self.names_dict[name]])  # Nicknames

                if gf.is_appear(window, name_variations):  # Check if the person appears in the window
                    if name not in self.people_windows_dict:
                        self.people_windows_dict[name] = []  # Initialize if not already present
                    self.people_windows_dict[name].append(window)

        # Sort the dictionary alphabetically by names
        self.people_windows_dict = dict(sorted(self.people_windows_dict.items()))

    def calculate_shared_windows(self):
        """
        Calculates the number of shared windows between each pair of people.

        :return: A dictionary where keys are tuples of two names and values are the count of shared windows.
        """
        pair_count_dict = {}
        names = list(self.people_windows_dict.keys())  # All people

        # Compare each pair of people
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                name1, name2 = names[i], names[j]
                windows1 = self.people_windows_dict[name1]
                windows2 = self.people_windows_dict[name2]

                # Count shared windows
                shared_count = sum(1 for window1 in windows1 for window2 in windows2 if window1 == window2)

                # Store the count if there are shared windows
                if shared_count > 0:
                    pair_count_dict[(name1, name2)] = shared_count

        return pair_count_dict

    def _find_connections(self):
        """
        Finds all connections between people based on the threshold.

        If two people share windows above the threshold, they are added as a connection.
        """
        full_connections_dict = self.calculate_shared_windows()
        for names, num_of_connections in full_connections_dict.items():
            if num_of_connections > self.threshold:
                self.people_connection_list.append(sorted(names))  # Ensure names are in alphabetical order

    def _to_json(self):
        """
        Converts the connections to a JSON format.

        The format uses lists of words for names to match the required structure.
        """
        formatted_connections = [
            [name.split() for name in connection]
            for connection in self.people_connection_list
        ]
        output = {
            "Question 6": {
                "Pair Matches": formatted_connections
            }
        }
        return json.dumps(output, indent=4)

    def get_json_format(self):
        """
        Public method to get the connections in JSON format.
        """
        return self._to_json()

    def __str__(self):
        """
        String representation of the connections in JSON format.
        """
        return self.get_json_format()
