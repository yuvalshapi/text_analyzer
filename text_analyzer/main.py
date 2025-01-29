#!/usr/bin/env python3

import argparse
import string
import os
import task1.textprocessor as tp
import data_analyzer.data_analyzer as da
import connection_finder.connection_finder as cf

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


def process_task(args):
    """
    Handles the execution of different tasks based on task_num.

    Args:
        args (Namespace): Parsed command-line arguments.

    Returns:
        str: JSON output of the processed task.
    """
    is_preprocessed = bool(args.preprocessed)
    s_path = args.preprocessed[0] if is_preprocessed else args.sentences
    name_path = args.names
    words_path = args.removewords

    # Process the text data
    processed_data = tp.TextPreprocessor(s_path, name_path, words_path, is_preprocessed, int(args.task))

    # Determine which class to use based on the task number
    task_num = int(args.task)
    if task_num == 1:
        return processed_data.get_json_format()
    if task_num in {2, 3, 4, 5}:
        task_handler = da.DataAnalyzer(processed_data, args.maxk, args.qsek_query_path)
        task_functions = {
            2: task_handler.sequence_counter,
            3: task_handler.names_counter,
            4: task_handler.kseqengine,
            5: task_handler.find_context,
        }

    elif task_num in {6, 7, 8}:
        task_handler = cf.ConnectionFinder(processed_data, int(args.windowsize), int(args.threshold), args.fixed_length,
                                           args.pairs)
        task_functions = {
            6: task_handler.find_connections,
            7: task_handler.check_connections,
            8: task_handler.check_connections,
        }

    else:
        print(f"Error: Task {task_num} is not supported.")
        return

    # Execute the corresponding function if the task exists
    return task_functions[task_num]()

if __name__ == '__main__':
    args = readargs()
    process_task(args)


