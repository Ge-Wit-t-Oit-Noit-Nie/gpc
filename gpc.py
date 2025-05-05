
from sly import Lexer
from sly import Parser

def convert_instruction_to_opcode(instruction):
    if instruction == "STOPPEN":
        return 0x00
    elif instruction == "BEWAAR_STATUS":
        return 0x01

    return -1  # Return -1 if the instruction is not recognized

class GPCLexer(Lexer):
    tokens = { INSTRUCTION, NUMBER, STRING, EQUALS, LPAREN, RPAREN, SEMICOLON }
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Define the tokens
    INSTRUCTION = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING      = r'"([^"\\]|\\.)*"'

    # Define the operators
    EQUALS  = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'
    SEMICOLON = r';'

    # Number token 
    @_(r'0x[0-9a-fA-F]+',r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        else:
            t.value = int(t.value)
        return t

    # Comment token 
    @_(r'//.*') 
    def COMMENT(self, t): 
        pass

class GPCParser(Parser):
    tokens = GPCLexer.tokens

    def _init_(self): 
        self.env = { } 

    @_('INSTRUCTION SEMICOLON')  ## Simple statement (no arguments)
    def statement(self, p):
        # Convert the instruction to opcode and return it
        code = convert_instruction_to_opcode(p.INSTRUCTION)
        if code == -1:
            raise ValueError(f"Unknown instruction: {p.INSTRUCTION}")
        return { 'instruction': code }

# Set main guard
if __name__ == "__main__":
    # Get the parameters from the command line
    import sys
    import os
    import argparse

    # Get the parameters from the command line
    # i(important) -i, --input: The input file to be processed
    # o(utput) -o, --output: The output file to be processed
    # v(erbose) -v, --verbose: The verbose level to be used

    parser = argparse.ArgumentParser(description="GPC - General Purpose Converter") 
    parser.add_argument("-i", "--input", type=str, required=True, help="The input file to be processed")
    parser.add_argument("-o", "--output", type=str, required=False, help="The output file to be created")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    if(args.input == None):
        print("Error: Input file is required")
        sys.exit(1)
    
    # If output is not specified, set it to the input file name with .bin extension
    if(args.output == None):
        args.output = os.path.splitext(args.input)[0] + ".bin"

    # Check if the input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} does not exist")
        sys.exit(1)

    # Check if the output file exists
    if os.path.exists(args.output):
        print(f"Error: Output file {args.output} already exists")
        sys.exit(1)

    print(f"Converting '{args.input}' and saving to '{args.output}'")

    # open the input file and read the contents
    with open(args.input, "r") as f:
        data = f.readlines()

    data = [line.strip() for line in data if line.strip()]  # Remove empty lines and strip whitespace

    # Create the lexer and parser
    gpc_lexer = GPCLexer()
    gpc_parser = GPCParser()

    for line in data:
        # print the step if verbose is enabled
        if args.verbose:
            print(f"Processing line: {line}")
        gpc_parser.parse(gpc_lexer.tokenize(line))  # Parse the data