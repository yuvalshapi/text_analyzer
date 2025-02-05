import os
import json
import pandas as pd
import numpy as np  # Import NumPy to handle NaN values

# Paths to the original data files
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "2_examples")
W_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "1_data", "data", "REMOVEWORDS.csv")

TASKS = ["Q1_examples", "Q2_examples", "Q3_examples", "Q4_examples", "Q5_examples", "Q6_examples", "Q7_examples", "Q8_examples"]
DATA_STORAGE_FILE = os.path.join(os.path.dirname(__file__), "test_data_storage.py")

# Dictionary to store data
test_data = {}

for task in TASKS:
    test_data[task] = {}
    for file_set in range(1, 5):  # Adjust based on the number of test cases
        try:
            s_path = os.path.join(BASE_DIR, task, f"example_{file_set}", f"sentences_small_{file_set}.csv")
            p_path = os.path.join(BASE_DIR, task, f"example_{file_set}", f"people_small_{file_set}.csv")
            conn_path = os.path.join(BASE_DIR, task, f"example_{file_set}", f"people_connections_{file_set}.json")
            kseq_path = os.path.join(BASE_DIR, task, f"example_{file_set}", f"kseq_query_keys_{file_set}.json")
            expected_result_path = os.path.join(BASE_DIR, task, f"example_{file_set}", f"Q{task[-1]}_result{file_set}.json")

            # Function to clean and replace NaN values
            def clean_data(df):
                if df is not None:
                    df = df.replace({np.nan: None})  # Convert NaN to None
                    return df.values.tolist()  # Convert to list
                return None

            # Read sentence file
            sentences = clean_data(pd.read_csv(s_path)) if os.path.exists(s_path) else None

            # Read people file (if it exists)
            people = clean_data(pd.read_csv(p_path)) if os.path.exists(p_path) else None

            # Read people connections (if applicable)
            connections = None
            if os.path.exists(conn_path):
                with open(conn_path, "r") as f:
                    connections = json.load(f)

            # Read k-sequence file (if applicable)
            kseq_queries = None
            if os.path.exists(kseq_path):
                with open(kseq_path, "r") as f:
                    kseq_queries = json.load(f)

            # Read expected results
            expected_result = None
            if os.path.exists(expected_result_path):
                with open(expected_result_path, "r") as f:
                    expected_result = json.load(f)

            # Store data in dictionary
            test_data[task][file_set] = {
                "sentences": sentences,
                "people": people,
                "connections": connections,
                "kseq_queries": kseq_queries,
                "expected_result": expected_result
            }

        except Exception as e:
            print(f"Skipping test case {file_set} in {task} due to: {e}")

# Save extracted data as a Python file
with open(DATA_STORAGE_FILE, "w") as f:
    f.write("test_data = ")
    json.dump(test_data, f, indent=4)

print(f"✅ Test data saved to `{DATA_STORAGE_FILE}`. You can now delete the original files.")
