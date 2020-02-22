import argparse, sys, json

from config import default_configuration
from classes import *
#---------------- program arguments ----------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Speed up exam question")
    parser.add_argument("-i", "--infile", nargs='?', metavar='', type=argparse.FileType('r'), default=None, help="path to configuration file if provided")
    parser.add_argument("-o", "--outfile", nargs='?', metavar='', type=argparse.FileType('w+', encoding="UTF-8"), default=sys.stdout, help="path to output file if provided")
    parser.add_argument('-q', '--num_questions', metavar='', type=int, default=1, help='number of questions to generate at once. Default 1')
    return parser.parse_args(), parser



def main():
    args, parser = parse_arguments()

    s = speedUp(default_configuration)
    print(json.dumps(s.constructQuestions(), indent=4))

if __name__ == "__main__":
    main()
