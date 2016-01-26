import sys

from binaryreps import *

counter = 0
PM = []
MyM = []  # First in here at place 27 (39 dec)
K1 = ["0a", "0c", "0d", "10", "13", "16", "35", "1f", "21", "0b", "00", "00", "00", "00", "25", "23"]

K2 = ["03", "04", "05", "07"]


def halt():
    createASMHex(ASMModes.Halt, GRxLocations.zero, MemoryMode.DirectLocation)


def writeMIA():
    global PM, MyM, K1, K2
    f = open('py.mia', 'w')
    f.write("PM:\n")
    for i in range(0, 256):
        counterstr = hex(i).replace("0x", "")
        while (len(counterstr) < 2):
            counterstr = "0" + counterstr
        if (i < len(PM)):
            f.write(counterstr + ": " + PM[i] + "\n")
        else:
            f.write(counterstr + ": 0000\n")
    f.write("\n")

    f.write("MyM:\n")
    f.write("""00: 00f8000
01: 008a000
02: 0000100
03: 0078080
04: 00fa080
05: 0078000
06: 00b8080
07: 0240000
08: 1184000
09: 0138080
0a: 00b0180
0b: 0000780
0c: 0190180
0d: 0380000
0e: 0880000
0f: 0130180
10: 0380000
11: 0a80000
12: 0130180
13: 0380000
14: 0c80000
15: 0130180
16: 0380000
17: 0041000
18: 000061a
19: 1a00a98
1a: 0130180
1b: 02c0000
1c: 0058000
1d: 10c0000
1e: 0118180
1f: 0000400
20: 000029b
21: 0380000
22: 0a80180
23: 01b8000
24: 00b4180
25: 0000480
26: 000029b\n""")
    for i in range(39, 128):
        counterstr = hex(i).replace("0x", "")
        while (len(counterstr) < 2):
            counterstr = "0" + counterstr
        if (i - 39 < len(MyM)):

            f.write(counterstr + ": " + MyM[i - 39] + "\n")
        else:
            f.write(counterstr + ": 0000000\n")
    f.write("\n")

    f.write("K1:\n")
    for i in range(0, 16):
        counterstr = hex(i).replace("0x", "")
        while (len(counterstr) < 2):
            counterstr = "0" + counterstr
        f.write(counterstr + ": " + K1[i] + "\n")
    f.write("\n")

    f.write("K2:\n")
    for i in range(0, 4):
        counterstr = hex(i).replace("0x", "")
        while (len(counterstr) < 2):
            counterstr = "0" + counterstr
        f.write(counterstr + ": " + K2[i] + "\n")
    f.write("\n")

    f.write("PC:\n00\n\n")

    f.write("ASR:\n00\n\n")

    f.write("AR:\n0000\n\n")

    f.write("HR:\n0000\n\n")

    f.write("GR0:\n0000\n\n")

    f.write("GR1:\n0000\n\n")

    f.write("GR2:\n0000\n\n")

    f.write("GR3:\n0000\n\n")

    f.write("IR:\n0000\n\n")

    f.write("MyPC:\n00\n\n")

    f.write("SMyPC:\n00\n\n")

    f.write("LL:\n00\n\n")

    f.write("O_flag:\n\n")
    f.write("C_flag:\n\n")
    f.write("N_flag:\n\n")
    f.write("Z_flag:\n\n")
    f.write("L_flag:\n\n")
    f.write("End_of_dump_file")


def getInt(value, moveBinStepsToLeft):
    return int(hex(value << moveBinStepsToLeft), 16)


def createMicroCode(alu: ALU_MODE, toBus: LOCATIONS, fromBus: LOCATIONS, s: GRxControl, p: PCAction, loop: Loop,
                    seq: Seq, adressHex=0x0):
    resultingCode = (
        getInt(alu.value, 21) + getInt(toBus.value, 18) + getInt(fromBus.value, 15) + getInt(s.value, 14) + getInt(
                p.value,
                13) + getInt(
                loop.value, 11) + getInt(seq.value, 7) + getInt(adressHex, 0))
    output = str(hex(resultingCode)).replace("0x", "")
    while (len(output) < 7):
        output = "0" + output
    MyM.append(output)

    # int(hex(mode.value << 12), 16))


