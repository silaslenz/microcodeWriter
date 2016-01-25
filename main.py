from binaryreps import *

def createASMHex(mode:ASMModes,toGRx:GRxLocations, memory:MemoryMode,adressBin=0b1000000000, adressHex=0xFFF):
    if adressBin<0b1000000000:
        resultingCode = (int(hex(mode.value<<12),16)+int(hex(toGRx.value<<10),16)+int(hex(memory.value<<8),16)+int(hex(adressBin<<0),16))
    elif (adressHex<0xFFF):
        resultingCode = (int(hex(mode.value<<12),16)+int(hex(toGRx.value<<10),16)+int(hex(memory.value<<8),16)+int(hex(adressHex<<0),16))
    print (int(hex(memory.value<<8),16))

    output=str(hex(resultingCode)).replace("0x","")

    while (len(output)<4):
        output="0"+output
    print (output)


createASMHex(ASMModes.Load,GRxLocations.three,MemoryMode.ImmediateLocation, adressHex=0xAA)