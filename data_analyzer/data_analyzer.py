import pandas as pd
import json
import copy
import task1.textprocessor as tp
import general_files.general_functions as gf
import general_files.json_formats as j_formats


class DataAnalyzer:
    """
    A class for analyzing processed text data. It performs various tasks like:
    - Counting occurrences of sequences.
    - Finding name mentions in sentences.
    - Identifying k-sequences (K-Seqs) in text.
    - Extracting context for names.

    This class works with already processed text data.
    """

    def __init__(self,
                 processed_data: tp.TextPreprocessor,
                 maxk: int = None,
                 kseq_file_path: str = None):
        """
        Initializes the DataAnalyzer with processed text data.

        Parameters:
        ----------
        processed_data : TextPreprocessor
            An instance of TextPreprocessor containing preprocessed sentences.
        maxk : int, optional
            The maximum sequence length to analyze (default is None).
        kseq_file_path : str, optional
            Path to a file containing k-sequences (default is None).
        """
        self.processed_data = processed_data
        self.maxk = maxk
        self.kseq_file_path = kseq_file_path

    def _count_occurrences(self):
        """
        Counts how many times sub-sequences (small parts of sentences) appear in the text.

        Returns:
        -------
        list of dict
            A list where each dictionary contains sequence counts for a specific length.
        """
        list_of_dicts = []

        for k in range(1, self.maxk + 1):
            dict_of_occurrences = {}

            # Loop through each sentence in the dataset
            for sentence in self.processed_data.get_processed_sentences():
                list_of_subs = gf.create_all_sublists(sentence, k)  # Generate k-length sublists

                # Count occurrences of each unique sublist
                for sub in list_of_subs:
                    key = ' '.join(sub)  # Convert list to string for dictionary storage
                    dict_of_occurrences[key] = dict_of_occurrences.get(key, 0) + 1

            # Store sorted occurrences for better readability
            sorted_dict = dict(sorted(dict_of_occurrences.items()))
            list_of_dicts.append(sorted_dict)

        return list_of_dicts

    def sequence_counter(self):
        """ Finds and counts sequences in sentences and returns as JSON. """
        list_of_dicts = self._count_occurrences()
        result_formatted = j_formats.json_format_t2(self.maxk, list_of_dicts)
        return json.dumps(result_formatted, indent=4)

    def _appearances_counter(self):
        """
        Counts occurrences of names and their variations in sentences.

        Returns:
        -------
        tuple(dict, dict)
            - Dictionary of name occurrences.
            - Dictionary mapping names to sentences where they appear.
        """
        sentences_list = self.processed_data.get_processed_sentences()
        names_dict = self.processed_data.get_dict_of_names()
        app_dict = {}
        person_sentences = {name: [] for name in names_dict.keys()}  # Initialize empty lists for names

        for sentence in sentences_list:
            sentence_str = " ".join(sentence)  # Convert sentence list to a single string

            for name in names_dict.keys():
                num_of_apps = 0  # Counter for occurrences
                name_variations = name.split() + names_dict[name]  # Get all variations of a name
                temp_sentence_str = copy.deepcopy(sentence_str)  # Prevent modification of the original sentence

                # Count occurrences of name variations
                for variation in name_variations:
                    count_app, _ = gf.count_and_remove(temp_sentence_str, variation)
                    num_of_apps += count_app

                if num_of_apps > 0:
                    app_dict[name] = app_dict.get(name, 0) + num_of_apps
                    if sentence_str not in person_sentences[name]:  # Avoid duplicate sentences
                        person_sentences[name].append(sentence_str)

        # Sort and remove names that didn't appear
        app_dict = {name: count for name, count in app_dict.items() if count > 0}
        app_dict = {name: app_dict[name] for name in sorted(app_dict.keys())}
        names_sentences = {name: person_sentences[name] for name in person_sentences.keys()}

        return app_dict, names_sentences

    def names_counter(self):
        """ Counts occurrences of names in sentences and returns JSON output. """
        app_dict, _ = self._appearances_counter()
        formatted_result = j_formats.json_format_t3(app_dict)
        return json.dumps(formatted_result, indent=4)

    def _build_kseq_dict(self):
        """
        Builds a dictionary mapping k-sequences (K-Seqs) to sentences.

        Returns:
        -------
        tuple(dict, list)
            - Dictionary of k-sequences and their sentences.
            - List of input k-sequences.
        """
        sentences_list = self.processed_data.get_processed_sentences()
        input_kseq = []
        kseq_in_dict = {}

        k_list = gf.load_kseqs_from_json(self.kseq_file_path)

        for kseq in k_list:
            input_kseq.append(gf.clean_text(kseq))  # Clean and store kseqs

        for sentence in sentences_list:
            str_sentence = ' '.join(sentence)  # Convert words list to string
            sub_sentence = gf.generate_substrings(str_sentence)  # Generate substrings

            for s in sub_sentence:
                if s in kseq_in_dict:
                    kseq_in_dict[s].append(str_sentence)
                else:
                    kseq_in_dict[s] = [str_sentence]

        for kseq in kseq_in_dict:
            kseq_in_dict[kseq] = sorted(set(kseq_in_dict[kseq]))  # Remove duplicates

        return kseq_in_dict, input_kseq

    def kseqengine(self):
        """ Identifies only predefined k-sequences in sentences and returns JSON output. """
        if not self.kseq_file_path:
            raise ValueError("No k-sequence file path provided for Task 4.")

        # Load k-sequences from JSON file
        input_kseqs = gf.load_kseqs_from_json(self.kseq_file_path)
        input_kseqs = [gf.clean_text(kseq) for kseq in input_kseqs]  # Clean input k-sequences

        sentences_list = self.processed_data.get_processed_sentences()
        found_kseq_dict = {}

        # Search for only predefined k-sequences in the text
        for kseq in input_kseqs:
            for sentence in sentences_list:
                str_sentence = ' '.join(sentence)  # Convert sentence list to a string
                if kseq in str_sentence:  # Match exact k-sequence
                    if kseq not in found_kseq_dict:
                        found_kseq_dict[kseq] = set()  # Use a set to prevent duplicates
                    found_kseq_dict[kseq].add(str_sentence)  # Add sentence to the set

        # Convert sets to sorted lists
        found_kseq_dict = {k: sorted(list(v)) for k, v in sorted(found_kseq_dict.items())}

        # Format results using json_format_t4
        formatted_result = j_formats.json_format_t4(found_kseq_dict)
        return json.dumps(formatted_result, indent=4)

    def prepare_kseqs(self):
        """
        Generates k-sequences (K-Seqs) for each name based on where they appear.

        Returns:
        -------
        dict
            Dictionary mapping names to their found K-Seqs.
        """
        _, names_sentences = self._appearances_counter()
        names_kseqs = {}

        for name in sorted(names_sentences.keys()):
            kseq_set = set()  # Use a set to avoid duplicate K-Seqs
            for sentence in names_sentences[name]:
                sentence_list = sentence.split()  # Convert sentence into a list of words

                # Ensure that all possible k-sequences (1 to maxk) are generated
                for i in range(1, self.maxk + 1):
                    kseqs = gf.create_all_sublists(sentence_list, i)
                    kseq_set.update(tuple(kseq) for kseq in kseqs)  # Ensure uniqueness

            # Convert set to sorted list while ensuring sequences are correct
            names_kseqs[name] = sorted([list(kseq) for kseq in kseq_set])

        return {name: kseqs for name, kseqs in names_kseqs.items() if kseqs}

    def find_context(self):
        """ Finds contextual K-Seqs for names and returns JSON output. """
        names_kseqs = self.prepare_kseqs()

        # Format results using json_format_t5
        formatted_result = j_formats.json_format_t5(names_kseqs)
        return json.dumps(formatted_result, indent=4)
