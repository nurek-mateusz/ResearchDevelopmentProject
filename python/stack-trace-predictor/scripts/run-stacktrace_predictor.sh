#!/bin/sh

# PUT THIS FILE INSIDE PROPER GIT REPOSITORY
# THIS SCRIPT REQUIRES PYTHON INSTALLED AND ADDED TO PATH

# path to `predict.py` file
stacktracepredictor=../python/stack-trace-predictor/predict.py

# path to input stacktrace file
stacktrace=../python/stack-trace-predictor/test-data/SPR-15078.txt

# stacktrace-predictor git range. Refer to stacktrace-predictor itself for more information
gitrange="--issue=SPR-15078 --trackerurl=http://jira.spring.io"

python $stacktracepredictor $gitrange $stacktrace