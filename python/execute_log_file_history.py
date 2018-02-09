import sys

from log_file_history import FileHistory

path = sys.argv[1]
filename = sys.argv[2]

file_history = FileHistory(path, filename)
print(file_history.get_author_with_number_of_commits())
print(file_history.get_author_with_lines_changed(comments=False))
print(file_history.get_author_with_lines_changed(comments=True))
print(file_history.get_all_authors())