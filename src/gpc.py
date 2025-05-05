
from sly import Lexer
from sly import Parser

def convert_instruction_to_opcode(instruction):
    if instruction == "STOPPEN":
        return 0x00
    elif instruction == "BEWAAR_STATUS":
        return 0x01

    return -1  # Return -1 if the instruction is not recognized

class GPCLexer(Lexer):
    tokens = { INSTRUCTION, NUMBER, STRING, SEPARATOR, EQUALS, LPAREN, RPAREN, SEMICOLON }
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Define the tokens
    INSTRUCTION = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING      = r'"([^"\\]|\\.)*"'

    # Define the operators
    EQUALS  = r'='
    SEPARATOR  = r','
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

    @_('INSTRUCTION ARGUMENTS SEMICOLON')  ## Simple statement ()
    def statement(self, p):
        # Convert the instruction to opcode and return it
        code = convert_instruction_to_opcode(p.INSTRUCTION)
        if code == -1:
            raise ValueError(f"Unknown instruction: {p.INSTRUCTION}")
        return { 'instruction': code }

    @_('INSTRUCTION SEMICOLON')  ## Simple statement (no arguments)
    def statement(self, p):
        # Convert the instruction to opcode and return it
        code = convert_instruction_to_opcode(p.INSTRUCTION)
        if code == -1:
            raise ValueError(f"Unknown instruction: {p.INSTRUCTION}")
        return { 'instruction': code }

    @_('LPAREN ARGUMENT RPAREN')
    def ARGUMENTS(self, p):
        return { 'arguments': p.ARGUMENT }

    @_('LPAREN ARGUMENT SEPARATOR ARGUMENT RPAREN')
    def ARGUMENTS(self, p):
        return { 'arguments': { p.ARGUMENT[0], p.ARGUMENT[1] }}

    @_('STRING EQUALS NUMBER')
    def ARGUMENT(self, p):
        return { 'string': p.STRING, 'number': p.NUMBER }