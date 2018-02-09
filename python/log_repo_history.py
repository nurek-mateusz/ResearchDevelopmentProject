import git
import matplotlib
import matplotlib.pyplot as plt

class RepoHistory:
    def __init__(self, path):
        g = git.Git(path)
        result = g.execute(["git", "shortlog", "HEAD", "-s", "-n"])

        authors = result.split("\n")
        self.authorsDict = {}
        for a in authors:
            tmp = a.split("\t")
            self.authorsDict[tmp[1]] = tmp[0].strip()

    def get_authors_with_commits(self):
        return self.authorsDict


# repoHistory = RepoHistory("/Users/mateusz/spring-framework/")
# print(repoHistory.get_authors_with_commits())
# matplotlib.use('TkAgg')
# plt.plot([1,2,3], [1,2,3], 'ro')
# plt.show()
