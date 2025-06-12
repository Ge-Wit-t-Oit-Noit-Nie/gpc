#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GPC - Ge Wit 't Oit Noit Nie Program Converter

This program is a converter for the GPC (Ge Wit 't Oit Noit Nie) programming language.
It converts the GPC source code into a binary format that can be used by STM32 Firmware.
"""

from lark import Lark, Transformer, UnexpectedInput
from tokenizer import Tokenizer
from code_generator import generate_binary
import logging

__copyright__ = "Copyright 2025, Ge Wit 't Oit Noit Nie"
__license__ = "MIT"
__version__ = "1.0.1"

# Set main guard
if __name__ == "__main__":
    """Main function for the GPC converter.
    This function is used to parse the command line arguments and convert the GPC source code into a binary format.
    It uses the Lark parser to parse the GPC source code and the InstructionTransformer to transform the parse tree into a list of instructions.
    The output is written to a binary file that can be used by STM32 Firmware.

    Usage:
        python gpc.py -i <input_file> -o <output_file> -v
    where:
        -i, --input: The input file to be processed
        -o, --output: The output file to be created
        -v, --verbose: Enable verbose output

    Example:
        python gpc.py -i test.gpc -o test.bin -v
    """
    # Get the parameters from the command line
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(description="GPC - General Purpose Converter")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="The input file to be processed"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=False, help="The output file to be created"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    # Set the logging level based on the verbose flag
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    if args.input == None:
        logging.error(f"Error: Input file is required")
        sys.exit(1)

    # Check if the input file exists
    if not os.path.exists(args.input):
        logging.error(f"Error: Input file {args.input} does not exist")
        sys.exit(1)

    # If output is not specified, set it to the input file name with .bin extension
    if args.output == None:
        args.output = os.path.splitext(args.input)[0] + ".bin"
        logging.debug(f"Output file not specified, using default '{args.output}'")

    # Check if the output file exists
    if os.path.exists(args.output):
        print(
            f"Warning: Output file {args.output} already exists, so it will be overwritten"
        )

    print(f"Converting '{args.input}' and saving to '{args.output}'")

    # open the input file and read the contents
    with open(args.input, "r") as f:
        sourcecode = f.read()

    # Create the parser
    with open("src/gpc.lark", "r") as file:
        grammar = file.read()


    # Parse and handle errors
    try:
        parser = Lark(grammar, parser="lalr", transformer=Tokenizer())
        tokenized = parser.parse(sourcecode)

        for stmt in tokenized:
            logging.debug(f"token: '{stmt}'")

        generate_binary(tokenized, args.output)
        logging.debug("binary created")
    except UnexpectedInput as e:
        print("Syntax error detected:")
        print(e)

    # write the parsed data to the output file. Each instruction is 16 bits long
#    with open(args.output, "wb") as f:
#        for instruction in parsed_data:
#            if isinstance(instruction, int):
#                f.write(
#                    instruction.to_bytes(2, byteorder="little")
#                )  # STM32 is little-endian
#            else:
#                raise ValueError(f"Invalid instruction: {instruction}")
