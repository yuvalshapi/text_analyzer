from task1.task1 import *

class SequenceCounter:
    """
    A class which count the occurrence of sub sentences in sentences,
    """
    def __init__(self,
                 sentences_file_path:str,
                 remove_words_file_path: str = None,
                 is_processed:bool = False,
                 k:int = 1):
        """ docstring"""

        self.seq_num = k

        #If processed we only load the file
        if is_processed:
            sentences_data = pd.read_json(sentences_file_path)
            self.sentences_list = sentences_data.loc["Processed Sentences", "Question 1"]

        #If not processed we should prepare the data
        else:
            data = TextPreprocessor(sentences_file_path,None, remove_words_file_path)
            self.sentences_list = data.get_processed_sentences()

    def _count_occurrences(self):
        """
        Counts the occurrences of sub-sentences (sublists) in sentences for sequence sizes up to `self.seq_num`.
        :return: A list of dictionaries, each dictionary containing sublist counts for a specific size.
        """
        list_of_dicts = []

        for k in range(1, self.seq_num + 1):  # Iterate over sublist sizes from 1 to seq_num
            dict_of_occurrences = {}

            for sentence in self.sentences_list:
                # Generate all sublists of size k
                list_of_subs = gf.create_all_sublists(sentence, k)

                for sub in list_of_subs:
                    # Convert the sublist to a string key for consistency
                    key = ' '.join(sub)
                    dict_of_occurrences[key] = dict_of_occurrences.get(key, 0) + 1

            # Sort the dictionary by keys
            sorted_dict = dict(sorted(dict_of_occurrences.items()))
            list_of_dicts.append(sorted_dict)

        return list_of_dicts

    def __str__(self):
        """

        :return:
        """
        return self._to_json()

    def _to_json(self):
        """
        Converts the counts into a JSON format as described.
        :return: JSON string representation of the results.
        """
        counts = self._count_occurrences()

        # Build the result dictionary in the desired format
        result = {
            "Question 2": {
                f"{self.seq_num}-Seq Counts": [
                    [f"{i}_seq", [[key, value] for key, value in counts[i - 1].items()]]
                    for i in range(1, self.seq_num + 1)
                ]
            }
        }

        # Convert the result to a JSON string
        return json.dumps(result, indent=4)

    def get_json_format(self):
        """
        Public method to get the formatted JSON structure.

        Returns:
        -------
        str
            The JSON string output of the `_to_json` method.
        """
        return self._to_json()

