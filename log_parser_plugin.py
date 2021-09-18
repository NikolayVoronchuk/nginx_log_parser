"""
Log file parser

This file consist of functions that are used to parse log files based on provided patterns from:
    log_patterns.py

"""
import re
from log_patterns import nginx_format


def read_file_line(file_name):
    """
    Function used to read file and return read line
    :param file_name:
    """
    try:
        with open(file_name, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line
    except IOError:
        print("Could not read file: {}".format(file_name))


def parse_log(log_file, pattern=nginx_format):
    """
    Function used to parse log file based on the provided format. Returns object with parsed lines, total count of lines
    parsed, successfully parsed count, failed to parse count.

    :param log_file:
    :param pattern:
    :return: result:
    """
    total_count = 0
    parsed_count = 0
    failed_to_parse_count = 0
    parsed_lines = []
    result = {}

    lines = read_file_line(log_file)

    for line in lines:
        matched = re.match(pattern, line)
        total_count += 1
        try:
            parsed_line = matched.groupdict()
            parsed_count += 1
            parsed_lines.append(parsed_line)

        except AttributeError:
            failed_to_parse_count += 1
            print('Line {} not parsed: {} '.format(total_count, line))

    result["parsed_lines"] = parsed_lines
    result["total_count"] = total_count
    result["parsed_count"] = parsed_count
    result["failed_to_parse_count"] = failed_to_parse_count

    return result
