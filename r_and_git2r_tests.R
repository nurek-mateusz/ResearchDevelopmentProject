# get all java files from repo 
allFiles = list.files(path = "/Users/mateusz/spring-framework/spring-core", recursive = TRUE, include.dirs = FALSE, pattern = ".+\\.java")

# git2r blame
repo <- repository('/Users/mateusz/spring-framework')

blameList = list()

for(file in allFiles) {
  tmp = blame(repo, paste("spring-core/", file, sep = ""))
  blameList = c(blameList, tmp)
}

# calling git commands from R
system("cd /Users/mateusz/spring-framework; git log", intern = TRUE)