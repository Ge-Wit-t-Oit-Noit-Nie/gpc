from lark import Lark, Transformer

# Define the instruction mapping
INSTRUCTION_MAP = {
    "STOPPEN": 0,
    "BEGIN_EINDE_PROGRAMMA_INDEX": 1,
    "WACHTEN": 2,
    "ZET_PORT_AAN": 3,
    "ZET_PORT_UIT": 4,
    "FLIP_POORT": 5,
    "BEWAAR_STATUS": 6,
    "SPRING": 7
}

def to_number(value):
    """Convert a number to its integer value."""

    if value.startswith("0b"):
        return int(value, 2)  # Convert binary string to int
    elif value.startswith("0o"):
        return int(value, 8)  # Convert octal string to int
    elif value.startswith("0d"):
        return int(value, 10)  # Convert decimal string to int
    elif value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)  # Convert hex string to int
    elif value.isdigit():
        return int(value)  # Convert decimal string to int
    else:
        raise ValueError(f"Invalid number: {value}")
    
# Define the transformer
class InstructionTransformer(Transformer):
    def param(self, args):
        print (f"Processing param: {args}")
        return {args[0].value.upper(): to_number(args[1].value)}  # Extract the value of the parameter

    def param_list(self, args):
        print (f"Processing param_list: {args}")
        param_list = {}
        for param in args:
            if isinstance(param, dict):
                param_list.update(param)
        return param_list

    def instruction(self, args):
        name = args[0].value  # Extract instruction name
        print (f"Processing instruction: {name}")

        if "STOPPEN" in name:
            return 0x0000

        elif "BEGIN_EINDE_PROGRAMMA_INDEX" in name:
            if len(args) > 1:
                params = args[1]            
            return 1 << 12 | (params.get('INDEX') & 0xFFF)

        elif "WACHTEN" in name:
            if len(args) > 1:
                params = args[1]
            return 2 << 12 | (params.get('DELAY') & 0xFFF)

        elif "ZET_PORT_AAN" in name:
            if len(args) > 1:
                params = args[1]

            return (3 << 12) | 0x0100 | (params.get('HSIO') << 9) | (params.get('PORTNR') & 0x001F)

        elif "ZET_PORT_UIT" in name:
            if len(args) > 1:
                params = args[1]

            return (4 << 12) | 0x0100 | (params.get('HSIO') << 9) | (params.get('PORTNR') & 0x001F)

        elif "FLIP_POORT" in name:
            if len(args) > 1:
                params = args[1]

            return (5 << 12) |  (params.get('HSIO') << 9) | (params.get('PORTNR') & 0x001F)

        elif "BEWAAR_STATUS" in name:
            if len(args) > 1:
                params = args[1]

            return (6 << 12)

        elif "SPRING" in name:
            if len(args) > 1:
                params = args[1]
            
            return 8 << 12 | (params.get('INDEX') & 0xFFF)  # SPRING instruction with index


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
        print(f"Error: Output file {args.output} already exists, so it will be overwritten")

    print(f"Converting '{args.input}' and saving to '{args.output}'")

    # open the input file and read the contents
    with open(args.input, "r") as f:
        sourcecode = f.read()

    # Create the parser
    parser = Lark.open("gpc.lark", rel_to=__file__, parser="lalr" ) #Lark(grammar, start="start", parser="lalr")
    tree = parser.parse(sourcecode)
    parsed_data = [InstructionTransformer().transform(instr) for instr in tree.children]

    #write the parsed data to the output file. Each instruction is 16 bits long
    with open(args.output, "wb") as f:
        for instruction in parsed_data:
            if isinstance(instruction, int):
                f.write(instruction.to_bytes(2, byteorder='big'))
            else:
                raise ValueError(f"Invalid instruction: {instruction}")
