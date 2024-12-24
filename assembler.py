from OPCODE import Opcode
from REGISTERS import Register


def assemble(assembler_file, machine_code_file):
    with open(assembler_file, 'r') as file:
        lines = file.readlines()

    binary_lines = []
    for line in lines:
        if line.startswith("//") or line == "\n":
            continue

        parts = line.strip().split()
        if len(parts) < 4:
            raise ValueError(f"Invalid instruction format: {line}")
        if len(parts) > 4:
            # CUT OFF ANY COMMENTS
            parts = parts[:4]

        if parts[0] not in Opcode.__members__:
            raise ValueError(f"Invalid opcode: {parts[0]} in instruction {line}")
        if parts[1] not in Register.__members__:
            raise ValueError(f"Invalid register: {parts[1]} in instruction {line}")
        if parts[2] not in Register.__members__:
            raise ValueError(f"Invalid register: {parts[2]} in instruction {line}")
        if parts[3] not in Register.__members__:
            raise ValueError(f"Invalid register: {parts[3]} in instruction {line}")

        opcode, reg1, reg2, reg3 = parts

        # GET EACH PART OF THE INSTRUCTION IN BINARY
        opcode_bin = Opcode[opcode].value[0]
        reg1_bin = Register[reg1].value[0]
        reg2_bin = Register[reg2].value[0]
        reg3_bin = Register[reg3].value[0]

        # COMBINE THE PARTS INTO A SINGLE BINARY STRING
        binary_instruction = f"{opcode_bin}{reg1_bin}{reg2_bin}{reg3_bin}"
        binary_lines.append(binary_instruction)

    with open(machine_code_file, 'w') as file:
        file.write("\n".join(binary_lines))

    print(f"Assembly complete. Machine code written to {machine_code_file}")