from enum import Enum
from binaryreps import *

def Load(toGRx:GRxLocations, memory:MemoryMode, adressBin=0b1000000000, adressHex=0xFFF):
    if adressBin<0b1000000000:
        resultingCode = (int(hex(0<<12),16)+int(hex(toGRx.value<<10),16)+int(hex(memory.value<<8),16)+int(hex(adressBin<<0),16))
    elif (adressHex<0xFFF):
        resultingCode = (int(hex(toGRx.value<<10),16)+int(hex(memory.value<<8),16)+int(hex(adressHex<<0),16))
    print (int(hex(memory.value<<8),16))

    output=str(hex(resultingCode)).replace("0x","")

    while (len(output)<4):
        output="0"+output
    print (output)

def alu(mode):
    print(ALU_MODE.ARaddBuss_NF.value)

Load(GRxLocations.three,MemoryMode.ImmediateLocation, adressHex=0xAA)