def createASMHex(mode, GRx: GRxLocations, memory: MemoryMode, adressHex=0x00):
    global PM
    # if adressBin < 0b1000000000:
    #     resultingCode = (
    #     getInt(mode.value,12) + getInt(GRx.value,10)+ getInt(memory.value,8) + getInt(adressBin,0))
    # elif (adressHex < 0xFFF):
    #     resultingCode = (
    #             getInt(mode.value,12) + getInt(GRx.value,10)+ getInt(memory.value,8) + getInt(adressHex,0))
    #
    # else:
    #     raise SyntaxError
    if type(mode) == int:
        resultingCode = (getInt(mode, 12) + getInt(GRx.value, 10) + getInt(memory.value, 8) + getInt(adressHex, 0))
    else:
        resultingCode = (
            getInt(mode.value, 12) + getInt(GRx.value, 10) + getInt(memory.value, 8) + getInt(adressHex, 0))
    output = str(hex(resultingCode)).replace("0x", "")

    while (len(output) < 4):
        output = "0" + output
    PM.append(output)
    return len(PM) - 1


def microSubAtMemorylocation():
    createMicroCode(ALU_MODE.ARorBuss, LOCATIONS.NOP, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.Increment)


def quicksort():
    pass


def switch():  # Moves GR0/1 to where they didn't come from
    decrease_location_in_PM(MemoryMode.DirectLocation, 0xD1)

    createASMHex(ASMModes.Store, GRxLocations.one, MemoryMode.IndirectLocation, 0xD1)
    # Increase D1 by one and move to HR
    createASMHex(len(K1) - 5, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xD1)
    # Move HR to D1
    createASMHex(len(K1) - 6, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xD1)
    createASMHex(ASMModes.Store, GRxLocations.zero, MemoryMode.IndirectLocation, 0xD1)


def create_microfun():
    global K1
    # Move HR to PM at pointed location
    K1[len(K1) - 6] = "27"
    createMicroCode(ALU_MODE.NOP, LOCATIONS.HR, LOCATIONS.PM, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)
    # Store location at HR
    K1[len(K1) - 4] = "28"
    createMicroCode(ALU_MODE.NOP, LOCATIONS.PM, LOCATIONS.HR, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)

    # Increase in PM
    K1[len(K1) - 5] = "29"
    # PM>AR
    createMicroCode(ALU_MODE.Buss, LOCATIONS.PM, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.Increment)
    # 0001+AR
    createMicroCode(ALU_MODE.ARaddBuss_NF, LOCATIONS.GRx, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.Increment)
    createMicroCode(ALU_MODE.NOP, LOCATIONS.AR, LOCATIONS.HR, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)

    # Decrease in PM
    K1[len(K1) - 3] = "2c"
    # PC>AR
    createMicroCode(ALU_MODE.Buss, LOCATIONS.PM, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.Increment)
    # 0001+AR
    createMicroCode(ALU_MODE.ARsubBuss, LOCATIONS.GRx, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.Increment)
    createMicroCode(ALU_MODE.NOP, LOCATIONS.AR, LOCATIONS.HR, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)

    # Branch to adr if n=0
    startlocation = "2f"
    K1[len(K1) - 1] = "2f"

    # 2f
    createMicroCode(ALU_MODE.NOP, LOCATIONS.NOP, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.JumpIfN, adressHex=0x31)
    # 30 if n=0 load IR to PC
    createMicroCode(ALU_MODE.NOP, LOCATIONS.IR, LOCATIONS.PC, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)
    # 31 if n=1 just move on
    createMicroCode(ALU_MODE.NOP, LOCATIONS.NOP, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)


    # Branch to adr if Z=1
    # 32
    K1[len(K1) - 2] = "32"

    # 32
    createMicroCode(ALU_MODE.NOP, LOCATIONS.NOP, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP,
                    Seq.JumpIfZ, adressHex=0x34)
    # 33 do nothing if Z=0
    createMicroCode(ALU_MODE.NOP, LOCATIONS.NOP, LOCATIONS.NOP, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)
    # 34 if Z=1 load IR to PC
    createMicroCode(ALU_MODE.NOP, LOCATIONS.IR, LOCATIONS.PC, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)

    # Branch always
    # 35
    createMicroCode(ALU_MODE.NOP, LOCATIONS.IR, LOCATIONS.PC, GRxControl.GRxField, PCAction.NOP, Loop.NOP, Seq.ToZero)


