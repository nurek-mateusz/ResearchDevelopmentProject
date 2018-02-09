from __future__ import print_function

import argparse
import logging
import os
import select
import sys
import msvcrt

# Fix to make cmd runnable from console without installing any module
# Just use `python cmd.py <args>`
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import git_stacktrace
from git_stacktrace import api

def main():
    usage = "git stacktrace [<options>] [<RANGE>] < stacktrace from stdin"
    description = "Lookup commits related to a given stacktrace."
    parser = argparse.ArgumentParser(usage=usage, description=description)
    range_group = parser.add_mutually_exclusive_group()
    range_group.add_argument('--since', metavar="<date1>", help='show commits '
                             'more recent than a specific date (from git-log)')
    range_group.add_argument('--until', metavar="<date2>", help='show commits '
                             'less recent than a specific date (from git-log)')
    range_group.add_argument('range', nargs='?', help='git commit range to use')
    parser.add_argument('-f', '--fast', action="store_true", help='Speed things up by not running '
                        'pickaxe if the file for a line of code cannot be found')
    parser.add_argument('-b', '--branch', nargs='?', help='Git branch. If using --since, use this to '
                        'specify which branch to run since on. Runs on current branch by default')
    parser.add_argument('--version', action="version",
                        version='%s version %s' % (os.path.split(sys.argv[0])[-1], git_stacktrace.__version__))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    logging.basicConfig(format='%(name)s:%(funcName)s:%(lineno)s: %(message)s')
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.since or args.until:
        git_range = api.convert_since_until(args.since, args.until, branch=args.branch)
        print("commit range: %s" % git_range, file=sys.stderr)
    else:
        if args.range is None:
            print("Error: Missing range and since, must use one\n")
            parser.print_help()
            sys.exit(1)
        git_range = args.range

    if not api.valid_range(git_range):
        print("Found no commits in '%s'" % git_range)
        sys.exit(1)

    if os.name == 'nt':
        blob = read_stdin()
        if not blob:
            raise Exception("No input found in stdin")
        print(blob)
        traceback = api.parse_trace(blob)
    else:
        if not select.select([sys.stdin], [], [], 0.0)[0]:
            raise Exception("No input found in stdin")
        blob = sys.stdin.readlines()
        traceback = api.parse_trace(blob)

    print(traceback)

    results = api.lookup_stacktrace(traceback, git_range, fast=args.fast)

    for r in results.get_sorted_results():
        print("")
        print(r)

    if len(results.get_sorted_results()) == 0:
        print("No matches found")

def read_stdin():
    return ''.join(sys.stdin.readlines()).strip()

if __name__ == "__main__":
    main()
