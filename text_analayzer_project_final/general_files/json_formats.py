import json
import string
from typing import Dict, List, Union


def json_format_t2(maxk: int, counts: List[Dict[str, int]]) -> Dict[str, Dict[str, List[List[Union[str, List[Union[str, int]]]]]]]:
    """
    Converts the counted sequences into a JSON format.

    :param maxk: Maximum sequence length.
    :param counts: List of dictionaries containing sequence counts.
    :return: JSON structure as a dictionary.
    """
    result = {
        "Question 2": {
            f"{maxk}-Seq Counts": [
                [f"{i}_seq", [[key, value] for key, value in counts[i - 1].items()]]
                for i in range(1, maxk + 1)
            ]
        }
    }
    return result


def json_format_t3(app_dict: Dict[str, int]) -> Dict[str, Dict[str, List[List[Union[str, int]]]]]:
    """
    Converts name occurrences into a JSON format.

    :param app_dict: Dictionary of name occurrences.
    :return: JSON structure as a dictionary.
    """
    name_mentions = [[name, count] for name, count in app_dict.items()]
    results = {"Question 3": {"Name Mentions": name_mentions}}
    return results


def json_format_t4(kseq_dict: Dict[str, List[str]]) -> Dict[str, Dict[str, List[List[Union[str, List[str]]]]]]:
    """
    Formats the found kseq matches into a JSON structure.

    :param kseq_dict: Dictionary mapping k-sequences to lists of sentences.
    :return: JSON structure as a dictionary.
    """
    output = {
        "Question 4": {
            "K-Seq Matches": [
                [
                    kseq,
                    [sentence.split() for sentence in kseq_dict[kseq]]  # Split sentences into words
                ]
                for kseq in kseq_dict
            ]
        }
    }
    return output


def json_format_t5(names_kseq_dict: Dict[str, List[List[str]]]) -> Dict[str, Dict[str, List[List[Union[str, List[str]]]]]]:
    """
    Converts the K-Seqs data into the required JSON format for Task 5.

    :param names_kseq_dict: Dictionary mapping names to lists of K-sequences.
    :return: JSON structure as a dictionary.
    """
    person_contexts = [
        [name, list(kseqs)] for name, kseqs in sorted(names_kseq_dict.items())
    ]

    result = {
        "Question 5": {
            "Person Contexts and K-Seqs": person_contexts
        }
    }
    return result


def json_format_t6(people_connection_list: List[List[str]]) -> Dict[str, Dict[str, List[List[List[str]]]]]:
    """
    Converts the connections to a JSON format.

    :param people_connection_list: List of connections, each containing pairs of names.
    :return: JSON structure as a dictionary.
    """
    formatted_connections = [
        [name.split() for name in connection]
        for connection in people_connection_list
    ]
    result = {
        "Question 6": {
            "Pair Matches": formatted_connections
        }
    }
    return result


def json_format7_8(list_of_connections: List[List[Union[str, bool]]], q_num: int) -> Dict[str, Dict[str, List[List[Union[str, bool]]]]]:
    """
    Converts the results into JSON format.
    - Uses "Question 7" if `q_num == 7` (any connection).
    - Uses "Question 8" if `q_num == 8` (fixed-length paths).

    :param list_of_connections: List of connection results.
    :param q_num: Question number (7 or 8).
    :return: JSON structure as a dictionary.
    """
    question_key = "Question 7" if q_num == 7 else "Question 8"

    result = {
        question_key: {
            "Pair Matches": list_of_connections
        }
    }
    return result

def json_format_9(sorted_groups):
    formatted_result = {"Question 9": {"group Matches": sorted_groups}}
    return formatted_result
