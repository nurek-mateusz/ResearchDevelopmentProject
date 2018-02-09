import sys
from plot_file import PlotFile

path = sys.argv[1]
filename = sys.argv[2]

PlotFile.plot(path, filename)
