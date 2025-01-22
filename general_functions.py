import string
import re
import pandas as pd


def clean_text(text=""):
    """
    Function which does all the string cleaning on the data
    1.Removing all punctuation
    2.Removing all unnecessary whitespaces + perfix etc'
    3.lowercasing
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = ''.join(char for char in text if char.isalnum() or char.isspace())

    return text
