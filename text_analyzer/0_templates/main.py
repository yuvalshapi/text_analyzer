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

def main():
    args=readargs()

    task_num = int(args.task)
    if args.preprocessed:
        is_preprocessed = True
    else:
        is_preprocessed = False

    if task_num == 1:
        s_path = args.sentences
        name_path = args.names
        words_path = args.removewords
        processed_data = task1.TextPreprocessor(s_path, name_path, words_path,task_num)
        print(processed_data.get_json_format())
    if task_num == 2:
        k_num = args.maxk
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            words_path = args.removewords
        processed_data = task2.SequenceCounter(s_path,words_path,is_preprocessed,k_num)
        print(processed_data.get_json_format())

    if task_num == 3:
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            words_path = args.removewords
            name_path = args.names
        processed_data = task3.NamesCounter(s_path,name_path,words_path,is_preprocessed)
        print(processed_data.get_json_format())

    if task_num == 4:
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            words_path = args.removewords
            kseq_file = args.qsek_query_path
        processed_data = task4.KseqEngine(s_path,words_path,kseq_file,is_preprocessed)
        print(processed_data.get_json_format())

    if task_num == 5:
        size_of_kseq = args.maxk
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            name_path = args.names
            words_path = args.removewords
        processed_data = task5.ContextFinder(s_path,name_path,words_path,is_preprocessed,size_of_kseq)
        print(processed_data.get_json_format())

    if task_num == 6:
        window_size = args.windowsize
        threshold = args.threshold
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            name_path = args.names
            words_path = args.removewords
        processed_data = task6.ConnectionFinder(s_path,name_path,words_path,is_preprocessed,window_size,threshold)
        print(processed_data.get_json_format())

    if task_num == 7:
        window_size = args.windowsize
        threshold = args.threshold
        pc_path = args.pairs
        if is_preprocessed:
            s_path = args.preprocessed
        else:
            s_path = args.sentences
            name_path = args.names
            words_path = args.removewords
        processed_data = task7.IndirectConnector(s_path,name_path,words_path,pc_path,is_preprocessed,window_size,threshold)
        print(processed_data.get_json_format())

if __name__=="__main__":
    main()


