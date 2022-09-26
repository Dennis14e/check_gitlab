#!/usr/bin/env python3

import argparse
import json
import sys
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server",
                    dest="server",
                    help="URL of the server to be checked.",
                    action="store",
                    default="https://gitlab.example.org/",
                    required=True)
parser.add_argument("-t", "--token",
                    dest="token",
                    help="Your access token for GitLab Health Checks",
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
parser.add_argument("--check-master",
                    dest="check_master",
                    help="Enable checking master status",
                    action="store_true")
parser.add_argument("--check-queues",
                    dest="check_queues",
                    help="Enable checking queues status",
                    action="store_true")
parser.add_argument("--check-rate-limiting",
                    dest="check_rate_limiting",
                    help="Enable checking rate limiting status",
                    action="store_true")
parser.add_argument("--check-sessions",
                    dest="check_sessions",
                    help="Enable checking sessions status",
                    action="store_true")
parser.add_argument("--check-shared-state",
                    dest="check_shared_state",
                    help="Enable checking shared state status",
                    action="store_true")
parser.add_argument("--check-trace-chunks",
                    dest="check_trace_chunks",
                    help="Enable checking trace chunks status",
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
        status = str(readiness_json[module][0]["status"])
    except:
        status = "unknown"
    try:
        message = str(readiness_json[module][0]["message"])
    except:
        message = ""
    return status, message


def check_all(readiness_json):
    results = dict()
    results["cache"] = check_module(readiness_json, "cache_check")
    results["db"] = check_module(readiness_json, "db_check")
    results["gitaly"] = check_module(readiness_json, "gitaly_check")
    results["master"] = check_module(readiness_json, "master_check")
    results["queues"] = check_module(readiness_json, "queues_check")
    results["rate_limiting"] = check_module(readiness_json, "rate_limiting_check")
    results["sessions"] = check_module(readiness_json, "sessions_check")
    results["shared_state"] = check_module(readiness_json, "shared_state_check")
    results["trace_chunks"] = check_module(readiness_json, "trace_chunks_check")
    return results


checks = check_all(get_readiness(args.server, args.token))
checks_done = 0
msgs = []

if args.check_cache or args.all:
    checks_done += 1
    if checks["cache"][0] != "ok":
        msgs.append("Cache check: Status=%s, Message=%s" % (checks["cache"][0], checks["cache"][1]))
if args.check_db or args.all:
    checks_done += 1
    if checks["db"][0] != "ok":
        msgs.append("Database check: Status=%s, Message=%s" % (checks["db"][0], checks["db"][1]))
if args.check_gitaly or args.all:
    checks_done += 1
    if checks["gitaly"][0] != "ok":
        msgs.append("Gitaly check: Status=%s, Message=%s" % (checks["gitaly"][0], checks["gitaly"][1]))
if args.check_master or args.all:
    checks_done += 1
    if checks["master"][0] != "ok":
        msgs.append("Master check: Status=%s, Message=%s" % (checks["master"][0], checks["master"][1]))
if args.check_queues or args.all:
    checks_done += 1
    if checks["queues"][0] != "ok":
        msgs.append("Queues check: Status=%s, Message=%s" % (checks["queues"][0], checks["queues"][1]))
if args.check_rate_limiting or args.all:
    checks_done += 1
    if checks["rate_limiting"][0] != "ok":
        msgs.append("Rate limiting check: Status=%s, Message=%s" % (checks["rate_limiting"][0], checks["rate_limiting"][1]))
if args.check_sessions or args.all:
    checks_done += 1
    if checks["sessions"][0] != "ok":
        msgs.append("Sessions check: Status=%s, Message=%s" % (checks["sessions"][0], checks["sessions"][1]))
if args.check_shared_state or args.all:
    checks_done += 1
    if checks["shared_state"][0] != "ok":
        msgs.append("Shared state check: Status=%s, Message=%s" % (checks["shared_state"][0], checks["shared_state"][1]))
if args.check_trace_chunks or args.all:
    checks_done += 1
    if checks["trace_chunks"][0] != "ok":
        msgs.append("Trace chunks check: Status=%s, Message=%s" % (checks["trace_chunks"][0], checks["trace_chunks"][1]))

if not msgs:
    print("OK - %d checks ok" % (checks_done))
    sys.exit(0)
else:
    print("UNKNOWN - " + "; ".join(msgs))
    sys.exit(3)
