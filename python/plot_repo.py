import math

import matplotlib.pyplot as plt

from log_repo_history import RepoHistory


class PlotRepo:
    @staticmethod
    def plot(path, bins=None):
        repo_history = RepoHistory(path)
        authors_dict = repo_history.get_authors_with_commits()
        x = []
        for a in authors_dict:
            x.append(int(authors_dict[a]))
        print(len(x))
        print(int(math.sqrt(len(x))))

        if bins:
            plt.hist(x, normed=True, histtype='stepfilled', bins=bins)
        else:
            plt.hist(x, normed=True, histtype='stepfilled', bins=int(math.sqrt(len(x))))

        plt.show()


# PlotRepo.plot("/Users/mateusz/spring-framework/", bins=100)