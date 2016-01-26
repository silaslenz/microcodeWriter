from enum import Enum


class ALU_MODE(Enum):
    NOP = 0b0000
    Buss = 0b0001
    BussComp = 0b0010
    Zero = 0b0011
    ARaddBuss = 0b0100
    ARsubBuss = 0b0101
    ARandBuss = 0b0110
    ARorBuss = 0b0111
    ARaddBuss_NF = 0b1000


class LOCATIONS(Enum):
    NOP = 0b000
    IR = 0b001
    PM = 0b010
    PC = 0b011
    AR = 0b100  # Only incoming
    HR = 0b101
    GRx = 0b110
    ASR = 0b111


class GRxControl(Enum):
    GRxField = 0b0
    MField = 0b1


class PCAction(Enum):
    NOP = 0b0
    Add = 0b1


class Loop(Enum):
    NOP = 0b00
    Decrement = 0b01
    FromBus = 0b10
    FromuADR = 0b11


class Seq(Enum):
    Increment = 0b0000
    FromK1 = 0b0001
    FromK2 = 0b0010
    ToZero = 0b0011
    FromuADR = 0b0101
    JumpIfZ = 0b1000
    JumpIfN = 0b1001
    JumpIfO = 0b1011


class MemoryMode(Enum):
    DirectLocation = 0b00
    ImmediateLocation = 0b01
    IndirectLocation = 0b10
    IndexedLocation = 0b11


class GRxLocations(Enum):
    zero = 0b00
    one = 0b01
    two = 0b10
    three = 0b11


class ASMModes(Enum):
    Load = 0
    Store = 1
    Add = 2
    Sub = 3
    And = 4
    LogicShiftLeft = 5
    Branch = 6
    BranchOnNotEquals = 7
    Halt = 9
    Compare = 8
