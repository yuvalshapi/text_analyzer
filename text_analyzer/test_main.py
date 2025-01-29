import os
import json
import subprocess
import general_files.general_test_functions as gtf

# ANSI escape codes for colored output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def run_task1_test():
    base_dir = "2_examples"
    for i in range(1, 4):
        print(f"\n=== Running Test for Task 1, File Set {i} ===")

        # File paths for the current iteration
        s_path = os.path.join(base_dir, "Q1_examples", f"example_{i}", f"sentences_small_{i}.csv")
        p_path = os.path.join(base_dir, "Q1_examples", f"example_{i}", f"people_small_{i}.csv")
        w_path = os.path.join(base_dir, "Q1_examples", f"example_{i}", "REMOVEWORDS.csv")
        e_path = os.path.join(base_dir, "Q1_examples", f"example_{i}", f"Q1_result{i}.json")
        output_path = os.path.join(base_dir, "Q1_examples", f"example_{i}", f"processed_result{i}.json")

        # Load the expected JSON result for the current iteration
        with open(e_path, 'r') as file:
            expected_result = json.load(file)

        # Run main.py with the appropriate arguments and save output to a file
        args = ["python", "main.py", "-t", "1", "-s", s_path, "-n", p_path, "-r", w_path]
        with open(output_path, "w") as outfile:
            subprocess.run(args, stdout=outfile, text=True)

        # Load the generated output for comparison
        with open(output_path, "r") as file:
            processed_result = json.load(file)

        # Compare and print results with sources
        if processed_result == expected_result:
            print(f"{Colors.GREEN}Task 1, File Set {i}: PASS{Colors.RESET}")
        else:
            print(f"{Colors.RED}Task 1, File Set {i}: FAIL{Colors.RESET}")
            gtf.print_differences_and_find_sources(processed_result, expected_result, sentences_file=s_path)

def test_task1():
    run_task1_test()

if __name__ == "__main__":
    run_task1_test()
