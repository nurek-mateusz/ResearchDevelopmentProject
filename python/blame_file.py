from datetime import datetime

import git

from blame_model import BlameModel


class GitBlame:
    def __init__(self, path, filename):
        g = git.Git(path)
        result = g.execute(["git", "blame", filename])
        logs = result.split("\n")
        print(logs)
        self.blameList = []

        for log in logs:
            log_split = log.split(" ")
            log_split = list(filter(None, log_split))

            hash = log_split[0]
            path = log_split[1]
            first_name = log_split[2].replace("(", "")
            last_name = log_split[3]
            date = log_split[4] + " " + log_split[5]
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            line_number = log_split[7].replace(")", "")
            line = log.split(") ")[1]

            self.blameList.append(BlameModel(hash, path, first_name, last_name, date, line_number, line))


blame = GitBlame("/Users/mateusz/spring-framework/spring-core/src/main/java/org/springframework/core/", "Ordered.java")
for b in blame.blameList:
    print("Hash: " + b.hash + " | Path: " + b.path + " | Author: " + b.first_name + " " + b.last_name + " | Date: " + str(
        b.date) + " | Line nr: " + b.line_number + " | " + b.line)
