from lark import Transformer

class Tokenizer(Transformer):
    # Entry point for the parse tree; returns the full list of parsed items
    def start(self, items):
        return items

    # Extracts a single statement from the list (either a function or a label)
    def statement(self, items):
        return items[0]

    # Transforms a function call into a dictionary with its name and parameters
    def function_call(self, items):
        name = str(items[0])
        params = items[1] if len(items) > 1 else []
        return {"type": "function", "name": name, "params": params}

    # Returns the list of parameters as-is
    def param_list(self, items):
        return items

    # Converts a parameter into a (name, value) tuple
    def param(self, items):
        return (str(items[0]), items[1])

    # Transforms a label into a dictionary with its name
    def label(self, items):
        return {"type": "label", "name": str(items[0])}

    # Converts a value token (hex or decimal) into an integer
    def value(self, items):
        val = items[0]
        if isinstance(val, str) and val.startswith("0x"):
            return int(val, 16)
        try:
            return int(val, 16)
        except:
            return str(val)
        
    # Converts a HEX_NUMBER token into a string
    def HEX_NUMBER(self, token):
        return str(token)

    # Converts a DEC_NUMBER token into a string
    def DEC_NUMBER(self, token):
        return str(token)

    # Converts a NAME token into a string
    def NAME(self, token):
        return str(token)
