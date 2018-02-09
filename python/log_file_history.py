import git

from commit import Commit


class FileHistory:

    def __init__(self, path, filename):
        g = git.Git(path)
        logs = g.log("--follow", "-p", "--", filename).split("\n")

        self.commits = []

        i = 0
        while i < len(logs):
            line = logs[i]
            commit = None
            if line.startswith("commit"):

                sha1 = line.split(" ")[1]

                i += 1
                author = logs[i].split("<")[0].split("Author: ")[1].strip()

                email = logs[i].split("<")[1]
                email = email[:len(email)-1].strip()

                i += 1
                date = logs[i].split("Date:   ")[1]

                next = True
                i += 1
                message = ""
                while next:
                    if logs[i].startswith("diff --git"):
                        next = False
                    elif logs[i]:
                        message += logs[i]
                    i += 1

                added = []
                deleted = []
                next2 = True

                while next2:
                    i += 1
                    if logs[i].startswith("@@"):
                        next = True
                        while next:
                            i += 1
                            if logs[i].startswith("+") and not logs[i].startswith("+++"):
                                added.append(logs[i])
                            elif logs[i].startswith("-") and not logs[i].startswith("---"):
                                deleted.append(logs[i])

                            if i + 1 >= len(logs) or logs[i + 1].startswith("commit"):
                                next = False
                            elif logs[i+1].startswith("@@"):
                                break

                    if i + 1 >= len(logs) or logs[i + 1].startswith("commit"):
                        next2 = False


                commit = Commit(author=author, email=email, date=date, sha1=sha1, message=message, addedLines=added, deletedLines=deleted)
                self.commits.append(commit)

            i += 1

    def get_all_commits(self):
        return self.commits

    def get_first_commit(self):
        return self.commits[-1]

    def get_last_commit(self):
        return self.commits[0]

    def get_all_authors(self):
        authors = set()
        for commit in self.commits:
            authors.add(commit.author)
        return authors

    def get_author_with_number_of_commits(self):
        authors = self.get_all_authors()
        authors_with_commits = {}
        for author in authors:
            commits_number = sum(c.author == author for c in self.commits)
            authors_with_commits[author] = commits_number
        return authors_with_commits

    def get_author_with_lines_changed(self, comments):
        authors = self.get_all_authors()
        authors_with_changes = {}
        for author in authors:
            lines_changed = 0
            for commit in self.commits:
                if author == commit.author:
                    addedLines = commit.addedLines
                    deletedLines = commit.deletedLines
                    if comments:
                        addedLines = self.remove_comments(commit.addedLines)
                        deletedLines = self.remove_comments(commit.deletedLines)
                    lines_changed += len(addedLines) + len(deletedLines)
            authors_with_changes[author] = lines_changed
        return authors_with_changes

    def remove_comments(self, lines):
            linesWithoutComments = []

            open_comment = False

            for i in range(len(lines)):
                tmp = lines[i][1:].strip()
                # if len(tmp) <= 1 or len(tmp) > 1 and tmp[:2] != "/*" and tmp[0] != "*":
                #     linesWithoutComments.append(lines[i])

                # line is //
                if tmp.find("//") == 0:
                    continue

                # line begin with /* and end with */
                if tmp.find("/*") == 0 and tmp.find("*/") == len(tmp) - 2:
                    continue

                if tmp.find("/*") > -1 and tmp.find("*/") == -1:
                    open_comment = True

                if tmp.find("/*") == 0:
                    continue

                if open_comment and tmp.find("/*") == -1 and tmp.find("*/") == -1:
                    continue

                if open_comment and tmp.find("*/") == len(tmp) - 2:
                    open_comment = False
                    continue

                linesWithoutComments.append(lines[i])

            return linesWithoutComments


# path = "/Users/mateusz/spring-framework/spring-core/src/main/java/org/springframework/core"
# filename = "Ordered.java"
# filename = "ReactiveTypeDescriptor.java"
# filename = "LocalVariableTableParameterNameDiscoverer.java"
#
# file_history = FileHistory(path, filename)

# print(file_history.get_author_with_number_of_commits())
#
# print(file_history.get_author_with_lines_changed(comments=False))
#
# print(file_history.get_author_with_lines_changed(comments=True))

# g = git.Git(path)
# logs = g.log("--follow", "-p", "--", filename).split("\n")
# print(logs)
# print(file_history.get_first_commit().author)
# print(file_history.get_first_commit().email)
# print(file_history.get_first_commit().date)
# print(file_history.get_first_commit().sha1)
# print(file_history.get_first_commit().message)
#
# print("\n")
#
# print(file_history.get_last_commit().author)
# print(file_history.get_last_commit().email)
# print(file_history.get_last_commit().date)
# print(file_history.get_last_commit().sha1)
# print(file_history.get_last_commit().message)
#
# print("\n")
#
# print(file_history.get_all_authors())
#

# path = "/Users/mateusz/Desktop/tmp"
# filename = "file1.java"
# file_history = FileHistory(path, filename)
# print(file_history.get_author_with_number_of_commits())
# print(file_history.get_author_with_lines_changed(comments=False))
# print(file_history.get_author_with_lines_changed(comments=True))
# print(file_history.get_all_authors())