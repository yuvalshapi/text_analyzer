import pandas as pd
import json
import re
import task1.textprocessor as task1
import task3.task3 as task3
import general_files.general_functions as gf

class ContextFinder:
    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 remove_words_file_path: str = None,
                 is_processed: bool = False,
                 N : int = 1):
        # If the input data is preprocessed, load it directly
        self.size_of_kseqs = N
        data = task3.NamesCounter(sentences_file_path,name_file_path, remove_words_file_path, is_processed)
        self.names_sentences = data.get_names_sentences()
        self.names_kseqs = {}
        self.sentences = data.get_sentences()
        self.prepare_kseqs()
    def prepare_kseqs(self):
        """
        Prepares K-Seqs (subsequences of size 1 to self.size_of_kseqs) for each person
        based on the sentences where their name (or nickname) is mentioned.

        This function performs the following steps:
        1. Iterates over each person in `self.names_sentences`.
        2. For each sentence in which the person appears, generates all K-Seqs
           (from size 1 to `self.size_of_kseqs`) using a helper function.
        3. Appends the generated K-Seqs to `self.names_kseqs[name]`.

        Attributes Used:
        ----------------
        - `self.names_sentences`: Dictionary where each key is a person's name and the value is
          a list of sentences in which they appear.
        - `self.size_of_kseqs`: Maximum size of the K-Seqs to be generated.
        - `self.names_kseqs`: Dictionary where each key is a person's name and the value is a
          list of their generated K-Seqs.

        Returns:
        --------
        None

        """
        # Iterate over each person in names_sentences, sorted alphabetically
        for name in sorted(self.names_sentences.keys()):
            # Use a set to ensure unique K-Seqs for the person
            kseq_set = set()
            kseqs = []
            # Process each sentence where the person is mentioned
            for sentence in self.names_sentences[name]:
                sentence_list = sentence.split()
                # Generate all K-Seqs (1 to size_of_kseqs) for the sentence
                for i in range(1, self.size_of_kseqs + 1):  # Range starts at 1
                    kseqs = gf.create_all_sublists(sentence_list, i)
                    # Add the K-Seqs as tuples to the set to ensure uniqueness
                    kseq_set.update(tuple(kseq) for kseq in kseqs)

            # Convert the set to a sorted list and store it
            self.names_kseqs[name] = sorted(kseq_set)

        # Remove entries where the list of K-Seqs is empty
        self.names_kseqs = {name: kseqs for name, kseqs in self.names_kseqs.items() if kseqs}

    def to_json(self):
        """
        Converts the K-Seqs data into the required JSON format for Task 5.

        Returns:
        --------
        str
            JSON string representing the data in the required format.


        """
        # Structure the output as a list of lists in the desired format
        person_contexts = [
            [name, list(kseqs)] for name, kseqs in sorted(self.names_kseqs.items())
        ]

        # Structure the final output dictionary
        output = {
            "Question 5": {
                "Person Contexts and K-Seqs": person_contexts
            }
        }

        # Convert to a JSON string with indentation for readability
        return json.dumps(output, indent=4)

    def __str__(self):
        return self.to_json()

    def get_json_format(self):
        return self.to_json()
