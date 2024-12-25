from enum import Enum

class Opcode(Enum):
    ADD = ("00010", 3)  # Adds reg2 and reg3, stores the result in reg1
    SUB = ("00011", 3)  # Subtracts reg3 from reg2, stores the result in reg1
    NOR = ("00100", 3)  # Performs bitwise NOR on reg2 and reg3, stores in reg1
    AND = ("00101", 3)  # Performs bitwise AND on reg2 and reg3, stores in reg1
    XOR = ("00110", 3)  # Performs bitwise XOR on reg2 and reg3, stores in reg1
    RSH = ("00111", 3)  # Right shifts reg2 by the value of reg3, stores in reg1
    LSH = ("01000", 3)  # Left shifts reg2 by the value of reg3, stores in reg1
    MUL = ("01001", 3)  # Multiplies reg2 and reg3, stores the result in reg1
    DIV = ("01010", 3)  # Divides reg2 by reg3, stores the result in reg1
    CMP = ("01011", 2)  # Compares reg1 and reg2, sets flags accordingly
    JMP = ("01100", 1)  # Unconditional jump to the address in reg1
    JEQ = ("01101", 1)  # Jumps to the address in reg1 if the EQ flag is set
    JNE = ("01110", 1)  # Jumps to the address in reg1 if the NEQ flag is set
    HLT = ("01111", 0)  # Halts the execution of the program
    LOAD = ("10000", 2)  # Loads the value from RAM address into reg1
    STORE = ("10001", 2)  # Stores the value in reg1 into a RAM address
    LOADI = ("10010", 2)  # Loads an immediate value into reg1
    STOREI = ("10011", 2)  # Stores an immediate value into a RAM address
    LOAD_INDIRECT = ("10100", 2)  # Loads the value from address in reg2 into reg1
    STORE_INDIRECT = ("10101", 2)  # Stores the value in reg1 into the address in reg2
