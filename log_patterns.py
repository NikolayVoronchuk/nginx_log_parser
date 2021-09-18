"""
Log patterns file that host different patterns for log files that can be imported into log_parser_plugin.py

using nginx log format: <remote_addr> - <remote_user> [<date>] "<http_verb> <http_path> <http_version>"
                        <http_response_code> <http_response_time_milliseconds> "<user_agent_string>"
"""

nginx_format = '(?P<remote_addr>(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.]))\s-\s(?P<remote_user>-|[a-z_-][a-z0-9_-]{0,100})\s(?P<date_time>\[(?P<date>[0-2][0-9]\/\w{3}\/[12]\d{3}):(?P<time>\d\d:\d\d:\d\d).*\])\s(?P<request>\"(?P<request_method>GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)\s(?P<req_uri>%[^\s]*|/[^\s]*)\s(?P<http_version>HTTP/\d\.\d)\")\s(?P<response_code>\d{3})\s(?P<http_response_time_milliseconds>\d+)\s\"(?P<user_agent>[^\"]+)\"'
