import argparse, sys, json

from config import default_configuration
from config import update_default_config
from classes import *
from util import printErr
#---------------- program arguments ----------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Speed up exam question")

    parser.add_argument("-i", "--infile", nargs='?', metavar='', \
        type=argparse.FileType('r', encoding="UTF-8"), \
            default=None, help="path to configuration file (JSON only) if provided")

    parser.add_argument("-o", "--outfile", nargs='?', metavar='', \
        type=argparse.FileType('w+', encoding="UTF-8"), \
            default=sys.stdout, help="path to output file if provided")

    parser.add_argument('-q', '--num_questions', nargs='?', metavar='', \
        type=int, default=1, help='number of questions to generate at once. Default 1')

    return parser.parse_args(), parser

# Equivalent to Main without the argparse
def run(config):
    s = speedUp(config)
    print(json.dumps(s.constructQuestions(), indent=4))

# The main method
def main():
    args, parser = parse_arguments()

    config = default_configuration

    # Process command line arguments firsts
    config["num_questions"] = args.num_questions

    # Input config file may overwrite commandline args
    if args.infile is not None:
        try:
            inputConfig = json.load(args.infile)
            config = update_default_config(inputConfig)
        except json.JSONDecodeError:
            # Error goes to stderr
            printErr("Error parsing config file")
        
    s = speedUp(config)
    print(json.dumps(s.constructQuestions(), indent=4), file=args.outfile)

if __name__ == "__main__":
    main()
