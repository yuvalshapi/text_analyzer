import string
import re
import pandas as pd


HEADER_SENTENCES_PREP_TEMPLATE = ""
def clean_text(text=""):
    """
    Function which does all the string cleaning on the data
    1.Removing all punctuation
    2.Removing all unnecessary whitespaces + perfix etc'
    3.lowercasing
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text)  # Replace punctuation with whitespace
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.strip()  # Trim leading/trailing spaces

    return text


def remove_words(list_of_text, words_to_remove):
    """
    Removes unwanted words from a list of text.
    Handles lists of arbitrary depth (1D, 2D, or deeper).

    :param list_of_text: A list of strings or nested lists of strings.
    :param words_to_remove: A list of words to remove from the text.
    :return: The modified list with unwanted words removed.
    """
    if isinstance(list_of_text, list):
        # Recursively process each item in the list
        return [
            remove_words(item, words_to_remove)  # Recursive call for nested lists
            for item in list_of_text
            if not (isinstance(item, str) and item in words_to_remove)  # Exclude unwanted words
        ]
    return list_of_text


def create_all_sublists(input_list, k):
    """
    Function which creates all sublists of size k from a given list.

    :param input_list: The input list from which to generate sublists.
    :param k: The desired size of each sublist.
    :return: A list of sublists, each of size k.
    """
    # Check if k is greater than the input list size
    if k > len(input_list) or k <= 0:
        return []  # Return an empty list if k is invalid

    # Generate sublists
    sublists = [input_list[i:i + k] for i in range(len(input_list) - k + 1)]
    return sublists
