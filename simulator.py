class Simulator:
    def __init__(self):
        # Initialize the simulator components
        self.registers = [0] * 16  # 16 registers of 8 bits
        self.ram = [0] * 256  # RAM with 256 positions of 8 bits
        self.rom = [0] * 256  # ROM with 256 positions of 8 bits
        self.pc = 0  # Program Counter
        self.flags = {"EQ": False, "NEQ": False}  # Flags for comparisons
        self.running = True  # State of the simulator

    def test_registers(self):
        self.registers[0] = 0b00000000
        self.registers[1] = 0b00000001
        self.registers[2] = 0b00000010
        self.registers[3] = 0b00000011
        self.registers[4] = 0b00000100
        self.registers[5] = 0b00000101
        self.registers[6] = 0b00000110
        self.registers[7] = 0b00000111
        self.registers[8] = 0b00001000
        self.registers[9] = 0b00001001
        self.registers[10] = 0b00001010
        self.registers[11] = 0b00001011
        self.registers[12] = 0b00001100
        self.registers[13] = 0b00001101
        self.registers[14] = 0b00001110
        self.registers[15] = 0b00001111

    def load_program(self, file_path):
        """
        Load a program from a file (binary instructions) into memory.
        """
        try:
            with open(file_path, 'r') as file:
                for i, line in enumerate(file):
                    if line.lstrip():  # Ignore empty lines
                        # Join the binary parts into a single string
                        binary_instruction = ''.join(line.split())
                        self.rom[i] = int(binary_instruction, 2)  # Convert binary to integer
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' was not found.")
        except ValueError as e:
            raise ValueError(f"Error processing a line in the file: {e}")

    def fetch(self):
        """
        Fetch the current instruction from memory.
        """
        if self.pc >= len(self.rom):
            raise ValueError("PC is out of range. Check if the program ends with HLT.")
        instruction = self.rom[self.pc]
        self.pc += 1
        return instruction

    def decode_and_execute(self, instruction):
        """
        Decodes and executes the current instruction.
        """
        opcode = (instruction >> 12) & 0b11111  # First 5 bits
        reg1 = (instruction >> 8) & 0b1111  # Next 4 bits
        reg2 = (instruction >> 4) & 0b1111  # Next 4 bits
        operand = instruction & 0b1111  # Last 4 bits

        print("Instruction:")
        print(f"Opcode: {opcode:05b}")
        print(f"Reg1: {reg1:04b}")
        print(f"Reg2: {reg2:04b}")
        print(f"Operand: {operand:04b}")

        # Opcodes implemented
        if opcode == 0b00010:  # ADD
            self.registers[operand] = (self.registers[reg1] + self.registers[reg2]) & 0xFF
            print(f"ADD: reg[{operand}] = reg[{reg1}] + reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b00011:  # SUB
            self.registers[operand] = (self.registers[reg1] - self.registers[reg2]) & 0xFF
            print(f"SUB: reg[{operand}] = reg[{reg1}] - reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b00100:  # NOR
            self.registers[operand] = ~(self.registers[reg1] | self.registers[reg2]) & 0xFF
            print(f"NOR: reg[{operand}] = ~(reg[{reg1}] | reg[{reg2}])")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b00101:  # AND
            self.registers[operand] = self.registers[reg1] & self.registers[reg2]
            print(f"AND: reg[{operand}] = reg[{reg1}] & reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b00110:  # XOR
            self.registers[operand] = self.registers[reg1] ^ self.registers[reg2]
            print(f"XOR: reg[{operand}] = reg[{reg1}] ^ reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b00111:  # RSH (Right Shift)
            self.registers[operand] = self.registers[reg1] >> self.registers[reg2]
            print(f"RSH: reg[{operand}] = reg[{reg1}] >> reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b01000:  # LSH (Left Shift)
            self.registers[operand] = (self.registers[reg1] << self.registers[reg2]) & 0xFF
            print(f"LSH: reg[{operand}] = reg[{reg1}] << reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b01001:  # MUL
            self.registers[operand] = (self.registers[reg1] * self.registers[reg2]) & 0xFF
            print(f"MUL: reg[{operand}] = reg[{reg1}] * reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b01010:  # DIV
            if self.registers[reg2] == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            self.registers[operand] = self.registers[reg1] // self.registers[reg2]
            print(f"DIV: reg[{operand}] = reg[{reg1}] // reg[{reg2}]")
            print(f"Result: {self.registers[operand]}")

        elif opcode == 0b01011:  # CMP (Compare)
            self.flags["EQ"] = self.registers[reg1] == self.registers[reg2]
            self.flags["NEQ"] = self.registers[reg1] != self.registers[reg2]
            print(f"CMP: reg[{reg1}] vs reg[{reg2}]")
            print(f"Flags: EQ={self.flags['EQ']}, NEQ={self.flags['NEQ']}")

        elif opcode == 0b01100:  # JMP (Jump)
            self.pc = reg2
            print(f"JMP: PC set to {self.pc}")

        elif opcode == 0b01101:  # JEQ (Jump if Equal)
            if self.flags["EQ"]:
                self.pc = reg2
            print(f"JEQ: PC set to {self.pc} if EQ={self.flags['EQ']}")

        elif opcode == 0b01110:  # JNE (Jump if Not Equal)
            if self.flags["NEQ"]:
                self.pc = reg2
            print(f"JNE: PC set to {self.pc} if NEQ={self.flags['NEQ']}")

        elif opcode == 0b01111:  # HLT (Halt)
            self.running = False
            print("HLT: Halting the program")

        elif opcode == 0b10000:  # LOAD
            self.registers[reg1] = self.ram[self.registers[reg2]]
            print(f"LOAD: reg[{reg1}] = RAM[reg[{reg2}]]")
            print(f"Result: {self.registers[reg1]}")

        elif opcode == 0b10001:  # STORE
            self.ram[self.registers[reg1]] = self.registers[reg2]
            print(f"STORE: RAM[reg[{reg1}]] = reg[{reg2}]")
            print(f"Result: {self.ram[self.registers[reg2]]}")

        elif opcode == 0b10010:  # LOADI (Load Immediate)
            self.registers[reg1] = opcode
            print(f"LOADI: reg[{reg1}] = immediate({opcode})")
            print(f"Result: {self.registers[reg1]}")

        elif opcode == 0b10011:  # STOREI (Store Immediate)
            self.ram[reg1] = opcode
            print(f"STOREI: RAM[{reg1}] = immediate({opcode})")
            print(f"Result: {self.ram[reg1]}")

        elif opcode == 0b10100:  # LOAD_INDIRECT
            self.registers[reg1] = self.ram[self.registers[reg2]]
            print(f"LOAD_INDIRECT: reg[{reg1}] = RAM[reg[{reg2}]]")
            print(f"RAM[{self.registers[reg2]}]: {self.ram[self.registers[reg2]]}")
            print(f"Result: {self.registers[reg1]}")

        elif opcode == 0b10101:  # STORE_INDIRECT
            self.ram[self.registers[reg2]] = self.registers[reg1]
            print(f"STORE_INDIRECT: RAM[reg[{reg2}]] = reg[{reg1}]")
            print(f"RAM[{self.registers[reg2]}]: {self.ram[self.registers[reg2]]}")
            print(f"Result: {self.registers[reg1]}")

        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def run(self):
        """
        Run the program loaded into memory.
        """
        print("Simulator started...")
        print("------------------------------")
        while self.running:
            instruction = self.fetch()
            self.decode_and_execute(instruction)
            self.print_state()
        print("Simulator halted.")

    def print_state(self):
        """
        Print the current state of registers, memory, and the PC.
        """
        print(f"PC: {self.pc}")
        print("Registers:", self.registers)
        print("Memory (first 16):", self.ram[:16])
        print("-" * 30)
