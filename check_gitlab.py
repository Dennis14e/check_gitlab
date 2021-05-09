#!/usr/bin/env python3

import json
import socket
import sys
import urllib.request
import argparse

program_name = "check_gitlab"

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server",
                    dest="server",
                    help="URL of the server to be checked.",
                    action="store",
                    default="https://gitlab.example.org/",
                    required=True)
parser.add_argument("-t", "--token",
                    dest="token",
                    help="Your access token for Gitlab Health Checks.",
                    action="store")
parser.add_argument("-a", "--check-all",
                    dest="all",
                    help="Enable all checks",
                    action="store_true")
parser.add_argument("--check-cache",
                    dest="check_cache",
                    help="Enable checking cache status",
                    action="store_true")
parser.add_argument("--check-db",
                    dest="check_db",
                    help="Enable checking database status",
                    action="store_true")
parser.add_argument("--check-gitaly",
                    dest="check_gitaly",
                    help="Enable checking gitaly status",
                    action="store_true")
parser.add_argument("--check-queues",
                    dest="check_queues",
                    help="Enable checking queues status",
                    action="store_true")
parser.add_argument("--check-redis",
                    dest="check_redis",
                    help="Enable checking redis status",
                    action="store_true")
parser.add_argument("--check-shared-state",
                    dest="check_shared_state",
                    help="Enable checking shared state status",
                    action="store_true")
args = parser.parse_args(sys.argv[1:])


def get_readiness(server, token=None):
    if not server.endswith("/", 0):
        server = server + "/"
    if token == None:
        request = urllib.request.urlopen(server + "-/readiness?all=1")
    else:
        request = urllib.request.urlopen(server + "-/readiness?token=" + token + "&all=1")
    responseStr = str(request.read().decode("utf-8"))
    return json.loads(responseStr)


def check_module(readiness_json, module):
    try:
        status = readiness_json[module][0]["status"]
    except:
        status = "unknown"
    try:
        message = readiness_json[module][0]["message"]
    except:
        message = ""
    return status, message


def check_all(readiness_json):
    results = dict()
    results["db_check"] = check_module(readiness_json, "db_check")
    results["redis_check"] = check_module(readiness_json, "redis_check")
    results["cache_check"] = check_module(readiness_json, "cache_check")
    results["queues_check"] = check_module(readiness_json, "queues_check")
    results["shared_state_check"] = check_module(readiness_json, "shared_state_check")
    results["gitaly_check"] = check_module(readiness_json, "gitaly_check")
    return results


checks = check_all(get_readiness(args.server, args.token))
result = 0
checks_done = 0

if args.check_cache or args.all:
    checks_done += 1
    if str(checks["cache_check"][0]) != "ok":
        print("Cache check: Status=" + str(checks["cache_check"][0]) + ", Message=" + str(checks["cache_check"][1]))
        result = 2
if args.check_db or args.all:
    checks_done += 1
    if str(checks["db_check"][0]) != "ok":
        print("Database check: Status=" + str(checks["db_check"][0]) + ", Message=" + str(checks["db_check"][1]))
        result = 2
if args.check_gitaly or args.all:
    checks_done += 1
    if str(checks["gitaly_check"][0]) != "ok":
        print("Gitaly check: Status=" + str(checks["gitaly_check"][0]) + ", Message=" + str(checks["gitaly_check"][1]))
        result = 2
if args.check_queues or args.all:
    checks_done += 1
    if str(checks["queues_check"][0]) != "ok":
        print("Queues check: Status=" + str(checks["queues_check"][0]) + ", Message=" + str(checks["queues_check"][1]))
        result = 2
if args.check_redis or args.all:
    checks_done += 1
    if str(checks["redis_check"][0]) != "ok":
        print("Redis check: Status=" + str(checks["redis_check"][0]) + ", Message=" + str(checks["redis_check"][1]))
        result = 2
if args.check_shared_state or args.all:
    checks_done += 1
    if str(checks["shared_state_check"][0]) != "ok":
        print("Shared state check: Status=" + str(checks["shared_state_check"][0]) + ", Message=" + str(checks["shared_state_check"][1]))
        result = 2
if (result == 0):
    print("OK - All checks ok")

print(str(checks_done) + " checks done.")
