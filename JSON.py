import re
import time
import sys

from enum import Enum


class Symbols(Enum):
    '''
    These are the accepted symbols in JSON. We'll use these to find/split
    segments of the string into Tokens
    '''
    OPEN_BRACE    = "{"
    CLOSE_BRACE   = "}"
    OPEN_BRACKET  = "["
    CLOSE_BRACKET = "]"
    COMMA         = ","
    COLON         = ":"


class Token:
    def __init__(self, token_type: str, value: str | int | bool):
        self.token_type = token_type
        self.value = value

    def __dict__(self):
        return {"token_type": self.token_type, "value": self.value}

    def __str__(self):
        return f'[{self.token_type}] {self.value}'


class Parser:
    def __init__(self):
        # We'll use this to set up some properties on the class
        # (apparently called Class Variables in Python but that
        # sounds terrible so we're not doing that)
        self.tokens: [Token] = []
        self.counter = 0

    def advance(self):
        token = self.tokens[self.counter]
        self.counter += 1
        return token

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
        # a closing bracket but later, we'll need to account for
        # missing/incorrect data.
        start = time.time()

        self.tokens = self.tokenize(data)

        end = time.time()
        print(f'Took {end - start} seconds')

        print(f'There are {len(self.tokens)} tokens')

        if len(self.tokens) == 0:
            print('No tokens could be found. Exiting')
            sys.exit()

        while self.counter < len(self.tokens):
            token = self.advance()
            node = self.parse_token(token)
            print(node)

    def parse_token(self, token: Token):
        value = token.value
        token_type = token.token_type
        match token_type:
            case "String":
                return {"type": token_type, "value": str(value)}
            case "Number":
                if "." in value:
                    return {"type": token_type, "value": float(value)}
                else:
                    return {"type": token_type, "value": int(value)}
            case "True":
                return {"type": "Boolean", "value": True}
            case "False":
                return {"type": "Boolean", "value": False}
            case "Null":
                return {"type": "Null", "value": None}
            case "BraceOpen":
                return self.parse_object(value)
            case "BracketOpen":
                return self.parse_array(value)
            case _:
                raise ValueError("Got a Token.token_type that was unexpected. Exiting")

    def parse_object(self, obj) -> {}:
        node = {"type": "Object", "value": {}}
        print("Starting to parse object", obj)
        token = self.advance()

        while token.token_type != "BraceClose":
            print(token)
            if token.token_type == "String":
                key = token.value
                token = self.advance()
                print("Token before Colon check", token)
                if token.token_type != "Colon":
                    raise ValueError("Expected : in key-value pair")
                token = self.advance()
                print("Token after Colon check", token)
                value = self.parse_token(token)
                node["value"][key] = value
            else:
                raise ValueError(f"Expected String key in object. Token type {token.token_type}")
            token = self.advance()
            print('Final token before Comma check', token)
            if token.token_type == "Comma":
                token = self.advance()
            print('Final final token', token, '\n')
        return node

    def parse_array(self, array):
        node = {"type": "Array", "value": []}
        token = self.advance()

        while token.token_type != "BracketClose":
            value = self.parse_token(token)
            node["value"].append(value)

            token = self.advance()
            if token.token_type == "Comma":
                token = self.advance()

        return node

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
        non_char_pattern = re.compile(r'[\d\w|\d+\.]')
        whitespace_pattern = re.compile(r'\s')

        print(f'Processing data of length {len(data)}')

        # Store the Tokens we find for later processing
        tokens = []

        # While our current character isn't the end of the string
        while current < len(data):
            # Get the current char
            char = data[current]

            # match statement to check for accepted symbols and strings
            match char:
                case Symbols.OPEN_BRACE.value:
                    tokens.append(Token("BraceOpen", char))
                    current += 1
                    continue
                case Symbols.CLOSE_BRACE.value:
                    tokens.append(Token("BraceClose", char))
                    current += 1
                    continue
                case Symbols.OPEN_BRACKET.value:
                    tokens.append(Token("BracketOpen", char))
                    current += 1
                    continue
                case Symbols.CLOSE_BRACKET.value:
                    tokens.append(Token("BracketClose", char))
                    current += 1
                    continue
                case Symbols.COMMA.value:
                    tokens.append(Token("Comma", char))
                    current += 1
                    continue
                case Symbols.COLON.value:
                    tokens.append(Token("Colon", char))
                    current += 1
                    continue
                case '"':
                    string = self.get_full_string(data, current + 1)
                    if string:
                        tokens.append(Token("String", string))
                        current += (len(string) + 2)
                        continue
                    else:
                        raise ValueError(
                            "JSON string found with no closing \" char"
                        )

            if non_char_pattern.match(char):
                value = ''
                while non_char_pattern.match(char):
                    value += char
                    current += 1
                    char = data[current]

                # If the char doesn't match the accepted symbols and isn't
                # a string, check if it's an int, float, null or boolean
                if value.isnumeric():
                    tokens.append(Token("Number", value))
                elif value == 'null':
                    tokens.append(Token("Null", value))
                elif value == 'true':
                    tokens.append(Token("True", value))
                elif value == 'false':
                    tokens.append(Token("False", value))
                elif '.' in value:
                    tokens.append(Token("Number", value))
                else:
                    raise ValueError(f"Unexpected value: {value}")

            # If it's whitespace, ignore and move on
            if whitespace_pattern.match(char):
                current += 1
                continue

        return tokens
