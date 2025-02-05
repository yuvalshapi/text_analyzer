import json
import copy
import text_analayzer_project_final.textprocessor.textprocessor as tp
import text_analayzer_project_final.general_files.general_functions as gf
import text_analayzer_project_final.general_files.json_formats as j_formats
from typing import Optional, List, Dict, Tuple


class DataAnalyzer:
    """
    A class for analyzing processed text data.

    This class performs various text analysis tasks, including:
    - **Counting sequences**: Identifies recurring word sequences in the text.
    - **Finding name mentions**: Detects how often names appear and in which sentences.
    - **Identifying predefined k-sequences (K-Seqs)**: Finds specific sequences in the text.
    - **Extracting context for names**: Determines word patterns associated with each name.

    ### Methods:
    - `sequence_counter()`: Returns a JSON representation of sequence occurrences.
    - `names_counter()`: Returns a JSON report on name mentions.
    - `kseqengine()`: Finds predefined k-sequences in the text.
    - `find_context()`: Finds k-sequence patterns around names.

    """
    def __init__(self,
                 processed_data: tp.TextPreprocessor,
                 maxk: Optional[int] = None,
                 kseq_file_path: Optional[str] = None) -> None:
        """
        Initializes the DataAnalyzer class and prepares it for analysis.

        ### Parameters:
        - `processed_data` (tp.TextPreprocessor): The processed text data to analyze.
        - `maxk` (int, optional): The maximum sequence length to analyze. Defaults to None.
        - `kseq_file_path` (str, optional): Path to a JSON file containing predefined k-sequences.
        """
        self.processed_data = processed_data
        self.maxk = maxk
        self.kseq_file_path = kseq_file_path

    def _count_occurrences(self) -> List[Dict[str, int]]:
        """
        Counts how many times sub-sequences (small parts of sentences) appear in the text.
        """
        list_of_dicts: List[Dict[str, int]] = []

        for k in range(1, self.maxk + 1):
            dict_of_occurrences: Dict[str, int] = {}

            for sentence in self.processed_data.get_processed_sentences():
                list_of_subs = gf.create_all_sublists(sentence, k)

                for sub in list_of_subs:
                    key = ' '.join(sub)
                    dict_of_occurrences[key] = dict_of_occurrences.get(key, 0) + 1

            sorted_dict = dict(sorted(dict_of_occurrences.items()))
            list_of_dicts.append(sorted_dict)

        return list_of_dicts

    def sequence_counter(self) -> str:
        """ Finds and counts sequences in sentences and returns as JSON. """
        list_of_dicts = self._count_occurrences()
        result_formatted = j_formats.json_format_t2(self.maxk, list_of_dicts)
        return json.dumps(result_formatted, indent=4)

    def _appearances_counter(self) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
        """
        Counts occurrences of names and their variations in sentences.
        """
        sentences_list = self.processed_data.get_processed_sentences()
        names_dict = self.processed_data.get_dict_of_names()
        app_dict: Dict[str, int] = {}
        person_sentences: Dict[str, List[str]] = {name: [] for name in names_dict.keys()}

        for sentence in sentences_list:
            sentence_str = " ".join(sentence)

            for name in names_dict.keys():
                num_of_apps = 0
                name_variations = name.split() + names_dict[name]
                temp_sentence_str = copy.deepcopy(sentence_str)

                for variation in name_variations:
                    count_app, _ = gf.count_and_remove(temp_sentence_str, variation)
                    num_of_apps += count_app

                if num_of_apps > 0:
                    app_dict[name] = app_dict.get(name, 0) + num_of_apps
                    if sentence_str not in person_sentences[name]:
                        person_sentences[name].append(sentence_str)

        app_dict = {name: count for name, count in app_dict.items() if count > 0}
        app_dict = {name: app_dict[name] for name in sorted(app_dict.keys())}
        names_sentences = {name: person_sentences[name] for name in person_sentences.keys()}

        return app_dict, names_sentences

    def names_counter(self) -> str:
        """ Counts occurrences of names in sentences and returns JSON output. """
        app_dict, _ = self._appearances_counter()
        formatted_result = j_formats.json_format_t3(app_dict)
        return json.dumps(formatted_result, indent=4)

    def _build_kseq_dict(self) -> Tuple[Dict[str, List[str]], List[str]]:
        """
        Builds a dictionary mapping k-sequences (K-Seqs) to sentences.
        """
        sentences_list = self.processed_data.get_processed_sentences()
        input_kseq: List[str] = []
        kseq_in_dict: Dict[str, List[str]] = {}

        k_list = gf.load_kseqs_from_json(self.kseq_file_path)

        for kseq in k_list:
            input_kseq.append(gf.clean_text(kseq))

        for sentence in sentences_list:
            str_sentence = ' '.join(sentence)
            sub_sentence = gf.generate_substrings(str_sentence)

            for s in sub_sentence:
                if s in kseq_in_dict:
                    kseq_in_dict[s].append(str_sentence)
                else:
                    kseq_in_dict[s] = [str_sentence]

        for kseq in kseq_in_dict:
            kseq_in_dict[kseq] = sorted(set(kseq_in_dict[kseq]))

        return kseq_in_dict, input_kseq

    def kseqengine(self) -> str:
        """ Identifies only predefined k-sequences in sentences and returns JSON output. """
        if not self.kseq_file_path:
            raise ValueError("No k-sequence file path provided for Task 4.")

        input_kseqs = gf.load_kseqs_from_json(self.kseq_file_path)
        input_kseqs = [gf.clean_text(kseq) for kseq in input_kseqs]

        sentences_list = self.processed_data.get_processed_sentences()
        found_kseq_dict: Dict[str, List[str]] = {}

        for kseq in input_kseqs:
            for sentence in sentences_list:
                str_sentence = ' '.join(sentence)
                if kseq in str_sentence:
                    if kseq not in found_kseq_dict:
                        found_kseq_dict[kseq] = set()
                    found_kseq_dict[kseq].add(str_sentence)

        found_kseq_dict = {k: sorted(list(v)) for k, v in sorted(found_kseq_dict.items())}
        formatted_result = j_formats.json_format_t4(found_kseq_dict)
        return json.dumps(formatted_result, indent=4)

    def prepare_kseqs(self) -> Dict[str, List[List[str]]]:
        """
        Generates k-sequences (K-Seqs) for each name based on where they appear.
        """
        _, names_sentences = self._appearances_counter()
        names_kseqs: Dict[str, List[List[str]]] = {}

        for name in sorted(names_sentences.keys()):
            kseq_set = set()
            for sentence in names_sentences[name]:
                sentence_list = sentence.split()

                for i in range(1, self.maxk + 1):
                    kseqs = gf.create_all_sublists(sentence_list, i)
                    kseq_set.update(tuple(kseq) for kseq in kseqs)

            names_kseqs[name] = sorted([list(kseq) for kseq in kseq_set])

        return {name: kseqs for name, kseqs in names_kseqs.items() if kseqs}

    def find_context(self) -> str:
        """ Finds contextual K-Seqs for names and returns JSON output. """
        names_kseqs = self.prepare_kseqs()
        formatted_result = j_formats.json_format_t5(names_kseqs)
        return json.dumps(formatted_result, indent=4)
