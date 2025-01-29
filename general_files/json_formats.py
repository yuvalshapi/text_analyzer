import json
import string


def json_format_t2(maxk,list):
    """
    Converts the counted sequences into a JSON format.

    Returns:
    str: JSON string representation of the results.
    """
    counts = list

    # Format the output in the required JSON structure
    result = {
        "Question 2": {
            f"{maxk}-Seq Counts": [
                [f"{i}_seq", [[key, value] for key, value in counts[i - 1].items()]]
                for i in range(1, maxk + 1)
            ]
        }
    }
    return result


def json_format_t3(app_dict):
    """
    Converts name occurrences into a JSON format.

    Returns:
    str: JSON formatted string.
    """

    name_mentions = [[name, count] for name, count in app_dict.items()]
    results = {"Question 3": {"Name Mentions": name_mentions}}
    return results

def json_format_t4(kseq_dict):
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
                    [sentence.split() for sentence in kseq_dict[kseq]]  # Split sentences into words
                ]
                for kseq in kseq_dict
            ]
        }
    }

    return output

def json_format_t5(names_kseq_dict):
    """
    Converts the K-Seqs data into the required JSON format for Task 5.

    Returns:
    --------
    str
        JSON string representing the data in the required format.


    """
    # Structure the output as a list of lists in the desired format
    person_contexts = [
        [name, list(kseqs)] for name, kseqs in sorted(names_kseq_dict.items())
    ]

    # Structure the final output dictionary
    result = {
        "Question 5": {
            "Person Contexts and K-Seqs": person_contexts
        }
    }

    # Convert to a JSON string with indentation for readability
    return result

def json_format_t6(people_connection_list):
    """
    Converts the connections to a JSON format.

    The format uses lists of words for names to match the required structure.
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

def json_format7_8(list_of_connections,q_num) -> str:
    """
    Converts the results into JSON format.
    - Uses "Question 7" if `self.fixed_len` is None (any connection).
    - Uses "Question 8" if `self.fixed_len` has a value (fixed-length paths).
    """
    question_key = "Question 7" if  q_num == 7  else "Question 8"

    result = {
        question_key: {
            "Pair Matches": list_of_connections
        }
    }
    return result