import re

from enum import Enum


class Symbols(Enum):
    OPEN_BRACE    = "{"
    CLOSE_BRACE   = "}"
    OPEN_BRACKET  = "["
    CLOSE_BRACKET = "]"
    COMMA         = ","
    COLON         = ":"

class Token:
    def __init__(self, token_type: str, value: str | int | bool):
        self.type = token_type
        self.value = value


class Parser:
    def __init__(self):
        # We'll use this to set up some properties on the class 
        # (apparently called Class Variables in Python but that 
        # sounds terrible so we're not doing that)
        pass

    def parse(self, data: str):
        # This is the main function. We need to split out the data
        # into any logical sequences and construct how we want it 
        # to end up from that.
        #
        # data = "[{'user': {'id': 1, 'first_name': 'Chevette', 'last_name': 'Washington', 'address': 'The Bridge, San Francisco'}},]"
        #
        # To properly parse this we need to find the beginning of the 
        # the first object that contains the 'user', then inside that
        # we collect the 'user' object by getting the data inside of 
        # the {} brackets
        #
        # So, we need to establish some rules. How are "objects" constructed
        # in JSON? How can we find the bounds of those objects? Are there 
        # different types of objects that use different delimeters?
        #
        # more_data = "[{'object': {'names': ['Jeffrey', 'Billy', 'Samwise', 'Marshal']}}]"
        #
        # So for the above we need to check for other brackets as well []. 
        # Clearly these two are different things. {} denotes an object, []
        # is for an array/list so we can collect/look for both.
        #
        # For now, we assume the data is correct. Each opening bracket has 
        # a closing bracket but later, we'll need to account for missing/incorrect
        # data.
        tokens = self.tokenize(data)
        print(f'There are {len(tokens)} tokens')
        for token in tokens:
            print(token.type, token.value)

    def get_full_string(self, data: str, start: int):
        idx = data[start:].find('"')
        if idx != -1:
            return data[start:start+idx]
        return None

    def tokenize(self, data: str) -> []:
        # If the opening char isn't a valid opening char, exit
        if data[0] not in [Symbols.OPEN_BRACKET.value, Symbols.OPEN_BRACE.value]:
            print('Not valid JSON. Womp womp.')
            return

        print('We got valid JSON baybeeeeee!')

        current = 0
        # Compile some ReGex for finding ints, floats, booleans and numbers as well as whitespace
        non_char_pattern = re.compile(r'[\d\w]')
        whitespace_pattern = re.compile(r'\s')

        print(f'Processing data of length {len(data)}')

        # Store the Tokens we find for later processing
        tokens = []

        # While our current character isn't the end of the string
        while current < len(data):
            # Get the current char
            char = data[current]

            # match statement to check against the accepted symbols and for strings
            match char:
                case Symbols.OPEN_BRACE.value:
                    tokens.append(Token("BraceOpen", char))
                case Symbols.CLOSE_BRACE.value:
                    tokens.append(Token("BraceClose", char))
                case  Symbols.OPEN_BRACKET.value:
                    tokens.append(Token("BracketOpen", char))
                case Symbols.CLOSE_BRACKET.value:
                    tokens.append(Token("BracketClose", char))
                case Symbols.COMMA.value:
                    tokens.append(Token("Comma", char))
                case Symbols.COLON.value:
                    tokens.append(Token("Colon", char))
                case '"':
                    string = self.get_full_string(data, current + 1)
                    if string:
                        tokens.append(Token("String", string))
                        current += (len(string) + 2)
                        continue
                    else:
                        raise ValueError(
                            f"JSON string found with no corresponding closing \" char"
                        )

            # If the char doesn't match the accepted symbols and isn't a string,
            # check if it's an int, float, null or boolean
            if non_char_pattern.match(char):
                if char.isnumeric():
                    tokens.append(Token("Number", char))
                elif char == 'null':
                    tokens.append(Token("Null", char))
                elif char == 'true':
                    tokens.append(Token("True", char))
                elif char == 'false':
                    tokens.append(Token("False", char))
                else:
                    raise ValueError(f"Unexpected value: {char}")

            # If it's whitespace, ignore and move on
            if whitespace_pattern.match(char):
                current += 1
                continue

            current += 1

        return tokens
