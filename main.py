#!/usr/bin/env python3

import argparse
import string
import os
import task1.textprocessor as task1
import task2.task2 as task2
import task3.task3 as task3
import task4.task4 as task4
import task5.task5 as task5
import task6.task6 as task6
import task7.task7 as task7


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

def process_task(task_num, args):
    """
    Handles the execution of different tasks based on task_num.

    Args:
        task_num (int): The selected task number.
        args (Namespace): Parsed command-line arguments.

    Returns:
        str: JSON output of the processed task.
    """
    is_preprocessed = bool(args.preprocessed)
    s_path = args.preprocessed[0] if is_preprocessed else args.sentences
    name_path = args.names
    words_path = args.removewords

    if task_num == 1:
        processed_data = task1.TextPreprocessor(s_path, name_path, words_path, task_num)

    elif task_num == 2:
        processed_data = task2.SequenceCounter(s_path, words_path, is_preprocessed, args.maxk)

    elif task_num == 3:
        processed_data = task3.NamesCounter(s_path, name_path, words_path, is_preprocessed)

    elif task_num == 4:
        processed_data = task4.KseqEngine(s_path, words_path, args.qsek_query_path, is_preprocessed)

    elif task_num == 5:
        processed_data = task5.ContextFinder(s_path, name_path, words_path, is_preprocessed, args.maxk)

    elif task_num == 6:
        processed_data = task6.ConnectionFinder(s_path, name_path, words_path, is_preprocessed, args.windowsize,
                                                args.threshold)

    elif task_num == 7:
        processed_data = task7.IndirectConnector(s_path, name_path, words_path, args.pairs, is_preprocessed,
                                                 args.windowsize, args.threshold)

    elif task_num == 8:
        processed_data = task7.IndirectConnector(s_path, name_path, words_path, args.pairs, is_preprocessed,args.fixed_length)
    else:
        raise ValueError("Invalid task number.")

    return processed_data.get_json_format()


def main():
    """
    Main function to parse arguments and execute the appropriate task.
    """
    args = readargs()
    task_num = int(args.task)

    try:
        result = process_task(task_num, args)
        print(result)
    except Exception as e:
        print(f"Error processing task {task_num}: {e}")


if __name__ == "__main__":
    main()


