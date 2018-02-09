@echo off
rem PUT THIS FILE INSIDE PROPER GIT REPOSITORY
rem THIS SCRIPT REQUIRES PYTHON INSTALLED AND ADDED TO PATH

rem path to `predict.py` file
set stacktrace-predictor=..\..\python\stack-trace-predictor\predict.py

rem path to input stacktrace file
set stacktrace=..\..\python\stack-trace-predictor\test-data\NEXUS-15278.txt

rem stacktrace-predictor git range. Refer to stacktrace-predictor itself for more information
set git-range=--issue="NEXUS-15278" --trackerurl="https://issues.sonatype.org" --since="1 year ago"

python %stacktrace-predictor% %git-range% %stacktrace%