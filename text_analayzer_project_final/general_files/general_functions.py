import string
import re
import pandas as pd
import json
from typing import List, Tuple, Dict, Any, Optional, Union

HEADER_SENTENCES_PREP_TEMPLATE = ""


def clean_text(text: str = "") -> str:
    """
    Cleans text by:
    1. Removing all punctuation.
    2. Removing unnecessary whitespaces and prefixes.
    3. Converting to lowercase.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text)  # Replace punctuation with whitespace
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.strip()  # Trim leading/trailing spaces
    return text


def remove_words(list_of_text: Union[List[Any], str], words_to_remove: List[str]) -> Union[List[Any], str]:
    """
    Removes unwanted words from a list of text.
    Handles lists of arbitrary depth (1D, 2D, or deeper).

    :param list_of_text: A list of strings or nested lists of strings.
    :param words_to_remove: A list of words to remove from the text.
    :return: The modified list with unwanted words removed.
    """
    if isinstance(list_of_text, list):
        return [
            remove_words(item, words_to_remove)  # Recursive call for nested lists
            for item in list_of_text
            if not (isinstance(item, str) and item in words_to_remove)  # Exclude unwanted words
        ]
    return list_of_text


def create_all_sublists(input_list: List[Any], k: int) -> List[List[Any]]:
    """
    Creates all sublists of size k from a given list.

    :param input_list: The input list from which to generate sublists.
    :param k: The desired size of each sublist.
    :return: A list of sublists, each of size k.
    """
    if k > len(input_list) or k <= 0:
        return []  # Return an empty list if k is invalid

    return [input_list[i:i + k] for i in range(len(input_list) - k + 1)]


def parse_json_to_lists(path: str, remove_words_path: Optional[str] = None) -> Tuple[List[Any], Dict[str, List[str]]]:
    """
    Parses a formatted JSON file to extract sentences and names.

    :param path: Path to the JSON file.
    :param remove_words_path: Optional path to a CSV file containing words to remove.
    :return: A tuple containing:
             - List of processed sentences.
             - Dictionary mapping names to their variations.
    """
    data = pd.read_json(path)

    sentences = data["Question 1"]["Processed Sentences"]
    names_list = data["Question 1"]["Processed Names"]
    names_dict = {
        ' '.join(entry[0]): [' '.join(nickname) for nickname in entry[1]]
        for entry in names_list
    }

    if remove_words_path:
        remove_words_df = pd.read_csv(remove_words_path)
        words_to_remove = remove_words_df.iloc[:, 0].dropna().str.strip().str.lower().tolist()
        names_dict = {
            remove_words([name], words_to_remove)[0]:
                remove_words(nicknames, words_to_remove)
            for name, nicknames in names_dict.items()
        }

    return sentences, names_dict


def count_and_remove(text: str, word: str) -> Tuple[int, str]:
    """
    Counts occurrences of 'word' in text and removes them.

    :param text: The text to search in.
    :param word: The word to count and remove.
    :return: A tuple containing:
             - The count of occurrences of 'word'.
             - The text with 'word' removed.
    """
    matches = re.findall(word, text)
    count = len(matches)

    text = re.sub(word, '', text)

    return count, text


def generate_substrings(input_string: str) -> List[str]:
    """
    Generates all possible substrings of the input string.

    :param input_string: The input string from which to generate substrings.
    :return: A list of substrings sorted from longest to shortest.
    """
    words = input_string.split()
    substrings = [" ".join(words[start:end]) for start in range(len(words)) for end in range(start + 1, len(words) + 1)]
    substrings.sort(key=len, reverse=True)

    return substrings


def load_kseqs_from_json(file_path: str) -> List[str]:
    """
    Load K-seqs from a JSON file and return them as a list of concatenated strings using pandas.

    :param file_path: Path to the JSON file.
    :return: List of strings where each string is a row of concatenated K-seq.
    """
    df = pd.read_json(file_path)
    first_column = df.iloc[:, 0]
    kseqs = first_column.apply(lambda row: " ".join(word.strip().lower() for word in row))

    return kseqs.tolist()


def is_appear(list_of_sentences: List[List[str]], word_list: List[List[str]]) -> bool:
    """
    Checks if any variation of a word appears in a list of sentences.

    :param list_of_sentences: List of lists of words (sentences).
    :param word_list: List of word variations to search for.
    :return: True if any variation is found in any sentence, False otherwise.
    """
    for sentence in list_of_sentences:
        for word in word_list:
            if any(part in sentence for part in word):
                return True
    return False
