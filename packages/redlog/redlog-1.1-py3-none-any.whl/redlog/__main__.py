#!/usr/bin/env python3

import argparse
import os
import re
import redlog
import time
from datetime import datetime
from termcolor import colored

COLORS = {
    redlog.Tag.DEBUG: "white",
    redlog.Tag.INFO: "cyan",
    redlog.Tag.WARNING: "yellow",
    redlog.Tag.ERROR: "red",
    redlog.Tag.CRITICAL: "red",
    redlog.Tag.SUCCESS: "green"
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Displays logs.")
    parser.add_argument("--host",
                        type=str,
                        default=os.environ.get("REDLOG_HOST", "localhost"),
                        help="Redis host; defaults to REDLOG_HOST env variable or 'localhost' if not set")
    parser.add_argument("--port", "-p",
                        type=int,
                        default=os.environ.get("REDLOG_PORT", 6379),
                        help="Redis port; defaults to REDLOG_PORT env variable or '6379' if not set")
    parser.add_argument("--db",
                        type=int,
                        default=os.environ.get("REDLOG_DB", 15),
                        help="Redis database number; defaults to REDLOG_DB env variable or '15' if not set")
    parser.add_argument("--time-format",
                        type=str,
                        default="%a %d %b %H:%M:%S",
                        help="Datetime format used to print out timestamps")

    parser.add_argument("--last", "-l",
                        type=str,
                        default=None,
                        help="Prints messages not older than the passed time range value, i.e. '10m' for 10 minutes")
    args = parser.parse_args()

    # parse the time range
    now = time.time()
    time_range = [0, now + 1]
    if args.last:
        match = re.match(r"(\d*)(s|sec|m|min|h|d|w)$", args.last)
        if match:
            units = {
                "s": 1,
                "sec": 1,
                "m": 60,
                "min": 60,
                "h": 3600,
                "d": 3600 * 24,
                "w": 3600 * 24 * 7,
            }
            num = int(match.group(1) or "1")
            time_range = (now - num * units[match.group(2)], now + 1)
        else:
            raise ValueError(f"Cannot interpret time range: {args.last}")

    # instantiate the database connection
    log = redlog.Log(host=args.host, port=args.port, db=args.db)
    threads = []

    # loop the messages
    for message in log.read(*time_range):
        millisec = (message.timestamp % 1) * 1000
        time_mark = datetime.fromtimestamp(message.timestamp).strftime(args.time_format) + ".%03d" % (millisec)

        prefix = ""
        indent = "\n" + " " * (len(time_mark) + 1)
        stroke = False
        for i, msg in enumerate(threads):
            # nothing
            if msg is None:
                prefix += "─" if stroke else " "
                indent += " "
            # in the thread
            elif message.pred == msg:
                prefix += "╰" if message.is_last else "├"
                indent += " " if message.is_last else "│"
                assert not stroke
                stroke = True
                threads[i] = None if message.is_last else message
            else:
                prefix += "┼" if stroke else "│"
                indent += "│"

        # shrink
        while len(threads) > 0 and threads[-1] is None:
            threads.pop(-1)

        # new thread
        if not message.is_last:
            if message.pred is None:
                # no predesessor: the thread is about to start
                threads.append(message)
                prefix += "╭"
                indent += " "
            elif message.pred is True:
                # a predecessor exists, but out of range
                threads.append(message)
                prefix += ":"
                indent += "│"

        # indent lines
        content = f"{indent} ".join(message.content.split("\n"))

        print(colored(time_mark, COLORS[message.tag]), colored(prefix, "white"), content)
