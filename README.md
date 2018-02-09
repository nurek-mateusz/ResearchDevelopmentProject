# PBR17c
Research & Development Project in Software Engineering

---

# Assigning Developers To Bugs Based On Error Stack Trace Using Issue Tracker and Version Control System

Bug assignment is hard and troublesome process, but at the same time very frequent and important. 
Automated solution could save time, increase assignment accuracy and increase team velocity.
This project is aiming towards using _JIRA_ and _Git_ data to predict the best developer to fix the issue, given some application stack trace. 

This repository will contains all scripts, applications and tutorials required to recreate research.

## Installation

Our tool works with Windows, MacOS and Linux.

### Python

This project uses `virtualenv` as well as `pipenv` to isolate workspace from other python environments.
Download and install Python 3.x from [this site](https://www.python.org/downloads/). 

#### Virtualenv

You can use `virtualenv` to isolate this application from other python environments on your computer.
The only thing you have to do is create new environment and activate it (don't worry, you can deactivate that at any time).

1. Install `virtualenv` using [this guide](https://virtualenv.pypa.io/en/stable/installation/)
2. Activate `virtualenv` by using appropriate `activate` script. On Windows that would be `cmd` or `ps1`, for  Posix systems it's enough to run `source bin/activate` from your `virtualenv` directory. [Here](https://virtualenv.pypa.io/en/stable/userguide/#usage) is more in depth guide.

After activating `virtualenv` proceed to installation as normal. Check next section for a guide.

#### Pipenv

This repository manages python libraries with `pipenv` package manager.
1. First you will of course need to install `pipenv` itself, this can be easily done with `pip`.
See [this](https://github.com/pypa/pipenv/blob/master/docs/install.rst) guide.
2. Run `pipenv install` inside *python\\* directory (where `Pipfile` is located).

>In case you have problems with `pipenv` not being recognized by shell (**especially on Windows**) check [this installation guide again](https://github.com/pypa/pipenv/blob/master/docs/install.rst#-installing-pipenv), and make sure you have python scripts folder in your `Path` environment variable.

## Use

In python/git_stacktrace/scripts we have some scripts with examples. We can use this scripts as template. In the script we set path to the stacktrace-predictor, file with stacktrace, range of commits and url to jira. We must copy the script to the repository and run it.

## Technology Stack

- Python

## Repositories of examples
- [WSO2 Carbon Multitenancy](https://github.com/wso2/carbon-multitenancy)
- [Spring Framework](https://github.com/spring-projects/spring-framework)
- [Hibernate ORM](https://github.com/hibernate/hibernate-orm)
- [Sonatype Nexus](https://github.com/sonatype/nexus-public)

## References

Python - [https://www.python.org/downloads/](https://www.python.org/downloads/)  
Virtualenv - [https://virtualenv.pypa.io/en/stable/](https://virtualenv.pypa.io/en/stable/)  
Pipenv - [https://docs.pipenv.org/](https://docs.pipenv.org/)  
