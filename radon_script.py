#!/usr/bin/python
from radon.complexity import cc_rank, cc_visit, sorted_results
from radon.metrics import mi_visit, mi_parameters
from radon.raw import analyze
from collections import OrderedDict
from radon.cli.tools import iter_filenames
from typing import NoReturn, List
import numpy as np
import re
import sys

stdoutOrigin = sys.stdout
sys.stdout = open("log.txt", "w")

def sort_dict(dictionary: OrderedDict) -> List:
    return list(reversed(sorted(dictionary.items())))


def mi_print(dictionary: OrderedDict) -> NoReturn:
    sorted_dict = sort_dict(dictionary)
    print('2.PROJECT FILES SORTED BY THE MAINTAINABILITY INDEX')
    print('N MI Filename')
    print('---------------------------------------------------')
    for n in range(len(sorted_dict)):
        print(n, np.round(sorted_dict[n][0], 2), sorted_dict[n][1])
    print()


def files_complexity_print(dictionary: OrderedDict) -> NoReturn:
    sorted_dict = sort_dict(dictionary)
    print('3. PROJECT FILES RANKED AND SORTED BY CYCLOMATIC COMPLEXITY')
    print('N | Rank | LLOC |  HV  |   % of LC   |    Filename')
    print('-------------------------------------------------')
    for n in range(len(sorted_dict)):
        rank, file_name, halstead_vol, logic_lines, lines_comment = sorted_dict[n][1]
        rank = cc_rank(rank)
        halstead_vol, lines_comment = np.round(halstead_vol, 2), np.round(lines_comment, 2)
        space = '  '
        print(n, space, rank, space, logic_lines, space, halstead_vol, space,
              lines_comment, space, file_name)


def methods_complexity_print(file: str, dictionary: OrderedDict) -> NoReturn:
    print('Methods of filename:', file)
    sorted_dict = sort_dict(dictionary)
    print('N | Score | Filename')
    print('--------------------------')
    for n in range(len(sorted_dict)):
        print(n, '  ', sorted_dict[n][0], '   ', sorted_dict[n][1])
    print()


if __name__ == '__main__':
    mi_dict = OrderedDict()
    param_dict = OrderedDict()
    print('1. METHODS OF PROJECT FILES SORTED BY CYCLOMATIC COMPLEXITY')

    for filename in iter_filenames(['.']):
        file_methods = []
        file_complexities = []
        methods_dictionary = OrderedDict()

        with open(filename) as fobj:
            source = fobj.read()

        # get cc blocks
        blocks = cc_visit(source)

        # get MI score
        mi = mi_visit(source, True)
        mi_dict[mi] = filename

        # get raw metrics
        raw = analyze(source)
        hal_vol, complexity, logic_lines, com_lines = mi_parameters(source)
        param_dict[complexity] = (complexity, filename, hal_vol, logic_lines,
                                  com_lines)

        # get metrics for each file
        file_complexity = sorted_results(blocks)
        try:
            file_methods.append(re.findall('(?<=.Function\(name=\')[^\']'
                                           '*(?=\')', str(file_complexity)))

            file_complexities.append(re.findall('(?<=.complexity=)\d*',
                                                str(file_complexity)))
        except IndexError:
            continue

        mask = np.arange(len(file_methods[0]))
        for complexity, method in zip(file_complexities, file_methods):
            try:
                for i in mask:
                    methods_dictionary[int(complexity[i])] = method[i]
                methods_complexity_print(filename, methods_dictionary)
            except IndexError:
                continue

    mi_print(mi_dict)
    files_complexity_print(param_dict)

sys.stdout.close()
sys.stdout = stdoutOrigin
