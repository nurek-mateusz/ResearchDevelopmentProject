import matplotlib.pyplot as plt
import os

from log_file_history import FileHistory


class PlotDirectory:
    @staticmethod
    def absolute_file_paths(directory):
       for dirpath,_,filenames in os.walk(directory):
           for f in filenames:
               yield os.path.abspath(os.path.join(dirpath, f))

    @staticmethod
    def plot(path):
        gen = PlotDirectory.absolute_file_paths(path)

        commit_dict = {}
        line_dict = {}

        commit_list = []
        line_list = []

        for file in gen:
            (path, filename) = os.path.split(file)
            file_history = FileHistory(path, filename)

            commits = file_history.get_author_with_number_of_commits()
            for c in commits:
                if c in commit_dict:
                    commit_dict[c] = commit_dict[c] + commits[c]
                else:
                    commit_dict[c] = commits[c]

            lines = file_history.get_author_with_lines_changed(True)
            for l in lines:
                if l in line_dict:
                    line_dict[l] = line_dict[l] + lines[l]
                else:
                    line_dict[l] = lines[l]

        for c in commit_dict:
            commit_list.append(commit_dict[c])

        for l in line_dict:
            line_list.append(line_dict[l])

        print(commit_dict)
        print(line_dict)

        plt.plot(commit_list, line_list, 'ro')
        plt.show()


# PlotDirectory.plot("/Users/mateusz/spring-framework/spring-core/src/main/java/org/springframework/lang")
