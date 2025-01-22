import string
import re
import pandas as pd
import general_functions as gf

class TextPreprocessor:
    """
    A class which used to make the preparations on the input text.
    The class parses the input paths and change the input data according to the various inputs
    """
    def __init__(self,
                 sentences_file_path:str,
                 name_file_path:str,
                 common_words_file_path:str,
                 prog_num:int):
        """
        A constructor for a TextPreprocessor object.
        :param sentences_file_path: A string holding the path to the actual "data" file.
        :param name_file_path: A string holding the path to the list of the names file.
        :param common_words_file_path: A string holding the path to the  common words file we should remove.
        :param prog_num: An integer that represents the program number output is expected.
        """
        self.sentences_data = pd.read_csv(sentences_file_path)
        #Converting the sentences from DF
        self.sentences_list = self.sentences_data[self.sentences_data.column[0]].tolist()
        self.people_names_data = pd.read_csv(name_file_path)
        self.other_names_list  = []
        self.names_list = []
        self.common_words = pd.read_csv(common_words_file_path)
        self.prog_num = prog_num

        self._process_names()
        self._process_data()
    def _process_data(self):
        """
        Function which gets a TextPreprocessor object and processes it:
        1. Splitting the data according to ","
        2. Removing all punctuation
        3. Converting all to lower case
        4. Removing all common words
        """
        #Splitting the strings by commas
        self.sentences_list = [item for s in self.sentences_list for item in s.split(",")]

        #Remove empty sentences from the list(action 'i')
        self.sentences_list = [s for s in self.sentences_list if s.strip()]

        #Clean the text
        self.sentences_list = [gf.clean_text(text) for text in self.sentences_list]

        #Delete the common words(action 'c')
        self._delete_words()

        #Splitting the string into list of words, making sentences become list of lists('h)
        self.sentences_list = [sentence.split() for sentence in self.sentences_list]

    def _process_names(self):
        """
        Function which gets a TextPreprocessor object and:
        1. Order the name and the other names into proper places in the object
        2. Remove duplicated full names(keeping only the first appearance)
        :return:
        """
        # Initialize a set to track unique names
        unique_names = set()
        filtered_rows = []
        # Iterate through the DataFrame to keep only the first occurrence of each full name (action 'f','j')
        for _, row in self.people_names_data.iterrows():
            full_name = row["Name"].strip()  # Clean and standardize the full name
            if full_name not in unique_names:
                unique_names.add(full_name)
                filtered_rows.append(row)

        # Create a cleaned DataFrame with unique names
        cleaned_df = pd.DataFrame(filtered_rows)

        #List which contain lists
        self.other_names_list = [[name.strip() for name in other_names.split(",") if name.strip()] for other_names in cleaned_df["Other Names"].fillna("")]
        self.names_list = cleaned_df["Name"].dropna().str.strip().tolist()


    def _delete_words(self):
        """
        Function which gets a TextPreprocessor object and deletes the unwanted words from the sentences
        """
        # Convert the column of common words to a Python list
        words_to_remove =  self.common_words["word"].dropna().str.strip().tolist()
        self.sentences_list = [item for item in self.sentences_list if item not in words_to_remove]


if __name__ == '__main__':
    p_path=r"text_analyzer\2_examples\Q1_examples\example_1\people_small_1.csv"
    s_path=""
    #T = TextPreprocessor("text_analyzer\2_examples\Q1_examples\example_1")
    print(pd.read_csv(p_path))