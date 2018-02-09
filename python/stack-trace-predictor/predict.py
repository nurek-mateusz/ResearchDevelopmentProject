import sys
import argparse
import os
from functools import reduce
from itertools import groupby
from math import exp

# Fix to make cmd runnable from console without installing any module
# Just use `python cmd.py <args>`
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import git_stacktrace
from git_stacktrace import api as git_stacktrace_api
from git_stacktrace.result import Result

from print_function_helpers import eprint, dprint, setDebugMode, getDebugMode
import issue_tracker


def main():

    usage = "stacktrace-predict [<options>] [<RANGE>] <stacktrace>"
    description = "Retrieves people most related to a given stacktrace fail."
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument(
        'stacktrace', help='path to file containing stacktrace')
    parser.add_argument('--since', metavar="<date1>", help='include commits '
                        'more recent than a specific date (from git-log). Overrides `range`')
    parser.add_argument('--until', metavar="<date2>", help='include commits '
                        'less recent than a specific date (from git-log). Overrides `range`')
    parser.add_argument('--issue', metavar="<issueid>",
                        help='issue id from JIRA to set git range automatically'
                        '. Overrides any git range parameters except --since')
    parser.add_argument('--trackerurl', metavar="<issueurl>",
                        help='issue tracker URL, only JIRA is currently supported. Required when using --issue')
    parser.add_argument('range', nargs='?', help='git commit range to use')
    parser.add_argument('-b', '--branch', nargs='?', help='git branch. If using --since and/or --until, use this to '
                        'specify which branch to run since on. Runs on current branch by default')
    parser.add_argument('--version', action="version",
                        version='%s version %s' % ('stacktrace predictor', '0.1.0'))
    parser.add_argument('--debug', action="store_true",
                        help='show debug prints')
    parser.add_argument('--commits', action="store_true",
                        help='show full associated commits data')
    args = parser.parse_args()

    # Set debug flag
    setDebugMode(args.debug)

    # Check if stacktrace file exists
    if not os.path.isfile(args.stacktrace):
        eprint("Error: Cannot open file `%s`" % args.stacktrace)
        sys.exit(1)

    # Read input stacktrace
    with open(args.stacktrace) as f:
        stacktrace = ''.join(f.readlines()).strip()
    dprint(stacktrace)

    # Get proper git range
    if args.issue:
        # This will fetch issue data from a tracker
        if not args.trackerurl:
            eprint(
                "Error: Tried to fetch issue data from tracker, but no `trackerurl` provided\n")
            parser.print_help()
            sys.exit(1)
        str_range = issue_tracker.fetch_range(args.trackerurl, args.issue)
        git_range = git_stacktrace_api.convert_since_until(
            args.since, str_range[1], branch=args.branch)
    elif args.since or args.until:
        git_range = git_stacktrace_api.convert_since_until(
            args.since, args.until, branch=args.branch)
    else:
        if args.range is None:
            eprint("Error: Missing range and since/until, must use one\n")
            parser.print_help()
            sys.exit(1)
        git_range = args.range

    print("commit range: %s" % git_range)

    # Validate that git range has some results
    if not git_stacktrace_api.valid_range(git_range):
        eprint("Found no commits in '%s'" % git_range)
        sys.exit(1)

    traceback = git_stacktrace_api.parse_trace(stacktrace)
    results = git_stacktrace_api.lookup_stacktrace(traceback, git_range, False)

    # Extract and sort results

    results_by_date = sorted(results.results.values(),
                             key=lambda result: result.date, reverse=True)

    sorted_results = []
    for line in traceback.lines:
        # This ambiguation is probably not needed, though git_filename should be more accurate
        # In edge cases there might be two files in exactly same packages but different projects
        file_name = line.git_filename if line.git_filename else line.trace_filename
        for result in results_by_date:
            if not result in sorted_results and result_contains_file(result, file_name):
                sorted_results.append(result)

    if len(sorted_results) != len(results_by_date):
        eprint("Fatal: There are commits found that do not contains code from the stacktrace!"
               "This is most likely a bug, report issue on our github")
        sys.exit(1)

    # This should probably be controlled by a optional parameter
    # sorted_results = results_by_date

    # Print commits
    if not sorted_results:
        print("No commits found. Try wider git range")
        sys.exit(0)
    elif args.commits or getDebugMode():
        for result in sorted_results:
            print("")
            print(result)

    last_updater = sorted_results[0].author
    # How much more important are new commits
    COMMIT_DECAY_LAMBDA = 1 / 10
    # Hom much more important are commits modyfing top lines in stacktrace
    STACKTRACE_DECAY_LAMBDA = 1 / 4

    updaters_sorted_by_rank = []
    # Commits by author
    # Have to sort again because of groupby implementation
    for key, committer in groupby(sorted(sorted_results, key=lambda x: x.author), key=lambda x: x.author):
        dprint(key)
        committer_score = 0
        # For each commit calculate impact on stacktrace's code
        for commit in committer:
            dprint("\tcommit - %s" % commit.commit)

            commit_score = 0
            # The newer the commit, the bigger the score
            commit_index = sorted_results.index(commit)
            commit_decay = exp(-COMMIT_DECAY_LAMBDA * commit_index)
            dprint("\tcommit_index - %s" % commit_index)
            dprint("\tcommit_decay - %s" % commit_decay)
            # The closer to the top, the bigger the score
            for line_index, line in enumerate(traceback.lines):
                file_name = line.trace_filename
                stacktrace_decay = exp(-STACKTRACE_DECAY_LAMBDA * line_index)
                dprint("\t\tfile_name - %s" % file_name)
                dprint("\t\t\tline_index - %s" % line_index)
                dprint("\t\t\tstacktrace_decay - %s" % stacktrace_decay)
                if result_contains_file(commit, file_name):
                    dprint("\t\t\t+1")
                    score = stacktrace_decay * 1
                    commit_score += score
            commit_score *= commit_decay
            dprint("\tcommit_score - %s" % commit_score)
            committer_score += commit_score
        dprint("\tcommitter_score - %s" % committer_score)
        updaters_sorted_by_rank.append((key, committer_score))
    updaters_sorted_by_rank = sorted(
        updaters_sorted_by_rank, key=lambda x: x[1])

    print("last updater - %s" % last_updater)
    print("stacktrace code authorship -")
    for committer in updaters_sorted_by_rank:
        print("\t{0:<60} | {1:<}".format(committer[0], committer[1]))


def result_contains_file(result: git_stacktrace.result.Result, file_name: str) -> bool:
    return (any(file_name in file_path for file_path in result.files_added) or
            any(file_name in file_path for file_path in result.files_deleted) or
            any(file_name in file_path for file_path in result.files_modified) or
            # Both sets below might be unnecessary
            any(file_name in file_path for file_path in result.lines_added) or
            any(file_name in file_path for file_path in result.lines_removed))


if __name__ == "__main__":
    sys.exit(main())
