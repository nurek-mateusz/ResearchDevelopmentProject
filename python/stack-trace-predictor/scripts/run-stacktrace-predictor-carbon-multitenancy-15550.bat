@echo off
rem PUT THIS FILE INSIDE PROPER GIT REPOSITORY
rem THIS SCRIPT REQUIRES PYTHON INSTALLED AND ADDED TO PATH

rem path to `predict.py` file
set stacktrace-predictor=..\..\python\stack-trace-predictor\predict.py

rem path to input stacktrace file
set stacktrace=..\..\python\stack-trace-predictor\test-data\CARBON-15550.txt

rem stacktrace-predictor git range. Refer to stacktrace-predictor itself for more information
set git-range=--issue="CARBON-15550" --trackerurl="https://wso2.org/jira"

python %stacktrace-predictor% %git-range% %stacktrace%