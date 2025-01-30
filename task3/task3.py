import copy
import json
from text_analayzer_project_final.general_files import general_functions as gf
from task1.textprocessor import TextPreprocessor


class NamesCounter:
    """
    A class to count occurrences of full names and their nicknames in a text corpus.
    """

    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 remove_words_file_path: str = None,
                 is_processed: bool = False):
        """
        Initializes the NamesCounter instance and processes the input data.

        Parameters:
        sentences_file_path (str): Path to the file containing sentences.
        name_file_path (str, optional): Path to the file containing names and nicknames.
        remove_words_file_path (str, optional): Path to the file containing words to be ignored.
        is_processed (bool, optional): Indicates if the input data is already preprocessed.
        """

        if is_processed:
            self.sentences_list, self.names_dict = gf.parse_json_to_lists(sentences_file_path)
        else:
            data = TextPreprocessor(sentences_file_path, name_file_path, remove_words_file_path)
            self.sentences_list = data.get_processed_sentences()
            self.names_dict = data.get_dict_of_names()

        self.app_dict = {}
        self.names_sentences = {}
        self._appearances_counter()

    def _appearances_counter(self):
        """
        Counts how many times names (full name or nicknames) appear in the text.
        Updates `app_dict` with occurrence counts and `names_sentences` with relevant sentences.
        """
        app_dict = {}
        person_sentences = {name: [] for name in self.names_dict.keys()}

        for sentence in self.sentences_list:
            sentence_str = " ".join(sentence)

            for name in self.names_dict.keys():
                num_of_apps = 0
                name_variations = name.split() + self.names_dict[name]
                temp_sentence_str = copy.deepcopy(sentence_str)

                for variation in name_variations:
                    count_app, _ = gf.count_and_remove(temp_sentence_str, variation)
                    num_of_apps += count_app

                if num_of_apps > 0:
                    app_dict[name] = app_dict.get(name, 0) + num_of_apps
                    if sentence_str not in person_sentences[name]:
                        person_sentences[name].append(sentence_str)

        app_dict = {name: count for name, count in app_dict.items() if count > 0}
        self.app_dict = {name: app_dict[name] for name in sorted(app_dict.keys())}
        self.names_sentences = {name: person_sentences[name] for name in person_sentences.keys()}

    def __str__(self):
        """
        Returns the JSON representation of the counted name occurrences.
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts name occurrences into a JSON format.

        Returns:
        str: JSON formatted string.
        """
        if not hasattr(self, "app_dict"):
            raise AttributeError("The appearances counter has not been run. Call `_appearances_counter` first.")

        name_mentions = [[name, count] for name, count in self.app_dict.items()]
        output = {"Question 3": {"Name Mentions": name_mentions}}
        return json.dumps(output, indent=4)

    def get_names_sentences(self):
        """
        Returns a dictionary where keys are names and values are sentences containing them.
        """
        return self.names_sentences

    def get_json_format(self):
        """
        Returns the JSON formatted name occurrence data.
        """
        return self._to_json()

    def get_sentences(self):
        """
        Returns the list of processed sentences.
        """
        return self.sentences_list
