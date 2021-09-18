"""
File consist of functions that used as a helpers to parse NGINX log files in log_parser_plugin
"""

import json


def get_top_ips(lines, max_client_ips):
    """
    Function used to collect top client IPs from the given input
    :param lines:
    :param max_client_ips:
    :return: top_n:
    """
    ips = {}
    for line in lines:
        try:
            ips[line['remote_addr']] = ips.get(line['remote_addr'], 0) + 1
        except LookupError:
            print("Exception raised while collecting IPs")

    sorted_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_ips[:max_client_ips]
    return top_n


def get_slowest_urls(lines, max_paths):
    """
    Function used to collect slowest URIs from the given input

    :param lines:
    :param max_paths:
    :return: slowest_n:
    """
    urls = {}
    avg = {}

    # Collecting all response time values for each uri
    for line in lines:
        try:
            response_time = int(line['http_response_time_milliseconds']) * 0.001
            uri = line['req_uri']
            urls.setdefault(uri, []).append(response_time)

        except LookupError:
            print("Exception raised while collecting URIs")

    # Calculating average response time for each uri
    for url in urls:
        try:
            values = urls.get(url)
            avg[url] = float('%.2f' % (sum(values) / len(values)))

        except LookupError:
            print("Exception raised while collecting URIs")

    # Sorting all average values to get top n slowest
    sorted_urls = sorted(avg.items(), key=lambda x: x[1], reverse=True)
    slowest_n = sorted_urls[:max_paths]
    return slowest_n


def dump_data_to_json(data, result_json):
    """
    Function used to convert data to JSON file
    :param data:
    :param result_json:
    """
    try:
        with open(result_json, 'w') as json_file:
            json.dump(data, json_file)

    except IOError:
        print("Could not write file: {}".format(result_json))
