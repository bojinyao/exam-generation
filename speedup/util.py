import sys

def printErr(msg):
    print(msg, file=sys.stderr)

# Used to geneate all valid choices and stored to computed_choices.py
def compute_all_choices(path):
    fp = open(path, 'w')
    valid_choices = [i for i in range(1, 101) if int(100/i) == 100/i]
    fp.write(str(valid_choices))
