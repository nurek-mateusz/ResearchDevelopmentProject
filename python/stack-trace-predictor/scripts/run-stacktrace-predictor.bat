@echo off
rem PUT THIS FILE INSIDE PROPER GIT REPOSITORY
rem THIS SCRIPT REQUIRES PYTHON INSTALLED AND ADDED TO PATH

rem path to `predict.py` file
set stacktrace-predictor=..\..\python\stack-trace-predictor\predict.py

rem path to input stacktrace file
set stacktrace=..\..\python\stack-trace-predictor\test-data\SPR-15810.txt

rem stacktrace-predictor git range. Refer to stacktrace-predictor itself for more information
set git-range=--until="now" --since"1 year ago"

python %stacktrace-predictor% %git-range% %stacktrace%