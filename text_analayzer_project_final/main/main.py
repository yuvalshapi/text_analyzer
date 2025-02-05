#!/usr/bin/env python3

import argparse
import sys
from text_analayzer_project_final.textprocessor import textprocessor
from text_analayzer_project_final.connection_finder import connection_finder
from text_analayzer_project_final.data_analyzer import data_analyzer


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )
    return parser.parse_args(args)


def validate_args(args):
    """
    Ensures that all required arguments for each task are provided.
    If a required argument is missing, prints an error and exits.
    """
    task_num = int(args.task)

    # General checks
    if not args.preprocessed and not args.sentences:
        print("Error: Either --sentences or --preprocessed must be provided.")
        sys.exit(1)

    if not args.removewords:
        print("Error: --removewords file is required.")
        sys.exit(1)

    # Task-specific checks
    if task_num in {2, 5} and not args.maxk:
        print(f"Error: --maxk is required for Task {task_num}.")
        sys.exit(1)

    if task_num == 4 and not args.qsek_query_path:
        print("Error: --qsek_query_path is required for Task 4.")
        sys.exit(1)

    if task_num in {6, 7, 8}:
        if not args.windowsize:
            print(f"Error: --windowsize is required for Task {task_num}.")
            sys.exit(1)
        if not args.threshold:
            print(f"Error: --threshold is required for Task {task_num}.")
            sys.exit(1)

    if task_num in {7, 8} and not args.pairs:
        print(f"Error: --pairs is required for Task {task_num}.")
        sys.exit(1)

    if task_num == 8 and not args.fixed_length:
        print("Error: --fixed_length is required for Task 8.")
        sys.exit(1)
    if  task_num > 8 or task_num < 1:
        print(f"Error: Task {task_num} is not supported.")
        sys.exit(1)
def process_task(args):
    """
    Handles the execution of different tasks based on task_num.

    Args:
        args (Namespace): Parsed command-line arguments.

    Returns:
        str: JSON output of the processed task.
    """
    validate_args(args)  # ✅ Ensure all required arguments are present

    is_preprocessed = bool(args.preprocessed)
    s_path = args.preprocessed[0] if is_preprocessed else args.sentences
    name_path = args.names
    words_path = args.removewords

    # Process the text data
    processed_data = textprocessor.TextPreprocessor(s_path, name_path, words_path, is_preprocessed, int(args.task))

    # Determine which class to use based on the task number
    task_num = int(args.task)
    if task_num == 1:
        return processed_data.get_json_format()
    if task_num in {2, 3, 4, 5}:
        task_handler = data_analyzer.DataAnalyzer(processed_data, args.maxk, args.qsek_query_path)
        task_functions = {
            2: task_handler.sequence_counter,
            3: task_handler.names_counter,
            4: task_handler.kseqengine,
            5: task_handler.find_context,
        }

    elif task_num in {6, 7, 8}:
        task_handler = connection_finder.ConnectionFinder(processed_data, int(args.windowsize), int(args.threshold), args.fixed_length,
                                           args.pairs)
        task_functions = {
            6: task_handler.find_connections,
            7: task_handler.check_connections,
            8: task_handler.check_connections,
        }


    # Execute the corresponding function if the task exists
    return task_functions[task_num]()


if __name__ == '__main__':
    args = readargs()
    process_task(args)
