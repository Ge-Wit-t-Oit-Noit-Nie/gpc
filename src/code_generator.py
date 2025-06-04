
import struct
import logging


# Define file_header structure to be used in the generation
file_header = {
	"BEGIN_PROGRAMMA": 0x00000000,
	"PAUZE_PROGRAMMA": 0x00000000,
	"EINDE_PROGRAMMA": 0x00000000
}

def encode_opcode(code, params):
	"""
 	Encodes a function opcode and its parameters into a single integer or byte sequence.

	This function is typically used to convert high-level function calls into
	compact binary representations suitable for writing to a binary file.

	Parameters:
	- code (str): The name of the function or operation to encode.
	- params (dict or list): The parameters associated with the function call.
							 These are used to compute the final encoded value,
							 often using bitwise operations.

	Returns:
	 - int or bytes: The encoded representation of the opcode and its parameters.
	"""
	result = bytearray()

	match code.upper():
		case "STOPPEN":
			# | Element | Bitmask               | Hex    | Parameter |
			# | ------- | --------------------- | ------ | --------- |
			# | OPCODE  | 0b0000 0000		    | 0x00   |           |
			result.append(0x00)

		case "PAUZE":
			# | Element | Bitmask               | Hex    | Parameter |
			# | ------- | --------------------- | ------ | --------- |
			# | OPCODE  | 0b0001 0000           | 0x10   |           |
			result.append(0x10)

		case "WACHTEN":
			# | Element | Bitmask               | Hex    | Parameter |
			# | ------- | --------------------- | ------ | --------- |
			# | OPCODE  | 0b0010 0000           | 0x2000 |           |
			# | OPCODE  | 0b0000 1111 1111 1111 | 0x0FFF |           |
			result.append(0x20 | (params[0][1] >> 8) )
			result.append(params[0][1] & 0xFF)

		case "ZET_POORT_AAN":
			# | Element | Bitmask               | Hex    | Parameter         |
			# | ------- | --------------------- | ------ | ----------------- |
			# | OPCODE  | 0b0011 0000 0000 0000 | 0x3000 |                   |
			# | STATUS  | 0b0000 0001 0000 0000 | 0x0100 |                   |
			# | HSIO    | 0b0000 0001 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
			# | POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |
			for param in params:
				if "POORT" == param[0].upper():
					poort = (param[1] & 0x001F)
				elif "HSIO" == param[0].upper():
					hsio = ((param[1] & 0x01) << 1) | 0x01
				else:
					logging.debug(f"{code} heeft een onbekende parameter {param[0]}")

			result.append(0x30 | hsio)
			result.append(poort)

		case "ZET_POORT_UIT":
			# | Element | Bitmask               | Hex    | Parameter         |
			# | ------- | --------------------- | ------ | ----------------- |
			# | OPCODE  | 0b0100 0000 0000 0000 | 0x3000 |                   |
			# | STATUS  | 0b0000 0000 0000 0000 | 0x0000 |                   |
			# | HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
			# | POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |
			for param in params:
				if "POORT" == param[0].upper():
					poort = (param[1] & 0x001F)
				elif "HSIO" == param[0].upper():
					hsio = ((param[1] & 0x01) << 1) 
				else:
					logging.debug(f"{code} heeft een onbekende parameter {param[0]}")

			result.append(0x30 | hsio)
			result.append(poort)
			
		case "FLIP_POORT":
			# | Element | Bitmask               | Hex    | Parameter         |
			# | ------- | --------------------- | ------ | ----------------- |
			# | OPCODE  | 0b0100 0000 0000 0000 | 0x4000 |                   |
			# | HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
			# | POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |
			for param in params:
				if "POORT" == param[0].upper():
					poort = (param[1] & 0x001F)
				elif "HSIO" == param[0].upper():
					hsio = (param[1] & 0x01) << 1
				else:
					logging.debug(f"{code} heeft een onbekende parameter {param[0]}")

			result.append(0x40 | hsio)
			result.append(poort)

		case "BEWAAR_STATUS":
			# | Element | Bitmask               | Hex    | Parameter |
			# | ------- | --------------------- | ------ | --------- |
			# | OPCODE  | 0b0110 0000           | 0x50   |           |
			result.append(0x50)
			
		case "SPRING":
			# | Element | Bitmask                         | Hex      | Parameter         |
			# | ------- | ------------------------------- | ------   | ----------------- |
			# | OPCODE  | 0b0111 0000 0000 0000 0000 0000 | 0x600000 |                   |
			# | INDEX   | 0b0000 0001 1111 1111 1111 1111 | 0x01FFFF | INDEX             |

			result.append(0x60 | (params[0][1] & 0x010000))
			result.append(params[0][1] & 0x01FFFF)

		case _:
			logging.debug(f"{code} is een onbekende instructie")

	return result

# Function to generate binary output
def generate_binary(tokens, output_filename):
	"""
	Converts a list of parsed tokens (representing function calls and labels)
	into a binary format and writes the result to a file.

	The binary format includes:
	- A fixed-size header for label addresses (e.g., START_OF_PROGRAM, etc.)
	- Encoded function opcodes and parameters using bitwise operations

	Parameters:
	- tokens (list): A list of dictionaries representing parsed statements,
					 where each item is either a function call or a label.
	- output_filename (str): The name of the output binary file to write.

	Returns:
	- None. Writes the binary data directly to the specified file.
	"""

	# Initialize binary data with header for labels
	# Each fixed label can potentially cover the entire memory scope: 128k.
	# in HEX 0x00020000	= 4 bytes 
	binary_data = bytearray()
	for label in file_header:
		binary_data.extend(struct.pack("<I", file_header[label]))

	# Generate binary data for each function call
	for stmt in tokens:
		if stmt["type"] == "function":
			binary_data.extend(encode_opcode(stmt["name"], stmt["params"]))
			
		elif stmt["type"] == "label":
			file_header[stmt["name"]] = len(binary_data)
	
	# Update label addresses in the header
	for label in file_header:
		address = file_header[label] + 2
		if "BEGIN_PROGRAMMA"==label:
			binary_data[0:4] = struct.pack("<I", address)
		elif "PAUZE_PROGRAMMA"==label:
			binary_data[5:8] = struct.pack("<I", address)
		elif "EINDE_PROGRAMMA"==label:
			binary_data[9:12] = struct.pack("<I", address)
		
	# Write binary data to file
	with open(output_filename, "wb") as f:
		f.write(binary_data)
