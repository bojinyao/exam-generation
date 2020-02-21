# Exam Generation Design Guide

A general reference guide for creating exam generation projects

## Table of Contents

- [Exam Generation Design Guide](#exam-generation-design-guide)
  - [Table of Contents](#table-of-contents)
  - [Software](#software)
    - [Main Software](#main-software)
    - [Other Software](#other-software)
  - [Project Structure](#project-structure)
    - [Python Modules](#python-modules)
      - [Python Modules Quick Tutorial](#python-modules-quick-tutorial)
      - [Optional](#optional)
        - [Step 1](#step-1)
        - [Step 2](#step-2)
    - [Packages](#packages)
    - [Docs](#docs)
    - [README Markdown File](#readme-markdown-file)
  - [Project Arguments](#project-arguments)
    - [Flags](#flags)
    - [Configuration File](#configuration-file)
  - [Output Rules](#output-rules)
    - [JSON Output Format](#json-output-format)

## Software

### Main Software

- Python 3.6+

For all projects, we are going to default to `python 3.6.0` and above. If you do not have the up-to-date python version, you can update your python using homebrew (<https://brew.sh/>) or through Anaconda (<https://www.anaconda.com/>).

Note: it is recommended to get your python through homebrew because it will be placed directly in your `/usr/local/bin/` directory, for Mac systems, which will not cause trouble when your MacOS is updated.

To check what python version you have, you can do:

```shell
python3 --version
```

if you're not sure if you have python3 installed, do:

```shell
python --version
```

### Other Software

There is no strict restriction on other software to stay compatible with everyone else; however, if you're using other kind(s) of software, please make sure to checkout [Project Structure --> Packages](#packages) for more detailed directions.

## Project Structure

Since this project is written by students, we need to anticipate real events such as graduation, that would result in the loss of the code creator. As such, we're choosing possibly the easiest way to keep everyone's code relevant, with nearly zero maintenance, that will ensure the survival of each individual's work in case of any unexpected leave. Consequently, this will hopefully ensure the longevity of the overall endeavor. The way we're going to organize everyone's project is through python modules ([below](#python-modules))

### Python Modules

If you haven't heard of python modules please check it out real quick (<https://docs.python.org/3/tutorial/modules.html>).

In summary, python modules is the go-to for building large python projects. As the name implies, we can modularize each individual's project and easily integrate everyone's code together when we need to. There are also some added benefits of flexibility, and general compatibility which might come in handy down the road.

#### Python Modules Quick Tutorial

Let's say you're working on a project inside `midterm-q1/` directory, and you'd like to convert your project into a python module. There are a few things you need to do. 

First of all, create an empty file called `__init__.py` at the top level of your directory. This file tells the python interpreter that this directory is meant to be a python module. For an additional functionality, please place your main script inside another file called `__main__.py`, and within your `__main__.py`, at the very bottom of the file, place the following block of code:

```python
if __name__ == "__main__":
    main()
```

Lastly, you will need to place the main logic (entry point) within a function called `main()` somewhere above the code block.

Your project structure might look like:

```shell
midterm-q1/
            __init__.py
            some_stuff.py
            __main__.py
            packages/       # checkout #Packages
            docs/           # checkout #Docs
            .git            # created by git
```

And inside your `__main__.py`, the code might look like:

```python=1
def main():
    parseFlags()
    doSomeStuff()
    outputJSON()

def parseFlags():
    ...

def doSomeStuff():
    ...

def outputJSON():
    ...

if __name__ == "__main__":
    main()

```

Having the `__main__.py` clearly defines your program entry point. As a result, your program, e.g. `midterm-q1` is directly callable like:

```shell
python3 midterm-q1
```

This way, future maintainers do not even need to open up your code and dig through project directory in order to use your code. To make your code more programmer-friendly, checkout [Flags](#flags).

#### Optional

In an attempt to future-proof the durability of your code, you can turn your `__main__.py` into an executable in Linux based systems by:

##### Step 1

Add a python path to top of your `__main__.py`. On my computer, after downloading python 3.7+ using homebrew, my python3 path is: `/usr/local/bin/python3` . So, at the top of my `__main__.py` I can add: `#!/usr/local/bin/python3` . You can find out the path to your python by doing:

```shell
which python3
```

Then just paste the path to the top of `__main__.py` like:

```shell=1
#!<path>
```

##### Step 2

Once you've modified the top of your `__main__.py`, you need to turn the file itself into an executable. To do it, navigate to the directory where your `__main__.py` lives, then do:

```shell
chmod +x __main__.py
```

doing this will give execution privileges to anyone with a copy of your file, and they will be able to execute your `__main__.py` like:

```shell
./__main__.py
```

without calling `python3` for example.


### Packages

### Docs

### README Markdown File

## Project Arguments

### Flags

### Configuration File

## Output Rules

### JSON Output Format
