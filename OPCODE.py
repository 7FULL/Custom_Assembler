from enum import Enum


class Opcode(Enum):
    ADD = "0010",
    SUB = "0011",
    NOR = "0100",
    AND = "0101",
    XOR = "0110",
    # RIGHT SHIFT
    RSH = "0111",
    