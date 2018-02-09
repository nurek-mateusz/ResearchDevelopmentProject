import sys
from plot_repo import PlotRepo

path = sys.argv[1]
bins = sys.argv[2]

PlotRepo.plot("/Users/mateusz/spring-framework/", int(bins))