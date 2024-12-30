from OPCODE import Opcode
from REGISTERS import Register


def assemble(assembler_file, machine_code_file):
    # Open the assembler file for reading
    with open(assembler_file, 'r') as file:
        lines = file.readlines()

    lines = prepare_code(lines)

    variables = {}  # Dictionary to store variables
    labels = {}  # Dictionary to store labels
    binary_lines = []  # List to store binary instructions

    # Identify labels and variables
    instruction_index = 0
    for line in lines:
        parts = line.split()

        # Check for label definition
        if parts[0].endswith(":"):
            label_name = parts[0][:-1]  # Remove the colon
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = instruction_index
            continue

        # Process variable definitions
        if parts[0] == "var":
            if len(parts) != 3:
                raise ValueError(f"Invalid variable definition: {line}")
            var_name, var_value = parts[1], parts[2]
            if var_name in variables:
                raise ValueError(f"Variable {var_name} is already defined.")
            # Check if the value is a register or a number
            if var_value in Register.__members__:
                variables[var_name] = Register[var_value].value[0]  # Store register reference
            elif var_value.isdigit() and 0 <= int(var_value) <= 255:
                variables[var_name] = format(int(var_value), '04b')  # Store numerical value in binary
            else:
                raise ValueError(f"Invalid variable value: {var_value} in line {line}")
            continue

        # If it's not a label or variable, it's an instruction
        instruction_index += 1

    # Assemble instructions
    for line in lines:
        parts = line.split()

        # Replace variables and labels
        parts = [variables.get(part, labels.get(part, part)) for part in parts]

        if parts[0] == "var" or parts[0].endswith(":"):
            continue

        # Validate opcode and operands
        if parts[0] not in Opcode.__members__:
            raise ValueError(f"Invalid opcode: {parts[0]} in instruction {line}")
        opcode = Opcode[parts[0]]
        operands = parts[1:]

        # Check the expected number of operands for this opcode
        expected_operands = opcode.value[1]
        if len(operands) != expected_operands:
            raise ValueError(f"Opcode {opcode.name} expects {expected_operands} operands, got {len(operands)}: {line}")

        # Handle specific operand types
        binary_operands = []
        for operand in operands:
            operand = str(operand)
            if operand in Register.__members__:  # If the operand is a register
                binary_operands.append(Register[operand].value[0])
            elif operand.isdigit() and 0 <= int(
                    operand) <= 255:  # If the operand is a valid immediate or memory address
                binary_operands.append(format(int(operand), '04b'))  # Convert to 8-bit binary
            else:
                raise ValueError(f"Invalid operand: {operand} in instruction {line}")

        # Combine opcode and operands into a single binary instruction
        opcode_bin = opcode.value[0]
        binary_instruction = f"{opcode_bin}{''.join(binary_operands)}"  # Fill remaining bits with 0

        if len(binary_instruction) < 17:
            binary_instruction = binary_instruction + '0' * (17 - len(binary_instruction))

        # Separate the binary instruction by spaces 5 bits 4 bits 4 bits 4 bits
        binary_instruction = binary_instruction[:5] + " " + binary_instruction[5:9] + " " + binary_instruction[9:13] + " " + binary_instruction[13:]

        binary_lines.append(binary_instruction)

    # Write the machine code to the output file
    with open(machine_code_file, 'w') as file:
        file.write("\n".join(binary_lines))

    print(f"Assembly complete. Machine code written to {machine_code_file}")


# Remove spaces and comments from the code and the lines comments
def prepare_code(lines):
    index = 0

    indexes_to_delete = []

    for line in lines:
        line = line.lstrip()

        # Skip comments and empty lines
        if line.startswith("//") or line == "\n" or line == "":
            # Delete the line
            indexes_to_delete.append(index)
            #continue

        # Delte spaces at the beginning of the line
        parts = line.split()

        # Check if any of the parts is a comment and remove it and the rest of the line
        if any("//" in part for part in parts):
            for i, part in enumerate(parts):
                if "//" in part:
                    parts = parts[:i]
                    break

            line = " ".join(parts)

        # Update the line in the list
        lines[index] = line

        index += 1

    reduction = 0

    # Delete the lines that are empty or are comments
    for index in indexes_to_delete:
        del lines[index-reduction]
        reduction += 1

    return lines