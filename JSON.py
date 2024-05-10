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
        pass
