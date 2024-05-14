import os
import sys

from pathlib import Path

from JSON import Parser

def main(filepath: str | os.PathLike):
    # Create an instance of the Parser class
    parser = Parser()    
    # Open the file using the path package
    with open(filepath) as data:
        # Parse file into a useful format (i.e. dict for JSON/CSV)
        parsed = parser.parse(data)
    pass

if __name__ == '__main__':
    args = sys.argv
    print(args)
    main(args[1])
