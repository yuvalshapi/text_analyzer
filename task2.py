from task1.task1 import *

class SequenceCounter:
    """
    A class which count the occurrence of sub sentences in sentences,
    """
    def __init__(self,
                 sentences_file_path:str,
                 remove_words_file_path: str = None,
                 is_processes:bool = False,
                 k:int = 1):
        """ docstring"""

        self.seq_num = k

        #If processed we only load the file
        if is_processes:
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

        # Convert the result to a JSON string
        return json.dumps(result, indent=4)


if __name__ == '__main__':
    def print_differences_and_find_sources(processed, expected, path="", sentences_file=None):
        """
        Recursively compares two dictionaries or lists, prints detailed differences,
        and locates the source of discrepancies in the source file if applicable.

        :param processed: The processed result (dict, list, or value).
        :param expected: The expected result (dict, list, or value).
        :param path: The path to the current key being compared (for context in nested structures).
        :param sentences_file: Path to the source file for locating discrepancies.
        """
        if isinstance(processed, dict) and isinstance(expected, dict):
            processed_keys = set(processed.keys())
            expected_keys = set(expected.keys())

            for key in processed_keys - expected_keys:
                print(f"Extra key at {path}/{key}: {processed[key]}")
            for key in expected_keys - processed_keys:
                print(f"Missing key at {path}/{key}: {expected[key]}")

            for key in processed_keys & expected_keys:
                print_differences_and_find_sources(processed[key], expected[key], path=f"{path}/{key}",
                                                   sentences_file=sentences_file)

        elif isinstance(processed, list) and isinstance(expected, list):
            min_length = min(len(processed), len(expected))
            for i in range(min_length):
                print_differences_and_find_sources(processed[i], expected[i], path=f"{path}[{i}]",
                                                   sentences_file=sentences_file)
            if len(processed) > len(expected):
                for i in range(len(expected), len(processed)):
                    print(f"Extra item at {path}[{i}]: {processed[i]}")
                    if sentences_file and "Processed Sentences" in path:
                        locate_sentence_in_file(sentences_file, i)
            elif len(expected) > len(processed):
                for i in range(len(processed), len(expected)):
                    print(f"Missing item at {path}[{i}]: {expected[i]}")

        else:
            if processed != expected:
                print(f"Difference at {path}:")
                print(f"  Processed: {processed}")
                print(f"  Expected:  {expected}")


    def locate_sentence_in_file(sentences_file, index):
        """
        Finds and prints the source of a discrepancy in the sentences file based on the index.

        :param sentences_file: Path to the sentences CSV file.
        :param index: The index in the processed result that contains the discrepancy.
        """
        try:
            df = pd.read_csv(sentences_file)

            if index >= len(df):
                print(f"Index {index} is out of bounds for the file with {len(df)} entries.")
                return

            raw_sentence = df.iloc[index].tolist()
            print(f"Source sentence for discrepancy at index {index}: {raw_sentence}")
        except Exception as e:
            print(f"Error reading file {sentences_file}: {e}")


    # Test logic
    base_dir = "text_analyzer"
    n1 = [3,4,5]
    # Iterate through 1, 2, and 3 for file sets
    for i in range(1, 4):
        print(f"\n=== Running Test for File Set {i} ===")

        # File paths for the current iteration
        p_path = os.path.join(base_dir, "2_examples", "Q2_examples", f"example_{i}", f"people_small_{i}.csv")
        s_path = os.path.join(base_dir, "2_examples", "Q2_examples", f"example_{i}", f"sentences_small_{i}.csv")
        w_path = os.path.join(base_dir, "1_data", "data", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, "2_examples", "Q2_examples", f"example_{i}", f"Q2_result{i}.json")

        # Output JSON file for processed result
        output_path = os.path.join(base_dir, "2_examples", "Q2_examples", f"example_{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Instantiate the TextPreprocessor class and get the result
        T = SequenceCounter(s_path,w_path,False,n1[i-1])
        processed_result = json.loads(T._to_json())

        # Save processed result to a file
        with open(output_path, 'w') as outfile:
            json.dump(processed_result, outfile, indent=4)
        print(f"Processed result saved to {output_path}")

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"File set {i}: PASS")
        else:
            print(f"File set {i}: FAIL")
            print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)