def save_num_in_place(num, place):  # Uses GR3
    createASMHex(ASMModes.Load, GRxLocations.three, MemoryMode.ImmediateLocation)
    createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.DirectLocation, num)
    createASMHex(ASMModes.Store, GRxLocations.three, MemoryMode.DirectLocation, place)


def load_from_PM_To_GRx(adressMode: MemoryMode, adress, grx: GRxLocations):
    return createASMHex(ASMModes.Load, grx, adressMode, adress)


def store_from_GRx_To_PM(adressMode: MemoryMode, adress, grx: GRxLocations):
    createASMHex(ASMModes.Store, grx, adressMode, adress)


def increase_location_in_PM(memorymode: MemoryMode, place):  # Uses GR3 and HR
    # Next two rows write 0001 to GR3 for future addition
    load_from_PM_To_GRx(MemoryMode.ImmediateLocation, 0x00, GRxLocations.three)
    print(createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.DirectLocation, 0x01))

    # Increase D1 by one and move to HR
    createASMHex(len(K1) - 5, GRxLocations.three, memorymode, place)
    # Move HR to D1
    createASMHex(len(K1) - 6, GRxLocations.zero, memorymode, place)

def decrease_location_in_PM(memorymode: MemoryMode, place):  # Uses GR3 and HR
    # Next two rows write 0001 to GR3 for future addition
    load_from_PM_To_GRx(MemoryMode.ImmediateLocation, 0x00, GRxLocations.three)
    print(createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.DirectLocation, 0x01))

    # Increase D1 by one and move to HR
    createASMHex(len(K1) - 3, GRxLocations.three, memorymode, place)
    # Move HR to D1
    createASMHex(len(K1) - 6, GRxLocations.zero, memorymode, place)


def bubble_sort():
    # Prestored values:
    # D0=0001 (List sorted=1)
    # D1=00E0 (Adress "i")


    global K1
    create_microfun()

    # D0>GR3 (0001)
    createASMHex(ASMModes.Load, GRxLocations.three, MemoryMode.DirectLocation, 0xD0)

    # D1>GR0
    createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.IndirectLocation, 0xD1)
    # Increase D1 by one and move to HR
    createASMHex(len(K1) - 5, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xD1)
    # Move HR to D1
    createASMHex(len(K1) - 6, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xD1)
    # D1>GR1
    createASMHex(ASMModes.Load, GRxLocations.one, MemoryMode.IndirectLocation, 0xD1)

    # Decrease D1 in HR
    createASMHex(len(K1) - 3, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xD1)
    # Move HR to D1
    createASMHex(len(K1) - 6, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xD1)
    # Compare GR1 and D1
    createASMHex(ASMModes.Compare, GRxLocations.zero, MemoryMode.IndirectLocation, 0xD1)

    # If N=1, i+1>i

    # Switch if n=1, else jump to #10
    createASMHex(len(K1) - 1, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x10)
    switch()
    # 0D
    # Decrease D1 in HR
    createASMHex(len(K1) - 3, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xD2)
    # Skip next instruction if already zero
    createASMHex(len(K1) - 1, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x10)
    # Decrease list_sorted (D2) by one
    createASMHex(len(K1) - 6, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xD2)
    # 10
    # Check if i(D1)=FF
    # Increase D1 by one and move to HR
    createASMHex(len(K1) - 5, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xD1)
    # Check for O=1 (Overflow) and skip next instruction if 1
    createASMHex(len(K1) - 2, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x13)

    # Move to start
    createASMHex(ASMModes.Branch, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x00)
    # Restore E0 to D1
    createASMHex(ASMModes.Load, GRxLocations.two, MemoryMode.ImmediateLocation)
    createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xE0)
    createASMHex(ASMModes.Store, GRxLocations.two, MemoryMode.DirectLocation, adressHex=0xD1)
    halt()

    #

    halt()


