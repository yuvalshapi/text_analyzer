import string
import re
import pandas as pd
import json


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


def parse_json_to_lists(path: str, remove_words_path: str = None):
    # Load the formatted JSON file
    data = pd.read_json(path)

    # Extracting the sentences
    sentences = data["Question 1"]["Processed Sentences"]

    # Extracting the names
    names_list = data["Question 1"]["Processed Names"]
    names_dict = {
        ' '.join(entry[0]): [' '.join(nickname) for nickname in entry[1]]
        for entry in names_list
    }

    # Apply word removal if a remove_words_path is provided
    if remove_words_path:
        remove_words_df = pd.read_csv(remove_words_path)
        words_to_remove = remove_words_df.iloc[:, 0].dropna().str.strip().str.lower().tolist()
        names_dict = {
            remove_words([name], words_to_remove)[0]:
                remove_words(nicknames, words_to_remove)
            for name, nicknames in names_dict.items()
        }

    return sentences, names_dict


def count_and_remove(text, word):
    """
    Function which counts the number of occurrences of 'word' in text and return it without the appernaces
    :param text string which represent the text we search in:
    :param word string which  we search in the text:
    :return:
    count INT number of occurrences of 'word' in text,
    text STR the text without the appearances of 'word'
    """
    # Find all appearances
    matches = re.findall(word, text)
    count = len(matches)

    # remove word from the text
    text = re.sub(word, '', text)

    return count, text


def generate_substrings(input_string: str) -> list:
    """
    Generates all possible substrings of the input string under the following conditions:
    1. Substrings are composed of words from the original string (words are separated by whitespace).
    2. Words in the substring must appear consecutively in the original string.

    The output list is sorted by the length of the substrings in descending order.

    :param input_string: The input string from which to generate substrings.
    :return: A list of substrings sorted from longest to shortest.
    """
    # Split the input string into words
    words = input_string.split()

    # Initialize a list to store all substrings
    substrings = []

    # Generate substrings by varying start and end positions
    for start in range(len(words)):
        for end in range(start + 1, len(words) + 1):
            substring = " ".join(words[start:end])
            substrings.append(substring)

    # Sort substrings by length in descending order
    substrings.sort(key=len, reverse=True)

    return substrings


def load_kseqs_from_json(file_path):
    """
    Load K-seqs from a JSON file and return them as a list of concatenated strings using pandas.

    :param file_path: Path to the JSON file.
    :return: List of strings where each string is a row of concatenated K-seq.
    """
    # Load the JSON file into a DataFrame
    df = pd.read_json(file_path)
    # Dynamically select the first column
    first_column = df.iloc[:, 0]

    # Process the "keys" column: join each list of words into a single string
    kseqs = first_column.apply(lambda row: " ".join(word.strip().lower() for word in row))

    # Return the list of strings
    return kseqs.tolist()

def is_appear(list,word_list):
    """
    Function which gets a  list of  list of strings stings and decide if a string appears in the list.
    :param list:
    :param string:
    :return:
    """
    for sentence in list:  # Iterate through each sentence in the window
        for word in word_list:  # Check each variation
            if any(part in sentence for part in word):  # Check if any word in the variation is in the sentence
                return True
    return False
if __name__ == '__main__':
    #print(parse_json_to_lists("Q1_result1.json"))
    #print(count_and_remove(" my baby has a baby in her ba by", "baby"))
    #print(load_kseqs_from_json("../task4/test_files/test1/kseq_query_keys_1.json"))
    list_of_strings = [
        ["apple", "banana", "cherry"],
        ["dog", "cat", "mouse"],
        ["sun", "moon", "stars"],
        ["python", "java", "c++"],
        ["car", "bike", "bus"],
        ["red", "blue", "green"],
        ["table", "chair", "sofa"],
        ["flower", "tree", "grass"],
        ["pen", "pencil", "eraser"]
    ]

    print(create_all_sublists(list_of_strings,3))
