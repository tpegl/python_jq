from path import path, Pathlike

from JSON import Parser

def main(filepath: str | Pathlike):
    # Create an instance of the Parser class
    parser = Parser()    
    # Open the file using the path package
    with open('./data/64KB.json') as data:
        # Parse file into a useful format (i.e. dict for JSON/CSV)
        parsed = Parser.parse(data)
    pass

if __name__ == '__main__':
    main()