def addAtFE(argv):
    createASMHex(ASMModes.Load, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xFE)
    createASMHex(ASMModes.Load, GRxLocations.one, MemoryMode.DirectLocation, adressHex=0xFE)
    createASMHex(ASMModes.Load, GRxLocations.two, MemoryMode.DirectLocation, adressHex=0xFE)
    createASMHex(ASMModes.Load, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xFE)
    createASMHex(ASMModes.LogicShiftLeft, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x0C)
    createASMHex(ASMModes.And, GRxLocations.one, MemoryMode.DirectLocation, adressHex=0xFB)
    createASMHex(ASMModes.And, GRxLocations.two, MemoryMode.DirectLocation, adressHex=0xFC)
    createASMHex(ASMModes.And, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xFD)
    createASMHex(ASMModes.LogicShiftLeft, GRxLocations.one, MemoryMode.DirectLocation, adressHex=0x08)
    createASMHex(ASMModes.LogicShiftLeft, GRxLocations.two, MemoryMode.DirectLocation, adressHex=0x04)
    createASMHex(ASMModes.Store, GRxLocations.one, MemoryMode.DirectLocation, adressHex=0xF7)
    createASMHex(ASMModes.Store, GRxLocations.two, MemoryMode.DirectLocation, adressHex=0xF8)
    createASMHex(ASMModes.Store, GRxLocations.three, MemoryMode.DirectLocation, adressHex=0xF9)
    createASMHex(ASMModes.Add, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xF7)
    createASMHex(ASMModes.Add, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xF8)
    createASMHex(ASMModes.Add, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xF9)
    createASMHex(ASMModes.Store, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0xFF)
    createASMHex(ASMModes.Halt, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x00)
    writeMIA()
    # Remember to set FB-FD (0F00...000F)


def compare_adr_with_grx(memorymode: MemoryMode, grx: GRxLocations, adr):
    createASMHex(ASMModes.Compare, grx, memorymode, adr)


def bubsort():
    savelistAdr = save_num_in_place(0x01, 0xD0)  # list sorted=1
    save_num_in_place(0xE0, 0xD1)  # location in list, "i"


    createFirstTmpAdr = load_from_PM_To_GRx(MemoryMode.IndirectLocation, 0xD1,
                                            GRxLocations.zero)  # Move value "i" to Gr0 (tmp)
    increase_location_in_PM(MemoryMode.DirectLocation, 0xD1)
    load_from_PM_To_GRx(MemoryMode.IndirectLocation, 0xD1,
                        GRxLocations.one)  # Move value "i" to Gr1
    compare_adr_with_grx(MemoryMode.IndirectLocation, GRxLocations.zero,
                         0xD1)  # Compare tmp2 with tmp (TMP<TMP2 => N=1)7

    createASMHex(len(K1) - 1, GRxLocations.zero, MemoryMode.DirectLocation, adressHex=0x25) #Move to compare code below (the one with print), if N=0, else switch (next row)


    switch()
    save_num_in_place(0x00,0xD0) # list_stored=0'
    # Alreade increased i


    print (load_from_PM_To_GRx(MemoryMode.ImmediateLocation,0x00,GRxLocations.three), "this is the location to jump to if tmp>tmp2")  # Write next value to GR3
    createASMHex(ASMModes.Load,GRxLocations.zero,MemoryMode.DirectLocation,0xFF) # 00FF
    compare_adr_with_grx(MemoryMode.DirectLocation,GRxLocations.three,0xD1) # Compare value at D1 with FF

    

    halt()


def main():
    create_microfun()
    bubsort()
    writeMIA()


if __name__ == '__main__':
    sys.exit(main())
