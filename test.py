import argparse

parser = argparse.ArgumentParser(description='Params for group')

parser.add_argument("-g", "--group", help="Prints number your group.", default=14)

args = parser.parse_args()

print(int(args.group))