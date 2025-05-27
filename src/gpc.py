#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GPC - Ge Wit 't Oit Noit Nie Program Converter

This program is a converter for the GPC (Ge Wit 't Oit Noit Nie) programming language.
It converts the GPC source code into a binary format that can be used by STM32 Firmware.
"""

from lark import Lark, Transformer
import logging

__copyright__ = "Copyright 2025, Ge Wit 't Oit Noit Nie"
__license__ = "MIT"
__version__ = "1.0.1"

# Define the instruction mapping
INSTRUCTION_MAP = {
    "STOPPEN": 0,
    "BEGIN_EINDE_PROGRAMMA_INDEX": 1,
    "WACHTEN": 2,
    "ZET_PORT_AAN": 3,
    "ZET_PORT_UIT": 4,
    "FLIP_POORT": 5,
    "BEWAAR_STATUS": 6,
    "SPRING": 7,
}


def to_number(value):
    """Convert a number to its integer value.
    The number can be in binary, octal, decimal, or hexadecimal format.

    Args:
        value (str): The number to convert. It can be in binary (0b), octal (0o), decimal (0d), or hexadecimal (0x) format.
    Returns:
        int: The integer value of the number.
    """
    logging.debug(f"Converting value: {value}")
    if value.startswith("0b"):
        logging.debug("Converting binary to int")
        return int(value, 2)  # Convert binary string to int
    elif value.startswith("0o"):
        logging.debug("Converting octal to int")
        return int(value, 8)  # Convert octal string to int
    elif value.startswith("0d"):
        logging.debug("Converting decimal to int")
        return int(value, 10)  # Convert decimal string to int
    elif value.startswith("0x") or value.startswith("0X"):
        logging.debug("Converting hexadecimal to int")
        return int(value, 16)  # Convert hex string to int
    elif value.isdigit():
        logging.debug("Converting decimal to int")
        return int(value)  # Convert decimal string to int
    else:
        raise ValueError(f"Invalid number: {value}")


class InstructionTransformer(Transformer):
    """Transformer for the GPC parser.
    This class is used to transform the parse tree into a list of instructions."""

    def param(self, args):
        """Transform a parameter into a dictionary."""
        logging.debug(f"Processing param: {args}")
        return {
            args[0].value.upper(): to_number(args[1].value)
        }  # Extract the value of the parameter

    def param_list(self, args):
        logging.debug(f"Processing param_list: {args}")
        param_list = {}
        for param in args:
            if isinstance(param, dict):
                param_list.update(param)
        return param_list

    def instruction(self, args):
        name = args[0].value  # Extract instruction name
        logging.debug(f"Processing instruction: {name}")

        if "STOPPEN" in name:
            return 0x0000

        elif "BEGIN_EINDE_PROGRAMMA_INDEX" in name:
            if len(args) > 1:
                params = args[1]
            return 1 << 12 | (params.get("INDEX") & 0xFFF)

        elif "WACHTEN" in name:
            if len(args) > 1:
                params = args[1]
            return 2 << 12 | (params.get("DELAY") & 0xFFF)

        elif "ZET_POORT_AAN" in name:
            if len(args) > 1:
                params = args[1]

            return (
                (3 << 12) | (params.get("HSIO") << 9) | (params.get("POORT") & 0x001F)
            )

        elif "ZET_POORT_UIT" in name:
            if len(args) > 1:
                params = args[1]

            return (
                (4 << 12) | (params.get("HSIO") << 9) | (params.get("POORT") & 0x001F)
            )

        elif "FLIP_POORT" in name:
            if len(args) > 1:
                params = args[1]

            return (
                (5 << 12) | (params.get("HSIO") << 9) | (params.get("POORT") & 0x001F)
            )

        elif "BEWAAR_STATUS" in name:
            if len(args) > 1:
                params = args[1]

            return 6 << 12

        elif "SPRING" in name:
            if len(args) > 1:
                params = args[1]

            return 7 << 12 | (
                params.get("INDEX") & 0xFFF
            )  # SPRING instruction with index


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
        logging.error("Error: Input file is required")
        sys.exit(1)

    # Check if the input file exists
    if not os.path.exists(args.input):
        logging.error(f"Error: Input file {args.input} does not exist")
        sys.exit(1)

    # If output is not specified, set it to the input file name with .bin extension
    if args.output == None:
        args.output = os.path.splitext(args.input)[0] + ".bin"
        logging.debug("Output file not specified, using default '{args.output}'")

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
    parser = Lark.open("gpc.lark", rel_to=__file__, parser="lalr")
    tree = parser.parse(sourcecode)
    parsed_data = [InstructionTransformer().transform(instr) for instr in tree.children]

    # write the parsed data to the output file. Each instruction is 16 bits long
    with open(args.output, "wb") as f:
        for instruction in parsed_data:
            if isinstance(instruction, int):
                f.write(
                    instruction.to_bytes(2, byteorder="little")
                )  # STM32 is little-endian
            else:
                raise ValueError(f"Invalid instruction: {instruction}")
