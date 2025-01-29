import pandas as pd
import json
from general_files import general_functions as gf
from task1.textprocessor import TextPreprocessor
import os


class KseqEngine:
    """
    A class to process sentences and k-sequences (kseqs) for text analysis.
    This class handles the extraction of kseqs from a provided list or file, builds a dictionary of kseqs,
    searches for kseq matches in sentences, and outputs results in a formatted JSON structure.

    Attributes:
    ----------
    sentences_list : list
        List of processed sentences from the input file.
    kseq_file_path : str
        Path to the file containing the k-sequences (kseqs).
    input_kseq : list
        Cleaned list of k-sequences to search for.
    kseq_in_sentences : dict
        Dictionary mapping each kseq to the sentences in which it appears.
    found_kseq_dict : dict
        Dictionary of kseqs found in the text, mapping each kseq to its matching sentences.

    Methods:
    -------
    _process_kseq()
        Cleans and loads kseqs from the provided file path.
    _build_kseq_dict()
        Builds a dictionary mapping kseqs to all sentences they appear in.
    _search_kseq()
        Finds all appearances of kseqs in the text, storing matches in a dictionary.
    _to_json()
        Outputs the results in a formatted JSON structure.
    """

    def __init__(self,
                 sentences_file_path: str,
                 remove_words_file_path: str = None,
                 kseq_file_path: str = None,
                 is_processed: bool = False):
        """
        Initializes the KseqEngine class by processing the input sentences and kseqs.

        Parameters:
        ----------
        sentences_file_path : str
            Path to the file containing the sentences to analyze.
        remove_words_file_path : str, optional
            Path to a file containing words to remove from the sentences (default is None).
        kseq_file_path : str, optional
            Path to the file containing the k-sequences (default is None).
        is_processed : bool, optional
            Flag indicating if the input file is preprocessed (default is False).
        """
        if is_processed:
            # Parse sentences directly if the input is already processed
            self.sentences_list = gf.parse_json_to_lists(sentences_file_path)[0]
        else:
            # Process the input file using the TextPreprocessor class
            data_to_process = TextPreprocessor(sentences_file_path, None, remove_words_file_path, 1)
            self.sentences_list = data_to_process.get_processed_sentences()

        # Initialize kseq-related attributes
        self.kseq_file_path = kseq_file_path
        self.input_kseq = []  # Cleaned list of kseqs
        self.kseq_in_sentences = {}  # Dictionary of kseqs and their matching sentences
        self.found_kseq_dict = {}  # Dictionary of kseqs found in the text

        # Process and build the kseq dictionaries
        self._process_kseq()
        self._build_kseq_dict()
        self._search_kseq()

    def _process_kseq(self):
        """
        Processes the kseq file and creates a cleaned list of k-sequences.
        Each kseq is stripped of unnecessary characters and formatted for search.
        """
        k_list = gf.load_kseqs_from_json(self.kseq_file_path)  # Load raw kseqs from file
        for kseq in k_list:
            self.input_kseq.append(gf.clean_text(kseq))  # Clean and append each kseq

    def _build_kseq_dict(self):
        """
        Builds a dictionary mapping each kseq to all sentences it appears in.
        The dictionary values are sorted alphabetically, and duplicates are removed.
        """
        for sentence in self.sentences_list:
            # Convert list of words to a single string
            str_sentence = ' '.join(sentence)

            # Generate all substrings (kseqs) of the sentence
            sub_sentence = gf.generate_substrings(str_sentence)

            # Populate the dictionary
            for s in sub_sentence:
                if s in self.kseq_in_sentences:
                    self.kseq_in_sentences[s].append(str_sentence)
                else:
                    self.kseq_in_sentences[s] = [str_sentence]

        # Ensure all lists are sorted and duplicates are removed
        for kseq in self.kseq_in_sentences:
            self.kseq_in_sentences[kseq] = sorted(set(self.kseq_in_sentences[kseq]))

    def _search_kseq(self):
        """
        Finds all appearances of the kseqs from the input list in the text.
        Populates the `found_kseq_dict` with kseqs and their matching sentences.
        """
        for kseq in self.input_kseq:
            # Check if kseq exists in the dictionary
            if kseq in self.kseq_in_sentences:
                self.found_kseq_dict[kseq] = self.kseq_in_sentences[kseq]

        # Sort the dictionary by keys for easier readability
        self.found_kseq_dict = dict(sorted(self.found_kseq_dict.items()))

    def _to_json(self):
        """
        Formats the found kseq matches into a JSON structure.

        Returns:
        -------
        str
            A JSON string formatted with indentation, containing kseq matches and their sentences.
        """
        output = {
            "Question 4": {
                "K-Seq Matches": [
                    [
                        kseq,
                        [sentence.split() for sentence in self.found_kseq_dict[kseq]]  # Split sentences into words
                    ]
                    for kseq in self.found_kseq_dict
                ]
            }
        }
        return json.dumps(output, indent=4)  # Return formatted JSON

    def __str__(self):
        """
        Returns a string representation of the KseqEngine, formatted as JSON.
        """
        return self._to_json()

    def get_json_format(self):
        """
        Public method to get the formatted JSON structure.

        Returns:
        -------
        str
            The JSON string output of the `_to_json` method.
        """
        return self._to_json()