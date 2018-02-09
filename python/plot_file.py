import matplotlib.pyplot as plt

from log_file_history import FileHistory


class PlotFile:
    @staticmethod
    def plot(path, filename):
        file_history = FileHistory(path, filename)

        lines = file_history.get_author_with_lines_changed(True)

        commits = file_history.get_author_with_number_of_commits()

        lines_list = []
        print(lines)
        for l in lines:
            lines_list.append(lines[l])

        commits_list = []
        print(commits)
        for c in commits:
            commits_list.append(commits[c])

        plt.plot(commits_list, lines_list, 'ro')
        plt.show()


# path = "/Users/mateusz/spring-framework/spring-core/src/main/java/org/springframework/core"
# filename = "OverridingClassLoader.java"
# filename = "ResolvableType.java"
# filename = "SmartClassLoader.java"
# filename = "Ordered.java"

# PlotFile.plot(path, filename)
