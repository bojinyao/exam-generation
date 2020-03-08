# Exam Generation Design Guide

A general reference guide for creating exam generation projects

## Table of Contents

- [Exam Generation Design Guide](#exam-generation-design-guide)
  - [Table of Contents](#table-of-contents)
  - [Change Log](#change-log)
  - [Software](#software)
    - [Main Software](#main-software)
    - [Other Software](#other-software)
  - [Project Structure](#project-structure)
    - [Python Modules](#python-modules)
      - [Python Modules Quick Tutorial](#python-modules-quick-tutorial)
      - [run(config)](#runconfig)
        - [project directory](#project-directory)
      - [Optional](#optional)
        - [Step 1](#step-1)
        - [Step 2](#step-2)
    - [Packages](#packages)
    - [Docs](#docs)
    - [README Markdown File](#readme-markdown-file)
    - [Assets](#assets)
  - [Program Arguments](#program-arguments)
    - [Arguments and Flags](#arguments-and-flags)
    - [Configuration File](#configuration-file)
    - [Default Argument(s)](#default-arguments)
  - [Error Reporting](#error-reporting)
  - [Output Rules](#output-rules)
    - [JSON Output Format](#json-output-format)
    - [JSON Output Example](#json-output-example)

## Change Log

[Change log in `docs/`](docs/changelog.md)

## Software

### Main Software

- Python 3.6+

For all projects, we are going to default to `python 3.6.0` and above. If you do not have the up-to-date python version, you can update your python using homebrew (<https://brew.sh/>) or through Anaconda (<https://www.anaconda.com/>).

Note: it is recommended to get your python through homebrew because it will be placed directly in your `/usr/local/bin/` directory, for Mac systems, which will not cause trouble when your OS is updated.

To check what python version you have, you can do:

```shell
python3 --version
```

if you're not sure if you have python3 installed, also try:

```shell
python --version
```

### Other Software

There is no strict restriction on other software to stay compatible with everyone else; however, if you're using other kind(s) of software, please make sure to checkout [Project Structure --> Packages](#packages) for more detailed directions.

## Project Structure

Since this project is written by students, we need to anticipate real events such as graduation, that would result in the loss of the code creator. As such, we're choosing hopefully the easiest way to keep everyone's code relevant, with nearly zero maintenance, that will ensure the survival of each individual's work in case of any unexpected leave. Consequently, this will hopefully ensure the longevity of the overall endeavor. We're going to organize everyone's project through python modules ([below](#python-modules))

### Python Modules

If you haven't heard of python modules please check it out real quick (<https://docs.python.org/3/tutorial/modules.html>).

In summary, python modules is the go-to for building large python projects. As the name implies, we can modularize each individual's project and easily integrate everyone's code together when we need to. There are also some added benefits of flexibility, and general compatibility which might come in handy far down the road.

#### Python Modules Quick Tutorial

Let's say you're working on a project inside `midterm-q1/` directory, and you'd like to convert your project into a python module. There are a few things you need to do.

First of all, create an empty file called `__init__.py` at the top level of your directory. This file tells the python interpreter that this directory is meant to be a python module. For an additional functionality, please place your main script inside another file called `__main__.py`, and within your `__main__.py`, at the very bottom of the file, place the following block of code:

```python
if __name__ == "__main__":
    main(...)
```

Lastly, you will need to place the main logic (entry point) within a function called `main()` somewhere above the code block.

#### run(config)

To provide a consistent API across all programs, you're required to define a python **function**, not method, with the signature `run(config : dict, *args, **kwargs) -> int`, where the **only** required input parameter is a dictionary, and **only** a dictionary will be passed to it when called outside of `"__main__"`. You should place this **function** inside your `__main__.py`

This function should return a `0` (zero) if no error ever occurred during its execution, and should return a none-zero, positive integer if anything went wrong. It is okay to simply return a `1` (one) to indicate that something went wrong. Optionally, you can return different numbers to indicate different types of error; however, what the none-zero number means should be outlined in your documentation!

This function will be called by default if your python module is imported like a library, and **only** a dictionary of your program's configurations will be passed to it. Your program do not have to use this function in its operations, but when this function is called, the program should function the same way!

- Why do we need this?
  - Consider `run(dict)` as the default entry point for someone calling your program as if it's a library. In normal programs, there is the familiar `main()`; however, you might want to use `main()` for your regular logical processes, so we're defaulting to a second common entry point `run(...)`.
  - Your `main()` might be doing some extra stuff like parsing command line options or printing to a console, importing and running `main()` will most likely crash the calling program too. As a result, with configurations (along will all other information your program possibly needs) as a single dictionary, `run(...)` function needs to execute without needing any additional inputs.

Regardless of whether your program is configurable at all, you have to have this function as an alternative entry point. And in the case there is no configuration for your program, an empty dictionary will be passed to it, and your function don't need to use that input. This function is going to be integral to integrating your program as part of the larger project!

Note: whenever you update `main()`, it is likely that you will need to update `run(...)` too, as a result, you either should be mindful of that fact, or simply use `run(...)` inside your `main()` as a good abstraction barrier that might also improve your code readability.

##### project directory

Your project directory might look like:

```shell
midterm-q1/
            __init__.py
            some_stuff.py
            __main__.py
            README.md       # your README
            packages/       # checkout #Packages
            docs/           # checkout #Docs
            .git            # created by git
            .gitignore      # you might need to create one
```

And inside your `__main__.py`, the code might look like:

```python=1
def run(config, *args, **kwargs):
    ...
    outputJSON()

def main(...):
    parseFlags()
    doSomeStuff()
    ...
    run(config)

def parseFlags():
    ...

def doSomeStuff():
    ...

def outputJSON():
    ...

if __name__ == "__main__":
    main(...)

```

Having the `__main__.py`, clearly defines your program's entry point. As a result, your program, e.g. `midterm-q1` is directly callable like:

```shell
python3 midterm-q1 <arguments>
```

This way, future maintainers do not even need to open up your code and dig through project directory in order to use your code. To make your code more programmer-friendly, checkout [Program Arguments](#program-arguments).

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

It is highly recommended that you search for existing libraries or packages that will solve your problem instead of reinventing every wheel. As a result, you might need to download some libraries that are not part of the standard python libraries.

When you do need to download packages, please put them inside a directory called `packages/`. This makes it easy for future maintainers to understand what code is downloaded, and they can perform updates if necessary. The downloaded packages will also enable your program to run off-line, and be resistant to package updates.

### Docs

Since this project is very distributed in personnel that consist of students, good documentation is key to enable others to properly use your program. For large programs, you might have multiple documentation files for different sections of your code, you should place these documentation files within a directory called `docs/` for easy future access.

Note: your `README.md` that is meant to explain your program should still be at the top level of your project directory (see [project directory](#project-directory)). Files within `docs/` are files like `help.txt`, `direction.txt`, etc.

### README Markdown File

You should write and actively maintain a file called `README.md` that appears at the front page of your github repository. Besides introducing your program, what it is, what it does, etc.

If you haven't seen files like this, or haven't used markdown before, no worries, it is not difficult to learn. For a quick summary, `README` is basically a file that a user to a program should read before proceeding to using the program. If you write your `README` in markdown, Github will automatically render it at the front page of your repository for others to see. And markdown is a simple popular markup language that lots of people have written tutorials and cheatsheets on. For example, the following link (<https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet>) is one of those cheatsheets.

**Your `README.md` should explain how to interact with your program!**

Consider your `README.md` as a user manual for your program. It should include all essential commands, flags and options that your program consumes. It is okay to leave out the nitty-gritty details that's not essential to using your program to directories like `docs/` ([above](#docs)). However, it is very important that your `README.md` covers everything from [Program Arguments](#program-arguments) that you did implement, including [default arguments](#default-arguments)!

If you have custom outputs, checkout [output rules](#output-rules), you should include these in the `README.md` as well. And if necessary, notify the group that works on parsing outputs so that your custom output will be integrated.

As a side note: we encourage you to write manuals like these and upload them to Github; instead of writing them in Google Doc for example. Reason being the ease of maintenance and version control. If you create a document like this and wish to share with others, what access privilege do you give others? If you do view only, what happens if someone updates your program and need to update the manual itself? If you do writable, what happens if someone accidentally deletes important content without realizing or anyone knowing? And linking Google Docs as manual is especially dangerous, consider if you graduate and you delete your Google Drive, the link to your user manual will be invalid, and no one will be able to use your program 🙁

### Assets

As a side note, if your project is rather complex and requires various data types, or even caches. It is recommended that you place your `packages/` directory ([above](#packages)) along with `docs/` directory ([above](#docs)) under a directory called `assets/`, this way, you don't clutter your top level directory with all kinds of stuff. For example, if you have pre-prepared images, your `assets/` directory might look like:

```shell
assets/
            packages/
            docs/
            images/
            miscellaneous/
```

## Program Arguments

Note: this entire section is optional, although, highly recommended! If you have any global variable in your code, you should have this! And as you read through this section, you will likely need to introduce certain global variables anyways.

Many programs take arguments to let users interact with the program in many different ways, and your program should too.

Some common ways to pass arguments to your program involve flags and configuration files. Below points have outlined both.

### Arguments and Flags

Flags refer to those dash (`-`) and english letter options you can pass to your program at startup. One example is your everyday `ls` like: `ls -a -l` or `ls -al` . In this example, `-a` and `-l` are flags that enable formatting of your `ls` program outputs. Arguments are those you can specify values instead of just turning something ON or OFF, like: `gcc -o example example.c` in this example, `-o` is the option, and `example` is the value.

You can make your program more dynamic and configurable through the use of arguments and flags.

To parse these arguments, python has a handful of standard libraries with nice APIs that you can import. One recommended parser is `argparse` and you can check it out here: (<https://docs.python.org/3/library/argparse.html>). It requires a bit of additional reading, but learning this will make your life much easier in the future. Additionally, many languages have powerful, built-in general purpose parsers like this one, learning one will make it easier to learn other parser in the future.

As a side note: it is worth the time to populate the description fields, as well as additional usage text so that when a user does `python3 <program name> -h` the help message might be enough to get the user started, instead of having to read through `README` on Github.

### Configuration File

Very often, your program might be able to consume so many different configuration options, where some options might have hierarchies, it'd be easier to also accept configuration file to configure your program. For the purpose of this project, we're asking everyone to use JSON (javascript object notation) format files for your configuration file. We understand JSON might not be your top choice for configuration file; however, JSON is easy to understand and readable, and we're also using the same format for program outputs (see [Output Rules](#output-rules)), it will be easier for others to adopt and start using your program sooner.

To add configuration file option, you can use an `argparse` as described [above](#arguments-and-flags) to automatically and safely find the figuration file using a path, then open it.

Additionally, if you do have configuration file, you should outline what the options are, what they do, and how they affect the program output **clearly** in your `README.md` file.

### Default Argument(s)

To make your program more user friendly, you should consider default arguments. Very often, a user simply wants to start using the program without reading through configuration rules. As a result, you should put some thoughts into what the default values should be for your configurations. This will also be helpful if someone decides to not pass any arguments, or giving your program an empty configuration file, **your program should not crash if no configuration is given.**

One of the ways to organize your configuration options is through a python dictionary or even a class. When you receive configuration(s), simply update corresponding `(key, value)` pairs. This way, default values should seem more natural and intuitive. Additionally, you will be able to pass this configuration to other classes or functions freely and succinctly.

## Error Reporting

It is likely that your program might need to report errors, either from illogical configuration, or exception during runtime, etc. Regardless of what the error is, or the cause of it, your program should not simply crash out! It is not unreasonable to fallback to the generic "catch-all" exception. You can also be more specific of the type of the exception your program might have, the point is to avoid crashing the calling program altogether.

In python3 it looks like:

```python
try:
    ...
except Exception as e:
    ... # handling the exception

    import sys
    print(f"your optional error message: {e}", file=sys.stderr)
```

Regardless how your program might handle the error itself, you should print/log to **standard error** instead of standard out.

NOTE: standard out is defaulted to default program outputs, e.g. your JSON outputs. As a result, pleases do NOT print to standard out if your program is not configured to output to an output file. This is to avoid conflict between regular JSON outputs and your program messages.

Optionally: if you have used some kind of a logger e.g. (<https://docs.python.org/3/howto/logging.html>) before, you *might* find it easier to use to handle debugging prints and error prints during development.

To recap, your `__main__.py` might now look like:

```python
def run(config, *args, **kwargs):
    try:
        ... # doing some parsing etc.
        ... # some additional logic etc.

        outputJSON()
        return 0
    except Exception as e:
        ... # handle the error

        import sys
        print(f"your optional error message: {e}", file=sys.stderr)
        return 1 # optionally, other >0 integer you might define

def main(...):
    parseFlags()
    doSomeStuff()
    ...
    run(config)

def parseFlags():
    ...

def doSomeStuff():
    ...

def outputJSON():
    ...

if __name__ == "__main__":
    main(...)

```

## Output Rules

To make your life easier, while creating a good abstraction barrier, we're going to ask you to create JSON outputs.

Why JSON outputs?

- JSON is a widely used and accepted form of output, many languages and systems and built-in support.
- If everyone writes their output as a JSON object, with some standardization, we can create one parser, that consumes every program's JSON output, and format nicely to HTML. This way, you don't have to deal with HTML, CSS, or JS formatting, and you don't have to do any work if some backend API changes.

---

**Information from here on is SUPER important! Make sure you understand what you're reading, and ask questions if anything is confusing to you!**

How to do JSON outputs?

Use python's default json library! Here are documentations and tutorial on how to use this library: (<https://docs.python.org/3/library/json.html>), (<https://www.w3schools.com/python/python_json.asp>)

```python
import json
```

- use `json.loads()` and `json.dumps()` to decode and encode your JSON objects. You can also use `json.load()` or `json.dump()` if you know what you're doing. You likely will not need to use `json.loads()` or `json.load()` since your program likely won't need to consume JSON.
- output your JSON to standard out *by default* ! Normally, you can just call `print(...)`.
  - you can output directly to some json file, like `output.json`, but this should only be enabled by argument or flag! Even then, your argument should take in a path, rather than simply writing to where the program is called <-- if this doesn't make sense to you, ask!
  - the idea behind this is to give calling program the right to name and decide on where and how to create the output file(s).
  - it is very easy for the calling program to capture/redirect your program's standard out.

>Note Keys in key/value pairs of JSON are always of the type `str`. When a dictionary is converted into JSON, all the keys of the dictionary are coerced to strings. As a result of this, if a dictionary is converted into JSON and then back into a dictionary, the dictionary may not equal the original one. That is, `loads(dumps(x)) != x` if `x` has non-string keys.

### JSON Output Format

Note: this section is prong to changes. We will make our best effort to inform you of any changes, and we will try our best to only add changes instead of modifying past decisions to reduce your code change.

- `"multiple_choice"` -> `list<obj>` : your program should be capable of generating more than 1 question at a time. Each question is represented as a JSON object, and all your questions are placed inside a list. Even if you only generate 1 question at a time, you should still place it inside a list.
- `"prompt"` -> `str` : the prompt of your question. You can add HTML formatting if you need to, we also support basic LaTex syntax. With HTML formatting, it is not recommended to have size related tags because it is a breach in abstraction. However, feel free to use `<strong>`, `<em>`, etc. tags. If within the same JSON object, your `"options"` contains more JSON objects, this prompt will be treated as a prolog to other sub-questions, and consequently, you shouldn't have any other `(key, val)` pairs besides this `"prompt"` and `"options"`.
- `"options"` -> `list<(str | obj)>` : a **ordered** list of either choice strings or JSON objects. Choice strings can include HTML or basic Latex formatting. JSON object can be another question, or something that has more `"options"` within a JSON object (this is recursive). You shouldn't have any other `(key, val)` pairs if this list contains JSON object(s).
- `"answers"` -> (`list<int>` | `int`) || (`list<str>` | `str`): possible answers to your prompt.
  - if your question type is `"multiple_choice"`, if this value is a list, the question will default to question type that's "select all that apply". If this value is an integer, the question type will be "select the right answer". The number is the index to `"options"`, basically indicating which choice(s) is correct. If you're creating a question type that has multiple correct answers, but there is only 1 correct answer, you should create a list with only 1 number in it.
  - if your question type is `"fill_in_blanks"`, your `"answers"` should always be *regular expression* string! The regular expression string have to be **Ruby regular expressions** (<https://www.rubyguides.com/2015/06/ruby-regex/>). Similar to `"multiple_choice"`, if you have multiple `<input>`s, this should be a list of regular expression strings, where each regular expression string corresponds to each `<input>` in the same order. If you only have 1 `<input>`, it is okay to just use a single regular expression string.
- `"images"` -> `list<obj>` : since we want to output everything to JSON, that includes images. We're using a list because JSON does not guarantee ordering of `(key, value)` pairs inside it's objects, and you might want your images ordered; luckily, it does preserve array/list ordering.
  - `"<title of an image>"` -> `str` : each image object only requires 1 `(key, value)` pair. The key will automatically be treated as caption/title of the image it corresponds to. The image itself has to be encoded as a string so that it can be stored within our JSON object. To convert any image to string and back, check out this link: (<https://www.programcreek.com/2013/09/convert-image-to-string-in-python/>). Essentially, you will be using the standard library `based64` (<https://docs.python.org/3/library/base64.html>). For consistency, **default encoding will be PNG images!**
  - `"type"` -> `str` : for display purposes, the calling program might need to know the type of image you have. If you have something other than PNG, you should add the image type extension here, without the dot.
- `<img src="<title/caption of an image>">`: if you want to display image(s) anywhere in your question, and as long as you have the `"images"` object storing the images within that question, you can use the familiar `<img>` html tag to indicate that you want to display an image; however, in the `src=` attribute, you should include ONLY the title of said image so that a given parser might understand which image you're referring to. You're welcome to set other attributes of the `<img>`, but **please refrain** from attributes like `size=`, `width=`, `height=` etc. because they'd violate the abstraction barrier.
- `"hints"` -> `list<str>` : in the spirit of autoquiz, we need to be able to provide hint(s) if a student were to select the wrong question. Your program should output theses hints along with your answers.
  - if your question type is `"multiple_choice"`, you should output a list (equal length to `"options"`) of strings. Your hint for this question type should be none-trivial (saying "not right" is not enough!), it should be helpful to the student. Please avoid long paragraphs for this one, a sentence or two is more than enough.
    - if the question is "select the correct answer", each corresponding wrong answer should have a hint on why that choice is incorrect. You can simply say "correct", or an empty string, for the correct choice (this is more of a place holder for easier indexing).
    - if the question is "select all that apply", if the choice should be selected, you should provide a hint for when the choice is NOT selected by a student; vice versa, if the choice should not be selected, you should provide a hint for when the choice IS selected by a student.
  - if your question type is `"fill_in_blanks"`, you should still provide a **list** of string(s) as a hint, where each hint corresponds to each `<input>` that a student would've answered incorrectly. In the case of a single `<input>`, this list will be of length 1. A useful hint would require some thought because it needs to generalize to infinitely answer. However, please keep your hint as short as possible.
- `"difficulty"` -> `int` : you should mark each question's difficulty on an integer scale of `1` - `5` (inclusive), where `1` being easiest, and `5` being most difficult.
- `"fill_in_blanks"` -> `list<obj>` : questions of type "fill in the blank". You should use `<input>` for place(s) where a single input is required. And if needed, you can chain multiple `<input>`s together to denote multiple required inputs. For example, a question might look like: "Abstraction includes both `<input>` and `<input>`", and the answer would be "generalization" and "detail removal". Although, questions that have long, word based answers are difficult to auto-grade in general...
- `<input>` : each one of these inside your `"prompt"` is considered a user input, basically a blank to be filled. You can have any number of these within a single `"prompt"`, and each one is considered a single input.

Term clarifications:

- "basic Latex": anything you can enclose using double `$$`. Since `$` also means "dollar", you must to enclose your mathematically expression with double `$$`. E.g. `$$\frac{dx}{dy} = \sum_{i=1}^n (3x^2 + 2x) \cdot x$$`
- "JSON object": a JSON object looks very much like a python dictionary, but all key, value is represented as strings.

### JSON Output Example

>If anything above or below seems confusing, or incorrect, you should message Max Yao directly on Slack

Below is an artificial example of a JSON output to give you a better idea of what the output might look like:

```json
{
    "multiple_choice": [
        {
            "prompt": "The following questions are algebra questions",
            "options": [
                {
                    "prompt":"<b>what</b> is $$1 + 1$$?",
                    "options": [
                        "equals to <b>2</b>",
                        "equals to <b>0</b>",
                        "equals to <b>1</b>"
                    ],
                    "hints": [
                        "correct",
                        "hint for if answer 0 is wrong",
                        "hint for if answer 1 is wrong"
                    ],
                    "answers": 0,
                    "difficulty": 1
                },
                {
                    "prompt":"<b>what</b> is $$3 \\cdot 4$$?",
                    "options": [
                        "3",
                        "4",
                        "12"
                    ],
                    "hints": [
                        "hint for if answer 3 is wrong",
                        "hint for if answer 4 is wrong",
                        "correct"
                    ],
                    "answers": 2,
                    "difficulty": 4
                }
            ]
        },
        {
            "prompt":"<em>Who's the best</em> Professor?",
            "options": [
                "Dan",
                "Denero",
                "Hug",
                "Hilfinger"
            ],
            "hints": [
                "hint for if Dan is not selected",
                "hint for if Denero is not selected",
                "hint for if Hug is not selected",
                "hint for if Hilfinger is not selected"
            ],
            "answers": [0, 1, 2, 3],
            "difficulty": 5
        },
        {
            "prompt":"<img src=\"an_image\">Corporate needs you to the find differences between these 2 pictures.",
            "options": [
                "<img src=\"first_image\">", "<img src=\"second_image\"", "None of these"
            ],
            "hints": [
                "hint for if image 1 is not selected",
                "hint for if image 2 is selected",
                "hint for if third option is selected"
            ],
            "answers": [1],
            "difficulty": 2,
            "images": [
                {
                    "an_image": "<encoded PNG image string>"
                },
                {
                    "first_image": "<encoded PNG image string>"
                },
                {
                    "type":"jpg",
                    "second_image": "<encoded JPG image string>",
                }
            ]
        }
    ],


    "fill_in_blanks": [
        {
            "prompt": "Name a traffic light color: <input>",
            "answers": "^(?i)(green|yellow|red)$",
            "hints": ["A useful string when input #1 answer is wrong"],
            "difficulty": 3
        },
        {
            "prompt": "Let's do sub questions within each sub question",
            "options": [
                {
                    "prompt": "This could be part a)",
                    "options": [
                        {
                            "prompt": "This is part i. of part a) <input>, <input>",
                            "answers": [
                                "^[\\w]$",
                                "\\d"
                                ],
                            "hints": [
                                "A useful string when input #1 answer is wrong",
                                "A useful string when input #2 answer is wrong"
                            ],
                            "difficulty": 2
                        }
                    ]
                },
                {
                    "prompt": "part b) has no <input> sub parts, but has images",
                    "answers": "\\d",
                    "hints": ["A useful string when input #1 answer is wrong"],
                    "difficulty": 3,
                    "images": [
                        {
                            "a cool image": "<encoded PNG image string>"
                        },
                        {
                            "type":"jpg",
                            "another cool image": "<encoded JPG image string>",
                        }
                    ]
                }
            ]
        }
    ]
}

```
