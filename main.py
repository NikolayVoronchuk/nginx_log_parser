#!/usr/bin/env python
"""
File that holds main runner function and drives plugin execution flow.

INPUT:
    --in: string, specifies the input file, and it is required.

    --out: string, specifies the output JSON file, and it is required.

    --max-client-ips: integer, defines the maximum number of results
    to output in the top_client_ips field. Defaults to 10 if not provided.

    --max-paths: integer, defined the maximum number of results
    to output on the top_path_avg_seconds field. Defaults to 10 if not provided.
    both --max-client-ips and --max-paths flags can take a value from the
    following range: 0 to 10000 - when any of the command line flags are
    invalid, the plugin must exit with return code of 1

EXAMPLE:
    main.py --in input.log --out output.json --max-client-ips 5 --max-paths 25

------------------------------------------------------------------------------------------------------------------------

OUTPUT:
    total_number_of_lines_processed: must be an integer value, containing
    total number of lines processed by the plugin.

    total_number_of_lines_ok: must be an integer value, containing total
    number of lines which were parsed successfully and were accounted for in
    the output.

    total_number_of_lines_failed: must be an integer value, containing total
    number of lines which failed to be parsed successfully due to format error,
    and hence didn't contribute to the end result counters.

    top_client_ips: must be an object with length not more than max-client-ips
    command line parameter, and must contain string representation of IP addresses,
    which appeared the most in the input data.

    top_path_avg_seconds: must be an object with length not more than max-paths
    command line parameter, and must contain string representations of the HTTP paths,
    which had the slowest average response times.
    Times should be floating point numbers with a precision of two decimals,
    and the paths should be URL decoded.

EXAMPLE:
{
      "total_number_of_lines_processed": 4,
      "total_number_of_lines_ok": 4,
      "total_number_of_lines_failed": 0,

      "top_client_ips": {
        "92.177.30.4": 1,
        "51.232.15.21": 1,
        "34.149.47.34": 1,
        "112.21.100.55": 1
      },

      "top_path_avg_seconds": {
        "/admin.php": 0.05,
        "/product/catalog": 1.09,
        "/product/cart": 1.2
      }
}
"""
import sys
import collections
from arguments_parser import parse_args
from log_parser_plugin import parse_log
from utils import get_top_ips, get_slowest_urls, dump_data_to_json
from output_model import output


def main():
    """
    Main runner function to initiate log parsing and generating JSON file with results
    """
    args = parse_args()

    # Arguments check
    if not args["max_client_ips"] >= 0 <= 10000:
        sys.exit(1)

    if not args["max_paths"] >= 0 <= 10000:
        sys.exit(1)

    # Parsing input file
    parsed_data = parse_log(args["in"])

    # Generating output object
    _output = output
    _output["total_number_of_lines_processed"] = parsed_data["total_count"]
    _output["total_number_of_lines_ok"] = parsed_data["parsed_count"]
    _output["total_number_of_lines_failed"] = parsed_data["failed_to_parse_count"]
    _output["top_client_ips"] = collections.OrderedDict(get_top_ips(parsed_data["parsed_lines"], args["max_client_ips"]))
    _output["top_path_avg_seconds"] = collections.OrderedDict(get_slowest_urls(parsed_data["parsed_lines"], args["max_paths"]))

    # Generating output JSON file
    dump_data_to_json(_output, args["out"])


if __name__ == "__main__":
    main()
