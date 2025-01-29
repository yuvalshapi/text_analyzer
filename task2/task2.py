from task1.textprocessor import *

class SequenceCounter:
    """
    A class that counts how many times small sequences (sub-sentences) appear in sentences.
    It supports different sizes of sequences up to `k` words long.
    """

    def __init__(self,
                 sentences_file_path: str,
                 remove_words_file_path: str = None,
                 is_processed: bool = False,
                 k: int = 1):
        """
        Initializes the SequenceCounter object.

        Parameters:
        sentences_file_path (str): Path to the file containing sentences.
        remove_words_file_path (str, optional): Path to file with words to remove (default is None).
        is_processed (bool): If True, the sentences are already processed and just need to be loaded.
        k (int): The maximum sequence length to count.
        """

        self.seq_num = k

        # If data is already processed, just load it
        if is_processed:
            sentences_data = pd.read_json(sentences_file_path)
            self.sentences_list = sentences_data.loc["Processed Sentences", "Question 1"]

        # If not processed, process the text first
        else:
            data = TextPreprocessor(sentences_file_path, None, remove_words_file_path)
            self.sentences_list = data.get_processed_sentences()

    def _count_occurrences(self):
        """
        Counts how many times sub-sentences (small sequences of words) appear in the text.
        The size of sub-sentences varies from 1 up to `self.seq_num`.

        Returns:
        list of dict: Each dictionary contains the count of different sequences of a certain length.
        """
        list_of_dicts = []

        for k in range(1, self.seq_num + 1):  # Count for sequence sizes 1 to seq_num
            dict_of_occurrences = {}

            for sentence in self.sentences_list:
                # Generate all possible sublists of size k
                list_of_subs = gf.create_all_sublists(sentence, k)

                for sub in list_of_subs:
                    # Convert the sublist into a string (so it can be stored in a dictionary)
                    key = ' '.join(sub)
                    dict_of_occurrences[key] = dict_of_occurrences.get(key, 0) + 1

            # Sort dictionary by key (optional, just for better readability)
            sorted_dict = dict(sorted(dict_of_occurrences.items()))
            list_of_dicts.append(sorted_dict)

        return list_of_dicts

    def __str__(self):
        """
        Returns the JSON representation of the counted sequences.

        Returns:
        str: JSON formatted string.
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts the counted sequences into a JSON format.

        Returns:
        str: JSON string representation of the results.
        """
        counts = self._count_occurrences()

        # Format the output in the required JSON structure
        result = {
            "Question 2": {
                f"{self.seq_num}-Seq Counts": [
                    [f"{i}_seq", [[key, value] for key, value in counts[i - 1].items()]]
                    for i in range(1, self.seq_num + 1)
                ]
            }
        }

        return json.dumps(result, indent=4)

    def get_json_format(self):
        """
        Public method to return the JSON formatted sequence counts.

        Returns:
        str: JSON string containing sequence counts.
        """
        return self._to_json()
