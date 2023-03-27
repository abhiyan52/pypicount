"""
    author: abhiyanhaze
    description: Logic and runner for lines of code counter

"""

import os
import sys
import time
from registry import LanguageSyntaxRegistry
from counter import LineCounter, CounterResult
from prettytable import PrettyTable
import asyncio


class LineCounterFactory:
    # Factory for creating Counters with appropriate interface for parsing
    @staticmethod
    def create_counter(filepath, extension):
        if not LanguageSyntaxRegistry._initialized:
            LanguageSyntaxRegistry.initialize(load_default=True)

        syntax = LanguageSyntaxRegistry.get_syntax(extension.lower())
        if not syntax:
            return None
        syntax_instance = syntax()
        counter_obj = LineCounter(filepath, syntax_instance)
        return counter_obj


def print_as_table(counter_result):  # Helper function to print the result as table
    extra_keys = counter_result.extra.keys()
    field_names = (
        [
            "Blank",
            "Comments",
            "Code",
            "Total"
        ]
    )
    field_names.extend(extra_keys)
    curr_row = (
        [
            counter_result.blank_lines,
            counter_result.comment_lines,
            counter_result.code_lines,
            counter_result.total_lines
        ]
    )
    curr_row.extend(list(counter_result.extra.values()))
    table = PrettyTable(field_names)
    table.add_row(curr_row)
    print(table)


def count_file(filepath):
    print(filepath)
    print("-------------------------------\n\n")
    _, ext = os.path.splitext(filepath)
    counter = LineCounterFactory.create_counter(filepath, ext)
    if not counter:
        return filepath
    result = counter.count_lines()
    print("The result for filepath %s is" % filepath)
    print_as_table(result)
    return result


async def count_lines_for_file(filepath):
    result = await asyncio.to_thread(count_file, filepath)
    return result


async def walk_and_count_lines(directory):
    counters = []
    tasks = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            task = asyncio.create_task(count_lines_for_file(full_path))
            tasks.append(task)
    for task in asyncio.as_completed(tasks):
        counter = await task
        counters.append(counter)
    return counters


async def count_lines_for_directory(directory):
    t1 = time.time()
    counter_results = await walk_and_count_lines(directory)

    lang_wise_dict = {}
    unsupported_list = []

    for result in counter_results:
        if type(result) == CounterResult:
            if result.class_name not in lang_wise_dict:
                lang_wise_dict[result.class_name] = result
            else:
                lang_wise_dict[result.class_name] += result
        elif result:
            unsupported_list.append(result)

    print("\n\n---------------------------------------------\n\n\n")
    print("The result for visting path %s is:", os.path.abspath(directory))

    for language_parser_class, aggregated_result in lang_wise_dict.items():
        print("Aggregated result from %s" % language_parser_class)
        print_as_table(aggregated_result)

    t2 = time.time()

    print(f"Scanned {len(counter_results)} files in {t2 - t1} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python line_counter.py <filename> or <filepath>")
    else:

        filepath = sys.argv[1]

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                "The following file is not found in the path"
            )
        filepath = os.path.abspath(filepath)
        if os.path.isfile(filepath):
            print("Running count for single file")
            count_result = count_file(filepath)
            if not count_result:
                print("The following file type %s is not supported" % filepath)
            print("---------------------------------------------")
        else:
            asyncio.run(count_lines_for_directory(filepath))
