import sys

from blame_file import GitBlame

sys.argv[1] = "C:\\Users\\bider\\OneDrive\\Documents\\GitHub\\PBR17c\\repos\\spring-framework\\spring-core\\src\\main\\java\\org\\springframework\\core"
sys.argv[2] = "AttributeAccessor.java"

path = sys.argv[1]
filename = sys.argv[2]

blame = GitBlame(path, filename)
for b in blame.blameList:
    print("Hash: " + b.hash + " | Path: " + b.path + " | Author: " + b.first_name + " " + b.last_name + " | Date: " + str(
        b.date) + " | Line nr: " + b.line_number + " | " + b.line)