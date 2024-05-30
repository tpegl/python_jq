import os
import sys

from JSON import Parser


def main(filepath: str | os.PathLike):
    # Create an instance of the Parser class
    parser = Parser()
    # Open the file using the path package
    with open(filepath) as f:
        # Parse file into a useful format (i.e. dict for JSON/CSV)
        data = f.read()
        parser.parse(data)


if __name__ == '__main__':
    args = sys.argv
    print(args)
    main(args[1])
