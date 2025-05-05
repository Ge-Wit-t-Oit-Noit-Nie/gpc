from lark import Lark, Transformer

# Define the instruction mapping
INSTRUCTION_MAP = {
    "BEGIN_EINDE_PROGRAMMA_INDEX": 1,
    "WACHTEN": 2,
    "ZET_PORT_AAN": 3,
    "ZET_PORT_UIT": 4,
    "FLIP_POORT": 5,
    "BEWAAR_STATUS": 6,
    "SPRING": 7,
    "STOPPEN": 8
}

# Define the transformer
class InstructionTransformer(Transformer):
    def instruction(self, args):
        name = args[0].value  # Extract instruction name
        instr_num = INSTRUCTION_MAP.get(name, 99)  # Default unknown instruction to 99
        params = []
        
        if len(args) > 1:  # Ensure parameters exist
            for param in args[1:]:
                if len(param.children) >= 1:  # Check if parameter has both key and value
                    for param in param.children[0:]:
                        param_name = param.children[0].value  # Correctly extract value
                        param_value = param.children[1].value  # Correctly extract value
                        params.append((param_name, param_value))  # Append the value to params
        
        return [instr_num] + params  # Combine instruction number and parameters

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
        sourcecode = f.read()

    # Create the parser
    parser = Lark.open("gpc.lark", rel_to=__file__, parser="lalr" ) #Lark(grammar, start="start", parser="lalr")
    tree = parser.parse(sourcecode)
    print(tree.pretty())  # Print the parse tree for debugging
    parsed_data = [InstructionTransformer().transform(instr) for instr in tree.children]
    print(parsed_data)

