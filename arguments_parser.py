"""
    File hold function to parse arguments that are being passed to the main method. Used ArgumentParser to add help
    strings and type check with default values.
"""

from argparse import ArgumentParser


def parse_args():
    """
    Function used to parse arguments that are passed to main function
    :rtype: object
    """
    arguments = ArgumentParser(
        description='using log format: \'$remote_addr - $remote_user [$date] "$request" $response_code $response_time '
                    '$user_agent\'',
    )
    arguments.add_argument("--in", "-i", required=True, help="NGINX log file, with defined format")
    arguments.add_argument("--out", "-o", required=True, help="Output JSON file")
    arguments.add_argument("--max-client-ips", default=10, type=int, help="defines the maximum number "
                                                                          "of results to output in "
                                                                          "the top_client_ips field. "
                                                                          "Defaults to 10 if not "
                                                                          "provided.")
    arguments.add_argument("--max-paths", default=10, type=int, help="defined the maximum number of "
                                                                     "results to output on the "
                                                                     "top_path_avg_seconds field. "
                                                                     "Defaults to 10 if not provided.")
    return vars(arguments.parse_args())
